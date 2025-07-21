'''
method to import nfl historical data from pro football reference and next gen stats
sources have data back to 2018 and 2016 respectivley
returns weekly data for each player
returns 3 csv files for receiving, rushing and passing
'''
import os
import nfl_data_py as nfl
import pandas as pd
import numpy as np

def load_combined_data(stat_type, years, weekly_data, output=False):
    '''
    returns pro football reference data using nfl_data_py
    NOTE: pfr data is not available before 2018, ngs data is not available before 2016
    :param type [str] - one of 'pass', 'rec', 'rush
    :param years [list[int]] - list of years for data
    :param output [bool] - if you want to open resulting csv
    :return [dataframe] - weekly stats for all players with stat type in year range
    '''
    # ensure data is correct
    assert stat_type in ['pass','rec','rush'], 'incorect stat type'
    if not isinstance(years, list):
        if isinstance(years, (int, float)):
            years = [int(years)]
        elif isinstance(years, str):
            years = list(int(years))
        else:
            raise TypeError('years needs to be a list of ints')
    years = [year for year in years if 2025>year>2017]
    # dict with columns to select from each data type
    pfr_col_list_keep = {
        'pass': ['season','week','team','opponent','pfr_player_name',
                 'passing_drop_pct','passing_bad_throw_pct','times_pressured_pct'],
        'rec': ['season','week','team','opponent','pfr_player_name',
                'receiving_drop_pct','receiving_rat'],
        'rush': ['season','week','team','opponent','pfr_player_name',
                 'carries','rushing_yards_before_contact_avg',
                 'rushing_yards_after_contact_avg'],
    }
    ngs_col_list_drop = ['player_short_name','player_jersey_number','player_last_name',
                 'player_first_name','player_gsis_id','player_position','team_abbr']
    ngs_stat_name_map = {'pass':'passing','rec': 'receiving','rush':'rushing'}
    # use function with pfr (pro football reference)
    df_pfr = nfl.import_weekly_pfr(stat_type,years)
    df_pfr = df_pfr[pfr_col_list_keep[stat_type]]
    # use function with ngs (next gen stats) and map stat name
    ngs_stat = ngs_stat_name_map[stat_type]
    df_ngs = nfl.import_ngs_data(ngs_stat, years)
    df_ngs.drop(columns=ngs_col_list_drop, inplace=True)
    # merge results
    df_merge = df_ngs.merge(df_pfr,
                            left_on=['season','week','player_display_name'],
                            right_on=['season', 'week', 'pfr_player_name'])
    # clean df and limit to regular season
    df_merge.rename(columns={'player_display_name': 'player'}, inplace=True)
    df_merge = df_merge[df_merge['season_type']=='REG']
    df_merge.drop(columns=['pfr_player_name','season_type'], inplace=True)
    # get snap count data
    snaps_df = nfl.import_snap_counts(years)[['season','week','player','offense_pct']]
    df_merge = df_merge.merge(snaps_df, how='left', on=['season','week','player'])
    # shift weeks by 1 so that the next weeks points are predicted with the team player will be on next week
    players = df_merge['player'].unique()
    for player in players:
        team_list = df_merge[df_merge['player']==player]['team'].to_list()
        new_team_list = team_list[1:]
        new_team_list.append(team_list[-1])
        df_merge.loc[df_merge['player']==player, 'team'] = new_team_list
    # merge team data
    team_weekly_df = weekly_data.copy()
    team_weekly_df.drop(columns=['player'], inplace=True)
    team_weekly_df = team_weekly_df.groupby(['season', 'week', 'team']).sum().reset_index()
    team_weekly_df.columns = ['team_'+col if not col in ['season', 'week', 'team'] else col for col in team_weekly_df.columns]
    df_merge = df_merge.merge(team_weekly_df, how='left', on=['season', 'week', 'team'])
    # merge additional individual data
    new_stats_cols = {
        'rush': ['season', 'week', 'player',
        'rushing_first_downs', 'rushing_epa'], 
        'pass': ['season', 'week', 'player',
        'passing_first_downs', 'passing_epa',
        'rushing_yards', 'rushing_tds', 'rushing_first_downs', 'rushing_epa'],
        'rec': ['season', 'week', 'player',
        'passing_first_downs', 'passing_epa']
        }
    cols = new_stats_cols[stat_type]
    weekly_data = weekly_data[cols]
    df_merge = df_merge.merge(weekly_data, how='left', on=['season','week','player'])
    # merge additional individual data
    # merge team fantasy points added and lost by roster changes
    df_merge = new_team_age_draft(df_merge)
    # add coach data
    df_merge = coach_data_input(df_merge)
    # calculate fantasy points
    df_merge['ffpts'] = add_ff_points(df_merge, stat_type)
    df_ffpts = df_merge.iloc[1:][['season','week','player','ffpts']]
    df_ffpts['week'] = df_ffpts['week'] - 1
    df_ffpts.rename(columns={'week':'temp_week', 'ffpts': 'ffpts_target'}, inplace=True)
    df_merge = df_merge.merge(df_ffpts, how='left', left_on=['season','week','player'], right_on=['season','temp_week','player'])
    df_merge.drop(columns=['temp_week'], inplace=True)
    # print if output true
    filename = stat_type + '_stats.csv'
    file_path = os.path.join('files', filename)
    df_merge.to_csv(file_path, index=False)
    if output:
        os.startfile(filename)

