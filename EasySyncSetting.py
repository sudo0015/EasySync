import subprocess
import sys
import os
from config import cfg, BufSize
from enum import Enum
from PySide6.QtCore import Qt, QPoint, QSize, QUrl, QRect, QPropertyAnimation, Signal
from PySide6.QtGui import QIcon, QFont, QColor, QPainter, QDesktopServices
from PySide6.QtWidgets import QFrame, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGraphicsOpacityEffect, QLabel, \
    QFileDialog, QScroller
from qfluentwidgets import (CardWidget, setTheme, Theme, IconWidget, BodyLabel, CaptionLabel, PushButton,
                            TransparentToolButton, RoundMenu, Action, ElevatedCardWidget,
                            ImageLabel, isDarkTheme, FlowLayout, MSFluentTitleBar, SimpleCardWidget,
                            HeaderCardWidget, InfoBarIcon, HyperlinkLabel, HorizontalFlipView,
                            PrimaryPushButton, TitleLabel, PillPushButton, setFont, SingleDirectionScrollArea,
                            VerticalSeparator, MSFluentWindow, NavigationItemPosition, GroupHeaderCardWidget,
                            ComboBox, SearchLineEdit, SubtitleLabel, MessageBox, ExpandLayout, SettingCardGroup,
                            SwitchSettingCard, CustomColorSettingCard, PushSettingCard, HyperlinkCard,
                            ExpandSettingCard, InfoBar, setThemeColor, ScrollArea, RangeSettingCard, OptionsSettingCard,
                            StateToolTip, InfoBarPosition, PrimaryPushSettingCard, SmoothScrollArea)
from qfluentwidgets import FluentIcon as FIF


class Widget(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)
        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class HomeInterface(SmoothScrollArea):
    sourceFolderChanged = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.stateTooltip = None
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.sourceGroup = SettingCardGroup(self.tr('源'), self.scrollWidget)
        self.actGroup = SettingCardGroup(self.tr('行为'), self.scrollWidget)
        self.performanceGroup = SettingCardGroup(self.tr('性能'), self.scrollWidget)
        self.storageGroup = SettingCardGroup(self.tr('存储'), self.scrollWidget)
        self.advanceGroup = SettingCardGroup(self.tr('高级'), self.scrollWidget)
        self.autoRunCard = SwitchSettingCard(
            FIF.POWER_BUTTON,
            self.tr("开机时启动"),
            self.tr(""),
            configItem=cfg.AutoRun,
            parent=self.actGroup)
        self.notifyCard = SwitchSettingCard(
            FIF.RINGER,
            self.tr("完成后通知"),
            self.tr(""),
            configItem=cfg.Notify,
            parent=self.actGroup)
        self.sourceFolderCard = PushSettingCard(
            self.tr('选择文件夹'),
            FIF.FOLDER,
            self.tr("班级文件夹"),
            cfg.get(cfg.sourceFolder),
            self.sourceGroup)
        self.scanCycleCard = RangeSettingCard(
            cfg.ScanCycle,
            FIF.UPDATE,
            self.tr('扫描周期'),
            parent=self.performanceGroup)
        self.bufSizeCard = OptionsSettingCard(
            cfg.BufSize,
            FIF.PIE_SINGLE,
            self.tr('缓冲区大小'),
            texts=[
                self.tr('32 MB'), self.tr('64 MB'),
                self.tr('128 MB'), self.tr('256 MB'),
                self.tr('512 MB'), self.tr('1 GB')],
            parent=self.performanceGroup)
        self.clearCard = PushSettingCard(
            self.tr('清除'),
            FIF.BROOM,
            self.tr('清除缓存'),
            self.tr(self.getSize()),
            self.storageGroup)
        self.recoverCard = PushSettingCard(
            self.tr('恢复'),
            FIF.CLEAR_SELECTION,
            self.tr('恢复默认设置'),
            self.tr('重置所有参数为初始值'),
            self.advanceGroup)
        self.devCard = PushSettingCard(
            self.tr('打开'),
            FIF.DEVELOPER_TOOLS,
            self.tr('开发者选项'),
            self.tr('打开配置文件'),
            self.advanceGroup)
        self.helpCard = PrimaryPushSettingCard(
            self.tr('转到帮助'),
            FIF.HELP,
            self.tr('帮助'),
            self.tr('常见问题与提示'),
            self.advanceGroup)
        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 0, 0, 0)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.sourceGroup.addSettingCard(self.sourceFolderCard)
        self.actGroup.addSettingCard(self.autoRunCard)
        self.actGroup.addSettingCard(self.notifyCard)
        self.performanceGroup.addSettingCard(self.scanCycleCard)
        self.performanceGroup.addSettingCard(self.bufSizeCard)
        self.storageGroup.addSettingCard(self.clearCard)
        self.advanceGroup.addSettingCard(self.recoverCard)
        self.advanceGroup.addSettingCard(self.devCard)
        self.advanceGroup.addSettingCard(self.helpCard)
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.sourceGroup)
        self.expandLayout.addWidget(self.actGroup)
        self.expandLayout.addWidget(self.performanceGroup)
        self.expandLayout.addWidget(self.storageGroup)
        self.expandLayout.addWidget(self.advanceGroup)

    def getSize(self):
        try:
            size = os.path.getsize('FastCopy2.ini')
        except:
            size = 0
        if os.path.exists('./Log'):
            for root, dirs, files in os.walk('./Log'):
                size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
        return str(int(size / 1024)) + ' KB'

    def __onSourceFolderCardClicked(self):
        folder = QFileDialog.getExistingDirectory(self, self.tr("选择文件夹"), "./")
        if not folder or cfg.get(cfg.sourceFolder) == folder:
            return
        cfg.set(cfg.sourceFolder, folder)
        self.sourceFolderCard.setContent(folder)

    def clearCache(self):
        w = MessageBox(
            '清除缓存',
            '缓存包含日志文件，确定清除吗？',
            self)
        w.yesButton.setText('确定')
        w.cancelButton.setText('取消')
        if w.exec():
            self.stateTooltip = StateToolTip('清除缓存', '正在执行', self)
            self.stateTooltip.move(self.width() - self.stateTooltip.width() - 15, 15)
            self.stateTooltip.show()
            if os.path.exists('./Log'):
                subprocess.Popen("del /s /q Log", shell=True)
            if os.path.exists('FastCopy2.ini'):
                subprocess.Popen("del /q FastCopy2.ini", shell=True)
            self.stateTooltip.setContent('缓存已清除')
            self.stateTooltip.setState(True)
            self.stateTooltip = None
            self.clearCard.contentLabel.setText(self.getSize())

    def recoverConfig(self):
        w = MessageBox(
            '恢复默认设置',
            '确定要重置所有设置吗？',
            self)
        w.yesButton.setText('确定')
        w.cancelButton.setText('取消')
        if w.exec():
            self.autoRunCard.setChecked(True)
            self.notifyCard.setChecked(True)
            self.scanCycleCard.setValue(10)
            self.bufSizeCard.setValue(BufSize._256)

    def openConfig(self):
        w = MessageBox(
            '打开配置文件',
            '随意修改参数可能导致 EasySync 无法正常运行，确定继续吗？',
            self)
        w.yesButton.setText('确定')
        w.cancelButton.setText('取消')
        if w.exec():
            os.startfile("config\\config.json")

    def __connectSignalToSlot(self):
        self.sourceFolderCard.clicked.connect(self.__onSourceFolderCardClicked)
        self.clearCard.clicked.connect(lambda: self.clearCache())
        self.recoverCard.clicked.connect(lambda: self.recoverConfig())
        self.devCard.clicked.connect(lambda: self.openConfig())


