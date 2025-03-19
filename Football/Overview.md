## Problem Definition

**Initial goal**: Develop a competitive edge for fantasy football by predicting player outcomes.  
Considerations: 
<br>

1. There are 3 main tasks that require decisions: drafting players, trading players, starting/sitting players. *Focus first on drafting since this decision only requires predicting player points without considering other interactions.* <br>

2. There are 4 main positions that will likely have different predictive factors: wide receivers, running backs, tight ends, and quarterbacks. *Focus first on wide receivers since each team can have 3 of them and there will be the most data since there are more receivers than running backs.*
<br>

**Revised goal**: Develop a competitive edge in drafting by predicting wide receiver outcomes.  
Considerations: <br>

3. Determine a baseline to measure improvement. *Define current state as drafting based on ADP (Average draft position of a given player based off all the drafts done by all leagues on a given platform).*
4. Determine attribute to predict. *Predict points per game played. This will avoid modeling errors when considering past injuries. Since injuries are not predictable, the most relevant information is the points scored per game, not total points scored. This will potentially allow the model to be extended to in-season predictions for trading and starting/sitting because points per game should still apply no matter how many games are left in the season.*
5. Determine if rookie performance can be predicted.  *not enough data in current data set.  Rookies are removed from model for now.  May be able to predict based on college performance and/or NFL draft position*
<br>

**Final goal**: Develop a model to predict non-rookie wide receiver points per game that outperforms drafting based on ADP.

## Data Acquisition
### Data Source
**Data Source: Pro Football Focus**

-	Includes historical data for all wide receivers per game for more than the last 10 years
-	Includes multiple types of detailed data to extract maximum insight
    -	basic statistical values such as yards, targets, touchdowns
    -	compound statistical values such as targeted quarterback rating, yards per route run, inline rate
    -	proprietary player grades metric which aggregates player performance on each play
 
### Clean Data
Create function to pull data in.  Using a function will make sure that I can always access clean data input after manipulating the data frame for various uses.<br>
cleaning steps: <br>

1.	Filter attributes
    1.	Using subject matter expertise, remove irrelevant data
    2.	remove absolute data when rate data is available
    3.	remove repetitive data that could be concluded from other data
2.	import data
    1.	filter out non-wider receivers
    2.	filter out the lowest percentiles of receivers
        1.	Many players are irrelevant to fantasy and including them would significantly weight the data towards low points per game
        2.	 Determine cutoff percentile by picking a value that excludes as many players as possible while still including most players from the ADP dataset. (this is a separate dataset that includes players ADP to be used for assessing predictive capability)
3.	For each player’s outcome for each year combine data for all previous years to collect independent and dependent values in each row.
4.	Each input column will expand into a column containing: the mean, standard deviation and slope as well as one column for each of the previous 6 years.  

### Explore Data
Exploration steps

1.	Start by filtering exploration attributes to just the mean values.  This should give a sense of the predictive relevance of each attribute without examining each of the ~200 attribute columns individually.  
2.	Identify null values – either fill or remove
3.	Plot each attribute to see data ranges and identify outliers
    1.	For columns with significant outliers remove data more than 3 standard deviations from the mean
4.	Apply null fill and standard deviation correction to data input function

### Explore Correlation
Exploration steps

1.	Create heatmap of correlation matrix to see the correlations to the target variable and other independent variables.
2.	Create adjusted correlation to fantasy points by:
    1.	Selecting attribute with highest correlation to target
    2.	Adjust correlation to target based on correlation between selected attribute and all others
    3.	Selecting the next highest attribute
3.	Attributes most independently correlated to points per game:
    1.	Fantasy Points
    2.	Targeted quarterback rating
    3.	Targets per game
    4.	Yards per reception
    5.	Targets

## Modeling
### Linear Regression

- start by building a linear regression since its a straightforward starting point. <br>
- because 'fantasy points per game mean' has a strong correlation to actual a linear model may be able to predict actual fantasy points per game well.
- best correlation: 0.78

### Random Forest

- the complex relationships between data might be better understood by a categorization model like random forest.  Decision trees will be able to represent if statements where one attribute only becomes relevant based on the outcome of previous analysis.  This would match well with an analysis like: yards after catch matter more if the depth of target is low, or: quantity of yards and touchdowns are affected by the quality of quarterback and should be handled differently depending on if they are good or bad.  <br>
- However, converting the categorical output of a random forest model into numeric prediction requires creativity.  The method applied here sets each integer quantity of points per game as a category.  Then based on the probability that the model sets for that category I will calculate a weighted average.  I can turn the range of outcomes this provides into a mean and a standard deviation.  <br>
- standard deviations will ve valuable information for making draft selections, if there are atainable from a model, it should be developed.  
- best correlation: 0.80

### Neural Network

- like the random forest the nerual network will help model the complex relationships between attributes.  However, it will be able to more directly calculate a numeric result.
- I also used this as an opportunity to learn about neural networks and linear algerbra by building my own neural network class.
- best correlation: 0.80

## Evaluation
### Compare to ADP tool
create method to make a create a randomized test draft.  Choose one team to draft based on predicted points per game, all others will draft based on ADP mean and standard deviation. <br>
compare average points per game for ADP teams to predicted team.

### Evaluate Linear Regression

1. create function to combine predictions for all years
2. evaluate linear regression using top 5 'mean' attributes
3. evaluate linear regression using itterativly selected attributes

**Results**

1. using top 5 'mean' attributes
    1. 2% more points per game compared to ADP
    2. 46% chance of underperforming ADP
    3. statistically significant
2. using itterativly selected attributes
    1. 4% more points per game compared to ADP
    2. 43% chance of underperforming ADP
    3. statistically significant
  
### Evaluate Random Forest

1. create function to create average predictions for rf model for each year
2. evaluate against adp

**Results**

1. 4% more points per game over ADP
2. 43% chance of underperforming ADP
2. statistically significant


### Evaluate Neural Network

1. create function to create average predictions for NN model for each year
2. use models selected during model development
    1. use 30 trials of a network where layer 1 has 10 neurons and all attributes are available to find best attributes
    2. build model with 500 iterations
    3. use 10 best attributes build a network with and 5 neurons in layer 1
    4. use 12 best attributes build a network with and 4 neurons in layer 1
3. evaluate against adp

**Results**

1. 10 attribute model
    1. 7% more points per game over ADP
    2. 38% chance of underperforming ADP
    2. statistically significant
2. 12 attribute model
    1. 8% more points per game over ADP
    2. 36% chance of underperforming ADP
    2. statistically significant
  
### Conclusion
| Model | Pct Points Over ADP | Pct Under ADP | Significant |
|--------------------------------|--------|--------|--------|
| Linear Regression 'means' | 2% | 46% | yes |
| Linear Regresson 'itterative'| 4% | 43% | yes |
| Random Forest | 4% | 43% | yes |
| Neural Network 10 attribute | 7% | 38% | yes |
| **Neural Network 12 attribute** | **8%** | **36%** | **yes** |

### Display Predictions for 2024
