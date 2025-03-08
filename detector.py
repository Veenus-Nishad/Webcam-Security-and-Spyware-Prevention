import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
from blocker import AccessBlocker
from logger import Logger
import logging
from webcam_monitor import WebcamMonitor
import psutil
import threading
import time

logging.basicConfig(
    filename='webcam_security.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class ThreatDetector:
    def __init__(self):
        self.logger = logging.getLogger("ThreatDetector")
        try:
            self.model = joblib.load('threat_model.pkl')
        except FileNotFoundError:
            self.model = self._train_model("webcam_dataset.csv")

    def _train_model(self, dataset_path):
        """
        Trains the ML model using the dataset.
        """
        # Load the dataset
        df = pd.read_csv(dataset_path)  # Replace with your dataset loading logic

        # Define features and target
        X = df[['access_time', 'frequency', 'duration', 'cpu_usage', 'network_activity']]  # Features
        y = df['is_malicious']  # Target

        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train the model
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X_train, y_train)
        
        # Evaluate the model
        y_pred = model.predict(X_test)
        print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
        print(classification_report(y_test, y_pred))
        
        # Save the model
        joblib.dump(model, 'threat_model.pkl')
        return model

    def analyze(self, process_info):
        """
        Analyzes process info using the trained model.
        """
        # Prepare features for prediction
        features = pd.DataFrame([{
            'access_time': process_info['hour'],
            'frequency': process_info['frequency'],
            'duration': process_info['duration'],
            'cpu_usage': process_info['cpu_usage'],
            'network_activity': process_info['network_activity']
        }])
        # Predict if the process is malicious
        prediction = self.model.predict(features)
        if prediction == 1:
            # Block the process if it's malicious
            AccessBlocker().block_process(process_info['pid'])
            Logger().log_alert(f"Malicious process blocked: {process_info['name']}")

    def _get_windows_webcam_processes(self):
        try:
            import winreg
            processes = []
            # Add proper error handling for registry access
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE, 
                    r"SYSTEM\CurrentControlSet\Control\Class\{6BDD1FC6-810F-11D0-BEC7-08002BE2092F}",
                    0, 
                    winreg.KEY_READ | winreg.KEY_WOW64_64KEY
                )
            except PermissionError:
                self.logger.error("Access denied to registry. Run as administrator.")
                return []
            
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return processes
        except Exception as e:
            self.logger.error(f"Windows webcam check failed: {e}")
            return []

if __name__ == "__main__":
    monitor = WebcamMonitor()
    monitor_thread = threading.Thread(target=monitor.run, daemon=True)
    monitor_thread.start()
    
    try:
        # More efficient wait
        while monitor_thread.is_alive():
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")