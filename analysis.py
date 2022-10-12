import pandas as pd
import numpy as np
from profile import search_term
from os.path import exists

cols_list = ['date', 'price', 'link_url']

data = pd.read_csv(f'{search_term}_data.csv')
uniques = data.drop_duplicates(subset=['link_url'])
print(uniques)


def mode(x):
    return pd.Series.mode(x)[0]


grouped = uniques.groupby('date').agg(
    {'price': [np.mean, np.min, np.max, mode]})


file_name = f'{search_term}_price.csv'

grouped.to_csv(file_name, mode='a', header=not exists(file_name))

print(pd.read_csv(file_name))