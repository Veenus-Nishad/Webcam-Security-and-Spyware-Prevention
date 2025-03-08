import subprocess
import platform

#Block unauthorized processes.

class AccessBlocker:
    def __init__(self):
        self.os_type = platform.system()

    def block_process(self, process_hash):
        if self.os_type == "Windows":
            self._block_windows(process_hash)
        elif self.os_type == "Linux":
            self._block_linux(process_hash)
        else:
            print("Unsupported OS")

    def _block_windows(self, process_hash):
        # Disable webcam via registry (admin rights required)
        try:
            subprocess.run(
                ['reg', 'add', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\CapabilityAccessManager\ConsentStore\webcam', 
                 '/v', 'Value', '/t', 'REG_DWORD', '/d', '0', '/f'],
                check=True
            )
            print("Webcam disabled")
        except subprocess.CalledProcessError as e:
            print(f"Failed to disable webcam: {e}")

    def _block_linux(self, process_hash):
        # Disable webcam kernel module
        try:
            subprocess.run(['sudo', 'modprobe', '-r', 'uvcvideo'], check=True)
            print("Webcam disabled")
        except subprocess.CalledProcessError as e:
            print(f"Failed to disable webcam: {e}")