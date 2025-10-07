from src.data_processing import DataProcessing
from src.model_training import ModelTraining
from config.paths_config import *

if __name__ == "__main__":
    processor = DataProcessing(INPUT_PATH, PROCESSED_PATH)
    processor.run()
    trainer = ModelTraining(PROCESSED_PATH, MODEL_PATH)
    trainer.run()
