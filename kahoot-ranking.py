# COMMAND ----------
# DBTITLE 1,Description
# MAGIC %md
# MAGIC # Kahoot Ranking
# MAGIC 
# MAGIC Este Notebook filtra os vencedores do Kahoot, retornando os primeiros n colocados.
# MAGIC 
# MAGIC ## ▶ Pontuação
# MAGIC ### 1. Pontos de pódio
# MAGIC Para cada Kahoot:
# MAGIC
# MAGIC 🥇1 lugar : 3 pontos
# MAGIC
# MAGIC 🥈2 lugar : 2 pontos
# MAGIC
# MAGIC 🥉3 lugar : 1 ponto
# MAGIC
# MAGIC ### 2. Pontos do Kahoot
# MAGIC O desempate é feito pela pontuação acumulada dos Kahoots. 

# COMMAND ----------
# DBTITLE 1,Imports
import os
import pandas as pd
from unidecode import unidecode
from fuzzywuzzy import process
import re

import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def clean_string(input_string):
    # Use a regular expression to remove spaces and numbers
    cleaned_string = re.sub(r'[\s\d\W]', '', input_string)

    # Remove accents using unidecode
    string = unidecode(cleaned_string).lower()

    return string

def normalize_name(name, known_names, mapping, threshold=30):
    """
    Normalize a name by checking against a mapping and known names.

    Parameters:
    name (str): The name to normalize.
    known_names (list): A list of known names to compare against.
    mapping (dict): A dictionary mapping names to their normalized forms.
    threshold (int): The minimum score for a match to be considered valid (default is 30).

    Returns:
    str: The normalized name if a match is found; otherwise, returns 'johann'.
    """
    if name in mapping:
        return mapping[name]

    match = process.extractOne(name, known_names)

    if match and match[1] >= threshold:
        return match[0]

    return 'johann'

# COMMAND ----------
# Set folder path
folder_path = "2025-3_EXODO"

# COMMAND ----------
# DBTITLE 1,Name exception dict 
# Define name aliases to substitute (check which names have more than 1 alias)
# 
# 'alias': 'originalname'
name_alias = {
    'mar+bi=marbi': 'mardabi',
    'marsembi': 'mardabi',
    'marbinoso': 'mardabi',
    'marcombi': 'mardabi',
    'marbinado': 'mardabi',
    'marbix': 'mardabi',
    'mardasuperbi': 'mardabi',
    'paidaantonell': 'mardabi',
    'antonella': 'mardabi',
    'bine': 'bidomar',
    'binedomar': 'bidomar',
    'sabrine': 'bidomar',
    'mardomar': 'johann',
    'quadra': 'johann',
    'quadrado': 'johann',
    'bigxand': 'xandao',
    'shaquilleomeal': 'johann',
    'bobberkurwa': 'johann',
    'paracetamal': 'johann',
    'quadroh': 'johann',
    'vaixco ': 'johann',
    'bagriel': 'johann',
    'mardomar': 'johann',
    'quadrado': 'johann',
    'luaraa': 'luara',
    'luaraara': 'luara',
    'kakerlake': 'johann',
    'fmr': 'johann',
    'pirarucu': 'johann',
    'tucunare': 'johann',
    'bambu': 'johann',
    'yej!b': 'yejin',
    'yej!n': 'yejin',
    'tirisco': 'johann',
    'luu': 'luara',
    'luuu': 'luara',
    'lua': 'luara',
    'luaura': 'luara',
    'luaraaa': 'luara',
    'gih': 'giovanna',
    'dionemario': 'dione',
    'gabyzinha': 'gaby',
    'gabriele': 'gaby',
    'xandao': 'xandao',
}

# COMMAND ----------
# DBTITLE 1,Main
# Get file info
file_list = [f for f in os.listdir(folder_path)]

df_dict = {}
for file_name in file_list:
    if file_name.endswith('.xlsx'):
        file_path = os.path.join(folder_path, file_name)
        key = file_name
        df_dict[key] = pd.read_excel(
            file_path, sheet_name='Final Scores', usecols="A:C", header=2
        )

# Create dataframe for podium
main_podium = pd.DataFrame()
# Join the files
for key in df_dict:
    podium = df_dict[key].rename(columns={df_dict[key].columns[0]: 'Podium'})
    main_podium = pd.concat([main_podium, podium])

# Rename columns
main_podium.rename(columns={'Total Score (points)': 'Points'}, inplace=True)
# Change data type
main_podium['Podium'] = main_podium['Podium'].astype(int)
main_podium['Points'] = main_podium['Points'].astype(int)

# Clean names
main_podium['Player'] = main_podium['Player'].apply(
    lambda x: clean_string(x))

# Substitute name aliases
main_podium['Player'] = main_podium['Player'].replace(name_alias)

# Assign Podium points
point_mapping = {1: 3, 2: 2, 3: 1}
main_podium['Podium_Points'] = main_podium['Podium'].map(point_mapping)

# COMMAND ----------
# [DEBUG] Display the unique players to verify
logging.debug(f'Unique Players raw:\n{sorted(main_podium['Player'].unique())}')

# COMMAND ----------
# DBTITLE 1,Final ranking
# Create final ranking
rank = (main_podium.loc[:, ['Player', 'Podium_Points', 'Points']]
        .groupby(['Player'])
        .sum()
        .reset_index())
# Index starts at 1
rank.index = rank.index + 1

# COMMAND ----------
# [DEBUG] Display unique players
logging.debug(f'Unique Players:\n{sorted(main_podium['Player'].unique())}')

# COMMAND ----------
# DBTITLE 1,Podium Variations
logging.info(f'\n[{folder_path}] Ranking por Podium Points e desempate por Points')

rank.sort_values(['Podium_Points', 'Points'],ascending=[False, False]) \
    .head(5) \
    .reset_index(drop=True)

# COMMAND ----------
# DBTITLE 1,Top 5 PODIUM PTS AND THEN BY ACCUMULATED PTS
logging.info(f'\n[{folder_path}] Ranking por top 5 Accumulated Points e ordenado por Podium Points')

rank.sort_values(['Points'], ascending=False) \
    .head(5) \
    .sort_values(['Podium_Points'], ascending=False) \
    .reset_index(drop=True)

# COMMAND ----------
# DBTITLE 1,Top 5 Points
logging.info(f'[{folder_path}] Ranking por Points')

rank.sort_values(['Points'], ascending=False) \
    .head(5) \
    .reset_index(drop=True)

# COMMAND ----------
# DBTITLE 1,file_list
file_list

# COMMAND ----------
# DBTITLE 1,Assiduidade | Presença
main_podium.groupby('Player')['Points'] \
           .count() \
           .sort_values(ascending=False) \
           .reset_index() \
           .rename(columns={'Points': 'Presença'})
