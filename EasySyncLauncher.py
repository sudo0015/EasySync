import sys
import darkdetect
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout, QLabel
from qfluentwidgets import setTheme, Theme, SubtitleLabel, setFont, SplitFluentWindow, FluentStyleSheet, isDarkTheme
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import TitleBar

def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


if isWin11():
    from qframelesswindow import AcrylicWindow as Window
else:
    from qframelesswindow import FramelessWindow as Window


class FluentTitleBar(TitleBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(45)
        self.hBoxLayout.removeWidget(self.minBtn)
        self.hBoxLayout.removeWidget(self.maxBtn)
        self.maxBtn.deleteLater()
        self.hBoxLayout.removeWidget(self.closeBtn)
        self.titleLabel = QLabel(self)
        self.titleLabel.setText("EasySync")
        self.titleLabel.setObjectName('titleLabel')
        self.vBoxLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing(0)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.setAlignment(Qt.AlignTop)
        self.buttonLayout.addWidget(self.minBtn)
        self.buttonLayout.addWidget(self.closeBtn)
        self.titleLayout = QHBoxLayout()
        self.titleLayout.setContentsMargins(0, 7, 0, 0)
        self.titleLayout.addWidget(self.titleLabel)
        self.titleLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.addLayout(self.buttonLayout)
        self.vBoxLayout.addStretch(1)
        self.hBoxLayout.addLayout(self.titleLayout, 0)
        self.hBoxLayout.addStretch(30)
        self.hBoxLayout.addLayout(self.vBoxLayout, 0)
        FluentStyleSheet.FLUENT_WINDOW.apply(self)


class MicaWindow(Window):

    def __init__(self):
        super().__init__()
        self.setTitleBar(FluentTitleBar(self))
        if isWin11():
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())


class Window(MicaWindow):
    def __init__(self):
        super().__init__()
        self.setTitleBar(FluentTitleBar(self))
        self.titleBar.raise_()
        self.setWindowTitle("EasySync")
        self.setWindowIcon(QIcon("icon.png"))
        self.resize(360, 145)
        desktop = QApplication.screens()[0].size()
        self.move(desktop.width() // 2 - self.width() // 2, desktop.height() // 2 - self.height() // 2)


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    if darkdetect.isDark():
        setTheme(Theme.DARK)
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
