import pandas as pd

from app import basedir
from app.utils.utils import geocode, get_place_arround, distance

fit = {
    'fit': {
        'кафе': ['manufacture'],
        'клиника': ['common', 'manufacture'],
    },
    'good': {
        'кафе': ['sport', 'malls', 'beauty'],
        'клиника': ['services']
    },
    'bad': {
        'кафе': ['cafe'],
        'клиника': ['medicine']
    }
}

def get_topk_places(k, type, place=None):
    data = pd.read_csv(basedir + '/data/df.csv', index_col=0)
    bizs = pd.read_csv(basedir + '/data/bizs.csv', index_col=0)
    locs = pd.read_csv(basedir + '/data/locs.csv', index_col=0)

    if place: 
        coords = geocode(place)

        data = get_place_arround(data, coords, 0.02)
        bizs = get_place_arround(bizs, coords, 0.02)
        locs = get_place_arround(locs, coords, 0.02)

    locs = locs[locs['type_custom'].isin(fit['fit'][type])]

    def func(x):    
        s = pd.Series()
        
        wifi = data.copy()
        wifi['distance'] = distance(data, x)
        wifi1 = wifi.sort_values('distance').iloc[0]
        
        s['counts'] = (wifi1['counts'] / 28).astype(int)
        s['usertime'] = (wifi1['dur_per_user']).astype(int)
        
        s['biz_arround'] = get_place_arround(bizs[bizs['type_custom'].isin(fit['good'][type])], x, 0.007)
        s['comp_arround'] = get_place_arround(bizs[bizs['type_custom'].isin(fit['bad'][type])], x, 0.007)
        
        s['biz_count'] = s['biz_arround'].shape[0]
        s['comp_count'] = s['comp_arround'].shape[0]
        
        s['biz_arround'] = list(s['biz_arround'].T.to_dict().values())
        s['comp_arround'] = list(s['comp_arround'].T.to_dict().values())
        
        return s

    df = locs.apply(func, axis=1)
    dfq = pd.concat([locs, df], axis=1)
    dfq['q'] = df['counts'] + df['usertime'] * 0.8 + df['biz_count'] * 2 - df['comp_count'] * 3

    values = list(dfq.sort_values('q', ascending=False).dropna().drop('q', axis=1).head(k).T.to_dict().values())

    return values