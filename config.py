from enum import Enum
from qfluentwidgets import qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator, OptionsValidator, \
    FolderValidator, RangeConfigItem, RangeValidator, EnumSerializer


class BufSize(Enum):
    _32 = "32 MB"
    _64 = "64 MB"
    _128 = "128 MB"
    _256 = "256 MB"
    _512 = "512 MB"
    _1024 = "1 GB"


class Config(QConfig):
    AutoRun = ConfigItem(
        "MainWindow", "AutoRun", True, BoolValidator())
    Notify = ConfigItem(
        "MainWindow", "Notify", False, BoolValidator())
    sourceFolder = ConfigItem(
        "MainWindow", "SourceFolder", "", FolderValidator())
    ScanCycle = RangeConfigItem(
        "MainWindow", "ScanCycle", 10, RangeValidator(1, 50))
    BufSize = OptionsConfigItem(
        "MainWindow", "BufSize", BufSize._256, OptionsValidator(BufSize), EnumSerializer(BufSize))
    dpiScale = OptionsConfigItem(
        "MainWindow", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)


HELP_URL = ""
cfg = Config()
qconfig.load('config/config.json', cfg)
