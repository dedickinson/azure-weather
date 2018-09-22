#!/usr/bin/env python3

import pandas as pd
import numpy as np
import pycountry

if __name__ == "__main__":
    data_file = 'data/postcodes.txt'

    columns = {
        'country_code': np.str,
        'postal_code': np.str,
        'place_name': np.str,
        'state': np.str,
        'admin_code1': np.str,
        'admin_name2': np.str,
        'admin_code2': np.str,
        'admin_name3': np.str,
        'admin_code3': np.str,
        'lat': np.float64,
        'long': np.float64,
        'accuracy': np.str
    }

    df = pd.read_csv(data_file,
                     sep='\t',
                     header=0,
                     names=columns.keys(),
                     dtype=columns,
                     low_memory=False,
                     usecols=['country_code', 'place_name',
                              'state', 'postal_code', 'lat', 'long', 'accuracy'])

    df['country'] = df.apply(
        lambda row: pycountry.countries.get(alpha_2=row['country_code']).name, axis=1)

    with open("tmp/postcodes.json", 'w') as f:
        f.write(df.to_json(orient='records'))

    print('-' * 79)
    print(df.info())
    print('-' * 79)
    print(df.describe())
    print('-' * 79)
    print(df.head(5))
    print('-' * 79)
