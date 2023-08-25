import pathlib
import pandas as pd
import os
import numpy as np


# Agrupando os dados num dict
def load_data():
  data_dir = pathlib.Path('data')
  data = {}
  for file_name in os.listdir(data_dir):
    city_name = file_name[8:].split('.')[0]
    data[city_name] = pd.read_csv(os.path.join(data_dir,file_name))

  # Eliminando colunas
  for k in data.keys():
    data[k].drop(['D-J-F','M-A-M','J-J-A','S-O-N'], axis=1, inplace=True)

  # Eliminar valores 999
  for k in data.keys():
    data[k].replace(999.90, np.NaN, inplace=True)
  
  return data


# Eliminando outliers
def get_limits(column, multiplier):
  q1 = column.quantile(0.25) # corresponde à 25% dos dados
  q3 = column.quantile(0.75) # corresponde ao restante (75%)
  iqr = q3 - q1
  limits = q1 - multiplier * iqr, q3 + multiplier * iqr
  return limits

def delete_outliers_per_column(df, column_name):
  rows = df.shape[0]
  lower_lim, upper_lim = get_limits(df[column_name])
  df = df.loc[(df[column_name] >= lower_lim) & (df[column_name] <= upper_lim), :]
  #print(column_name)
  deleted_rows = rows - df.shape[0]
  return df, deleted_rows

def delete_outliers(df):
  for month in df.columns[1:13]:
    df, deleted_rows = delete_outliers_per_column(df, month)
    #print(f'{deleted_rows} linha(s) removida(s).')
  return df

# Preenchendo outliers com NaN
def filling_outliers(df, multiplier):
  for month in df.columns[1:13]:
    lower_lim, upper_lim = get_limits(df[month], multiplier)
    outlier_indices = df[(df[month] > upper_lim) | (df[month] < lower_lim)].index
    df.loc[outlier_indices, month] = np.nan
  return df


# Funções de interesse para o app
def get_cities(data):
  cities = []
  for column in data:
    cities.append(column)
  return cities

def get_options(data):
  options = []
  for month in data["salvador"].columns[1:]:
    item = {}
    item["label"] = month
    item["value"] = month
    options.append(item)
  return options

def set_outlier_multiplier(df, multiplier):
  for k in df.keys():
    df[k] = filling_outliers(df[k], multiplier)
  return df

def set_fill(df, tipo):
  if(tipo == "nada"):
    return df
  elif(tipo == "fillna"):
    for k in df.keys():
      df[k] = df[k].fillna(method="ffill")
    return df
  elif(tipo == "interpolacao"):
    for k in df.keys():
      df[k] = pd.DataFrame(df[k])
      df[k] = df[k].interpolate(method='linear')
    return df
