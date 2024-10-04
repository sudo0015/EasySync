import os
import sys
import subprocess
import darkdetect
from win32file import GetDiskFreeSpace
from PySide6.QtGui import QIcon, QColor
from win32api import GetVolumeInformation
from PySide6.QtCore import Qt, QEasingCurve, Slot, QPoint
from PySide6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QLabel, QStackedWidget, QWidget
from qfluentwidgets import setTheme, Theme, isDarkTheme, CheckBox, FlowLayout, PrimaryPushButton, PushButton, \
    SubtitleLabel, Pivot, TransparentToolButton, RoundMenu, AvatarWidget, BodyLabel, CaptionLabel, Action, \
    TransparentPushButton
from qfluentwidgets.common.style_sheet import FluentStyleSheet
from qframelesswindow import TitleBar
from qfluentwidgets import FluentIcon as FIF


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
        self.minBtn.deleteLater()
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


class OptionInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.backBtn = TransparentPushButton(FIF.RETURN, '返回', self)
        self.slectAll = CheckBox('全选', self)
        self.slectAll.setTristate(True)
        self.slectAll.setChecked(True)

        self.yuwen = CheckBox('语文', self)
        self.shuxue = CheckBox('数学', self)
        self.yingyu = CheckBox('英语', self)
        self.wuli = CheckBox('物理', self)
        self.huaxue = CheckBox('化学', self)
        self.shengwu = CheckBox('生物', self)
        self.zhengzhi = CheckBox('政治', self)
        self.lishi = CheckBox('历史', self)
        self.dili = CheckBox('地理', self)
        self.jishu = CheckBox('技术', self)
        self.ziliao = CheckBox('资料', self)
        self.yuwen.setChecked(True)
        self.shuxue.setChecked(True)
        self.yingyu.setChecked(True)
        self.wuli.setChecked(True)
        self.huaxue.setChecked(True)
        self.shengwu.setChecked(True)
        self.zhengzhi.setChecked(True)
        self.lishi.setChecked(True)
        self.dili.setChecked(True)
        self.jishu.setChecked(True)
        self.ziliao.setChecked(True)
        self.flowLayout = FlowLayout(self, needAni=True)
        self.flowLayout.setAnimation(250, QEasingCurve.OutQuad)
        self.flowLayout.setContentsMargins(20, 0, 20, 10)
        self.flowLayout.setVerticalSpacing(15)
        self.flowLayout.setHorizontalSpacing(35)
        self.flowLayout.addWidget(self.backBtn)
        self.flowLayout.addWidget(self.slectAll)
        self.flowLayout.addWidget(self.yuwen)
        self.flowLayout.addWidget(self.shuxue)
        self.flowLayout.addWidget(self.yingyu)
        self.flowLayout.addWidget(self.wuli)
        self.flowLayout.addWidget(self.huaxue)
        self.flowLayout.addWidget(self.shengwu)
        self.flowLayout.addWidget(self.zhengzhi)
        self.flowLayout.addWidget(self.lishi)
        self.flowLayout.addWidget(self.dili)
        self.flowLayout.addWidget(self.jishu)
        self.flowLayout.addWidget(self.ziliao)
        self.exeBtn = PrimaryPushButton('执行同步', self)
        self.exitBtn = PushButton('取消', self)
        self.exeBtn.setFixedSize(140, 30)
        self.exitBtn.setFixedSize(140, 30)
        self.flowLayout.addWidget(self.exeBtn)
        self.flowLayout.addWidget(self.exitBtn)


class AskInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.btnLayout = QHBoxLayout(self)
        self.infoLayout = QHBoxLayout(self)
        self.infoLabel = SubtitleLabel(self.GetDriveName() + ' (' + drive + ')')
        self.infoBtn = TransparentToolButton(FIF.INFO, self)
        self.syncBtn = PrimaryPushButton(FIF.SYNC, '同步', self)
        self.openBtn = PushButton(FIF.FOLDER, '打开', self)
        self.btnLayout.addWidget(self.syncBtn)
        self.btnLayout.addWidget(self.openBtn)
        self.btnLayout.setContentsMargins(10, 10, 10, 10)
        self.infoLayout.setContentsMargins(20, 0, 20, 10)
        self.infoLayout.addWidget(self.infoLabel)
        self.infoLayout.addStretch(1)
        self.infoLayout.addWidget(self.infoBtn)
        self.mainLayout.addStretch()
        self.mainLayout.addLayout(self.infoLayout)
        self.mainLayout.addLayout(self.btnLayout)

    def GetDriveName(self):
        if GetVolumeInformation(drive)[0] != '':
            return GetVolumeInformation(drive)[0]
        else:
            return "U盘"

class ProfileCard(QWidget):
    def __init__(self, avatarPath: str, name: str, size: str, parent=None):
        super().__init__(parent=parent)
        self.avatar = AvatarWidget(avatarPath, self)
        self.nameLabel = BodyLabel(name, self)
        self.sizeLabel = CaptionLabel(size, self)
        color = QColor(206, 206, 206) if isDarkTheme() else QColor(96, 96, 96)
        self.sizeLabel.setStyleSheet('QLabel{color: '+color.name()+'}')
        color = QColor(255, 255, 255) if isDarkTheme() else QColor(0, 0, 0)
        self.nameLabel.setStyleSheet('QLabel{color: '+color.name()+'}')
        self.setFixedSize(307, 82)
        self.avatar.setRadius(24)
        self.avatar.move(2, 6)
        self.nameLabel.move(64, 13)
        self.sizeLabel.move(64, 32)

