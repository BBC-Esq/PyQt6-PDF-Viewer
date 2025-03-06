from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QFileDialog, QPushButton
from PyQt6.QtGui import QAction
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage

class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()

        self.setWindowTitle("PDF Viewer")
        self.setGeometry(0, 28, 1000, 750)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.webView = QWebEngineView()
        self.webView.settings().setAttribute(self.webView.settings().WebAttribute.PluginsEnabled, True)
        self.webView.settings().setAttribute(self.webView.settings().WebAttribute.PdfViewerEnabled, True)
        self.layout.addWidget(self.webView)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Enter text to search...")
        self.search_input.returnPressed.connect(lambda: self.search_text(self.search_input.text()))
        self.layout.addWidget(self.search_input)

        self.create_file_menu()

    def create_file_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Choose PDF')

        open_action = QAction('Open', self)
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        filename, _ = file_dialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        if filename:
            self.webView.setUrl(QUrl.fromLocalFile(filename))

    def search_text(self, text):
        flag = QWebEnginePage.FindFlag.FindCaseSensitively
        if text:
            self.webView.page().findText(text, flag)
        else:
            self.webView.page().stopFinding()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())
