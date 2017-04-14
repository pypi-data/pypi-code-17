#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import os
import fnmatch

from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QGridLayout, QFileDialog,
                             QLabel, QTextEdit, QTableWidget, QTableWidgetItem)


class ArgumentSelector(QWidget):
    def __init__(self):
        super().__init__()

        self.directory_path = '/home'
        self.file_button = QPushButton("Open Directory")
        self.file_button.clicked.connect(self.enumerate_files)

        self.cell_button = QPushButton("OK")
        self.cell_button.clicked.connect(self.select_argument)

        self.clear_button = QPushButton("Clear Arguments")
        self.clear_button.clicked.connect(self.clear_argument)

        self.argument_label = QLabel('Argument list')

        # Set Table
        self.table = QTableWidget()
        self.table_item = QTableWidgetItem()
        self.table.setRowCount(0)
        self.table.setColumnCount(1)
        self.table.itemSelectionChanged.connect(self.add_argument)

        # Stretch table option
        self.table.horizontalHeader().setStretchLastSection(True)

        # Cell name
        self.table.setHorizontalHeaderLabels(["FileList"])
        self.textbox = QTextEdit(self)

        # Layout Management
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.grid.addWidget(self.file_button, 0, 0)
        self.grid.addWidget(self.clear_button, 0, 3)
        self.grid.addWidget(self.table, 1, 0, 1, 4)
        self.grid.addWidget(self.argument_label, 5, 0, 5, 4)

        self.grid.addWidget(self.textbox, 10, 0, 10, 4)
        self.grid.addWidget(self.cell_button, 20, 3)
        self.setWindowTitle('File dialog')
        self.show()

        # Read argument history file.
        try:
            with open('.arg_history', 'r') as f:
                for row in f:
                    row = row.rstrip()
                    self.textbox.append(row)
        except FileNotFoundError:
            # print("There isn't a  argument history.")
            pass

    def enumerate_files(self):
        """
        Set selected files in the table
        """
        self.directory_path = QFileDialog.getExistingDirectory(self, 'Open directory', '/home')
        try:
            files = os.listdir(self.directory_path)

        except (FileNotFoundError, TypeError):
            # print("You don't select directory.")
            return

        # Ignore .files
        files = [f for f in files if not fnmatch.fnmatch(f, ".*")]

        self.table.setRowCount(len(files))
        self.table.setColumnCount(1)

        for i, file in enumerate(files):
            self.table.setItem(0, i, QTableWidgetItem(file))

    def select_argument(self):
        """
        Add Selected path and to sys.arg.
        And create a argument history file.This file will be read when restarting a program.

        """

        path_text = self.textbox.toPlainText()
        path_list = path_text.split("\n")
        for path in path_list:
            sys.argv.append(path)

        with open('.arg_history', 'w') as f:
            f.write(path_text)
        self.close()

    def clear_argument(self):
        """
        Clear text box.

        """
        self.textbox.clear()

    def add_argument(self):
        """
        Add selected file path to text box.
        """
        items = self.table.selectedItems()
        self.textbox.append(self.directory_path + "/" + items[0].text())


class ShowArgumentSelector(object):
    def __init__(self):
        # Execution
        app = QApplication(sys.argv)
        arg = ArgumentSelector()
        app.exec_()
