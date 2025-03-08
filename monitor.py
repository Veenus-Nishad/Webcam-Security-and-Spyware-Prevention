import psutil
import time
import platform
import logging
from hashlib import sha256
import base64

# Track processes accessing the webcam in real-time.

class WebcamMonitor:
    def __init__(self):
        self.logger = logging.getLogger("WebcamMonitor")
        self.os_type = platform.system()
        
    def _get_webcam_processes(self):
        # Track processes accessing the webcam (OS-specific)
        if self.os_type == "Windows":
            return self._get_windows_webcam_processes()
        elif self.os_type == "Linux":
            return self._get_linux_webcam_processes()
        else:
            self.logger.error("Unsupported OS")
            return []

    def _get_windows_webcam_processes(self):
        # Check webcam access via Windows registry or WMI (simplified example)
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Class\{6BDD1FC6-810F-11D0-BEC7-08002BE2092F}")
            processes = []
            for proc in psutil.process_iter(['pid', 'name']):
                # Check if process is accessing webcam (placeholder logic)
                processes.append(proc.info)
            return processes
        except Exception as e:
            self.logger.error(f"Windows webcam check failed: {e}")
            return []

    def _get_linux_webcam_processes(self):
        # Check /dev/video* devices (simplified example)
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name']):
                # Check if process has open file descriptors to /dev/video*
                for fd in proc.open_files():
                    if '/dev/video' in fd.path:
                        processes.append(proc.info)
            return processes
        except Exception as e:
            self.logger.error(f"Linux webcam check failed: {e}")
            return []

    def run(self):
        while True:
            processes = self._get_webcam_processes()
            if processes:
                self.logger.warning(f"Webcam accessed by: {processes}")
                # Hash process names for ML input (SHA-256 + Base64)
                hashed_processes = [
                    base64.b64encode(sha256(p['name'].encode()).hexdigest()
                    for p in processes
                ]
                # Pass to Threat Detector
                ThreatDetector().analyze(hashed_processes)
            time.sleep(2)  # Check every 2 seconds