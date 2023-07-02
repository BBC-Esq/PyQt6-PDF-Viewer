from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QFileDialog, QMenu, QMenuBar, QPushButton
from PyQt6.QtGui import QAction
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage
from os import path

class SearchLineEdit(QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key.Key_Return:
            self.parent.next_button.click()

class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        self.setWindowTitle("PDF Viewer")
        self.setGeometry(0, 28, 1000, 750)

        # Create the central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create the layout for central widget
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.webView = QWebEngineView()
        self.webView.settings().setAttribute(self.webView.settings().WebAttribute.PluginsEnabled, True)
        self.webView.settings().setAttribute(self.webView.settings().WebAttribute.PdfViewerEnabled, True)
        
        # Add the QWebEngineView to the layout
        self.layout.addWidget(self.webView)

        # Create a QLineEdit for search input
        self.search_input = SearchLineEdit(self)
        self.search_input.setPlaceholderText("Enter text to search...")
        self.layout.addWidget(self.search_input)

        # Create a horizontal layout for 'Next' and 'Previous' buttons
        self.button_layout = QHBoxLayout()

        self.next_button = QPushButton("Next")
        self.next_button.clicked.connect(lambda: self.search_text(self.search_input.text(), forward=True))
        self.button_layout.addWidget(self.next_button)

        self.prev_button = QPushButton("Previous")
        self.prev_button.clicked.connect(lambda: self.search_text(self.search_input.text(), forward=False))
        self.button_layout.addWidget(self.prev_button)

        # Add the button layout to the main layout
        self.layout.addLayout(self.button_layout)

        # Connect the QLineEdit's textChanged signal to a custom slot
        self.search_input.textChanged.connect(self.search_text)

        # Create a file menu
        self.create_file_menu()

    def create_file_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        filename, _ = file_dialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        if filename:
            self.webView.setUrl(QUrl("file:///" + filename.replace('\\', '/')))

    def search_text(self, text, forward=True):
        flag = QWebEnginePage.FindFlag.FindBackward if not forward else QWebEnginePage.FindFlag.FindCaseSensitively
        if text:
            # If there's text in the QLineEdit, search for it
            self.webView.page().findText(text, flag)
        else:
            # If the QLineEdit is empty, stop searching
            self.webView.page().stopFinding()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    test_pdf = "[ENTER_PATH_HERE]"
    test_pdf = test_pdf.replace("\\", "/")
    win.webView.setUrl(QUrl("file:///" + test_pdf))
    sys.exit(app.exec())
