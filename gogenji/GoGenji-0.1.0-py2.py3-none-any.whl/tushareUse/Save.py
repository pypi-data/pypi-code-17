from .Helper import *

#save images to word
def saveImagesToWord(title,content,numberOfPictures):
    r = openDocument()
    r.add_text(title)
    r.add_text(content)
    no = 0
    for i in range(0, numberOfPictures):
        no = no + 1
        filename = 'Files/Images/i{}.png'.format(no)
        r.add_picture(filename)
    saveDocument()

#save text to word
def saveTextToWord(content):
    r = openDocument()
    r.add_text(content)
    saveDocument()

#save table to word
def saveTableToWord(name, content):
    r = openDocument()
    r.add_text('                                                                                                                                                                           ')
    r.add_text('\nTable Name: {}'.format(name))
    if name == 'basics':
        table = addTableToDocument(content.shape[0],2)
        for i in range(0, content.shape[0]):
            table.rows[i].cells[0].text = ['{}'.format(content.iloc[[i]])][0].split('\n')[0].split('   ')[0]
            table.rows[i].cells[1].text = ['{}'.format(content.iloc[[i]])][0].split('\n')[0].split('   ')[1]
    else:
        table = addTableToDocument(content.shape[0]+1, content.shape[1])
        for j in range(content.shape[-1]):
            table.cell(0,j).text = content.columns[j]
            # if j>12: #will experience serious lag
            #     break
        for i in range(content.shape[0]):
            # if i > 12:
            #     break
            for j in range(content.shape[-1]):
                # if j >12:
                #     break
                table.cell(i+1,j).text = str(content.values[i,j])
    saveDocument()

#save images to local and close
def saveImage(plt,noOfImage):
    filename = 'Files/Images/i{}.png'.format(noOfImage)
    plt.savefig(filename)
    plt.close()#comment this if need to see images