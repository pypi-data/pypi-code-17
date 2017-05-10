#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import hashlib
import ast 
import lxml.etree as ET
import xml.sax.saxutils as SAX
 
import gspread_tools as GSTool 

from difflib import SequenceMatcher


TRANSLATE_OR_NOT = {'false':'##### Ignore #####', 
                    '':'##### Need Translate #####'}


def check_similar(str1, str2):

    if(isinstance(str1, unicode)):
        str1 = str1.encode('utf-8')
    if(isinstance(str2, unicode)):
        str2 = str2.encode('utf-8')

    return SequenceMatcher(None, str1, str2).ratio()

    
def escape_check(input_str):

    # 1. single ['] and ["] should be escaped.
    # chr(92) = '\'
    block = input_str.split("'")
    input_str = block[0]
    for i in range(1, len(block)):
        if(len(input_str) == 0 or input_str[-1] != chr(92)):
            input_str += chr(92)
        input_str += "'" + block[i]
    
    block = input_str.split('"')
    input_str = block[0]
    for i in range(1, len(block)):
        if(len(input_str) == 0 or input_str[-1] != chr(92)):
            input_str += chr(92)
        input_str += '"' + block[i]
    
    return input_str
    
 
def namestring_to_googlesheet(ws, ns_manager, selected_keys=None, mode=None, title_order=None):

    global TRANSLATE_OR_NOT

    if(selected_keys == None):
        selected_keys = ns_manager.order
    if(title_order == None):
        title_order = ns_manager.file_id_list
    else:
        title_order = [x for x in title_order if x in ns_manager.file_id_list]
    title = ['Upload done.', 'Platform', 'Translatable', 'Description'] + title_order
        
    data = [title]
    ns = ns_manager.namestring
    for key in selected_keys:
    
        row_data = [key.decode('utf-8') if isinstance(key, str) else key, 
                    ns[key]['attrib'].get('platform' , '# ERROR #'),
                    ns[key]['attrib'].get('translatable', '# ERROR #'),
                    ns[key]['attrib'].get('description' , '# ERROR #')]

#        for file_id in ns_manager.file_id_list:
        for file_id in title_order:
        
            if(file_id not in ns_manager.file_id_list):
                continue

            default_str = TRANSLATE_OR_NOT[ns[key]['attrib'].get('translatable')]
            row_data.append(ns[key]['content'].get(file_id, default_str))
        #    print prefix + ns_manager.namestring[key].get(file_id, default_str)
        #    row_data.append((prefix + ns_manager.namestring[key].get(file_id, default_str)).decode('utf-8'))
        data.append(row_data)
        
    if(mode == None):
        GSTool.upload_to_current_row(ws, data, 1)
    else:
        print '[#] Use mode: %s, to upload data.' % mode
        GSTool.upload_data(ws, data, mode=mode, flag_name='END_FLAG')
        
    return

    
def googlesheet_to_namestring(ws, ns_manager=None):
 
    all_values = ws.get_all_values()
    if(len(all_values) == 0):
        print('\033[1;33m[#] Worksheet not found or no data.\033[1;m')
        return ns_manager
    else:
        rows = len(all_values)
        cols = len(all_values[0])
        print('[#] Get data from googlesheet...')

    if(ns_manager == None):
        ns_manager = NameStringManager()
            
    ns_manager.file_id_list = all_values[0][4:]
    for i in range(1, rows):
    
        if(len(all_values[i][0]) == 0):
            continue
        
        key = all_values[i][0]
    #    key = key.decode('utf-8') if isinstance(key, unicode) else key
        ns_manager.order.append(key)
        ns_manager.namestring[key] = ns_manager.namestring.get(key, {'attrib':{}, 'content':{}})
        
        attrib = {  'platform':ast.literal_eval(all_values[i][1]),
                    'translatable':'false' if(len(all_values[i][2]) != 0) else '', 
                    'description':all_values[i][3]}
                    
        ns_manager.namestring[key]['attrib'] = attrib
        
