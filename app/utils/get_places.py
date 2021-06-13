from typing import List, Dict

import pandas as pd
import numpy as np

from app import basedir

def get_topk_places(k: int) -> List[Dict]:
    data = pd.read_csv(basedir + '/data/df.csv')

    data_sorted = data.sort_values(['dur_per_user'], ascending=[0])

    top_k = data_sorted.head(k)

    topk_list = list(top_k.T.to_dict().values())

    print(topk_list)

    return topk_list