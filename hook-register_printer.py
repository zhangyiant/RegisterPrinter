# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
datas= collect_data_files('register_printer',excludes=["tests*"])