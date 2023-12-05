import os, sys
from dataclasses import dataclass

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessed_file_path = os.path.join('data_source', 'preprocessed.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()


    def get_tranformed_data(self):
        '''
        Return transformed data.
        '''
        try:
            numerical_features = [
                'writing_score',
                'reading_score' 
            ]
            
            categorical_features = [
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course'
            ]

            numerical_pipeline = Pipeline(
                steps = [
                    ( 'imputer', SimpleImputer(strategy='median') ),
                    ( 'scaler', StandardScaler() )
                ]
            )

            categorical_pipeline = Pipeline(
                steps = [
                    ('imputer', SimpleImputer(strategy='most_frequent') ),
                    ('one_hot', OneHotEncoder() )
                ]
            )

            logging.info('Numerical transformation completed')

            logging.info('Categorical transformation completed')

            preprocessing = ColumnTransformer([
                ( 'numerical_pipeline', numerical_pipeline, numerical_features ),
                ( 'categorical_pipeline', categorical_pipeline, categorical_features)
            ])

            return preprocessing

        except Exception as e:
            raise CustomException(e, sys)


    def initiate_data_transformation(self, train_data_path, test_data_path):
        try:
            train_df = pd.read_csv(train_data_path)
            test_df = pd.read_csv(test_data_path)

            logging.info('Read train and test data completed')
            logging.info('Get pre-processing')
            
            pre_processing_obj = self.get_tranformed_data()

            target_feature = 'math_score'

            input_train_df = train_df.drop( columns=[target_feature], axis=1 )
            target_train_df = train_df[ target_feature ]

            input_test_df = test_df.drop( columns=[target_feature] ,axis=1 )
            target_test_df = test_df[ target_feature ]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_train_preprocessed = pre_processing_obj.fit_transform(input_train_df)
            input_test_preprocessed = pre_processing_obj.fit_transform(input_test_df)

            train_arr = np.c_[
                input_train_preprocessed, np.array(target_train_df)
            ]

            test_arr = np.c_[ input_test_preprocessed, np.array(target_test_df) ]

            logging.info(f"Saved preprocessing object.")

            save_object(
                file_path=self.data_transformation_config.preprocessed_file_path,
                obj=pre_processing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessed_file_path,
            )

        except Exception as e:
            raise CustomException(e, sys)