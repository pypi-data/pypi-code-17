"""
I'm saving several tools that seem to get a lot of use into one convenient place to save time on
lookup and for ease of import.
These are really just a complete python noob's attempt to gather all the useful tools that I've
come across so far in my perpetually futile attempts to pass myself off as a half-assed decent
programmer.
"""
import pickle
import collections
import functools
import inspect
import os.path
import re
import unicodedata
import uuid

####################################################################################################
########################################## CLASS HELPERS ###########################################

def gencomment(text, **kwargs):
    hdict = {'left': '<', 'center': '^', 'right': '>'}
    halign = hdict.get(kwargs.get('halign','^'))
    width = kwargs.get('width', 100)
    text = f' {text} '
    try:
        return '{:#{halign}{width}}'.format(text, halign=halign, width=width)
    except Exception as ex:
        print(ex)

####################################################################################################
############################################ DECORATORS ############################################

######################################## Class, (no pickle) ########################################
class memoized(object):
   """Decorator. Caches a function's return value each time it is called.
   If called later with the same arguments, the cached value is returned
   (not reevaluated).
   """
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      if not isinstance(args, collections.Hashable):
         # uncacheable. a list, for instance.
         # better to not cache than blow up.
         return self.func(*args)
      if args in self.cache:
         return self.cache[args]
      else:
         value = self.func(*args)
         self.cache[args] = value
         return value
   def __repr__(self):
      """Return the function's docstring."""
      return self.func.__doc__
   def __get__(self, obj, objtype):
      """Support instance methods."""
      return functools.partial(self.__call__, obj)

######################################### Class, (pickle) ##########################################

class Memorize(object):
   """
   A function decorated with @Memorize caches its return
   value every time it is called. If the function is called
   later with the same arguments, the cached value is
   returned (the function is not reevaluated). The cache is
   stored as a .cache file in the current directory for reuse
   in future executions. If the Python file containing the
   decorated function has been updated since the last run,
   the current cache is deleted and a new cache is created
   (in case the behavior of the function has changed).
   """

   def __init__(self, func):
       self.func = func
       self.set_parent_file()  # Sets self.parent_filepath and self.parent_filename
       self.__name__ = self.func.__name__
       self.set_cache_filename()
       if self.cache_exists():
           self.read_cache()  # Sets self.timestamp and self.cache
           if not self.is_safe_cache():
               self.cache = {}
       else:
           self.cache = {}

   def __call__(self, *args):
       if not isinstance(args, collections.Hashable):
           return self.func(*args)
       if args in self.cache:
           return self.cache[args]
       else:
           value = self.func(*args)
           self.cache[args] = value
           self.save_cache()
           return value

   def set_parent_file(self):
       """
       Sets self.parent_file to the absolute path of the
       file containing the memoized function.
       """
       rel_parent_file = inspect.stack()[-1].filename
       self.parent_filepath = os.path.abspath(rel_parent_file)
       self.parent_filename = _filename_from_path(rel_parent_file)

   def set_cache_filename(self):
       """
       Sets self.cache_filename to an os-compliant
       version of "file_function.cache"
       """
       filename = _slugify(self.parent_filename.replace('.py', ''))
       funcname = _slugify(self.__name__)
       self.cache_filename = filename + '_' + funcname + '.cache'

   def get_last_update(self):
       """
       Returns the time that the parent file was last
       updated.
       """
       last_update = os.path.getmtime(self.parent_filepath)
       return last_update

   def is_safe_cache(self):
       """
       Returns True if the file containing the memoized
       function has not been updated since the cache was
       last saved.
       """
       if self.get_last_update() > self.timestamp:
           return False
       return True

   def read_cache(self):
       """
       Read a pickled dictionary into self.timestamp and
       self.cache. See self.save_cache.
       """
       with open(self.cache_filename, 'rb') as f:
           data = pickle.loads(f.read())
           self.timestamp = data['timestamp']
           self.cache = data['cache']

   def save_cache(self):
       """
       Pickle the file's timestamp and the function's cache
       in a dictionary object.
       """
       with open(self.cache_filename, 'wb+') as f:
           out = dict()
           out['timestamp'] = self.get_last_update()
           out['cache'] = self.cache
           f.write(pickle.dumps(out))

   def cache_exists(self):
       """
       Returns True if a matching cache exists in the current directory.
       """
       if os.path.isfile(self.cache_filename):
           return True
       return False

   def __repr__(self):
       """ Return the function's docstring. """
       return self.func.__doc__

   def __get__(self, obj, objtype):
       """ Support instance methods. """
       return functools.partial(self.__call__, obj)

