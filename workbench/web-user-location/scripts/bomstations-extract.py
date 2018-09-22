#!/usr/bin/env python3

import pandas as pd
import numpy as np


def load_station_data(station_col_specification):
    station_df = pd.read_fwf(stations_out_file,
                             header=2,
                             na_values=['..', '.....'],
                             skip_blank_lines=True,
                             skipfooter=6,
                             colspecs=station_col_specification)

    station_df.drop(index=0, inplace=True)

    return station_df


def get_column_specification():
    station_cols = '------- ----- ---------------------------------------- ------- ------- -------- --------- -------------- --- ---------- -------- ------'

    station_col_specification = []

    col_start = 0

    for ix, ch in enumerate(station_cols):
        if ch == ' ':
            station_col_specification.append((col_start, ix))
            col_start = ix + 1

    station_col_specification.append((col_start, ix + 1))
    return station_col_specification


if __name__ == "__main__":
    stations_data = ''
    stations_out_file = 'data/stations.txt'
    station_col_spec = get_column_specification()

    df = load_station_data(station_col_spec)

    rename_mapper = {
        'Site': 'id',
        'Dist': 'dist',
        'Site name': 'name',
        'Start': 'start',
        'End': 'end',
        'Lat': 'lat',
        'Lon': 'lon',
        'Source': 'source',
        'STA': 'state',
        'Height (m)': 'height',
        'Bar_ht': 'bar_ht',
        'WMO': 'wmo_id'
    }
    df.rename(rename_mapper, inplace=True, axis='columns')

    df.loc[:, 'state'] = df['state'].str.lower()
    df.loc[:, 'country'] = 'australia'
    df.loc[:, 'country_code'] = 'AU'
    df.loc[:, 'provider'] = 'bom'

    with open("tmp/stations.json", 'w') as f:
        f.write(df.to_json(orient='records'))

    print('-' * 79)
    print(df.info())
    print('-' * 79)
    print(df.describe())
    print('-' * 79)
    print(df.head(5))
    print('-' * 79)