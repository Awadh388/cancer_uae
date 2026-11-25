"""Train the reproducible benchmark model and save its evaluation report."""
from src.pipeline import run_training

if __name__ == "__main__":
    result = run_training(tune=True)
    print("Saved model and metrics. Test macro-F1:", result["test_metrics"]["macro_f1"])