#        ns_manager.namestring[key]['attrib']['translatable'] = 'false' if(len(trans) != 0) else ''
#        ns_manager.namestring[key]['attrib']['description'] = ''
        
        for j in range(4, cols):
            file_id = all_values[0][j]
            if(all_values[i][j] in [TRANSLATE_OR_NOT['false'], TRANSLATE_OR_NOT['']]):
                continue
            else:
            #    ns_manager.namestring[key][file_id] = all_values[i][j].decode('utf-8')
               ns_manager.namestring[key]['content'][file_id] = all_values[i][j]
        
    ws.update_acell('A1', 'Download done.')
    print('\033[1;32m[+] Get data done!\033[1;m')
    return ns_manager
    

class NameStringManager:

    strfile_name = { 'android':'strings.xml',
                     'ios':'Localizable.strings'}
                             
    def __init__(self, order=None, namestring=None):
    
        if(order == None):
            if(namestring != None):
                self.order = namestring.keys()
            else:
                self.order = []
        else:
            self.order = order
            
        if(namestring == None):
            self.namestring = {}
        else:
            self.namestring = namestring
        
        self.xmltemplate_path = None
        self.file_id_list = []   
        self.deleted_ns = None
        self.name_mapping = None

        
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
    #    return False        
        return NotImplemented

        
    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
    #    return not self.__eq__(other)
        return NotImplemented    
      
      
    def size(self):
        return len(self.order)

        
    def __hash__(self):
        # Override the default hash behavior (that returns the id or the object)
    #    return hash(tuple(sorted(self.__dict__.items())))
        return int(self.get_hash(), 16)

        
    def get_entry_num(self):
        if(self.namestring == {}):
            return 0
        return sum([len(self.namestring[key]['content'].keys()) for key in self.namestring.keys()])

        
    def get_hash(self):
        
        ns = self.namestring
        m = hashlib.md5()
        file_id_str = ''.join(self.file_id_list)
        key_str = ''.join(ns.keys()).encode('utf-8')
        subkey_str = ''.join([''.join(ns[key]['content'].keys()) for key in ns.keys()]).encode('utf-8')
        entry_str = ''.join([''.join([ns[key]['content'][id].encode('utf-8') for id in ns[key]['content'].keys()]) for key in ns.keys()])
        
        m.update(file_id_str)
        m.update(key_str)
        m.update(subkey_str)
        m.update(entry_str)
        return m.hexdigest()

        
    def get_deleted_ns(self):
        return self.deleted_ns

        
    def set_xmltemplate(self, path):
        self.xmltemplate_path = path
    #    print '[+] xml template file : ' + path
        return

        
    def set_name_mapping(self, name_mapping):
        self.name_mapping = name_mapping
    #    print '[+] set name mapping done.'
        return
    
    
    def dir2lang(self, dir_name):
        if(self.name_mapping == None):
            print '[-] name_mapping not set.'
            return dir_name
        return self.name_mapping['dir_name'].get(dir_name, dir_name)
                
        
    def lang2dir(self, lang_name):
        if(self.name_mapping == None):
            print '[-] name_mapping not set.'
            return lang_name
        return self.name_mapping['lang_name'].get(lang_name, lang_name)
        
        
    def import_namestring(self, param):

        # Check parameters       
        if( param.get('platform', None) == None or
            param.get('target_path', None) == None):
            
            print '[-] Wrong parameters format.'
            return False
        else:
            target_path = param['target_path']
            platform = param['platform']
            
        if(platform not in ['ios', 'android']):
            print '[-] Unknown platform for "%s"' % (platform)
            return False
       
        if(os.path.exists(target_path) == False):
            print "[-] Target path doesn't exist."
            return False
        
        file_id_list = []
        dir_list = os.listdir(target_path)
        for subdir in dir_list:
            
            file_id = self.dir2lang(subdir)
            
            ns_file_path = '%s/%s/%s' % (target_path, subdir, self.strfile_name[platform])
            if(os.path.exists(ns_file_path) == False):
                continue
            else:
                print '[#] Find %s : %s' % (self.strfile_name[platform], ns_file_path)
                file_id_list.append(file_id)
        
            if(platform == 'ios'):
                self.localizable_to_namestring(file_id=file_id, file_path=ns_file_path)
            else:
                self.xmlfile_to_namestring(file_id=file_id, file_path=ns_file_path)
        
        self.file_id_list = file_id_list
        print self.file_id_list
