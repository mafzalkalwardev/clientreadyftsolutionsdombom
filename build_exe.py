"""
Build script - FT Solutions Auto Dialer Pro
Run: python build_exe.py
"""
import json
import os
import subprocess
import sys


def pip(*pkgs):
    subprocess.check_call([sys.executable, "-m", "pip", "install", *pkgs])


DEPS = [
    "PyQt6", "PyQt6-WebEngine",
    "pandas", "openpyxl", "Pillow", "pyperclip", "pyinstaller",
]

print("=" * 60)
print("  FT Solutions - Auto Dialer Pro  |  Build")
print("=" * 60)
print("\nInstalling dependencies...")
for dep in DEPS:
    try:
        pip(dep)
        print(f"  OK {dep}")
    except Exception as e:
        print(f"  WARN {dep}: {e}")

# Default config
if not os.path.exists("dialer_config.json"):
    with open("dialer_config.json", "w") as f:
        json.dump({
            "theme": "dark",
            "n_slots": 1,
            "call_timeout": 60,
            "cooldown": 3.0,
            "voicemail_hangup_sec": 3,
            "excel_path": "",
        }, f, indent=2)
    print("\nCreated default dialer_config.json")

# ICO from logo image
LOGO_PNG = "ftsolutionslogo.jpg"
LOGO_ICO = "logo.ico"
icon_arg = []
if os.path.exists(LOGO_PNG):
    try:
        from PIL import Image
        img   = Image.open(LOGO_PNG).convert("RGBA")
        sizes = [(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)]
        imgs  = []
        for sz in sizes:
            c = Image.new("RGBA", sz, (0, 0, 0, 0))
            r = img.copy(); r.thumbnail(sz, Image.LANCZOS)
            c.paste(r, ((sz[0]-r.width)//2, (sz[1]-r.height)//2))
            imgs.append(c)
        imgs[0].save(LOGO_ICO, format="ICO",
                     sizes=sizes, append_images=imgs[1:])
        print(f"\nCreated {LOGO_ICO}")
    except Exception as e:
        print(f"\nWARN ICO creation failed (non-fatal): {e}")

sep = ";" if os.name == "nt" else ":"

# PyQt6 WebEngine needs special hooks
cmd = [
    "pyinstaller", "--onefile", "--windowed",
    "--distpath", "release",
    "--name", "FTSolutions_AutoDialer",
    f"--add-data=dialer_config.json{sep}.",
    f"--add-data=contacts_sample.csv{sep}.",
    f"--add-data=src{sep}src",
    "--hidden-import=PyQt6.QtWebEngineWidgets",
    "--hidden-import=PyQt6.QtWebEngineCore",
    "--hidden-import=PyQt6.sip",
    "--hidden-import=pandas",
    "--hidden-import=openpyxl",
    "--hidden-import=PIL",
    "--hidden-import=pyperclip",
    "--collect-all=PyQt6",
    "--collect-all=PyQt6.QtWebEngineWidgets",
]
for logo in (LOGO_PNG,):
    if os.path.exists(logo):
        cmd.append(f"--add-data={logo}{sep}.")
if icon_arg:
    cmd += icon_arg
cmd.append("autodialer_gui.py")

print("\nBuilding EXE...")
result = subprocess.run(cmd)
print()
if result.returncode == 0:
    print("=" * 60)
    print("  BUILD SUCCESSFUL")
    print("  release/FTSolutions_AutoDialer.exe")
    print("=" * 60)
else:
    print("Build failed - check output above.")
    sys.exit(1)
