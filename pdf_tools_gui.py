import PyQt5.QtWidgets as qtw
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
import pikepdf
import os
import argparse
from styles.stylesheets import StyleSheet_Clear, StyleSheet_Select, StyleSheet_Combine, \
     StyleSheet_Remove, StyleSheet_QListWidget, StyleSheet_Encrypt, StyleSheet_Main



class MainApp(qtw.QWidget):
    """
    Main window for the GUI, which allows merging and encrypting PDFs
    Inherit from PyQt5.QtWidgets.QWidget --> Provides functionality like: self.resize(x,y) for the main window
    """

    def __init__(self):
        """
        Set up:
        -----------
        Window
        Stylesheets
        Icons
        Layout
        QListWidget
        Buttons
        -----------
        """

        super().__init__()

        ### Get stylesheets
        self.StyleSheet_Select = StyleSheet_Select
        self.StyleSheet_Clear = StyleSheet_Clear
        self.StyleSheet_Combine = StyleSheet_Combine
        self.StyleSheet_Remove = StyleSheet_Remove
        self.StyleSheet_QListWidget = StyleSheet_QListWidget
        self.StyleSheet_Encrypt = StyleSheet_Encrypt
        self.StyleSheet_Main = StyleSheet_Main


        ### Set window size
        self.resize(1500,700)
        ### Set GUI-icon
        self.setWindowIcon(QtGui.QIcon('icons/pdf_icon.png'))
        ### Set GUI-title
        self.setWindowTitle("PDF-Tools")
        self.setStyleSheet(self.StyleSheet_Main)

        ### Grid-Layout
        grid_layout = qtw.QGridLayout()
        self.setLayout(grid_layout)

        ### Sublayout for buttons
        sublayout1 = qtw.QGridLayout()


        ### Icons
        self.icon_pdf = QtGui.QIcon("icons/pdf_icon.png")
        self.icon_directory = QtGui.QIcon("icons/icons8-folder-64.png")
        self.icon_clear = QtGui.QIcon("icons/icons8-delete-48.png")
        self.icon_combine = QtGui.QIcon("icons/icons8-docunemts-zusammenführen-50.png") ### From: https://icons8.de/icon/meukjqGfdrFj/docunemts-zusammenf%C3%BChren
        self.icon_encrypt = QtGui.QIcon("icons/icons8-encrypt-50.png")
        self.icon_success = QtGui.QIcon("icons/icons8-task-completed-48.png") ### From: https://icons8.com/icon/40318/task-completed

        ### List Widget
        self.list1 = PDFListWidget()
        self.list1.setStyleSheet(self.StyleSheet_QListWidget)


        ### Label
        self.label_data = qtw.QLabel(text="Dateien:")

        ### Buttons
        ### Button to select files
        self.button_select = qtw.QPushButton(text="SELECT FILES", clicked=self.select_files)
        self.button_select.setStyleSheet(self.StyleSheet_Select)
        self.button_select.setIcon(self.icon_directory)

        ### Button to clear all files in the QListWidget
        self.button_clear = qtw.QPushButton(text="CLEAR ALL", clicked=self.clear_all)
        self.button_clear.setStyleSheet(self.StyleSheet_Clear)
        self.button_clear.setIcon(self.icon_clear)

        ### Button to clear the selected files in the QListWidget
        self.button_remove = qtw.QPushButton(text="CLEAR SELECTED", clicked=self.remove_files)
        self.button_remove.setStyleSheet(self.StyleSheet_Remove)
        self.button_remove.setIcon(self.icon_clear)

        ### Button to merge the files in the QListWidget
        self.button_combine = qtw.QPushButton(text="MERGE PDFs", clicked=self.combine_pdfs)
        self.button_combine.setStyleSheet(self.StyleSheet_Combine)
        self.button_combine.setIcon(self.icon_combine)

        ### Button to encrypt a single file in the QListWidget
        self.button_encrypt = qtw.QPushButton(text="ENCRYPT PDF", clicked=self.encrypt_pdf)
        self.button_encrypt.setStyleSheet(self.StyleSheet_Encrypt)
        self.button_encrypt.setIcon(self.icon_encrypt)

        ### Debug button
        self.button_debug = qtw.QPushButton(text="DEBUG", clicked=self.debug_files)

        ### Message box warning
        self.wrong_file_format = qtw.QMessageBox()
        self.wrong_file_format.setIcon(qtw.QMessageBox.Warning)
        self.wrong_file_format.setWindowTitle("Warning")
        self.wrong_file_format.setWindowIcon(self.icon_clear)

        ### Message box success
        self.message_success = qtw.QMessageBox()
        self.message_success.setIcon(qtw.QMessageBox.Information)
        self.message_success.setWindowTitle("Success")
        self.message_success.setWindowIcon(self.icon_success)

        ### Sub-Layout for buttons
        ### Necessary to display multiple buttons in one cell
        sublayout1.addWidget(self.button_select, 0, 0)
        sublayout1.addWidget(self.button_clear, 0, 1)
        sublayout1.addWidget(self.button_remove, 0, 2)
        sublayout1.addWidget(self.button_combine, 0, 3)
        sublayout1.addWidget(self.button_encrypt, 0, 4)

        ### Grid-Layout main-window
        grid_layout.addLayout(sublayout1, 0, 0)
        grid_layout.addWidget(self.list1, 1, 0)

        ### Show GUI
        self.show()


    def select_files(self):
        """
        This function enables the user to select multiple files and displays them as items in the QListWidget
        :return: None
        """

        ### Get list of filenames
        ### qtw.QFileDialog.getOpenFileNames() return tuple with two elements: ( [filenames], something_else)
        fnames = qtw.QFileDialog.getOpenFileNames()[0]


        for fname in fnames:

            ### Check for pdf-files
            ### If file-type is not .pdf: Display warning box
            if not fname.endswith(".pdf"):
                self.wrong_file_format.setText(f"Wrong file format:\n{fname}")
                self.wrong_file_format.exec_()

            else:
                self.list1.addItem(fname)

        ### Add icons to items
        self.add_icons()



    def remove_files(self):
        """
        This function removes the selected items from the QlistWidget
        :return: None
        """

        items = self.list1.selectionModel().selectedIndexes()

        for item in items:
            self.list1.takeItem(item.row())


    def add_icons(self):
        """
        This function adds a PDF-icon to every QListWidgetItem
        :return: None
        """

        for i in range(self.list1.count()):
            self.list1.item(i).setIcon(self.icon_pdf)


    def combine_pdfs(self):
        """
        This function combines the PDF-files listed in the QListWidget and saves the merged files
        :return: None
        """

        ### Get all files listed in QListWidget
        files = [str(self.list1.item(i).text()) for i in range(self.list1.count())]


        if len(files) < 2:
            self.wrong_file_format.setText("At least two files required for merging!")
            self.wrong_file_format.exec_()
            return


        ### Create pikepdf instance
        pdf = pikepdf.Pdf.new()
        version = pdf.pdf_version

        ### Combine files
        for file in files:
            src = pikepdf.Pdf.open(file)
            version = max(version, src.pdf_version)
            pdf.pages.extend(src.pages)

        ### Select target dir
        target_dir = qtw.QFileDialog.getExistingDirectory(self, "Select directory for the merged files...")

        ### Get new filename
        new_filename, ok = qtw.QInputDialog.getText(self, 'PDF-Merger', 'Enter new filename:')

        ### Append .pdf if not provided by the user
        if not new_filename.endswith(".pdf"):
            new_filename += ".pdf"

        ### Safe merged PDF-files
        pdf.save(target_dir + os.sep + new_filename, min_version=version)


        self.message_success.setText("PDFs successfully merged!")
        self.message_success.exec_()


        self.clear_all()


    def clear_all(self):
        """
        This function clears the QlistWidget
        :return: None
        """
        self.list1.clear()


    def encrypt_pdf(self):
        """
        This function encrypts a single pdf-file with a password required by the user
        :return:
        """

        ### Check number of files in the QListWidget
        if self.list1.count() != 1:
            self.wrong_file_format.setText("Provide exactly one file!")
            self.wrong_file_format.exec_()

        else:

            ### Get filepath
            filepath = str(self.list1.item(0).text())
            ### Create pikepdf-instance
            pdf = pikepdf.Pdf.open(filepath)

            ### Request password twice
            pass1, ok1 = qtw.QInputDialog.getText(self, "Password", "Enter Password:", qtw.QLineEdit.Password)
            pass2, ok2 = qtw.QInputDialog.getText(self, "Password", "Repeat Password:", qtw.QLineEdit.Password)

            while pass1 != pass2:

                self.wrong_file_format.setText(f"Passwords do not match! Please enter passwords again!")
                self.wrong_file_format.exec_()

                pass1, ok1 = qtw.QInputDialog.getText(self, "Password", "Enter Password:", qtw.QLineEdit.Password)
                pass2, ok2 = qtw.QInputDialog.getText(self, "Password", "Repeat Password:", qtw.QLineEdit.Password)

            ### Save encrypted pdf-file
            target_dir_str = qtw.QFileDialog.getExistingDirectory(self, "Select directory for the encrypted file...")
            new_filename = os.path.splitext(os.path.basename(filepath))[0] + "_encrypted.pdf"
            pdf.save(target_dir_str + os.sep + new_filename, encryption=pikepdf.Encryption(owner=pass1, user=pass2, R=4))
            pdf.close()

            self.message_success.setText("PDF succesfully encrypted!")
            self.message_success.exec_()

            ### Clear QListWidget
            self.clear_all()


    def debug_files(self):
        """
        Debug function for test-purposes
        :return:  None
        """

        text, ok = qtw.QInputDialog.getText(self, 'Text Input Dialog', 'Enter your name:')
        print(text, ok)





