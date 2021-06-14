import pandas as pd

from app import basedir
from app.utils.utils import geocode, get_place_arround, distance

fit = {
    'fit': {
        'cafe': ['manufacture', 'services'],
        'medicine': ['common', 'services'],
        'beauty': ['common', 'services', 'retail'],
        'retail': ['retail', 'common'],
        'services': ['services', 'common']
    },
    'good': {
        'cafe': ['sport', 'malls', 'beauty'],
        'medicine': ['services', 'sport'],
        'beauty': ['sport', 'entertainment', 'business'],
        'retail': ['sport', 'beauty', 'business'],
        'services': ['business', 'malls']
    },
    'bad': {
        'cafe': ['cafe'],
        'medicine': ['medicine'],
        'beauty': ['beauty'],
        'retail': ['malls'],
        'services': ['services']
    },
    'land': {
        'cafe': ['метро', 'парк', 'памятник'],
        'medicine': ['метро', 'жилой комплекс'],
        'beauty': ['метро', 'жилой комплекс'],
        'retail': ['метро', 'жилой комплекс'],
        'services': ['метро']
    }
}

def get_topk_places(k, type, place=None, price=None, area=None):
    data = pd.read_csv(basedir + '/data/df.csv', index_col=0)
    bizs = pd.read_csv(basedir + '/data/bizs.csv', index_col=0)
    locs = pd.read_csv(basedir + '/data/locs.csv', index_col=0)
    lands = pd.read_csv(basedir + '/data/lands.csv', index_col=0)

    if place: 
        coords = geocode(place)

        data = get_place_arround(data, coords, 0.02)
        bizs = get_place_arround(bizs, coords, 0.02)
        locs = get_place_arround(locs, coords, 0.03)
        lands = get_place_arround(lands, coords, 0.03)

    locs = locs[locs['type_custom'].isin(fit['fit'][type])]

    if price[0]:
        locs = locs[(locs['cost'] >= price[0]) & (locs['cost'] <= price[1])]
    if area[0]:
        locs = locs[(locs['area'] >= price[0]) & (locs['area'] <= area[1])]

    def func(x):    
        s = pd.Series()
        
        wifi = data.copy()
        wifi['distance'] = distance(data, x)
        wifi1 = wifi.sort_values('distance').iloc[0]
        
        s['counts'] = (wifi1['counts'] / 28).astype(int)
        s['usertime'] = (wifi1['dur_per_user']).astype(int)
        
        s['biz_arround'] = get_place_arround(bizs[bizs['type_custom'].isin(fit['good'][type])], x, 0.007, return_dist=True)
        s['comp_arround'] = get_place_arround(bizs[bizs['type_custom'].isin(fit['bad'][type])], x, 0.007, return_dist=True)
        s['land_arround'] = get_place_arround(lands[lands['type_custom'].isin(fit['land'][type])], x, 0.01, return_dist=True)
        
        s['biz_count'] = s['biz_arround'].shape[0]
        s['comp_count'] = s['comp_arround'].shape[0]

        s['metro_dist'] = 1.5
        s['metro_station'] = ""

        metros =  s['land_arround']
        metros = metros[metros['type'] == 'metro']
        if not metros.empty:
            metro_idx = metros['place_dist'].argmin()
            s['metro_dist'] = metros.iloc[metro_idx]['place_dist']
            s['metro_station'] = metros.iloc[metro_idx]['name']
        
        s['biz_arround'] = list(s['biz_arround'].T.to_dict().values())
        s['comp_arround'] = list(s['comp_arround'].T.to_dict().values())
        s['land_arround'] = list(s['land_arround'].T.to_dict().values())

        return s

    df = locs.apply(func, axis=1)

    if df.empty:
        return []

    dfq = pd.concat([locs, df], axis=1)
    dfq['q'] = df['counts'] + df['usertime'] * 0.8 + df['biz_count'] * 2 - df['comp_count'] * 3 - df['metro_dist'] * 80

    values = list(dfq.sort_values('q', ascending=False).dropna().drop('q', axis=1).head(k).T.to_dict().values())

    return values