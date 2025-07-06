
from PyQt5.QtWidgets import QFileDialog

def get_file_path(file_type="All Files (*.*)"):
    """
    Opens a file dialog to select a file of a specified type and returns the file path.

    :param file_type: A string specifying the file type filter (e.g., "Text Files (*.txt)").
    :return: The selected file path as a string, or an empty string if no file is selected.
    """
    # Create an instance of the file dialog
    dialog = QFileDialog()
    # Set the file type filter
    dialog.setNameFilter(file_type)
    # Open the dialog and get the selected file path
    if dialog.exec_():
        selected_file = dialog.selectedFiles()
        if selected_file:
            return selected_file[0]  # Return the first selected file path
    return ""
