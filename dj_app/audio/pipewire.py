"""PipeWire integrace"""

import subprocess
import os


class PipeWireManager:
    """Správce PipeWire audio engine"""
    
    @staticmethod
    def is_installed():
        """Zkontroluj jestli je PipeWire nainstalován"""
        try:
            subprocess.run(["which", "pipewire"], capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    @staticmethod
    def is_running():
        """Zkontroluj jestli PipeWire běží"""
        try:
            result = subprocess.run(
                ["systemctl", "--user", "is-active", "pipewire"],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except:
            return False
    
    @staticmethod
    def start():
        """Spusť PipeWire"""
        try:
            subprocess.run(
                ["systemctl", "--user", "start", "pipewire"],
                check=True
            )
            print("✅ PipeWire spuštěn")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Chyba při spuštění PipeWire: {e}")
            return False
    
    @staticmethod
    def open_qpwgraph():
        """Otevři Qpwgraph pro vizuální routing"""
        try:
            subprocess.Popen(["qpwgraph"])
            print("✅ Qpwgraph otevřen")
            return True
        except FileNotFoundError:
            print("❌ Qpwgraph není nainstalován")
            return False
