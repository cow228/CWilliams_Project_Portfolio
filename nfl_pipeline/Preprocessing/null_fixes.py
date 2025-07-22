"""
manual fixes for the null values found in preprocessing
"""
import pandas as pd

def fix_cols(df, drops, means, zeros):
    """
    applies specified fixes to nulls in columns
    """
    # drops
    drop_cols = drops
    if len(drop_cols) >0:
        df.dropna(subset=drop_cols, inplace=True)
    # means
    mean_cols = means
    if len(mean_cols) >0:
        for col in mean_cols:
            df[col] = df[col].fillna(df[col].mean())
    # zeros
    zero_cols = zeros
    if len(zero_cols) >0:
        df[zero_cols] = df[zero_cols].fillna(0)

    return df

if __name__ == '__main__':
    # fixes for rec_stats
    rec_df = pd.read_csv('import_files/rec_stats.csv')
    drop_cols = ['ffpts_target','ffpts']
    mean_cols = []
    zero_cols = ['passing_epa','draft_number','draft_pos_decay','fpts_lost','fpts_gained',
                'passing_first_downs',
                'coach_penalty_yards','coach_first_down','coach_punt_attempt',
                'coach_td_prob','coach_3d_pct','coach_pass_oe',
                'team_passing_first_downs','team_passing_tds','team_passing_yards','team_rushing_epa',
                'team_rushing_first_downs','team_rushing_tds','team_rushing_yards','team_passing_epa',
                'avg_expected_yac','avg_yac_above_expectation','avg_yac','yards','avg_cushion']
    rec_df = fix_cols(rec_df, drop_cols, mean_cols, zero_cols)
    rec_df.to_csv('import_files/rec_stats.csv',index=False)

    # fixes for rush_stats
    rush_df = pd.read_csv('import_files/rush_stats.csv')
    drop_cols = ['ffpts_target','ffpts']
    mean_cols = []
    zero_cols = ['draft_number','draft_pos_decay','fpts_lost','fpts_gained',
                'coach_td_prob','coach_3d_pct',
                'coach_penalty_yards','coach_first_down','coach_punt_attempt','coach_pass_oe',
                'team_rushing_tds','team_rushing_first_downs','team_passing_first_downs',
                'team_passing_tds','team_passing_epa','team_rushing_yards','rushing_epa',
                'rushing_first_downs','team_rushing_epa','team_passing_yards']
    rush_df = fix_cols(rush_df, drop_cols, mean_cols, zero_cols)
    rush_df.to_csv('import_files/rush_stats.csv',index=False)

    # fixes for pass_stats
    pass_df = pd.read_csv('import_files/pass_stats.csv')
    drop_cols = ['ffpts_target','ffpts']
    mean_cols = []
    zero_cols = ['draft_number','draft_pos_decay','fpts_lost','fpts_gained',
                'coach_td_prob','coach_3d_pct',
                'coach_penalty_yards','coach_first_down','coach_punt_attempt','coach_pass_oe',
                'team_rushing_tds','team_rushing_first_downs','team_passing_first_downs',
                'team_passing_tds','team_passing_epa','team_rushing_yards','rushing_epa',
                'rushing_first_downs','team_rushing_epa','team_passing_yards',
                'rushing_tds','rushing_yards','passing_epa','passing_first_downs']
    pass_df = fix_cols(pass_df, drop_cols, mean_cols, zero_cols)
    pass_df.to_csv('import_files/pass_stats.csv',index=False)