from enum import Enum


class TargetCacheValue(Enum):
    ANY = 0
    FILESYSTEM_PATH = 1
    FILE_PATH = 2
    FOLDER_PATH = 3
    DEFINED = 4
