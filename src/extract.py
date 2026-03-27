import requests
import json
import os 

import logging
logger = logging.getLogger(__name__)


def extract_data(current_url, empty_list):
    try:
        while current_url is not None :
            response = requests.get(current_url, timeout=5)
            response.raise_for_status()
            data = response.json()
            empty_list.extend(data.get("results", []))
            new_url = data.get("next")
            current_url = new_url
    except requests.exceptions.HTTPError as e : 
        logger.error(f"HTTP error : {e}")
    except requests.exceptions.ConnectionError:
        logger.error("Connection problem")
    except requests.exceptions.Timeout :
        logger.error("Timeout error")
    except requests.exceptions.RequestException as any_e : 
        logger.error(f"General error : {any_e}")

path = "./data/raw/"

def folder_creation(path):
    try : 
        os.makedirs(path)
        logger.info(f"The path is open : {path}")
    except FileExistsError :
        logger.info("The path was already opened")

folder_creation(path)

def write_raw_data(path, data, name_file:str):
    try:
        with open(path+str(name_file)+'.json', 'w', encoding='utf-8') as file : 
            json.dump(data, file, indent=4, ensure_ascii=False)
        logger.info("Data loaded")
    except FileNotFoundError: 
        logger.error("Folder, path, don't exist") 
