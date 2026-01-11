# Performance metrics
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt

def evaluate_performance(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    print(f"Mean Absolute Error: {mae}")
    print(f"R-Squared Score: {r2}")
    
    plt.figure(figsize=(10,5))
    plt.plot(y_true.values, label="Actual")
    plt.plot(y_pred, label="Predicted")
    plt.legend()
    plt.show()