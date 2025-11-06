# Databricks notebook source  # noqa: D100, INP001

# COMMAND ----------
# DBTITLE 1,Imports
import logging
import os
import pandas as pd
from unidecode import unidecode
from fuzzywuzzy import process
import re

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# omit databricks message "Received command c on object id p0"
logging.getLogger("py4j").setLevel(logging.ERROR)


# COMMAND ----------
# DBTITLE 1,Functions
def clean_string(regex, input_string):
    # Use a regular expression to remove spaces and numbers
    cleaned_string = re.sub(regex, "", input_string)

    # Remove accents using unidecode
    string = unidecode(cleaned_string).lower()

    return string


# COMMAND ----------
# DBTITLE 1,Set folder path
folder_path = "2025-3_EXODO"

# COMMAND ----------
# DBTITLE 1,Get file info
csv_list = [file for file in os.listdir(folder_path) if file.endswith(".csv")]

dict_csv = {}
for file_name in csv_list:
    file_path = os.path.join(folder_path, file_name)
    key = file_name
    dict_csv[key] = pd.read_csv(file_path)

df_csv = pd.DataFrame()
for key in dict_csv:
    csv_podium = dict_csv[key]
    df_csv = pd.concat([df_csv, csv_podium]).reset_index(drop=True)

df_csv["points"] = df_csv["points"].map(lambda x: x*20)
df_csv["place"] = (
    df_csv["place"]
    .map(lambda x: clean_string(r"\D", x))
    .astype(int)
)

df_csv = df_csv.rename(columns={
    "student": "Player",
    "points": "Points",
    "place": "Podium"
})

point_mapping = {1: 3, 2: 2, 3: 1}
df_csv["Podium_Points"] = df_csv["Podium"].map(point_mapping)

# COMMAND ----------
# DBTITLE 1,Export to csv
df_csv.to_csv(f"{folder_path}/blooket_ranking.csv", index=False)

# COMMAND ----------
