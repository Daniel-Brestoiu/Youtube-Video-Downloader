# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['/Users/daniel/Desktop/Programming/Python/Personal Projects/Youtube to MP3/', 'interface.py'],
             pathex=['/Users/daniel/Desktop/Programming/Python/Personal Projects/Youtube to MP3'],
             binaries=[('/System/Library/Frameworks/Tk.framework/Tk', 'tk'), ('/System/Library/Frameworks/Tcl.framework/Tcl', 'tcl')],
             datas=[('/Users/daniel/Desktop/Programming/Python/Personal Projects/Youtube to MP3/*.png', '.')],
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
          [],
          exclude_binaries=True,
          name='',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='')
app = BUNDLE(coll,
             name='.app',
             icon=None,
             bundle_identifier=None)
