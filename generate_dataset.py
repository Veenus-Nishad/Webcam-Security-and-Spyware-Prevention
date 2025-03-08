import pandas as pd
import numpy as np
from faker import Faker

# Generate a synthetic dataset for testing
def generate_dataset(n_samples=1000):
    """
    Generates a synthetic dataset for webcam access patterns.
    Replace this with your own dataset loading logic.
    """
    fake = Faker()
    data = {
        "process_name": [fake.word() + ".exe" for _ in range(n_samples)],  # Process names
        "access_time": np.random.randint(0, 24, size=n_samples),  # Hour of the day
        "frequency": np.random.poisson(lam=3, size=n_samples),    # Access frequency
        "duration": np.random.exponential(scale=10, size=n_samples),  # Duration in seconds
        "cpu_usage": np.random.uniform(0.1, 50.0, size=n_samples),   # CPU usage in %
        "network_activity": np.random.choice([0, 1], size=n_samples),  # 0 = No, 1 = Yes
        "is_malicious": np.random.choice([0, 1], size=n_samples, p=[0.8, 0.2])  # 0 = Legit, 1 = Malicious
    }
    return pd.DataFrame(data)

# Save the dataset to a CSV file
dataset = generate_dataset()
dataset.to_csv("webcam_dataset.csv", index=False)
print("Dataset generated and saved as 'webcam_dataset.csv'.")