def add_ff_points(df, stat_type):
    """
    based on dataframe and stat type calculate fantasy points.
    calculate only based on that stat, so no rec stats for rush.
    This will make prediction easier.
    """
    # identify the relevant stat cols for each type
    stat_cols = {
        'rush': (['rush_yards', 'rush_touchdowns'],[0.1,6]),
        'pass': (['pass_yards', 'pass_touchdowns','interceptions'],[0.04,4,-2]),
        'rec': (['receptions','yards','rec_touchdowns'],[0.5,0.1,6])
    }
    pts = np.zeros(len(df))
    for i in range(len(stat_cols[stat_type])):
        col = stat_cols[stat_type][0][i]
        mult = stat_cols[stat_type][1][i]
        pts += df[col]*mult
    
    return pts

def new_team_age_draft(df):
    """
    import file with team/old team values as well as age and draft position
    calculate the team by team fantasy point change from new players.
    smooth out new player ffpts and draft positon with moving average
    """
    df_new_data = pd.read_csv('files/player_age_draft_team.csv')[['season','week','player','draft_number','age','games_played', 'draft_pos_decay']]
    df_new_team_points = pd.read_csv('files/new_team_pts.csv')[['season','week','team','fpts_gained','fpts_lost']]
    
    df = df.merge(df_new_data, how='left', on=['season','week','player'])
    df = df.merge(df_new_team_points, how='left', on=['season','week','team'])

    return df

def coach_data_input(df):
    """
    input coaching data from csv
    """
    coach_df = pd.read_csv('files/coach_data.csv')
    coaches = coach_df['coach'].unique()
    for coach in coaches:
        team_list = coach_df[coach_df['coach']==coach]['team'].to_list()
        new_team_list = team_list[1:]
        new_team_list.append(team_list[-1])
        coach_df.loc[coach_df['coach']==coach, 'team'] = new_team_list

    df = df.merge(coach_df, how='left', on=['season','week','team'])
    return df

if __name__ == '__main__':
    select_years = [2018,2019,2020,2021,2022,2023,2024]
    # import weekly data
    cols = ['season', 'week', 'recent_team', 'player_display_name',
        'passing_yards', 'passing_tds', 'passing_first_downs', 'passing_epa',
        'rushing_yards', 'rushing_tds', 'rushing_first_downs', 'rushing_epa']
    weekly_df = nfl.import_weekly_data(select_years, cols)
    weekly_df.rename(columns={'recent_team':'team','player_display_name':'player'}, inplace=True)
    # import positional data and merge with weekly
    for select_type in ['pass','rec','rush']:
        load_combined_data(select_type,select_years,weekly_df)
