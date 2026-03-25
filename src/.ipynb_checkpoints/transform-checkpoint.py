import logging
import pandas as pd

logger = logging.getLogger(__name__)

path = "./data/raw/"

people = pd.read_json(path+'raw_people.json')
planets = pd.read_json(path+'raw_planets.json')
species = pd.read_json(path+'raw_species.json')

# Inspection

# This part can be find in the main.ipynb 

# Cleaning
df_people = people.drop(['films', 'vehicles', 'starships', 'created', 'edited', 'url'], axis=1)
df_planets = planets.drop(['films', 'created', 'edited', 'url'], axis=1)
df_species = species.drop(['films', 'created', 'edited', 'url'], axis=1)

# Remove list in DataFrame that can prevent futher cleaning
def get_id_from_url(v):
    if isinstance(v, str) : # handle types before
        if len(v.split('/')) >= 2  and v.split('/')[-2].isdigit() : 
            return v.split('/')[-2]
        return pd.NA
    if isinstance(v, list) :
        if len(v) == 0 : # empty list
            return pd.NA
        if len(v[0].split('/')) >= 2 and v[0].split('/')[-2].isdigit() : # inside the list
            return v[0].split('/')[-2]
        return pd.NA
    if pd.isna(v) : 
        return pd.NA
    return pd.NA # if v isn't a list, a string or NaN

try :  
    df_people['homeworld'] = df_people['homeworld'].apply(get_id_from_url)
    df_people['species'] = df_people['species'].apply(get_id_from_url)
    df_planets['residents'] = df_planets['residents'].apply(get_id_from_url)
    df_species['homeworld'] = df_species['homeworld'].apply(get_id_from_url)
    df_species['people'] = df_species['people'].apply(get_id_from_url)
except Exception as e : 
    logger.error(f'An error occured {e}')

# Checking :
# df_people['species']
# df_people['homeworld']

# Handling unwanted values such as unknown, n/a, ...
def replace_for_nan(dataframe):
    nan_values = pd.NA
    dataframe = dataframe.replace("", nan_values).replace("n/a", nan_values).replace("unknown", nan_values).replace('none', nan_values).replace("indefinite", nan_values) 
    return dataframe

df_people = replace_for_nan(df_people)
df_planets = replace_for_nan(df_planets)
df_species = replace_for_nan(df_species)

# Checking : 
# df_people.isnull().sum()
# df_planets.isnull().sum()
# df_species.isnull().sum()

# Change the mix in classification and designation and harmonise the name in classification
# Here mask is a filter and loc will change all the occurences 
mask = ((df_species["classification"] == "sentient") &
        (df_species["designation"] == "reptilian"))
df_species.loc[mask, ["classification", "designation"]] = ["reptilian", "sentient"]

df_species['classification'] = df_species['classification'].str.strip().str.lower()
df_species['classification'] = df_species['classification'].replace({
    "mammals":"mammal",
    "reptile":"reptilian"})

# Change the inconsistancy in language 
df_species["language"] = df_species["language"].str.strip().str.title()

df_people.dropna(how='all', axis=1, inplace=True)
df_planets.dropna(how='all', axis=1, inplace=True)
df_species.dropna(how='all', axis=1, inplace=True)

if df_people.duplicated().sum() > 0 :
    df_people.drop_duplicates(inplace=True)
if df_planets.duplicated().sum() > 0 :
    df_planets.drop_duplicates(inplace=True)
if df_species.duplicated().sum() > 0:
    df_species.drop_duplicates(inplace=True)

def erase_if_morehalh_miss_v(df) : 
    threshold = round(len(df) * 0.5)
    df = df.dropna(thresh=threshold, axis=1)
    return df

df_people = erase_if_morehalh_miss_v(df_people)
df_planets = erase_if_morehalh_miss_v(df_planets)
df_species = erase_if_morehalh_miss_v(df_species)

try : 
    df_people.rename(columns={"homeworld":"id_homeworld", "species":"id_species"}, inplace=True)
    df_planets.rename(columns={"residents":"id_people"}, inplace=True)
    df_species.rename(columns={"homeworld":"id_homeworld", "people":"id_people"}, inplace=True)
except Exception as e : 
    logger.error(f'An error occured {e}')

def preparing_str_for_astype(v):
    if isinstance(v, str) :  
        v = v.replace(',', '').replace('.','')
        return v
    return v
    
try : 
    df_people['height'] = df_people['height'].apply(preparing_str_for_astype).astype('Int64')
    df_people['mass'] = df_people['mass'].apply(preparing_str_for_astype).astype('Int64')
    df_people['id_homeworld'] = df_people['id_homeworld'].apply(preparing_str_for_astype).astype('Int64')
    df_people['id_species'] = df_people['id_species'].apply(preparing_str_for_astype).astype('Int64')
    df_planets['rotation_period'] = df_planets['rotation_period'].apply(preparing_str_for_astype).astype('Int64')
    df_planets['orbital_period'] = df_planets['orbital_period'].apply(preparing_str_for_astype).astype('Int64')
    df_planets['diameter'] = df_planets['diameter'].apply(preparing_str_for_astype).astype('Int64')
    df_planets['id_people'] = df_planets['id_people'].apply(preparing_str_for_astype).astype('Int64')
    df_species['average_height'] = df_species['average_height'].apply(preparing_str_for_astype).astype('Int64')
    df_species['id_homeworld'] = df_species['id_homeworld'].apply(preparing_str_for_astype).astype('Int64')
    df_species['id_people'] = df_species['id_people'].apply(preparing_str_for_astype).astype('Int64')
except Exception as e :
    logger.error(f'An error occured {e}')