class PDFListWidget(qtw.QListWidget):
    """
    This class is the main instance of the GUI and handles the behavior of the QListWidget
    Inherit from PyQt5.QtWidgets.QListWidget --> Provides functionality like: self.setAcceptDrops for the QListWidget
    """

    def __init__(self):
        """
        Set up:
        ------------
        QListWidget
        Font
        Icons
        Message Box
        ------------
        """
        super().__init__()


        ### IMPORTANT: Set InternalMove
        ### https://stackoverflow.com/questions/22489018/pyqt-how-to-get-most-of-qlistwidget
        self.setAcceptDrops(True)
        self.setDragDropMode(qtw.QAbstractItemView.InternalMove)
        ### Allow multiple selections
        self.setSelectionMode(qtw.QAbstractItemView.ExtendedSelection)

        ### Font
        font = QtGui.QFont("Times", 15, QtGui.QFont.Normal)
        self.setFont(font)

        ### Icon
        self.icon_pdf = QtGui.QIcon("icons/pdf_icon.png")
        self.icon_directory = QtGui.QIcon("icons/icons8-folder-64.png")
        self.icon_clear = QtGui.QIcon("icons/icons8-delete-48.png")

        ### Message box
        self.wrong_file_format  = qtw.QMessageBox()
        self.wrong_file_format.setIcon(qtw.QMessageBox.Warning)
        self.wrong_file_format.setWindowTitle("Warning")
        self.wrong_file_format.setWindowIcon(self.icon_clear)


    ### Override virtual function: https://doc.qt.io/qt-5/qlistwidget.html
    def dragEnterEvent(self, event):
        """
        This function handles the events of files entering the QListWidget
        :param event: The current event to handle
        :return: None
        """

        ### Check if its an internal or external event
        ### Internal event: moving files within the QListWidget
        ### External event: Dropping files from the file explorer into the QListWidget
        ### External case: event.source() != self
        if event.source() != self:

            if event.mimeData().hasUrls:
                event.accept()
            else:
                event.ignore()

        ### Internal case: Call parent method:
        ### https://stackoverflow.com/questions/27216195/how-to-enable-both-internal-reordering-and-external-dropping-in-a-qt-widget
        else:
            super().dragEnterEvent(event)

    ### Override virtual function: https://doc.qt.io/qt-5/qlistwidget.html
    def dragMoveEvent(self, event):
        """
        This function handles the events of moving files in the QListWidget
        :param event: The current event to handle
        :return: None
        """

        ### Check if its an internal or external event
        ### External case: event.source() != self
        if event.source() != self:

            if event.mimeData().hasUrls():
                event.setDropAction(Qt.CopyAction)
                event.accept()
            else:
                event.ignore()

        ### Internal case: Call parent method
        else:
            super().dragMoveEvent(event)

    ### Override virtual function: https://doc.qt.io/qt-5/qlistwidget.html
    def dropEvent(self, event):
        """
        This function handles the events of dropping files in the QListWidget
        :param event: The current event to handle
        :return: None
        """

        ### Check if its an internal or external event
        ### External case: event.source() != self
        if event.source() != self:

            if event.mimeData().hasUrls():
                event.setDropAction(Qt.CopyAction)
                event.accept()

                links = []
                for url in event.mimeData().urls():

                    # https://doc.qt.io/qt-5/qurl.html
                    if url.isLocalFile():
                        filename = str(url.toLocalFile())
                        if not filename.endswith(".pdf"):
                            self.wrong_file_format.setText(f"Wrong file format:\n{filename}")
                            self.wrong_file_format.exec_()
                        else:
                            links.append(filename)
                    else:
                        filename = str(url.toString())
                        if not filename.endswith(".pdf"):
                            self.wrong_file_format.setText(f"Wrong file format:\n{filename}")
                            self.wrong_file_format.exec_()
                        else:
                            links.append(filename)

                self.addItems(links)
                self.add_icons()

            else:
                event.ignore()

        ### Internal case: Call parent method
        else:
            super().dropEvent(event)



    def add_icons(self):
        """
        This function adds icons to externally added files
        :return: None
        """

        for i in range(self.count()):
            self.item(i).setIcon(self.icon_pdf)



def handle_args(main, qlist):
    """
    This function checks if flags where set and displays the respective help
    :param main: Flag for help(MainApp)
    :param qlist: Flagg for help(PDFListWidget)
    :return: None, exit program if one flag was set
    """
    if main is True or qlist is True:

        if main is True:
            print(help(MainApp))

        if qlist is True:
            print(help(PDFListWidget))

        exit()


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("--main", "-m", action='store_true', help="Flag for information about MainApp")
    parser.add_argument("--qlist", "-q", action='store_true', help="Flag for information about PDFListWidget")

    args, unknown = parser.parse_known_args()

    main = args.main
    qlist = args.qlist
    handle_args(main, qlist)


    ### Create an instance of QApplication
    app = qtw.QApplication([])
    ### Create an instance of the application's GUI.
    mw = MainApp()
    ### Run application
    app.exec_()
