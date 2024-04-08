# generator.spec

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['./src/azure_iac/command.py'],
             pathex=['./src/azure_iac/command.py'],
             binaries=[],
             datas=[
                ('./src/azure_iac/bicep_templates', 'bicep_templates'), 
                ('./src/azure_iac/terraform_templates', 'terraform_templates')
             ],
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
          name='generator',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )