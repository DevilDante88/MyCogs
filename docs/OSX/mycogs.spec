# -*- mode: python -*-


from kivy.tools.packaging.pyinstaller_hooks import install_hooks
import os

install_hooks(globals())
gst_plugin_path = os.environ.get('GST_PLUGIN_PATH').split(':')[0]
print 'GST PLUGIN PATH: ', gst_plugin_path

a = Analysis(['/Users/matteo/compiledmycogs/MyCogs/main.py'],
             pathex=['/Users/matteo/PyInstaller-2.1/mycogs'],
             hiddenimports=[],
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='mycogs',
          debug=False,
          strip=None,
          upx=True,
          console=False )
coll = COLLECT(exe, Tree('/Users/matteo/compiledmycogs/MyCogs/'),
               Tree(os.path.join(gst_plugin_path, '..')),
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='mycogs')
app = BUNDLE(coll,
             name='mycogs.app',
             icon=None)
