import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
import numpy as np

#Use ML to classify processes as legitimate or malicious.

class ThreatDetector:
    def __init__(self):
        # Load or train a model (example: Isolation Forest for anomaly detection)
        try:
            self.model = joblib.load('threat_model.pkl')
        except:
            self.model = self._train_model()

    def _train_model(self):
        # Generate synthetic training data (replace with real data)
        data = {
            'process_hash': [np.random.randint(1e5, 1e6) for _ in range(100)],
            'is_legit': [1 if x % 2 == 0 else -1 for x in range(100)]
        }
        df = pd.DataFrame(data)
        model = IsolationForest(contamination=0.1)
        model.fit(df[['process_hash']])
        joblib.dump(model, 'threat_model.pkl')
        return model

    def analyze(self, hashed_processes):
        # Predict anomalies
        predictions = self.model.predict([[hash] for hash in hashed_processes])
        for hash, pred in zip(hashed_processes, predictions):
            if pred == -1:
                AccessBlocker().block_process(hash)
                Logger().log_alert(f"Malicious process detected: {hash}")