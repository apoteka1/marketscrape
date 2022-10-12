import pandas as pd
import numpy as np
from profile import search_term
import matplotlib.pyplot as plt

cols_list = ['date', 'price', 'link_url']

data = pd.read_csv(f'{search_term}_data.csv')
uniques = data.drop_duplicates()

grouped = uniques.groupby(['date'])

def mode(x):
    return pd.Series.mode(x)[0]

aggregated = grouped.agg(
    # {'date': 'count'},
    ave_price=pd.NamedAgg(column="price", aggfunc=np.mean),
    min_price=pd.NamedAgg(column="price", aggfunc=np.min),
    max_price=pd.NamedAgg(column="price", aggfunc=np.max),
    most_common=pd.NamedAgg(column="price", aggfunc=mode),
    number_for_sale=pd.NamedAgg(column="date", aggfunc='count'),
).reset_index()

# convert date to datetime
# grouped['date'] = pd.to_datetime(grouped['date'], format="%d:%m:%Y")

print(aggregated)

aggregated.plot(x="date", y=["ave_price", "min_price", "max_price"])
plt.show()

file_name = f'{search_term}_price'

aggregated.to_csv(f'{file_name}.csv', mode='w')

aggregated.to_html(f'{file_name}.html') 