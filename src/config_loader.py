import yaml

def load_config():    
    try :
        with open("config_yaml/config.yaml", 'r') as file : 
            return yaml.safe_load(file)
    except FileNotFoundError : 
        print("File is not found")
    except yaml.YAMLError : 
        print("Syntaxe error in the YAML file")
    except Exception as e :
        print(f"An error occured : {e}") 