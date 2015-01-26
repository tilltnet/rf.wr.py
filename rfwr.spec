# -*- mode: python -*-

block_cipher = None


a = Analysis(['/home/phobo/ownCloud/raumfeld/rfwrpy/rfwr.py'],
             pathex=['/home/phobo/ownCloud/raumfeld/rfwrpy'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             cipher=block_cipher)
pyz = PYZ(a.pure,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='rfwr',
          debug=False,
          strip=None,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='rfwr')
