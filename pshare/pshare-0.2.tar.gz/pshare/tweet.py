# Author: Brandon Powers

# Holds a readable model for a Tweet, fields for both verbose & non-verbose output

class Tweet:
    def __init__(self, name, screen_name, text, created_at, id_num):
        self.name = name
        self.screen_name = screen_name
        self.text = text
        self.created_at = created_at
        self.id_num = id_num

    def display(self, verbose):
        if verbose:
            print self.name + ' (@' + self.screen_name + ')'
            print self.created_at
            print self.id_num
            print self.text
        else:
            print self.name + ' (@' + self.screen_name + ')'
            print self.text
        print
