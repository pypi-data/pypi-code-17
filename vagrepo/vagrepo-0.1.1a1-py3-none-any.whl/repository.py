import json
import os
import os.path
import pathlib

class Repository:

    PATH_DEFAULT = os.path.expanduser(os.path.join('~', '.vagrepo'))
    METADATA_FN = 'metadata.json'

    def __init__(self, path=None):
        if path is None:
            self.path = Repository.PATH_DEFAULT
        else:
            self.path = path

        if not os.path.exists(self.path):
            os.makedirs(self.path)
        elif not os.path.isdir(self.path):
            raise ValueError('path %s is not a directory' % self.path)

    @property
    def box_names(self):
        pattern = '**/%s' % Repository.METADATA_FN
        matches = pathlib.Path(self.path).glob(pattern)
        paths = [m.parent.relative_to(self.path) for m in matches]
        return ['/'.join(p.parts) for p in paths]

    def create(self, name, description=None):
        '''Create a new box'''
        name_parts = name.split('/')
        box_dir = pathlib.Path(self.path, *name_parts)
        metadata_path = pathlib.Path(box_dir, Repository.METADATA_FN)
        box_dir.mkdir(parents=True)
        with metadata_path.open('w') as f:
            json.dump({'name': name, 'versions': []}, f)

#     @property
#     def boxes(self):
#         pattern = '**/%s' % METADATA_FN
#         matches = pathlib.Path(self.path).glob(pattern)
#         return [Box(str(m)) for m in matches]

# class Box:
#     def __init__(self, path):
#         self.path = path

