import sys
import darkdetect
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout
from qfluentwidgets import setTheme, Theme, SubtitleLabel, setFont, SplitFluentWindow
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow.webengine import FramelessWebEngineView


class TipInterface(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("tipInterface")

        self.webView = FramelessWebEngineView(self)
        self.webView.load(QUrl("https://www.baidu.com"))
        self.webView.settings().setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, False)
        self.webView.setContextMenuPolicy(Qt.NoContextMenu)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 48, 0, 0)
        self.vBoxLayout.addWidget(self.webView)


class HelpInterface(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("homeInterface")

        self.webView = FramelessWebEngineView(self)
        self.webView.load(QUrl("file:///sample1.htm"))
        self.webView.settings().setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, False)
        self.webView.setContextMenuPolicy(Qt.NoContextMenu)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 48, 0, 0)
        self.vBoxLayout.addWidget(self.webView)


class QuestionInterface(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("questionInterface")

        self.webView = FramelessWebEngineView(self)
        self.webView.load(QUrl("https://www.bing.com"))
        self.webView.settings().setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, False)
        self.webView.setContextMenuPolicy(Qt.NoContextMenu)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 48, 0, 0)
        self.vBoxLayout.addWidget(self.webView)


class CodeInterface(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("codeInterface")

        self.webView = FramelessWebEngineView(self)
        self.webView.load(QUrl("https://www.bing.com"))
        self.webView.settings().setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, False)
        self.webView.setContextMenuPolicy(Qt.NoContextMenu)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(0, 48, 0, 0)
        self.vBoxLayout.addWidget(self.webView)


class Window(SplitFluentWindow):

    def __init__(self):
        super().__init__()
        self.tipInterface = TipInterface(self)
        self.helpInterface = HelpInterface(self)
        self.questionInterface = QuestionInterface(self)
        self.codeInterface = CodeInterface(self)
        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.tipInterface, FIF.ACCEPT, "快速上手")
        self.addSubInterface(self.helpInterface, FIF.DICTIONARY, "用户手册")
        self.addSubInterface(self.questionInterface, FIF.QUESTION, "常见问题")
        self.addSubInterface(self.codeInterface, FIF.CODE, "源代码")
        self.navigationInterface.setAcrylicEnabled(True)

    def initWindow(self):
        self.resize(900, 700)
        self.setWindowIcon(QIcon('help.png'))
        self.setWindowTitle('EasySync 帮助')

        desktop = QApplication.screens()[0].size()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    if darkdetect.isDark():
        setTheme(Theme.DARK)
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    w.setMicaEffectEnabled(True)
    app.exec()
