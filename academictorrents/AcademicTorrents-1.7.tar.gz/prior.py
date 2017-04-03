import npyscreen,pdb, six, sys

_handles = None
_so = None

class PriorityForm(npyscreen.FormMultiPageAction):
    
    def afterEditing(self):        
        self.parentApp.setNextForm(None)        
        tempDict = self.priorityDict
        for h, priorityList in tempDict.items():
            new_priorityList = []
            for i in range(h.get_torrent_info().num_files()):
                if i in priorityList.value:
                    new_priorityList.append(1)
                else:
                    new_priorityList.append(0)
            self.priorityDict[h]=new_priorityList
        global _so
        _so = self.priorityDict
        #self.editing = False
    
    def on_ok(self):
        pass
    
    def on_cancel(self):
        exit()
    
    def create(self):
        self.priorityDict = {}
        for h in _handles:
            paths = []
            for f in h.get_torrent_info().files():
                paths.append(f.path)
            self.priorityDict[h] = self.add_widget_intelligent(npyscreen.TitleMultiSelect, max_height = 5, value = [1,], name=h.name(),
                values = paths, scroll_exit=True)        

class PriorityApp(npyscreen.NPSAppManaged):
    def onStart(self):        
        self.addForm('MAIN', PriorityForm, name='Files to download')
        
    def set_handler(self,handles):
        global _handles
        _handles = handles

def get_so():
    return _so
    
