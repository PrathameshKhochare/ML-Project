import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainer
from src.components.model_trainer import ModelTrainerConfig

@dataclass
class DataIngectionConfig:
    train_data_path: str=os.path.join('artifacts',"train.csv")
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"data.csv")

class DataIngection:
    def __init__(self):
        self.ingection_config = DataIngectionConfig()

    def initiate_data_ingection(self):
        logging.info("Entered the data injection method or component")
        try:
            df = pd.read_csv('Notebook\Data\stud.csv')
            logging.info("Read the dataset in the form of DataFrame")

            os.makedirs(os.path.dirname(self.ingection_config.train_data_path),exist_ok= True)
            
            df.to_csv(self.ingection_config.raw_data_path,index=False,header=True)

            logging.info("Train Test Split initiated")
            train_set ,test_set = train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingection_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingection_config.test_data_path,index=False,header=True)

            logging.info("Ingection of Data is completed")

            return(
                self.ingection_config.train_data_path,
                self.ingection_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e,sys)
        
if __name__ == "__main__":
    obj = DataIngection()
    train_data , test_data = obj.initiate_data_ingection()

    data_transformation = DataTransformation()
    train_arr,test_arr,_ = data_transformation.initiate_data_transformation(train_data,test_data)

    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))

    