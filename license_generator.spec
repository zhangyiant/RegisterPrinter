# -*- mode: python ; coding: utf-8 -*-
import os.path

block_cipher = None

with open(os.path.join(SPECPATH, "VERSION"), "r") as f:
    version_str = f.readline()
version_str = version_str.strip()

a = Analysis(['license_generator.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
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
          name='LicenseGenerator-' + version_str,
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True , icon='registerPrinter.ico')