import src.data.java_types as java_types


class JavaType:
    def __init__(self, type_string):
        self.class_name = java_types.fetch_type(type_string)
        if not self.class_name:
            raise ValueError("Unrecognized type ['%s']" % type_string)

        self.dependency = java_types.fetch_dependency(self.class_name)

    def has_dependency(self):
        return not not self.dependency
