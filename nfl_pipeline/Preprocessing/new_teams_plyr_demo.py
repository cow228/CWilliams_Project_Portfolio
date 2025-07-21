"""
import data from nfl_data_py for player team, age, draft position
find out where players changed teams
"""
import nfl_data_py as nfl
import pandas as pd

if __name__ == '__main__':
    years = [2018,2019,2020,2021,2022,2023,2024]
    df = nfl.import_weekly_rosters(years)


    df = df[(df['position'].isin(['QB','RB','WR','TE']))*(df['game_type']=='REG')][['season','team','week','player_name','draft_number','age']]
    df.rename(columns={'player_name':'player'}, inplace=True)


    df = df.sort_values(by=['season','week']).reset_index(drop=True)
    df['prev_team'] = 0
    df['games_played'] = 0

    player_list = df['player'].unique()
    player_quant = len(player_list)
    current_player = 0
    for player in player_list:
        current_player += 1
        # create offset list of teams played for each week
        team_list = df[df['player']==player]['team'].to_list()
        prev_team_list = [team_list[0]]
        prev_team_list.extend(team_list[:-1])
        # create element showing games played
        games_played = list(range(1,len(team_list)+1))
        # apply lists to dataframe per player
        df.loc[df['player']==player,'prev_team'] = prev_team_list
        df.loc[df['player']==player,'games_played'] = games_played

        if current_player%100 == 0:
            print('player {}/{}'.format(current_player, player_quant))
    df['draft_pos_decay'] = df['draft_number'] / df['games_played']

    df_ffpts = nfl.import_weekly_data(years, ['player_display_name','season','week','fantasy_points_ppr','position_group'])
    df_ffpts = df_ffpts[df_ffpts['position_group'].isin(['QB','WR','RB','TE'])]
    df_ffpts.rename(columns={'player_display_name':'player'}, inplace=True)

    df_ffpts['fantasy_points_ra'] = df_ffpts['fantasy_points_ppr'].rolling(window=15, min_periods=1).mean()
    df_ffpts.drop(columns=['fantasy_points_ppr','position_group'],inplace=True)

    df = df.merge(df_ffpts, how='left', on=['season','week','player'])

    # calculate per team, new fpts
    df['is_new_team'] = df['prev_team'] != df['team']
    df_nt = df[df['is_new_team'] == True][['season','week','team','fantasy_points_ra','player','prev_team']]
    # df_nt.to_csv('files/new_team.csv', index=False)
    df_nt.drop(columns=['player','prev_team'], inplace=True)

    df_nt_grouped_gain = df_nt.groupby(['season','week','team']).sum().reset_index()
    df_nt_grouped_gain.rename(columns={'fantasy_points_ra':'fpts_gained'}, inplace=True)

    df_nt = df[df['is_new_team'] == True][['season','week','prev_team','fantasy_points_ra']]
    df_nt_grouped_loss = df_nt.groupby(['season','week','prev_team']).sum().reset_index()
    df_nt_grouped_loss.rename(columns={'fantasy_points_ra':'fpts_lost', 'prev_team':'team'}, inplace=True)
    df_nt_grouped = df_nt_grouped_gain.merge(df_nt_grouped_loss, how='left', on=['season','week','team'])

    df_nt_grouped['fpts_gained'] = df_nt_grouped['fpts_gained'].rolling(window=4, min_periods=1).mean()
    df_nt_grouped['fpts_lost'] = df_nt_grouped['fpts_lost'].rolling(window=4, min_periods=1).mean()

    # send results to csv for use in other functions
    df_nt_grouped.to_csv('files/new_team_pts.csv', index=False)
    df.to_csv('files/player_age_draft_team.csv', index=False)

