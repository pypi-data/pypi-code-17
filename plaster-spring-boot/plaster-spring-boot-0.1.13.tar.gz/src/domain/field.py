from java_type import JavaType


class Field:
    def __init__(self, field_name, field_type):
        self.name = field_name
        self.field_type = JavaType(field_type)

    def __str__(self):
        return '%s %s' % (str(self.field_type), str(self.name))

