import pathlib
import pandas as pd
import os

# Agrupando os dados num dict
data_dir = pathlib.Path('data')
data = {}
for file_name in os.listdir(data_dir):
  city_name = file_name[8:].split('.')[0]
  data[city_name] = pd.read_csv(os.path.join(data_dir,file_name))


# Eliminando colunas
for k in data.keys():
  data[k].drop(['D-J-F','M-A-M','J-J-A','S-O-N'], axis=1, inplace=True)


# Eliminando outliers
def get_limits(column):
  q1 = column.quantile(0.25) # corresponde à 25% dos dados
  q3 = column.quantile(0.75) # corresponde ao restante (75%)
  iqr = q3 - q1
  limits = q1 - 1.5 * iqr, q3 + 1.5 * iqr
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

for k in data.keys():
  data[k] = delete_outliers(data[k])


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
  