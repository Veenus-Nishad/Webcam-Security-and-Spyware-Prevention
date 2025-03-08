import psutil
import time
import platform
import logging
from hashlib import sha256
import base64

class WebcamMonitor:
    def __init__(self):
        self.logger = logging.getLogger("WebcamMonitor")
        self.os_type = platform.system()
        
    def _get_webcam_processes(self):
        if self.os_type == "Windows":
            return self._get_windows_webcam_processes()
        elif self.os_type == "Linux":
            return self._get_linux_webcam_processes()
        else:
            self.logger.error("Unsupported OS")
            return []

    def _get_windows_webcam_processes(self):
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Class\{6BDD1FC6-810F-11D0-BEC7-08002BE2092F}")
            processes = []
            for proc in psutil.process_iter(['pid', 'name']):
                processes.append(proc.info)
            return processes
        except Exception as e:
            self.logger.error(f"Windows webcam check failed: {e}")
            return []

    def _get_linux_webcam_processes(self):
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.pid == 1 or proc.username() == 'root':
                        continue
                    for fd in proc.open_files():
                        if '/dev/video' in fd.path:
                            processes.append(proc.info)
                            break
                except (psutil.AccessDenied, psutil.NoSuchProcess):
                    continue
            return processes
        except Exception as e:
            self.logger.error(f"Linux webcam check failed: {str(e)}")
            return [] 

    def run(self):
        """Continuously monitor webcam access"""
        while True:
            processes = self._get_webcam_processes()
            if processes:
                self.logger.warning(f"Webcam accessed by: {processes}")
                for process in processes:
                    self.logger.info(f"Detected webcam access by: {process['name']} (PID: {process['pid']})")
            time.sleep(2)  # Check every 2 seconds 