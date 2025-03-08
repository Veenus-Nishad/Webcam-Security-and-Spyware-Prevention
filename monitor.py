import time
from webcam_monitor import WebcamMonitor
from detector import ThreatDetector
import logging
import platform
import psutil

# Add basic logging configuration at the start
logging.basicConfig(
    filename='webcam_security.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    logger = logging.getLogger(__name__)
    monitor = WebcamMonitor()
    detector = ThreatDetector()
    
    logger.info("Starting webcam monitoring...")
    try:
        while True:
            processes = monitor._get_webcam_processes()
            if processes:
                print(f"Found webcam processes: {processes}")
                logger.info(f"Found processes: {processes}")
                for process in processes:
                    detector.analyze(process)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nStopping webcam monitoring...")
    except Exception as e:
        logging.error(f"Error in main loop: {str(e)}")
    finally:
        logging.info("Monitor stopped")

def _get_linux_webcam_processes(self):
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                # Skip system processes and processes we don't have access to
                if proc.pid == 1 or proc.username() == 'root':
                    continue
                    
                # Check if process has open file descriptors to /dev/video*
                proc_files = proc.open_files()
                if any('/dev/video' in fd.path for fd in proc_files):
                    processes.append(proc.info)
                    
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                # Silently skip processes we can't access
                continue
            except Exception as e:
                # Log only unexpected errors
                self.logger.debug(f"Error checking process {proc.pid}: {str(e)}")
                continue
                
        return processes
        
    except Exception as e:
        # Log only unexpected errors that affect the entire function
        self.logger.error(f"Unexpected error in webcam monitoring: {str(e)}")
        return []

if __name__ == "__main__":
    main()