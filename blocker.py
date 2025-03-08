import subprocess
import platform

class AccessBlocker:
    def __init__(self):
        """
        Initializes the access blocker.
        """
        self.os_type = platform.system()  # Detect the operating system

    def block_process(self, pid):
        """
        Blocks a process by its PID.
        """
        if self.os_type == "Windows":
            self._block_windows(pid)
        elif self.os_type == "Linux":
            self._block_linux(pid)
        else:
            print("Unsupported OS")

    def _block_windows(self, pid):
        """
        Blocks a process on Windows.
        """
        try:
            subprocess.run(['taskkill', '/PID', str(pid), '/F'], check=True)
            print(f"Process {pid} blocked.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to block process: {e}")

    def _block_linux(self, pid):
        """
        Blocks a process on Linux.
        """
        try:
            subprocess.run(['kill', '-9', str(pid)], check=True)
            print(f"Process {pid} blocked.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to block process: {e}")