def _slugify(value):
   """
   Normalizes string, converts to lowercase, removes
   non-alpha characters, and converts spaces to
   hyphens. From
   http://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename-in-python
   """
   value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
   value = re.sub(r'[^\w\s-]', '', value.decode('utf-8', 'ignore'))
   value = value.strip().lower()
   value = re.sub(r'[-\s]+', '-', value)
   return value

def _filename_from_path(filepath):
   return filepath.split('/')[-1]

############################################## TOOLS ###############################################

def flatten(aList):
    """
    aList: a list
    Returns a copy of aList, which is a flattened version of aList
    """
    return ([aList] if not(type(aList) == list)
            else aList if len(aList) == 0
            else flatten(aList[0]) + flatten(aList[1:]))

####################################################################################################
############################################## TREES ###############################################



def sanitize_id(id):
    return id.strip().replace(" ", "")

(_ADD, _DELETE, _INSERT) = range(3)
(_ROOT, _DEPTH, _WIDTH) = range(3)

class Node:

    def __init__(self, name, identifier=None, expanded=True):
        self.__identifier = (str(uuid.uuid1()) if identifier is None else
                sanitize_id(str(identifier)))
        self.name = name
        self.expanded = expanded
        self.__bpointer = None
        self.__fpointer = []

    @property
    def identifier(self):
        return self.__identifier

    @property
    def bpointer(self):
        return self.__bpointer

    @bpointer.setter
    def bpointer(self, value):
        if value is not None:
            self.__bpointer = sanitize_id(value)

    @property
    def fpointer(self):
        return self.__fpointer

    def update_fpointer(self, identifier, mode=_ADD):
        if mode is _ADD:
            self.__fpointer.append(sanitize_id(identifier))
        elif mode is _DELETE:
            self.__fpointer.remove(sanitize_id(identifier))
        elif mode is _INSERT:
            self.__fpointer = [sanitize_id(identifier)]

class Tree:

    def __init__(self):
        self.nodes = []

    def get_index(self, position):
        for index, node in enumerate(self.nodes):
            if node.identifier == position:
                break
        return index

    def create_node(self, name, identifier=None, parent=None):

        node = Node(name, identifier)
        self.nodes.append(node)
        self.__update_fpointer(parent, node.identifier, _ADD)
        node.bpointer = parent
        return node

    def show(self, position, level=_ROOT):
        queue = self[position].fpointer
        if level == _ROOT:
            print("{0} [{1}]".format(self[position].name, self[position].identifier))
        else:
            print("\t"*level, "{0} [{1}]".format(self[position].name, self[position].identifier))
        if self[position].expanded:
            level += 1
            for element in queue:
                self.show(element, level)  # recursive call

    def expand_tree(self, position, mode=_DEPTH):
        # Python generator. Loosly based on an algorithm from 'Essential LISP' by
        # John R. Anderson, Albert T. Corbett, and Brian J. Reiser, page 239-241
        yield position
        queue = self[position].fpointer
        while queue:
            yield queue[0]
            expansion = self[queue[0]].fpointer
            if mode is _DEPTH:
                queue = expansion + queue[1:]  # depth-first
            elif mode is _WIDTH:
                queue = queue[1:] + expansion  # width-first

    def is_branch(self, position):
        return self[position].fpointer

    def __update_fpointer(self, position, identifier, mode):
        if position is None:
            return
        else:
            self[position].update_fpointer(identifier, mode)

    def __update_bpointer(self, position, identifier):
        self[position].bpointer = identifier

    def __getitem__(self, key):
        return self.nodes[self.get_index(key)]

    def __setitem__(self, key, item):
        self.nodes[self.get_index(key)] = item

    def __len__(self):
        return len(self.nodes)

    def __contains__(self, identifier):
        return [node.identifier for node in self.nodes if node.identifier is identifier]



####################################################################################################


