import pandas as pd
from profile import search_term

cols_list = ['date', 'price']

result = pd.read_csv(f'{search_term}_data.csv', usecols=cols_list)

grouped = result.groupby('date').agg(
    {'price': ['mean', 'min', 'max', pd.Series.mode]})


print(grouped)
