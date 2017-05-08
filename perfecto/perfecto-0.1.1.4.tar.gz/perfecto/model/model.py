class Project:
    def __init__(self, name, version):
        self.name = name
        self.version = version


class Job:
    def __init__(self, name, number=0):
        self.name = name
        self.number = number
