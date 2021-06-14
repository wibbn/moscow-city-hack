import pandas as pd

from app import basedir
from app.utils.utils import get_place_arround

def get_heatmap(coords, r):
    data = pd.read_csv(basedir + '/data/df.csv', index_col=0)
    locs = pd.read_csv(basedir + '/data/locs.csv', index_col=0)

    data = list(get_place_arround(data, coords, r).T.to_dict().values())

    locs = get_place_arround(locs, coords, r)
    locs = list(locs[['lat', 'lng']].T.to_dict().values())

    return data, locs