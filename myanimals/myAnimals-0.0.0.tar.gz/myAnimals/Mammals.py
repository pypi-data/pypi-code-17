class Mammals:
    def __init__(self):
        self.members = ['Tiger', 'Bat', 'Whale']
    def printMembers(self):
        print('Printing ...')
        for member in self.members:
            print('\t member = %s' % member)
