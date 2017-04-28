#!/usr/bin/env python
import os.path
import importlib


from paleomix.node import Node, CommandNode
from paleomix.atomiccmd.builder import \
    AtomicCmdBuilder, \
    use_customizable_cli_parameters, \
    create_customizable_cli_parameters
from paleomix.common.fileutils import \
    describe_files, \
    move_file, \
    reroot_path
from paleomix.common.utilities import \
    safe_coerce_to_tuple


class SimpleExecNode(CommandNode):
    """Basic CommandNode to execute command-line scripts"""
    def __init__(self, executable, input_file, output_file, options={},
                 description=None, dependencies=()):

        cmd = AtomicCmdBuilder([executable, "%(IN_FILE)s", "%(OUT_FILE)s"],
                               IN_FILE=input_file,
                               OUT_FILE=output_file)

        for opt, value in options.iteritems():
            cmd.set_option(opt, value)

        if description is None:
            description = "<%r : %r -> %r>" % (os.path.basename(executable),
                                               input_file, output_file)

        CommandNode.__init__(self,
                             command=cmd.finalize(),
                             description=description,
                             dependencies=dependencies)


class ExecNode(CommandNode):
    @create_customizable_cli_parameters
    def customize(cls, call, description=None, threads=1,
                  dependencies=(), builder_kwargs={}):

        if not description:
            call = safe_coerce_to_tuple(call)
            description = "<%r>" % " ".join(call)

        cmd = AtomicCmdBuilder(call, **builder_kwargs)

        return {"command": cmd,
                "description": description}

    @use_customizable_cli_parameters
    def __init__(self, params):
        CommandNode.__init__(self,
                             params.command.finalize(),
                             params.description,
                             params.threads,
                             params.dependencies)


class ExecModuleNode(Node):
    """run a python function as a Node"""
    def __init__(self, module, function, input_files, output_files,
                 dependencies=(), description=None,
                 function_in_args="input_files",
                 function_out_args="output_files",
                 function_out_tmp=None,
                 **function_kwargs):
        self.module = 'paleomix.tools.metabit.' + module
        self.function = function
        self.function_in_args = function_in_args
        self.function_out_args = function_out_args
        self.function_kwargs = function_kwargs
        # args that must redirect to tmp dir
        # typically output directories
        self.function_out_tmp = function_out_tmp

        if not description:
            description = module + '.' + function

        description = "<%s: %s -> %s>" % (description,
                                          describe_files(input_files),
                                          describe_files(output_files))

        Node.__init__(self,
                      description=description,
                      input_files=input_files,
                      output_files=output_files,
                      dependencies=dependencies)

    def _run(self, config, temp):
        module = importlib.import_module(self.module)
        func = getattr(module, self.function)

        input_files = list(self.input_files)
        output_files = [reroot_path(temp, filename)
                        for filename in self.output_files]

        # resolve conflict in case 'input_files' is also an argument for the function
        #if "input_files" in func.func_code.co_varnames:
        #    self.function_kwargs.update({"input_files": input_files})
        if self.function_in_args:
            if isinstance(self.function_in_args, list):
                for in_arg, in_file in zip(self.function_in_args, input_files):
                    self.function_kwargs.update({in_arg: in_file})
            else:
                self.function_kwargs.update({self.function_in_args: input_files})

        #if "output_files" in func.func_code.co_varnames:
        #    self.function_kwargs.update({"output_files": output_files})
        if self.function_out_args:
            if isinstance(self.function_out_args, list):
                for out_arg, out_file in zip(self.function_out_args, output_files):
                    self.function_kwargs.update({out_arg: out_file})
            else:
                self.function_kwargs.update({self.function_out_args: output_files})

        if self.function_out_tmp:
            if isinstance(self.function_out_tmp, str):
                self.function_out_tmp = [self.function_out_tmp]

            for out_tmp in self.function_out_tmp:
                self.function_kwargs[out_tmp] \
                    = reroot_path(temp, self.function_kwargs[out_tmp])

        func(**self.function_kwargs)

    def _teardown(self, _config, temp):
        expected_files = [reroot_path(temp, filename)
                          for filename in self.output_files]

        self._check_for_missing_files(expected_files, "output")
        for tmp_f, commited_f in zip(expected_files, list(self.output_files)):
            move_file(tmp_f, commited_f)
