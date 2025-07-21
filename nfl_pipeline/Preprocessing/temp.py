import nfl_data_py as nfl

# print(nfl.see_weekly_cols())

# df = nfl.import_weekly_data([2023,2024], ['player_display_name','season','week','fantasy_points_ppr','position_group'])
# df = df[df['position_group'].isin(['QB','WR','RB','TE'])]

# df['fantasy_points_ra'] = df['fantasy_points_ppr'].rolling(window=15, min_periods=1).mean()

# df.to_csv('temp.csv',index=False)

print(nfl.import_weekly_rosters([2024]).to_markdown())