#!/usr/bin/env python3

import pandas as pd
import numpy as np

if __name__ == "__main__":
    data_file = 'data/geonames.txt'

    headers = [
        'geonameid',
        'name',
        'asciiname',
        'alternatenames',
        'lat',
        'long',
        'feature_class',
        'feature_code',
        'country_code',
        'cc2',
        'admin1_code',
        'admin2_code',
        'admin3_code',
        'admin4_code',
        'population',
        'elevation',
        'dem',
        'timezone',
        'modification_date'
    ]

    df = pd.read_csv(data_file, 
                    sep='\t', 
                    header=0, 
                    names=headers, 
                    index_col=0,
                    low_memory=False)[['name','lat','long', 'feature_class', 'feature_code']]
    df = df[(df['feature_class'] == 'P')]
    df.loc[:, 'country'] = 'australia'

    with open("../site/data/locations.json", 'w') as f:
        f.write(df.to_json(orient='records'))