class Main(MSFluentWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.homeInterface = HomeInterface(self)
        self.logInterface = Widget('log Interface', self)
        self.aboutInterface = Widget('about Interface', self)
        self.homeInterface.setObjectName('homeInterface')
        self.logInterface.setObjectName('logInterface')
        self.aboutInterface.setObjectName('aboutInterface')
        self.addSubInterface(self.homeInterface, FIF.HOME, '设置', FIF.HOME_FILL)
        self.addSubInterface(self.logInterface, FIF.DOCUMENT, '日志')
        self.navigationInterface.addItem(
            routeKey='Help',
            icon=FIF.HELP,
            text='帮助',
            onClick=lambda: self.onHelpBtn(),
            selectable=False,
            position=NavigationItemPosition.BOTTOM, )
        self.addSubInterface(self.aboutInterface, FIF.INFO, '关于', FIF.INFO, NavigationItemPosition.BOTTOM)
        self.navigationInterface.setCurrentItem(self.homeInterface.objectName())
        self.homeInterface.helpCard.clicked.connect(lambda: self.onHelpBtn())
        self.resize(800, 600)
        self.setWindowTitle('EasySync 设置')
        self.setWindowIcon(QIcon('icon.png'))
        self.titleBar.raise_()
        desktop = QApplication.screens()[0].size()
        self.move(desktop.width() // 2 - self.width() // 2, desktop.height() // 2 - self.height() // 2)

    def onHelpBtn(self):
        """REPLACE"""
        # subprocess.Popen("D:\EasySync\.venv\Scripts\python.exe EasySyncHelp.py", shell=True)
        print("clicked")


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    w = Main()
    w.show()
    app.exec()
