import threading
from monitor import WebcamMonitor

if __name__ == "__main__":
    monitor = WebcamMonitor()
    # Run in a background thread
    monitor_thread = threading.Thread(target=monitor.run, daemon=True)
    monitor_thread.start()
    
    # Keep the main thread alive
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Stopping...")