import os
import pandas as pd

from app import basedir

def get_data():

    data3 = pd.read_csv(basedir + '/data/duraion_2021-03-01_low.csv')
    data4 = pd.read_csv(basedir + '/data/duraion_2021-04-01_low.csv')
    data5 = pd.read_csv(basedir + '/data/duraion_2021-05-01_low.csv')

    data = pd.concat([data3, data4, data5], axis=0)

    data['lat'] = data['gps'].map(lambda x: float(x[1:-1].split(',')[0]))
    data['lng'] = data['gps'].map(lambda x: float(x[1:-1].split(',')[1]))
    data = data.drop('gps', axis=1)
    data['counts'] = 1

    data_small = data[['lat', 'lng', 'counts', 'duration']]

    df = data_small.groupby(['lat', 'lng']).sum().reset_index()

    df['dur_per_user'] = df['duration'] / df['counts']

    return df