#        exit()
        return True
    

    def delete_namestring_waring(self, param):
    
        old_ns = NameStringManager()
        old_ns.set_name_mapping(self.name_mapping)
        old_ns.import_namestring(param)
        
        deleted_key = [x for x in old_ns.order if (x not in self.order) == True]
        
        if(len(deleted_key) != 0):
            print('\033[1;33m\n[#] These strings will be deleted from all the %s files:\n\033[1;m' % 
                  (self.strfile_name[param['platform']]))
                  
            for i, dns in enumerate(deleted_key):
                if(param['platform'] == 'android'):
                    print('    [%d] <string name=\033[1;36m"%s"\033[1;m>' % (i, dns))
                else:
                    print('    [%d] \033[1;36m"%s"\033[1;m' % (i, dns))
            print('\033[1;33m\n[#] Are you sure to do it? (y/n) \033[1;m')
            
            if(raw_input() != 'y'):
                print('\033[1;33m[#] Do nothing.\033[1;m')
                exit()
            else:
                print('\033[1;33m[#] Deleted.\033[1;m')
                deleted_ns = NameStringManager()
                deleted_ns.file_id_list = [x for x in old_ns.file_id_list]
                deleted_ns.order = deleted_key
                
                for i, key in enumerate(deleted_key):
                    deleted_ns.namestring[key] = old_ns.namestring[key].copy()
                return deleted_ns
                
        return NameStringManager()

        
    def export_namestring(self, param=None):
        
        # Check parameters       
        if( param.get('platform', None) == None or
            param.get('target_path', None) == None):
            print '[-] Wrong parameters format.'
            return False
        else:
            target_path = param['target_path']
            platform = param['platform']
            if(platform not in ['ios', 'android']):
                print '[-] Unknown platform type: %s' % (platform)
                return False
            elif(platform == 'android' and self.xmltemplate_path == None):
                print '[-] strings.xml template file not found.'
                return False
        
        if(os.path.exists(target_path) == False):
            os.mkdir(target_path)
            self.deleted_ns = NameStringManager()
        else:
            # Check and warn user if the directory exists.
            self.deleted_ns = self.delete_namestring_waring(param)
        
    #    dir_list = os.listdir(target_path)
        for file_id in self.file_id_list:
            
            subdir = self.lang2dir(file_id)
            subdir_path = target_path + '/' + subdir
            if(os.path.exists(subdir_path) == False):
                os.mkdir(subdir_path)
            
            ns_file_path = subdir_path + '/' + self.strfile_name[platform]
            if(platform == 'ios'):
                self.namestring_to_localizable(file_id=file_id, file_path=ns_file_path)
            else:
                self.namestring_to_xmlfile(file_id=file_id, file_path=ns_file_path)
        
        return True

        
    def xmlfile_to_namestring(self, file_id, file_path):
        
        tree = ET.parse(file_path)
        root = tree.getroot()
        for child in root:
        
            raw_text = ET.tostring(child, encoding = 'unicode', method = 'html').strip()
            text = raw_text[raw_text.find('>') + 1:].replace('</string>', '') 
        #    text = (raw_text.replace('<string>', '')).replace('</string>', '')
            
            if(child.attrib.get('name') == None):
                continue
                
            key = child.attrib['name']
            if(self.namestring.get(key, None) == None):
                attrib = {  'translatable':child.attrib.get('translatable', ''), 
                            'description':'', 
                            'platform':['android']}
                self.namestring[key] = {'attrib':attrib, 'content':{}}
                self.order.append(key)
            
            if(self.namestring[key]['content'].get(file_id, None) == None):
                if(text == None):
                    text = ''
                elif(len(text) > 1 and (text[0] == '"' and text[-1] == '"')):
                    text = text[1:-1]
                    
                # xml.sax.saxutils.unescape(string): 
                #     Replace &amp; , &lt; and &gt; with '&', '<' and '>' respectively.
                     
                self.namestring[key]['content'][file_id] = SAX.unescape(text)
            #    self.namestring[key][file_id] = inv_escape_check(text).encode('utf-8')
                
        return
        

    def localizable_to_namestring(self, file_id, file_path):
    
        with open(file_path, 'r') as f:
            
            for line in f:            
                line = line.strip()
                pat = r'.*?"(.*)"\s*=\s*"(.*)";.*' 
                match = re.search(pat, line)
                
                if(match == None):
                    continue    
                key = match.group(1).decode('utf-8')
                value = match.group(2).decode('utf-8')
                
                if(self.namestring.get(key, None) == None):
                    attrib = {'translatable':'', 'description':'', 'platform':['ios']}
                    self.namestring[key] = {'attrib':attrib, 'content':{}}
                    self.order.append(key)
                
                if(self.namestring[key]['content'].get(file_id, None) == None):
                    self.namestring[key]['content'][file_id] = value
            
        return
            
            
    def namestring_to_xmlfile(self, file_id, file_path):
    
        tree = ET.ElementTree(file=self.xmltemplate_path)
        root = tree.getroot()
        root.text = '\n\n    '
        
        for i, key in enumerate(self.order):
        
            attrib = self.namestring[key]['attrib']
            if('android' not in attrib['platform']):
                continue
        
            translatable = attrib.get('translatable', '')
            value = self.namestring[key]['content'].get(file_id, None)
            if(value == None):
                continue
            
            temp_node = ET.SubElement(root, 'string')
            temp_node.text = '"%s"' % (escape_check(value))
        #    temp_node.text = '"' + escape_check(content).decode('utf-8') + '"'
            
            temp_node.attrib['name'] = key
            if(len(translatable) != 0):
                temp_node.attrib['translatable'] = 'false'
                
            temp_node.tail = '\n    '
            if(i == len(self.order) - 1):
                temp_node.tail += '\n\n'
    
        output = ET.tostring(tree, method = "html", encoding = 'utf-8')
        output = output.replace('&lt;', '<')
        output = output.replace('&gt;', '>')
        with open(file_path, 'w') as f:
            f.write(output)
            
        return
        
        
    def namestring_to_localizable(self, file_id, file_path):

        print file_id, file_path
    
        with open(file_path, 'w') as f:
            for i, key in enumerate(self.order):
            
                attrib = self.namestring[key]['attrib']
                if('ios' not in attrib['platform']):
                    continue
                    
                value = self.namestring[key]['content'].get(file_id, None)
                if(value == None):
                    continue
                
                if(isinstance(key, unicode) == True):
                    key = key.encode('utf-8')
                if(isinstance(value, unicode) == True):
                    value = value.encode('utf-8')
                
                f.write('"%s" = "%s";\n\n' % (key, value))
                
        return
            
            
    def merge_manager(self, other_manager):
    
        if (isinstance(other_manager, self.__class__) == False):
            print '[NameStringManager] merge_manager() fail: "Invalid ns_manager object"'
            return False
        
        print self.file_id_list 
        print other_manager.file_id_list
    #    exit()
        
        # Merge file-id-list.
        for file_id in other_manager.file_id_list:
            if(file_id not in self.file_id_list):
                self.file_id_list.append(file_id)

        temp_order = []
        temp_ns = {}
        other_ns = other_manager.namestring
        # Merge namestring.
        for key in other_ns.keys():
            
            # key exist.
            if(self.namestring.get(key) != None):
            
                # Check platform.
                platform = other_ns[key]['attrib'].get('platform', None)[0]
                
                # Consistent platform 
                if(platform in self.namestring[key]['attrib'].get('platform')):
                    for file_id in other_ns[key]['content'].keys():
                        if( self.namestring[key]['content'].get(file_id) == None):
                            self.namestring[key]['content'][file_id] = other_ns[key]['content'][file_id]
                
                # Inconsistent platform 
                else:
                
                    flag = 0
                    for file_id in other_ns[key]['content'].keys():
                        value = other_ns[key]['content'][file_id]
                        if(self.namestring[key].get(file_id) != value):
                            flag = 1
                            break
                    
                    # Consistent content, add platform tag directly
                    if(flag == 0):
                        self.namestring[key]['attrib']['platform'].append(platform)
                        
                    # Inonsistent content, add a conflict key.
                    else:
                        conflict_key = key + ' (%s)' % platform
                        self.order.append(conflict_key)
                        self.namestring[conflict_key] = other_manager.namestring[key].copy()
                            
            # key doesn't exist.
            else:
                
                platform = other_ns[key]['attrib'].get('platform', None)[0]
                
                # first merge mode
                if(platform == 'ios'):
                
                    # do key matching.
                    flag = 0
                    value = other_ns[key]['content'][file_id]
                    
                    for andr_key in self.namestring.keys():
                    
                        andr_value = self.namestring[andr_key]['content'][file_id]
                        ios_value = value
                        
                        ratio = check_similar(andr_value, ios_value)
                        if(ratio >= 0.70):
                            if(len(self.namestring[andr_key]['attrib']['description']) == 0):
                                self.namestring[andr_key]['attrib']['description'] = '[similar] ios_key: ' + key + '(%.2f)' % ratio
                            else:
                                self.namestring[andr_key]['attrib']['description'] += '\n[similar] ios_key: ' + key + '(%.2f)' % ratio
                        
                    if(flag == 0):
                        temp_order.append(key)
                        temp_ns[key] = other_ns[key]
                    #    self.order.append(key)
                    #    self.namestring[key] = other_ns[key].copy()
                        continue
                
                # normal mode
                else:
                    self.order.append(key)
                    self.namestring[key] = other_ns[key].copy()
                    continue
        
        for key in temp_order:
            self.order.append(key)
            self.namestring[key] = temp_ns[key].copy()
        
        return True
        
        '''
        if(ratio == 1.0):
            self.namestring[andr_key]['attrib']['platform'].append(platform)
            flag = 1
        '''
        '''
        if(self.namestring[andr_key]['content'][file_id] == value):
            print '============ The same ============'
            print 'ios_key: ', key.encode('utf-8')
            print 'android_key: ', andr_key.encode('utf-8')
            print 'Has the same value: ', value.encode('utf-8')
            
            if(len(self.namestring[andr_key]['attrib']['description']) == 0):
                self.namestring[andr_key]['attrib']['description'] = '[same] ios_key: ' + key
            else:
                self.namestring[andr_key]['attrib']['description'] += '\n[same] ios_key: ' + key
                
            self.namestring[andr_key]['attrib']['platform'].append(platform)
            flag = 1
            
        else:    
            
            andr_value = self.namestring[andr_key]['content'][file_id]
            ios_value = value
            if (check_similar(andr_value, ios_value)):
        #    lower_andr_value = self.namestring[andr_key]['content'][file_id].lower()
        #    lower_ios_value = value.lower()
        #    if(lower_andr_value == lower_ios_value):
                print '============ Similar ============'
                print 'ios_key: ', key.encode('utf-8')
                print 'android_key: ', andr_key.encode('utf-8')
                print 'Has similar value: ', value.encode('utf-8')
                
                if(len(self.namestring[andr_key]['attrib']['description']) == 0):
                    self.namestring[andr_key]['attrib']['description'] = '[similar] ios_key: ' + key
                else:
                    self.namestring[andr_key]['attrib']['description'] += '\n[similar] ios_key: ' + key
        '''
    
    
        '''
            # Consistent platform 
            if(platform in self.namestring[key]['attrib'].get('platform')):
            
                # Uncommon key
                if(self.namestring.get(key) == None):
                    self.order.append(key)
                    self.namestring[key] = other_ns[key].copy()
                    continue
            
                # Common key
                for file_id in other_ns[key]['content'].keys():
                    if( self.namestring[key]['content'].get(file_id) == None):
                        self.namestring[key]['content'][file_id] = other_ns[key]['content'][file_id]
                        
            # Inconsistent platform    
            else:
            
                # Common key
                
            
                # Uncommon key
                for file_id in other_ns[key]['content'].keys():
                    
                    flag = 0
                    value = other_ns[key]['content'][file_id]
                    for andr_key in self.namestring.keys():
                        if(self.namestring.keys[andr_key]['content'][file_id] == value):
                            print 'android_key: ' + andr_key
                            print 'ios_key: ' + key
                            print 'Has the same value: '+ value
                            self.namestring[andr_key]['attrib']['platform'].append(platform)
                            flag = 1
                    
                    if(flag == 0):
                        conflict_key = key + ' (%s)' % platform
                        self.order.append(conflict_key)
                        self.namestring[conflict_key] = other_manager.namestring[key].copy()
                            
                #    if(self.namestring[key]['content'][file_id] == other_manager.namestring[key]['content'][file_id]):
                #        print 
        
                if(self.namestring[key]['content'] == other_manager.namestring[key]['content']):
                    self.namestring[key]['attrib']['platform'].append(platform)
                else:
                    conflict_key = key + ' (%s)' % platform
                    self.order.append(conflict_key)
                    self.namestring[conflict_key] = other_manager.namestring[key].copy()
        '''
    