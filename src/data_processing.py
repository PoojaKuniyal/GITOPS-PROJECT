import os
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from sklearn.inspection import permutation_importance

logger = get_logger(__name__)

class DataProcessing:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.df = None
        self.features = None
        self.selected_features = None

        os.makedirs(self.output_path, exist_ok=True)
        logger.info("Data processing initialized...")

    def load_data(self):
        try:
            self.df = pd.read_csv(self.input_path)
            logger.info("Data loaded successfully..")
        except Exception as e:
            logger.error(f"error while loading data {e}")
            raise CustomException("failed to load data", e)

    def preprocess(self):
        try:
            self.df["Timestamp"] = pd.to_datetime(self.df.Timestamp, errors='coerce')
            self.df = self.df.dropna(subset=['Timestamp'])  # Ensure we drop rows with invalid timestamps

            categorical_cols = ['Operation_Mode', 'Efficiency_Status']
            for col in categorical_cols:
                self.df[col] = self.df[col].astype('category')

            label_encoder = LabelEncoder()
            self.df['Efficiency_Target'] = label_encoder.fit_transform(self.df['Efficiency_Status'])

            label_encoder = LabelEncoder()
            self.df['Operation_Mode'] = label_encoder.fit_transform(self.df['Operation_Mode'])

            logger.info("Basic pre-processing done..")
        except Exception as e:
            logger.error(f"failed to do processing {e}")
            raise CustomException("failed pre-processing", e)

    def feature_selection(self):
        try:
            self.features = ['Operation_Mode', 'Temperature_C', 'Vibration_Hz',
                             'Power_Consumption_kW', 'Network_Latency_ms', 'Packet_Loss_%',
                             'Quality_Control_Defect_Rate_%', 'Production_Speed_units_per_hr',
                             'Predictive_Maintenance_Score', 'Error_Rate_%']

            X = self.df[self.features]
            y = self.df['Efficiency_Target']

            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)

            clf = LogisticRegression(random_state=42, max_iter=1000)
            clf.fit(X_train, y_train)

            result = permutation_importance(clf, X_test, y_test, n_repeats=10, random_state=42, n_jobs=-1)
            importance_df = pd.DataFrame({
                'Feature': self.features,
                'importances': result.importances_mean
            })

            importance_df = importance_df.sort_values(by='importances', ascending=False)
            self.selected_features = importance_df[importance_df['importances'] > 0.01]['Feature'].tolist()

            logger.info(f"{(self.selected_features)} features selected")

            logger.info("Feature selection done...")
        except Exception as e:
            logger.error(f"Failed to do feature selection {e}")
            raise CustomException("Failed to do Feature selection", e)

    def split_save(self):
        try:
            X = self.df[self.selected_features]
            y = self.df["Efficiency_Target"]
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

            joblib.dump(X_train, X_TRAIN_PATH)
            joblib.dump(X_test, X_TEST_PATH)
            joblib.dump(y_train, Y_TRAIN_PATH)
            joblib.dump(y_test, Y_TEST_PATH)
            joblib.dump(scaler, SCALER_PATH)

            logger.info("Saved successfully")
        except Exception as e:
            logger.error(f"error while split and save {e}")
            raise CustomException("Failed to save")

    def run(self):
        self.load_data()
        self.preprocess()
        self.feature_selection()
        self.split_save()

if __name__ == "__main__":
    processor = DataProcessing(INPUT_PATH, PROCESSED_PATH)
    processor.run()
