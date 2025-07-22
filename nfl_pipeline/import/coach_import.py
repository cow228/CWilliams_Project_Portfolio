"""
imports data for coaches.  collects statistics on moving average basis
"""

import nfl_data_py as nfl
import pandas as pd

if __name__ == '__main__':
    # print(list(nfl.see_pbp_cols()))
    cols = ['home_team','away_team','week','season','posteam','home_coach','away_coach',
            'pass_oe','td_prob','third_down_converted','third_down_failed',
            'punt_attempt','first_down','penalty_yards',
            'game_id']
    years = [2018,2019,2020,2021,2022,2023,2024]
    df = nfl.import_pbp_data(years,cols)
    # df.to_csv('import_files/base_coach.csv')
    # print(df.columns)
    group_map = {'pass_oe':'sum',
                'td_prob':'mean',
                'third_down_converted': 'sum',
                'third_down_failed': 'sum',
                'punt_attempt':'sum',
                'first_down':'sum',
                'penalty_yards': 'sum'}
    # print columns that just get added in by package
    drop_cols = [col for col in df.columns if not col in cols]
    df.drop(columns=drop_cols, inplace=True)
    
    # get data for home and away team
    df_home = df[df['home_team'] == df['posteam']].copy()
    df_home.rename(columns={'home_team':'team','home_coach':'coach'},inplace=True)
    df_home.drop(columns=['away_team','away_coach'],inplace=True)
    df_away = df[df['away_team'] == df['posteam']].copy()
    df_away.rename(columns={'away_team':'team','away_coach':'coach'},inplace=True)
    df_away.drop(columns=['home_team','home_coach'],inplace=True)
    df = pd.concat([df_home, df_away])

    # df.rename(columns={'home_coach':'coach'}, inplace=True)
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
        new_name = 'coach_'+col
        df.rename(columns={col:new_name},inplace=True)

    df.to_csv('import_files/coach_data.csv',index=False)