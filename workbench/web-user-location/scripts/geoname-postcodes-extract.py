#!/usr/bin/env python3

import pandas as pd
import numpy as np

if __name__ == "__main__":
    data_file = 'data/postcodes.txt'

    headers = [
        'country_code',
        'postal_code',
        'place_name',
        'admin_name1',
        'admin_code1',
        'admin_name2',
        'admin_code2',
        'admin_name3',
        'admin_code3',
        'lat',
        'long',
        'accuracy'
    ]

    df = pd.read_csv(data_file,
                     sep='\t',
                     header=0,
                     names=headers,
                     index_col=0,
                     low_memory=False)[['place_name', 'postal_code', 'lat', 'long']]

    df.loc[:, 'country'] = 'australia'

    with open("../site/data/postcodes.json", 'w') as f:
        f.write(df.to_json(orient='records'))
