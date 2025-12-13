import numpy as np

try:
    from data_loader import load_metrics
    CAN_LOAD_REAL_DATA = True
except:
    CAN_LOAD_REAL_DATA = False
    print("⚠ Data loader not available, using dummy data only")


def generate_dummy_data(size=100):
    np.random.seed(42)
    normal_data = np.random.normal(50, 5, size) # Normal data around mean=50
    
    anomaly_indices = [20, 45, 80]
    for idx in anomaly_indices:
        normal_data[idx] = np.random.choice([20, 80])  # Outliers
    return normal_data


def calculate_baseline(data):
    baseline = {
        'mean': np.mean(data),
        'std': np.std(data),
        'median': np.median(data)
    }
    return baseline


def detect_anomalies(data, baseline, threshold=2):
    anomalies = []
    mean = baseline['mean']
    std = baseline['std']
    
    for i, value in enumerate(data):
        z_score = abs((value - mean) / std)
        if z_score > threshold:
            anomalies.append({
                'index': i,
                'value': value,
                'z_score': z_score
            })
            
    return anomalies

if __name__ == "__main__":
    USE_REAL_DATA = False  # Set to True when you want to test with real data
    
    if USE_REAL_DATA and CAN_LOAD_REAL_DATA:
        print("Loading REAL data from TimescaleDB...")
        df = load_metrics(metric_type="cpu", hours=24)
        
        if not df.empty:
            data = df['value'].values
            print(f"Loaded {len(data)} real data points")
        else:
            print("No real data found, using dummy data")
            data = generate_dummy_data()
    else:
        print("Using DUMMY data")
        data = generate_dummy_data()

    print(f"Generated {len(data)} data points")
    
    baseline = calculate_baseline(data)
    print(f"\nBaseline Statistics:")
    print(f"  Mean: {baseline['mean']:.2f}")
    print(f"  Std Dev: {baseline['std']:.2f}")
    print(f"  Median: {baseline['median']:.2f}")
    
    anomalies = detect_anomalies(data, baseline, threshold=2)
    print(f"\nDetected {len(anomalies)} anomalies:")
    for anomaly in anomalies:
        print(f"  Index {anomaly['index']}: value={anomaly['value']:.2f}, z-score={anomaly['z_score']:.2f}")
