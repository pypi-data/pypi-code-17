class Mammals:
    def __init__(self):
        self.members = ['Eagle', 'Sparrow', 'Mina']
    def printMembers(self):
        print('Printing ...')
        for member in self.members:
            print('\t member = %s' % member)

