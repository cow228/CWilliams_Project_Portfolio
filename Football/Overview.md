# Goal
Determine if yearly fantasy footbal stats can be used to predict next year's stats <br>
focus on year long stats to ignore huge week-to-week variation <br>
focus on wide recievers to simply any differences between position groups<br>
get stats from PFF.com

### Import data from source
filter data to just take WRs <br>
also filter to take the top 50% of targets - this is about 30, which is about 2 per game.  This is a reasonable metric to filter out the least targeted WRs <br>
Choose list of fields that could be relevant - this is largley a judgement call

### First analysis
#### Inital Results

start with most likely categorie - fpts_game <br>
see if the 3 descriptive stats about fpts_game can describe the actual result <br>
include players that only have 1 data point - results in 418 samples
<br><br>
results <br>
params = ['fpts_game_std', 'fpts_game_mean', 'fpts_game_slope'] <br>
R score  0.3835332807297631 <br>
Slope [-1.50362489  0.8159471   1.95048244] <br>
Intercept 1.33 

#### Next Trials 
(none more successful, yearly values very close): <br>
compound factor: fpts_game_mean + fpts_game_slope <br>
compound factor: fpts_game_mean + (fpts_game_slope * fpts_game_std) <br>
factors: targets (broken intto mean, slope, std) <br>
compound factor: earned_fpts <br>
factors: fpts_game_mean, fpts_game_slope, earned_fpts <br> 
factors: use list of yearly values for fpts, not fpts stats
<br><br>

### Explain Error
based off of the factors found in inital look (fpts_mean, fpts_slope, fpts_std) try to find explaination for error <br>
#### Regression on other factors
first step is to create a measurement of error and to perform linear regression on remaining factors to check for correlation
no factors created an r score better than 0.03 <br>
before this create an average of error based on multiple regression runs with different seeds
##### Absolute Error
Check if error is related to magnitude of fantasy points, check the same for absolute value of error <br>
check if other factors are more closely related to absolute error than regular error none more than r=0.05<br>
##### Evaluate Situation Changes
measure tumult, new team, new WR on team <br>
next: new coach, new QB

###### New Team
This box plot shows the error of broken into categories based on whether that player in on a new team.  The results show that there is a usable difference between them.  Players that go to a new team are overestimated by about 2 points. <br>
![new team box plot](/Football/images/new_team_error.png) <br>
CONCLUSION: new team penalty of -2 will be included in calculations <br>
<br>
similar analysis done for players who had a new wr join their team. <br>
CONCLUSION: not a significant difference to be included in prediction
<br><br>
RSCORE including new team correction: 0.434

