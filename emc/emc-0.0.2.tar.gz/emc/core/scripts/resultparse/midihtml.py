from re import search

from os import listdir

if __name__ == '__main__':
    outputDir = '/home/csaba/src/csabasulyok.bitbucket.org/emc/midi/ecal2017'
    
    spacing = 0
    tab = ' ' * spacing
    
    htmlHeader = tab + '''<script src="sorttable.js"></script>
    
    <table style="width:100%" class="sortable">
      <thead>
        <tr>
          <th><a href="#a">Time stamp</a></th>
          <th><a href="#a">Instruction set</a></th>
          <th><a href="#a">VM Architecture</a></th>
          <th><a href="#a">Memory size</a></th>
          <th><a href="#a">Generation</a></th>
          <th><a href="#a">Grade</a></th>
          <th><a href="#a">Download link</a></th>
        </tr>
      </thead>
      <tbody>
    '''.replace("\n", "\n" + tab)
    
    htmlFooter = tab + '''  </tbody>
      <tfoot>
      </tfoot>
    </table>
    '''.replace("\n", "\n" + tab)
    
    
    htmlStr = htmlHeader
    
    ocis = {'Immediate':'Complex',
            'ImmediateHarvard':'Complex',
            'SingleRisc':'Single-instruction',
            'SingleRiscHarvard':'Single-instruction',
            'Stack':'Stack-based',
            'StackHarvard':'Stack-based' }
    archs = {'Immediate':'Von Neumann',
             'ImmediateHarvard':'Harvard',
             'SingleRisc':'Von Neumann',
             'SingleRiscHarvard':'Harvard',
             'Stack':'Von Neumann',
             'StackHarvard':'Harvard' }
    
    for mf in listdir(outputDir):
        match = search('emc-ecal2017-score([0-9\.]+)-oci([a-zA-Z]+)-mem([0-9]+)-time([0-9-]+)\.mid', mf)
        
        if match:
            grade = match.group(1)
            ociType = match.group(2)
            oci = ocis[ociType]
            arch = archs[ociType]
            memSize = int(match.group(3))
            timeStamp = match.group(4)
            
            htmlStr += tab + '    <tr><td>%s</td><td>%s</td><td>%s</td><td>%d</td><td>9999</td><td>%s</td><td><a href="midi/ecal2017/%s">Download</a></td></tr>\n' %(
                    timeStamp, oci, arch, memSize, grade, mf)
    
    htmlStr += htmlFooter
    print htmlStr