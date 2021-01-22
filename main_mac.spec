# -*- mode: python ; coding: utf-8 -*-
import os.path

block_cipher = None

version_file_path = os.path.join(
    SPECPATH,
    "register_printer",
    "VERSION"
)
with open(version_file_path, "r") as f:
    version_str = f.readline()
version_str = version_str.strip()

a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=[
                 (
                     "register_printer/templates/*",
                     "register_printer/templates"
                 ),
                 (
                     "register_printer/VERSION",
                     "register_printer"
                 )
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['tcl', 'tk', 'tkinter'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='RegisterPrinter-' + version_str,
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True, icon="registerPrinter.ico")
