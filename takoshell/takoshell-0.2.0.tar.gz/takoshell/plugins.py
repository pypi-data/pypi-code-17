# This file is part of tako
# Copyright (c) 2015-2017 Adam Hartz <hartz@mit.edu> and contributors
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the Soopycat License, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the Soopycat License for more details.
#
# You should have received a copy of the Soopycat License along with this
# program.  If not, see <https://smatz.net/soopycat>.
#
#
# tako is a fork of xonsh (http://xon.sh)
# xonsh is Copyright (c) 2015-2016 the xonsh developers and is licensed under
# the 2-Clause BSD license.


class PluginEnv(dict):
    def __init__(self, *args, parent=None, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.parent = parent

    def __getitem__(self, key):
        if dict.__contains__(self, key):
            return dict.__getitem__(self, key)
        else:
            if self.parent is None:
                raise KeyError
            else:
                return self.parent[key]

    def __contains__(self, key):
        if dict.__contains__(self, key):
            return True
        else:
            return self.parent.__contains__(self, key)
