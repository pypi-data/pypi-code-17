import fileinput
import logging
import os

import concurrent.futures
from six.moves.urllib.parse import urlparse

from .handlers import handler_for_url


class InvalidDirective(Exception):
    pass


class Directive(object):
    @classmethod
    def from_raw_line(cls, raw_line, inpfile="??", lineno="??"):
        D = cls()
        D.location, source = raw_line.strip().split(None, 1)
        if urlparse(D.location).netloc:
            msg = "A local destination must be supplied: "
            msg += "{} (line {})".format(D.location, inpfile, lineno)
            raise InvalidDirective(msg)
        try:
            url, D.source_options = cls.parse_source(source)
        except Exception as e:
            raise InvalidDirective('Unable to parse source "{}": {}'.format(source, e))
        D.source = handler_for_url(url)
        return D

    @staticmethod
    def parse_source(source):
        options = {}
        if ";" in source:
            url, opt_string = source.strip().rsplit(";", 1)
            for opt in opt_string.split(","):
                opt = opt.strip()
                options.update(dict((opt.split("="),)))
        else:
            url = source
        return url, options

    def run(self):
        return self.source.get(self.location, self.source_options)

    def __repr__(self):
        substs = {'class': self.__class__.__name__,
                  'source': self.source.source,
                  'dest': self.location,
                  'options': " {}".format(self.source_options)
                             if self.source_options else ""}
        return "<{class}: {source} -> {dest}{options}>".format(**substs)

    def run_with_dependency(self, wait_for=None):
        """
        Process this directive by invoking its run() method.  If wait_for is
        specified, it will be considered a dependency, and processing the
        directive won't start until the result from wait_for is available.

        :param directive:
            A Directive instance.
        :param wait_for:
            A callable. If given, the directive will not
            be processed until this callable returns a value.
        """
        if wait_for:
            res = wait_for()
            if not res:
                return False
        return self.run()


class Config(object):
    def __init__(self, config_files):
        """
        Processes the given config_files and populates self.directive_map with
        Directive instances, as well as self.tree with the relationships
        between directives, taking into account the paths they will create.

        Note that self.directive_map is a dictionary with locations (i.e.
        destination paths) as keys and the actual Directive as the value. The
        keys are used to later order the Directives for processing.

        :param config_files:
            A list of configuration files to read

        """
        self.directive_map = {}
        raw_lines = fileinput.input(config_files)
        for raw_line in raw_lines:
            if self.ignored_line(raw_line):
                continue
            directive = Directive.from_raw_line(raw_line,
                                                inpfile=fileinput.filename(),
                                                lineno=fileinput.filelineno())
            self.directive_map[directive.location] = directive

        # The tree is a dict with the parent as key and a list of its children
        # as the value. For non-root nodes they will be in the tree twice:
        # once for their node, and once in another node's children list.
        # When building the tree, sorting the paths guarantees we'll see
        # parents before children So a KeyError means a parent wasn't declared
        # at all, which should warn the user.
        # Also, we sort split lists per-path, to ensure the ordering is
        # per path component (i.e. filesystem-correct) and not lexical
        self.tree = {'': []}
        for path_as_array in sorted([location.split("/") for location in
                                     self.directive_map.keys()]):
            parent = "/".join(path_as_array[:-1])
            child = "/".join(path_as_array)
            if parent in self.tree:
                self.tree[parent].append(child)
            elif os.path.isdir(parent):
                logging.warn("Parent directory {} is not specified ".format(parent) +
                             "in the configuration, using existing directory")
                self.tree[''].append(child)
            else:
                raise InvalidDirective("Parent directory {} ".format(parent) +
                                       "does not exist and is not in the configuration")
            # Add my list of children
            self.tree[child] = []

    def sequential_directives(self):
        """
        Generates directives to be processed in sequential order.

        :returns:
            Directive instances
        """
        for location in sorted(self.directive_map.keys(), key=len):
            yield self.directive_map[location]

    def concurrent_directives(self):
        """
        Generates the next directive to process concurrently, and an optional
        dependency which needs to be finished before the returned directive can
        be processed.

        Dependencies will be yielded in order, that is, a directive A will
        always come before any directives that have A as a dependency.

        :returns:
            Tuples of (directive, dependency). Directive is a Directive
            instance, dependency can be either a Directive instance or None
            for a directive with no dependencies.
        """
        directives = self.tree['']
        parent = None
        stack = []
        parent_stack = []
        while True:
            # If current directives is empty?
            if not directives:
                # And the stack of pending directive sets is also empty?
                if not stack:
                    # then we're done
                    break
                else:
                    # We need to continue processing what's in the stack,
                    # so pop away
                    directives = stack.pop()
                    parent = parent_stack.pop()
            # Pop next directive, yield it with its parent
            directive = directives.pop()
            yield(self.directive_map[directive],
                  self.directive_map[parent] if parent else None)
            # Are there children, i.e. a subtree to walk with me as parent?
            if self.tree[directive]:
                # Yes. If I still have unprocessed directives at this level,
                # store the current directives and parent to get back to them
                # later.
                if directives:
                    stack.append(directives)
                    parent_stack.append(parent)
                # What are the new directives and parent?
                directives = self.tree[directive]
                parent = directive

    def ignored_line(self, raw_line):
        "Blank lines and #Comments are ignored"
        line = raw_line.strip()
        if len(line) == 0:
            return True
        if line.startswith("#"):
            return True
        return False

    def build(self, dry_run=False):
        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=len(self.directive_map))
        self.futures = {}
        futures_to_locs = {}
        results = ConfigResults()
        for directive, dependency in self.concurrent_directives():
            if dry_run:
                depstring = " depends on {}".format(dependency.location) \
                    if dependency else ""
                print("{directive}{depends}".format(directive=directive,
                                                    depends=depstring))
            else:
                # the dependency has to be a callable, either a future's
                # result method which blocks until the future is finished,
                # or a "no-wait" lambda that just returns true immediately.
                if dependency:
                    assert dependency.location in self.futures,\
                        "Depends on not-yet-seen directive"
                    dep_callable = self.futures[dependency.location].result
                else:
                    def dep_callable():
                        return True

                this_future = self.executor.submit(
                    directive.run_with_dependency, dep_callable)
                self.futures[directive.location] = this_future
                futures_to_locs[this_future] = directive.location
        for f in self.futures.values():
            results.append(f.result())
        self.executor.shutdown(wait=True)
        return results


class ConfigResults(list):
    """ A list of HandlerResults that evaluates true if all results in the list are true.
    """
    def __bool__(self):
        return all(self)

    def __nonzero__(self):
        return self.__bool__()

    def __str__(self):
        return self.generate_config()

    def generate_config(self):
        """
        :return: The contents of a codetree config file matching the given results.
        """
        lines = [str(r) for r in self]
        joined = "\n".join(lines)
        if len(joined) > 0:
            joined += "\n"

        return joined
