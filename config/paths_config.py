import os

PROCESSED_PATH = "artifacts/processed"
INPUT_PATH = "artifacts/raw/dataa.csv"

X_TRAIN_PATH =os.path.join(PROCESSED_PATH, "X_train.pkl")
X_TEST_PATH =os.path.join(PROCESSED_PATH, "X_test.pkl")
Y_TRAIN_PATH =os.path.join(PROCESSED_PATH, "y_train.pkl")
Y_TEST_PATH =os.path.join(PROCESSED_PATH, "y_test.pkl")

SCALER_PATH = os.path.join(PROCESSED_PATH,"scaler.pkl")


MODEL_PATH = "artifacts/models"
os.makedirs(MODEL_PATH, exist_ok=True)
MODEL_SAVED_PATH = os.path.join(MODEL_PATH,"model.pkl")
