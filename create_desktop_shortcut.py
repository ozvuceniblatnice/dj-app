#!/usr/bin/env python3
"""Desktop shortcut creator for DJ App"""

import os
from pathlib import Path
import subprocess
import sys

def create_desktop_shortcut():
    """Create desktop shortcut for DJ App"""
    
    home = Path.home()
    repo_dir = home / "dj-app"
    desktop_dir = home / "Desktop"
    
    # Ensure Desktop directory exists
    desktop_dir.mkdir(exist_ok=True)
    
    # Create .desktop file (Linux)
    if sys.platform.startswith('linux'):
        desktop_file = desktop_dir / "DJ-App.desktop"
        
        content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=DJ App
Comment=Professional DJ Mixing Application
Exec=bash -c 'cd {repo_dir} && source venv/bin/activate && python3 -m dj_app'
Icon={repo_dir}/dj_app/gui/assets/icon.png
Terminal=false
Categories=Audio;Music;
X-GNOME-Autostart-enabled=false
"""
        
        desktop_file.write_text(content)
        os.chmod(desktop_file, 0o755)
        print(f"✅ Desktop zkratka vytvořena: {desktop_file}")
    
    # Create .app shortcut (macOS)
    elif sys.platform == 'darwin':
        app_dir = desktop_dir / "DJ App.app"
        contents_dir = app_dir / "Contents"
        macos_dir = contents_dir / "MacOS"
        macos_dir.mkdir(parents=True, exist_ok=True)
        
        # Create launcher script
        launcher = macos_dir / "launcher"
        launcher_content = f"""#!/bin/bash
cd {repo_dir}
source venv/bin/activate
python3 -m dj_app
"""
        launcher.write_text(launcher_content)
        os.chmod(launcher, 0o755)
        
        # Create Info.plist
        plist_file = contents_dir / "Info.plist"
        plist_content = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleExecutable</key>
    <string>launcher</string>
    <key>CFBundleIdentifier</key>
    <string>com.djapp.mixer</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>DJ App</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
</dict>
</plist>"""
        plist_file.write_text(plist_content)
        print(f"✅ macOS App vytvořena: {app_dir}")
    
    # Create .lnk shortcut (Windows)
    elif sys.platform == 'win32':
        try:
            import win32com.client
            
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut_path = str(desktop_dir / "DJ App.lnk")
            
            shortcut = shell.CreateShortcut(shortcut_path)
            shortcut.TargetPath = str(repo_dir / "venv" / "Scripts" / "python.exe")
            shortcut.Arguments = f"-m dj_app"
            shortcut.WorkingDirectory = str(repo_dir)
            shortcut.IconLocation = str(repo_dir / "dj_app" / "gui" / "assets" / "icon.ico")
            shortcut.save()
            
            print(f"✅ Desktop zkratka vytvořena: {shortcut_path}")
        except ImportError:
            print("⚠️  Pro Windows je potřeba: pip install pywin32")
            print("Vytvoř zkratku ručně:")
            print(f"  1. Klikni pravým tlačítkem na plochu")
            print(f"  2. Nová > Zkratka")
            print(f"  3. Vložit umístění: cmd /c cd {repo_dir} && venv\\Scripts\\python -m dj_app")

if __name__ == "__main__":
    create_desktop_shortcut()
