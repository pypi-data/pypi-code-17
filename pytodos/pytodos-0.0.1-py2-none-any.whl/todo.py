# -*- coding: utf-8 -*-
class Todo(object):

    def __init__(self):
        """Todo Base Class
        """
        self.todos = []

    def init(self):
        """init `todo` file
        if file exists, then initialization self.todos
        and record current max index of todos
        : when add a new todo, the `idx` via only `self.current_max_idx + 1`
        """
        print 'Hello world'
        return 'hello world'
