import logging
import pandas as pd 
import os

logger = logging.getLogger(__name__)

path_load = "./data/clean/"

os.makedirs(path_load, exist_ok=True)

def load(dataframe, name_file) : 
    try : 
        file_path = os.path.join(path_load, name_file + ".csv")
        dataframe.to_csv(file_path, sep=',', index=False) 
        logger.info(f"{name_file}.csv saved")
    except Exception as e:
        logger.error(f"Error during load: {e}")
