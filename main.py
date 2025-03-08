import threading
from monitor import WebcamMonitor
import time
import psutil

if __name__ == "__main__":
    # Initialize the webcam monitor
    monitor = WebcamMonitor()
    # Run the monitor in a background thread
    monitor_thread = threading.Thread(target=monitor.run, daemon=True)
    monitor_thread.start()
    
    # Keep the main thread alive
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Stopping...")