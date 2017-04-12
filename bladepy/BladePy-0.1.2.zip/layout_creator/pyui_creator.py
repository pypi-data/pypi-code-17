import os


def createPyUI(input_ui_file_dir, output_py_file_dir):
    """
    Function to translate a .ui file created in Qt Designer to a .py file that is readable by PyQt.

    @param input_ui_file_dir [.ui file] A file created in Qt Designer
    @param output_py_file_dir [.py file] A file that will be the translation of the file created in Qt Designer
    @return None
    """

    # Finds the absolute path for the PyQt .ui translator module
    pyui_creator_dir = os.path.join(os.path.dirname(__file__), "pyuic.py")

    # Creates a variable that is "python absolute_path\pyuic.py" to be run afterwards
    command_starter = "python %s" % pyui_creator_dir

    # Display a message that the translated .py files are being updated (or created)
    print("Updating %s..." % os.path.basename(output_py_file_dir))

    # Executes the command in a Terminal
    os.system("%s -x %s -o %s" % (command_starter, input_ui_file_dir, output_py_file_dir))

    return
