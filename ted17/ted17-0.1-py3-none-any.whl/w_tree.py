# -*- coding: utf-8 -*-

import PyQt5.QtWidgets as Qw
import PyQt5.QtCore as Qc
import locale
import sys


class Foo:
    def __init__(self, **args):
        for key, value in args.items():
            setattr(self, key, value)

    def todic(self):
        # Return a dictionary of attributes: values
        dic = {}
        for attr in [i for i in self.__dict__.keys() if i[:1] != '_']:
            dic[attr] = getattr(self, attr)
        return dic

    def __repr__(self):
        txt = 'Class Foo with attributes:\n'
        for attr in [i for i in self.__dict__.keys() if i[:1] != '_']:
            txt += '%s : %s\n' % (attr, getattr(self, attr))
        return txt


def tst():
    rv = Foo(onoma='Teddy', xora='Ellada')
    return rv


class Node():
    def __init__(self, name, parent, txtfields, vals):
        self._name = name
        self._parent = parent
        self._children = []
        self._txtfields = txtfields
        self._vals = vals
        self._cols = self._txtfields + self._vals
        self.no_txts = len(txtfields)
        self.no_vals = len(vals)
        self.types = [0 for i in range(self.no_txts)] + [1 for i in range(self.no_vals)]
        if parent is not None:
            # Μετά την δημιουργία νέου node κάνουμε τα αθροίσματα ιεραρχικά
            parent.add_child(self)
            self.update_parent(self._cols)
        print(self.types)

    def update_parent(self, cols):
        # Εδώ γίνεται ο υπολογισμός των αθροισμάτων στην ιεραρχία
        print(self._name, self._cols)
        if self._parent:
            for i, el in enumerate(cols):
                if self.types[i]:
                    self._parent._cols[i] += cols[i]
            if self._parent._parent is not None:
                self._parent.update_parent(cols)

    def type_info(self):
        return "NODE"

    def add_child(self, child):
        self._children.append(child)

    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def value(self, column):
        if self.types[column]:
            return locale.format("%0.2f", self._cols[column], grouping=True)
        else:
            return self._cols[column]

    def value_formated(self, column):
        return self._vals[column]

    def set_value(self, value, column):
        self._vals[column] = value

    def child(self, row):
        return self._children[row]

    def child_count(self):
        return len(self._children)

    def parent(self):
        return self._parent

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)

    def __repr__(self):
        return self._name


class Treemodel(Qc.QAbstractItemModel):
    def __init__(self, root, headers, parent=None):
        super().__init__(parent)
        self._root_node = root
        self._headers = headers

    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self._root_node
        else:
            parentNode = parent.internalPointer()
        return parentNode.child_count()

    def columnCount(self, parent):
        rnod = self._root_node
        return(rnod.no_txts + rnod.no_vals + 1)
        # return len(self._headers)

    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == Qc.Qt.DisplayRole or role == Qc.Qt.EditRole:
            if index.column() == 0:
                return node.name()
            else:
                return node.value(index.column() - 1)
        if role == Qc.Qt.TextAlignmentRole:
            if index.column() >= 1:  # ???

                if node.types[index.column() - 1]:
                    return Qc.Qt.AlignRight
                else:
                    return Qc.Qt.AlignLeft

    def headerData(self, section, orientation, role):
        if role == Qc.Qt.DisplayRole:
            if len(self._headers) - 1 < section:
                return 'no header'
            return self._headers[section]
        if role == Qc.Qt.TextAlignmentRole:
            return Qc.Qt.AlignCenter

    def flags(self, index):
        return Qc.Qt.ItemIsEnabled | Qc.Qt.ItemIsSelectable | Qc.Qt.ItemIsEditable

    def parent(self, index):
        node = self.getNode(index)
        parentNode = node.parent()
        if parentNode == self._root_node:
            return Qc.QModelIndex()
        return self.createIndex(parentNode.row(), 0, parentNode)

    def index(self, row, column, parent):
        parentNode = self.getNode(parent)
        childItem = parentNode.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return Qc.QModelIndex

    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self._root_node


class Treedata(Qw.QTreeView):
    def __init__(self, parent=None):
        super().__init__(parent)
        # if model:
        #     self.setModel(model)
        # self.setRootIndex(model.index(0,0, None))


def lmo_hierarchy(lmos, split_char='.'):
    '''
    Δίνοντας ένα λογαριασμό της μορφής x2.34.56
    επιστρέφει ['x', 'x2', 'x2.34', 'x2.34.56', 't', <'t267' ή 't35'>]
    '''
    assert len(lmos) > 1
    listfinal = []
    listlmo = lmos.split(split_char)
    listfinal.append(lmos[0])
    tmp = ''
    for el in listlmo:
        if tmp == '':
            tmp = el
        else:
            tmp = split_char.join([tmp, el])
        listfinal.append(tmp)
    return listfinal


def nc():
    vls = [['54.00.7113', 'ΦΠΑ ΠΩΛΗΣΕΩΝ 13%', 0, 13],
           ['71.00.7013', 'ΠΩΛΗΣΕΙΣ 13%', 0, 100]
           ]
    nd = {}
    nd['0'] = Node('root', None, ['v1'], [0, 0])
    for val in vls:
        hier = lmo_hierarchy(val[0])
        print(hier)
        for i, el in enumerate(hier[:-1]):
            if i == 0:
                key = '0'
            else:
                key = hier[i-1]
            print(el, nd[key])
            nd[el] = Node(el, nd[key], [''], [0, 0])
        nd[val[0]] = Node(val[0], nd[hier[-2]], [val[1]], [val[2], val[3]])
    return nd['0']

if __name__ == '__main__':
    nd = Node('root', None, ['a1', 'a2'], [0, 0])
    nd0 = Node('root', None, ['a1', 'a2'], [0, 0])
    nd1 = Node('10', nd0, ['ted', 'laz'], [1, 10])
    nd2 = Node('20', nd0, ['pop', 'daz'], [0, 0])
    nd3 = Node('20.00', nd2, ['pop', 'daz'], [3, 30])
    nd4 = Node('20.01', nd2, ['pop', 'daz'], [0, 0])
    nd5 = Node('20.01.00', nd4, ['pop', 'daz'], [4, 40.31])
    nd6 = Node('20.01.01', nd4, ['pop', 'daz'], [5, 50.25])
    nd7 = Node('30', nd0, ['pop', 'daz'], [5, 50])
    print(nd0._vals)
    aaa = Foo(epo='Laz', ono='Ted')
    aaa

    app = Qw.QApplication(sys.argv)
    treeview = Treedata()
    labels = ['Λογαριασμός', 'Περιγραφή', 'Χρέωση', 'Πίστωση']
    trmod = Treemodel(nc(), labels, treeview)
    treeview.setModel(trmod)
    treeview.show()
    sys.exit(app.exec_())
