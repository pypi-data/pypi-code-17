import os
import sys

class TLCount:

    def __init__(self):
        self.textLine = 0

    def traverseDir(self, dir_path):
        dir_list = os.listdir(dir_path)
        for dir_name in dir_list:
            if os.path.isdir(dir_path + dir_name):
                sub_dir = dir_path + dir_name + '/'
                # print sub_dir + ' is Dir.' #debug code
                self.traverseDir(sub_dir)
            elif os.path.isfile(dir_path + dir_name):
                if self.fileFilter(dir_name):
                    file_path = dir_path + dir_name
                    self.countLine(file_path)
                else:
                    continue

    def printTextLine(self):
        print 'total line is %d.' % self.textLine

    def countLine(self, filePath):
        # print '\n\n ' + filePath #debug code
        content = open(filePath, 'r')
        i = 0
        for c in content:
            # print c  #debug code
            i += 1
        # print 'SINGLE FILE %d LINES.\n' % i #debug code
        self.textLine += i

    def fileFilter(self, fileName):
        suffix = fileName.split('.')[-1]
        if suffix == 'py':
            return True
        else:
            return False

    def main(self):
        path = sys.argv[1] + '/'
        tlc = self.tlc()
        tlc.traverseDir(path)
        tlc.printTextLine()

def main():
    path = sys.argv[1] + '/'
    tlc = TLCount()
    tlc.traverseDir(path)
    tlc.printTextLine()

if __name__ == '__main__':
    # path = '/Users/MacbookAir/Desktop/django_demo/'
    # path = '/Users/MacbookAir/PycharmProjects/'
    main()
    # print tlc.fileFilter('a.txt.c.py')
