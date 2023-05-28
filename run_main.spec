# -*- mode: python ; coding: utf-8 -*-

import site
import os

block_cipher = None

assert len(site.getsitepackages()) > 0

package_path = site.getsitepackages()[0]
for p in site.getsitepackages():
    if "site-package" in p:
        package_path = p
        break

a = Analysis(
    ['run_main.py'],
    pathex=[],
    binaries=[],

    # ポイント1
    datas=[(os.path.join(package_path, "altair/vegalite/v4/schema/vega-lite-schema.json"), "./altair/vegalite/v4/schema/"),
        (os.path.join(package_path, "streamlit/static"), "./streamlit/static"),
        (os.path.join(package_path, "streamlit/runtime"), "./streamlit/runtime")],

    # ポイント2
    hiddenimports=['pandas', 'BeautifulSoup4','requests', 'streamlit_toggle', 'pyarrow.vendored.version'],

    hookspath=['./hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

#---------------計量化ここから---------------
Key = ['mkl']

def remove_from_list(input, keys):
    outlist = []
    for item in input:
        name, _, _ = item
        flag = 0
        for key_word in keys:
            if name.find(key_word) > -1:
                flag = 1
        if flag != 1:
            outlist.append(item)
    return outlist

a.binaries = remove_from_list(a.binaries, Key)
#---------------計量化ここまで---------------
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='run_main',
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
