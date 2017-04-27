'''
Generate HTML code for a model directory (hall of fame on EMC website)
'''
from re import search

from emc.core.integ.modeldir import ModelDirectory


def generateHtml(path):
    md = ModelDirectory(path)
    
    spacing = 8
    tab = ' ' * spacing
    htmlStr = tab + '<table style="width:100%">\n'
    htmlStr += tab + '  <tr><td><b>Time stamp</b></td><td><b>Crop times</b></td><td><b>Download link</b></td></tr>\n'
    for mf in md.filenames:
        match = search('emc_time([0-9-]+)_cropped_([0-9\.]+)_([0-9\.]+)\.mid', mf)
        
        if match:
            timeStamp = match.group(1)
            cropStart = match.group(2)
            cropEnd = match.group(3)
            
            htmlStr += tab + '  <tr><td>%s</td><td>%ss-%ss</td><td><a href="midi/halloffame/%s">Download</a></td></tr>\n' %(
                    timeStamp, cropStart, cropEnd, mf)
        
        else:
            print 'Warning: no match for %s' %mf
    
    htmlStr += tab + '</table>'
    print htmlStr

if __name__ == '__main__':
    path = 'd:/QM/ECS750/csabasulyok.bitbucket.org/emc/midi/halloffame'
    generateHtml(path)