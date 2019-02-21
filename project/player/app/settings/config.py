import os
from os.path import dirname
from  pathlib import Path


class Config:
    LIST_PENDING_LIB = ["lib-001","lib-001"]#,"lib-001","lib-001","lib-001","lib-001","lib-001","lib-001","lib-001","lib-001","lib-001","lib-001","lib-005","lib-002"]
    ROOT_DIR = dirname(dirname(dirname(__file__)))
    DATA_DIR = ROOT_DIR+os.sep+"data"
    LIBS_DIR = DATA_DIR + os.sep + "libs"
    STUFFS_DIR = DATA_DIR + os.sep + "temp"
    MYDB_DIR = DATA_DIR + os.sep + "mydb"
    DOWNLOAD_DIR = DATA_DIR + os.sep + "download"