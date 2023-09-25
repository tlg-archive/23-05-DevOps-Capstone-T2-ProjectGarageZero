# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

add_datas=[('./data/*.json' , './' 'data'), ('./data/*.txt' , './' 'data'), ('./sound/*.mp3' , './' 'sound'),('./sound/*.ogg' , './' 'sound')]

a = Analysis(
    ['main-gui.py'],
    pathex=[],
    binaries=[],
    datas=add_datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [('python3.10', None, 'OPTION')],
    name='Project Garage Zero',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
