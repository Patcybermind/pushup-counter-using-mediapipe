# -*- mode: python ; coding: utf-8 -*-


a = Analysis(['my_script.py'],
             pathex=['C:\\Users\\patog\\OneDrive\\Documents\\coding\\visoneer\\test folder\\'],
             binaries=[],
             datas=[
                 ('C:\\Python312\\python312.dll', '.'),  # Include the Python DLL
                 ('C:\\Python312\\Lib\\site-packages\\mediapipe\\python\\solutions\\*.*', 'mediapipe\\python\\solutions'),
                 ('C:\\Users\\patog\\OneDrive\\Documents\\coding\\visoneer\\test folder\\.venv\\Lib\\site-packages\\mediapipe\\modules\\pose_landmark\\*.*', 'mediapipe/modules/pose_landmark'),
                 ('C:\\Users\\patog\\OneDrive\\Documents\\coding\\visoneer\\test folder\\go_lower.mp3', '.'), # Add any other necessary directories here.
                 ('C:\\Python312\\Lib\\site-packages\\mediapipe\\modules\\pose_detection\\pose_detection.tflite', 'mediapipe/modules/pose_detection/'),
             ],
             hiddenimports=['cv2', 'mediapipe', 'numpy', 'threading', 'pygame'],
             hookspath=['C:\\Python312\\Lib\\site-packages\\PyInstaller\\hooks'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             #cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=False,
    name='my_script',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
#coll = COLLECT(
#    exe,
#    a.binaries,
#    a.datas,
#    strip=False,
#    upx=True,
#    upx_exclude=[],
#    name='my_script',
#)
