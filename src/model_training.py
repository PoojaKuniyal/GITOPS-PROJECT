import os
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from sklearn.metrics import accuracy_score, precision_score

logger =get_logger(__name__)

class ModelTraining:
    def __init__(self,processed_data_path, model_output_path):
        self.processed_data_path = processed_data_path
        self.model_output_path = model_output_path
        self.clf = None

        self.X_train ,self.X_test,self.y_train, self.y_test =None,None,None,None
        os.makedirs(self.model_output_path, exist_ok=True)

    def load_data(self):
        try:
            self.X_train = joblib.load(X_TRAIN_PATH)
            self.X_test = joblib.load(X_TEST_PATH)
            self.y_train = joblib.load(Y_TRAIN_PATH)
            self.y_test = joblib.load(Y_TEST_PATH)

            logger.info("Data loaded successfully")
        except Exception as e:
            logger.error(f"error while loading data {e}")
            raise CustomException("failed to load data", e)
            
    def train_model(self):
        try:
            self.clf = LogisticRegression(random_state=42, max_iter=1000)
            self.clf.fit(self.X_train, self.y_train)

            joblib.dump(self.clf, MODEL_SAVED_PATH )
            logger.info("model trained and saved..")
        except Exception as e:
            logger.error(f"error while training model..{e}")
            raise CustomException("faied to train model", e)

    def evaluate_model(self):
        try:
            y_pred = self.clf.predict(self.X_test)
            accuracy = accuracy_score(self.y_test, y_pred)
            precision = precision_score(self.y_test, y_pred, average="weighted")

            logger.info(f"Accuracy : {accuracy}")
            logger.info(f"Precision : {precision}")
        except Exception as e:
            logger.error(f"Error while evaluating model {e}")
            raise CustomException("failed to evaluate model", e)
        
    def run(self):
        self.load_data()
        self.train_model()
        self.evaluate_model()


if __name__ =="__main__":
    trainer = ModelTraining(PROCESSED_PATH, MODEL_PATH)
    trainer.run()