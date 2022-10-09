import pandas as pd
from profile import search_term
from os.path import exists

cols_list = ['date', 'price']

result = pd.read_csv(f'{search_term}_data.csv', usecols=cols_list)

grouped = result.groupby('date').agg(
    {'price': ['mean', 'min', 'max', pd.Series.mode]})

file_name = f'{search_term}_price.csv'


grouped.to_csv(file_name, mode='a', header=not exists(file_name))

print(pd.read_csv(file_name))