class MainWindow(MicaWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(FluentTitleBar(self))
        self.titleBar.raise_()
        self.setWindowTitle("EasySync")
        self.setWindowIcon(QIcon("icon.png"))
        self.setFixedSize(360, 145)
        self.desktop = QApplication.screens()[0].size()
        self.move(self.desktop.width() - self.width() - 20, self.desktop.height() - self.height() - 60)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.pivot = Pivot(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)
        self.askInterface = AskInterface(self)
        self.optionInterface = OptionInterface(self)
        self.askInterface.infoBtn.clicked.connect(lambda: self.infoBtnOn())
        self.askInterface.syncBtn.clicked.connect(lambda: self.syncBtnOn())
        self.askInterface.openBtn.clicked.connect(lambda: self.openBtnOn())
        self.optionInterface.backBtn.clicked.connect(lambda: self.backBtnOn())
        self.optionInterface.exeBtn.clicked.connect(lambda: self.exeBtnOn())
        self.optionInterface.exitBtn.clicked.connect(lambda: self.exitBtnOn())
        self.addSubInterface(self.askInterface, 'askInterface', 'Ask')
        self.addSubInterface(self.optionInterface, 'optionInterface', 'Option')
        self.pivot.setVisible(False)
        self.vBoxLayout.addWidget(self.titleBar)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget.setCurrentWidget(self.askInterface)
        self.pivot.setCurrentItem(self.askInterface.objectName())
        self.pivot.currentItemChanged.connect(lambda k: self.stackedWidget.setCurrentWidget(self.findChild(QWidget, k)))

    def addSubInterface(self, widget: QLabel, objectName, text):
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(routeKey=objectName, text=text)

    def GetDriveName(self):
        if GetVolumeInformation(drive)[0] != '':
            return GetVolumeInformation(drive)[0]
        else:
            return "U盘"

    def GetDriveSize(self):
        """
        if GetVolumeInformation(drive)[4] != '':
            return GetVolumeInformation(drive)[4]
        else:
            return "未知"
        """
        sectorsPerCluster, bytesPerSector, numFreeClusters, totalNumClusters = GetDiskFreeSpace(drive)
        freeSpace = format((numFreeClusters * sectorsPerCluster * bytesPerSector) / 1024 / 1024 / 1024, '.1f')
        totalSpace = format((sectorsPerCluster * bytesPerSector * totalNumClusters) / 1024 / 1024 / 1024, '.1f')
        return freeSpace + 'GB可用，共' + totalSpace + 'GB'

    @Slot()
    def infoBtnOn(self):
        menu = RoundMenu(parent=self)
        card = ProfileCard('UsbIcon.png', self.GetDriveName()+' ('+drive+')', self.GetDriveSize(), menu)
        menu.addWidget(card, selectable=False)
        menu.addSeparator()
        SettingAction=Action(FIF.SETTING, '设置')
        """NEED REPLACE"""
        #SettingAction.triggered.connect(lambda: subprocess.Popen("D:\EasySync\.venv\Scripts\python.exe EasySyncSetting.py",shell=True))
        SettingAction.triggered.connect(lambda: subprocess.Popen("EasySyncSetting.exe",shell=True))
        menu.addAction(SettingAction)
        menu.addAction(Action(FIF.CLOSE, '关闭'))
        menu.exec(QPoint(self.x()+self.askInterface.infoBtn.x()-315, self.y()+self.askInterface.infoBtn.y()-55))

    def syncBtnOn(self):
        self.stackedWidget.setCurrentWidget(self.optionInterface)
        self.pivot.setCurrentItem(self.optionInterface.objectName())
        self.pivot.currentItemChanged.connect(lambda k: self.stackedWidget.setCurrentWidget(self.findChild(QWidget, k)))
        self.setFixedSize(360, 300)
        self.move(self.desktop.width() - self.width() - 20, self.desktop.height() - self.height() - 60)

    def openBtnOn(self):
        os.startfile(drive)
        sys.exit()

    def backBtnOn(self):
        self.stackedWidget.setCurrentWidget(self.askInterface)
        self.pivot.setCurrentItem(self.askInterface.objectName())
        self.pivot.currentItemChanged.connect(lambda k: self.stackedWidget.setCurrentWidget(self.findChild(QWidget, k)))
        self.setFixedSize(360, 145)
        self.move(self.desktop.width() - self.width() - 20, self.desktop.height() - self.height() - 60)

    def exeBtnOn(self):
        arg = drive
        if self.optionInterface.yuwen.isChecked():
            arg += " 1"
        else:
            arg += " 0"
        if self.optionInterface.shuxue.isChecked():
            arg += " 1"
        else:
            arg += " 0"
        if self.optionInterface.yingyu.isChecked():
            arg += " 1"
        else:
            arg += " 0"
        if self.optionInterface.wuli.isChecked():
            arg += " 1"
        else:
            arg += " 0"
        if self.optionInterface.huaxue.isChecked():
            arg += " 1"
        else:
            arg += " 0"
        if self.optionInterface.shengwu.isChecked():
            arg += " 1"
        else:
            arg += " 0"
        if self.optionInterface.zhengzhi.isChecked():
            arg += " 1"
        else:
            arg += " 0"
        if self.optionInterface.lishi.isChecked():
            arg += " 1"
        else:
            arg += " 0"
        if self.optionInterface.dili.isChecked():
            arg += " 1"
        else:
            arg += " 0"
        if self.optionInterface.jishu.isChecked():
            arg += " 1"
        else:
            arg += " 0"
        if self.optionInterface.ziliao.isChecked():
            arg += " 1"
        else:
            arg += " 0"
        subprocess.Popen("EasySyncMain.exe " + arg, shell=True)
        sys.exit()

    def exitBtnOn(self):
        sys.exit()


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    if darkdetect.isDark():
        setTheme(Theme.DARK)
    app = QApplication(sys.argv)
    if len(sys.argv) != 2:
        sys.exit()
    drive = sys.argv[1]
    w = MainWindow()
    w.show()
    app.exec()
