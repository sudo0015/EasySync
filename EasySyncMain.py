import os
import sys
import subprocess
import darkdetect
from PySide6.QtGui import QIcon
from win32api import GetVolumeInformation
from PySide6.QtCore import Qt, QThread, Signal, QEvent
from PySide6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QLabel, QWidget
from qfluentwidgets import setTheme, Theme, BodyLabel, isDarkTheme, PushButton, SubtitleLabel, ProgressBar, \
    InfoBar, InfoBarIcon, InfoBarPosition, IndeterminateProgressBar
from qfluentwidgets.common.style_sheet import FluentStyleSheet
from qframelesswindow.utils import startSystemMove
from qframelesswindow.titlebar.title_bar_buttons import CloseButton, MaximizeButton, MinimizeButton, TitleBarButton
from qfluentwidgets import FluentIcon as FIF
from config import cfg


def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


if isWin11():
    from qframelesswindow import AcrylicWindow as Window
else:
    from qframelesswindow import FramelessWindow as Window


class TitleBarBase(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.minBtn = MinimizeButton(parent=self)
        self.closeBtn = CloseButton(parent=self)
        self.maxBtn = MaximizeButton(parent=self)
        self._isDoubleClickEnabled = True
        self.resize(200, 32)
        self.setFixedHeight(32)
        self.minBtn.clicked.connect(self.window().showMinimized)
        self.maxBtn.clicked.connect(self.__toggleMaxState)
        self.window().installEventFilter(self)

    def eventFilter(self, obj, e):
        if obj is self.window():
            if e.type() == QEvent.WindowStateChange:
                self.maxBtn.setMaxState(self.window().isMaximized())
                return False
        return super().eventFilter(obj, e)

    def mouseDoubleClickEvent(self, event):
        if event.button() != Qt.LeftButton or not self._isDoubleClickEnabled:
            return
        self.__toggleMaxState()

    def mouseMoveEvent(self, e):
        if sys.platform != "win32" or not self.canDrag(e.pos()):
            return
        startSystemMove(self.window(), e.globalPos())

    def mousePressEvent(self, e):
        if sys.platform == "win32" or not self.canDrag(e.pos()):
            return
        startSystemMove(self.window(), e.globalPos())

    def __toggleMaxState(self):
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()
        if sys.platform == "win32":
            from qframelesswindow.utils.win32_utils import releaseMouseLeftButton
            releaseMouseLeftButton(self.window().winId())

    def _isDragRegion(self, pos):
        width = 0
        for button in self.findChildren(TitleBarButton):
            if button.isVisible():
                width += button.width()
        return 0 < pos.x() < self.width() - width

    def _hasButtonPressed(self):
        return any(btn.isPressed() for btn in self.findChildren(TitleBarButton))

    def canDrag(self, pos):
        return self._isDragRegion(pos) and not self._hasButtonPressed()

    def setDoubleClickEnabled(self, isEnabled):
        self._isDoubleClickEnabled = isEnabled


class TitleBar(TitleBarBase):
    def __init__(self, parent):
        super().__init__(parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.minBtn, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.maxBtn, 0, Qt.AlignRight)
        self.hBoxLayout.addWidget(self.closeBtn, 0, Qt.AlignRight)


class FluentTitleBar(TitleBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFixedHeight(45)
        self.hBoxLayout.removeWidget(self.minBtn)
        self.hBoxLayout.removeWidget(self.maxBtn)
        self.maxBtn.deleteLater()
        self.hBoxLayout.removeWidget(self.closeBtn)
        self.titleLabel = QLabel(self)
        self.titleLabel.setText("EasySync - " + self.GetDriveName() + ' (' + drive + ')')
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

    def GetDriveName(self):
        if GetVolumeInformation(drive)[0] != '':
            return GetVolumeInformation(drive)[0]
        else:
            return "U盘"


class MicaWindow(Window):

    def __init__(self):
        super().__init__()
        self.setTitleBar(FluentTitleBar(self))
        if isWin11():
            self.windowEffect.setMicaEffect(self.winId(), isDarkTheme())


class SyncThread(QThread):
    valueChange = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.is_paused = bool(0)
        self.progress_value = int(0)

    def run(self):
        while True:
            if taskList:
                if taskList[0] == 1:
                    currentFolder = folder + r"\语文"
                elif taskList[0] == 2:
                    currentFolder = folder + r"\数学"
                elif taskList[0] == 3:
                    currentFolder = folder + r"\英语"
                elif taskList[0] == 4:
                    currentFolder = folder + r"\物理"
                elif taskList[0] == 5:
                    currentFolder = folder + r"\化学"
                elif taskList[0] == 6:
                    currentFolder = folder + r"\生物"
                elif taskList[0] == 7:
                    currentFolder = folder + r"\政治"
                elif taskList[0] == 8:
                    currentFolder = folder + r"\历史"
                elif taskList[0] == 9:
                    currentFolder = folder + r"\地理"
                elif taskList[0] == 10:
                    currentFolder = folder + r"\技术"
                elif taskList[0] == 11:
                    currentFolder = folder + r"\资料"
                taskList.pop(0)
                subprocess.call('fcp.exe /cmd=sync /bufsize=' + buf + ' /log=FALSE "' + currentFolder + '" /to="' + destFolder + '"',shell=True)
                self.progress_value = int((taskNum - len(taskList)) / taskNum * 100)
                self.valueChange.emit(self.progress_value)
            else:
                self.progress_value = -1
                self.valueChange.emit(self.progress_value)
                return


class MainWindow(MicaWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(FluentTitleBar(self))
        self.titleBar.raise_()
        self.setWindowTitle("EasySync - " + self.GetDriveName() + ' (' + drive + ')')
        self.setWindowIcon(QIcon("icon.png"))
        self.resize(500, 130)
        self.setFixedHeight(130)
        desktop = QApplication.screens()[0].size()
        self.move(desktop.width() // 2 - self.width() // 2, desktop.height() // 2 - self.height() // 2)

        self.thread_running = False
        self.setup_thread()
        self.start_thread()

        self.titleBar.closeBtn.clicked.connect(lambda: self.cancelBtnOn())

        self.mainLayout = QVBoxLayout(self)
        self.topLayout = QHBoxLayout(self)
        self.bottomLayout = QHBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.topLayout.setContentsMargins(20, 0, 20, 5)
        self.bottomLayout.setContentsMargins(20, 5, 20, 20)

        self.statusLabel = SubtitleLabel(self)
        self.statusLabel.setText("准备中")
        self.isPrepare = True
        self.cancelBtn = PushButton(FIF.CLOSE, '取消同步', self)
        self.cancelBtn.clicked.connect(lambda: self.cancelBtnOn())
        self.topLayout.addWidget(self.statusLabel)
        self.topLayout.addStretch(1)
        self.topLayout.addWidget(self.cancelBtn)

        self.inProgressBar = IndeterminateProgressBar(self)
        self.progressBar = ProgressBar(self)
        self.spaceLabel = QLabel(self)
        self.spaceLabel.setFixedWidth(5)
        self.progressLabel = BodyLabel(self)
        self.progressBar.setVisible(False)
        self.spaceLabel.setVisible(False)
        self.progressLabel.setVisible(False)
        self.bottomLayout.addWidget(self.inProgressBar)

        self.mainLayout.addWidget(self.titleBar)
        self.mainLayout.addStretch(1)
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)

    def setup_thread(self):
        self.thread = SyncThread()
        self.thread.valueChange.connect(lambda: self.set_value())
        self.thread_running = True

    def set_value(self):
        if self.thread.progress_value == -1:
            if cfg.Notify.value:
                """NEED REPLACE"""
                # subprocess.Popen("D:\EasySync\.venv\Scripts\python.exe Notification.py "+drive)
                subprocess.Popen("Notification.exe " + drive, shell=True)
            sys.exit()
        if self.isPrepare:
            self.statusLabel.setText("正在同步")
            self.bottomLayout.removeWidget(self.inProgressBar)
            self.inProgressBar.deleteLater()
            self.progressBar.setVisible(True)
            self.spaceLabel.setVisible(True)
            self.progressLabel.setVisible(True)
            self.isPrepare = False

        self.progressBar.setValue(self.thread.progress_value)
        self.progressLabel.setText(str(self.thread.progress_value) + '%')
        self.bottomLayout.addWidget(self.progressBar)
        self.bottomLayout.addWidget(self.spaceLabel)
        self.bottomLayout.addWidget(self.progressLabel)

    def start_thread(self):
        if self.thread_running:
            self.thread.start()
        if not self.thread_running:
            self.setup_thread()
            self.thread.start()

    def stop_thread(self):
        self.thread.quit()
        self.thread_running = False
        subprocess.call("taskkill -f -im fcp.exe", shell=True)
        sys.exit()

    def GetDriveName(self):
        if GetVolumeInformation(drive)[0] != '':
            return GetVolumeInformation(drive)[0]
        else:
            return "U盘"

    def cancelBtnOn(self):
        yesBtn = PushButton('确定')
        yesBtn.clicked.connect(lambda: self.stop_thread())
        w = InfoBar(icon=InfoBarIcon.WARNING, title='取消同步？', content='', orient=Qt.Horizontal, isClosable=True,
                    position=InfoBarPosition.BOTTOM, duration=-1, parent=self)
        w.addWidget(yesBtn)
        w.show()


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    if darkdetect.isDark():
        setTheme(Theme.DARK)
    app = QApplication(sys.argv)
    drive = sys.argv[1]
    taskList = []
    for i in range(2, 13):
        if sys.argv[i] == '1':
            taskList.append(i - 1)
    taskNum = len(taskList)
    buf=str(cfg.BufSize.value)[9:]
    folder=cfg.sourceFolder.value
    destFolder = drive + '\\' + os.path.basename(folder) + '\\'
    w = MainWindow()
    w.show()
    app.exec()
