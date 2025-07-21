import nfl_data_py as nfl
import pandas as pd

if __name__ == '__main__':
    # print(list(nfl.see_pbp_cols()))
    cols = ['home_team','week','season','posteam','home_coach',
            'pass_oe','td_prob','home_wp','third_down_converted','third_down_failed',
            'punt_attempt','first_down','penalty_yards','total_home_epa',
            'total_home_rush_epa','total_home_pass_epa','game_id']
    years = [2018,2019,2020,2021,2022,2023,2024]
    df = nfl.import_pbp_data(years,cols)
    # print(df.columns)
    group_map = {'pass_oe':'sum',
                'td_prob':'mean',
                'home_wp':'mean',
                'third_down_converted': 'sum',
                'third_down_failed': 'sum',
                'punt_attempt':'sum',
                'first_down':'sum',
                'penalty_yards': 'sum',
                'total_home_epa': 'last',
                'total_home_rush_epa': 'last',
                'total_home_pass_epa': 'last'}
    # print columns that just get added in by package
    drop_cols = [col for col in df.columns if not col in cols]
    df.drop(columns=drop_cols, inplace=True)
    
    # filter data
    df = df[df['home_team'] == df['posteam']]
    df.rename(columns={'home_team':'team','home_coach':'coach'}, inplace=True)
    df.drop(columns=['posteam','game_id'], inplace=True)
    
    idx_cols = ['season','week','coach','team']
    df = df.groupby(idx_cols).agg(group_map).reset_index()
    # comput 3rd down pct
    df['3d_pct'] = df['third_down_converted'] / (df['third_down_converted'] + df['third_down_failed'])
    df.drop(columns=['third_down_converted','third_down_failed'], inplace=True)

    # compute rolling averages
    for col in df.columns:
        if col in idx_cols:
            continue
        df[col] = df[col].rolling(window=6, min_periods=1).mean()

    df.to_csv('files/coach_data.csv',index=False)