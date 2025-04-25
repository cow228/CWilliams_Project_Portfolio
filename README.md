# List of Projects
This repository contains projects that I have completed independently in Python. 
Each project has a brief write-up here and a more detailed "Overview" page in its respective folder

## Fantasy Football Predictor
Build Model to predict fantasy football points per game for wide recievers. <br>
Build function to import data in usable format. <br>
Explore data. <br>
Model with linear regression, random forest and neural network. <br>
Compare predictions to randomized trials of drafts based on average draft position.

## Data Mining Pipeline
Code to automatically handle most phases of data mining <br>
1) Preprocessing
  - Identify null values
  - Handle outliers by capping (either std or iqr) or removing.  Identifies percent of each feature affected.
  - Testing feature normality then applying appropriate normality corrections.  Identifies features that are still non-normal
2) Feature selection
  - Identifies meaningful polynomial features using lasso regression and adds them to the candidate feature set
  - Calcualtes appropriate correlation metrics for each feature compared to target based on data type (chooses from: mutual information, chi squared, ANOVA, distance correlation, pearson correlation, and lift)
  - Performs singular value decomposition and adds summed feature weights to feature selection consideration
  - Builds decision tree and adds feature weights to feature selection consideration
3) Model selection
  - Iterates through models based on target and features types, starting from simple models.  Considers: Naive Bayes, linear Regressions, Logistic Regressions, Support Vector Machines, Random Forests, Nueral Networks
  - For Each Model normalizes data then performs grid search
  - Grid search starts with few, far apart parameters, if a significant difference in accuracy is observed grid search repeats with more narrow values centered on best parameters from the inital search.
  - Displays precision recall curve for classifiers
  - allows input of data specific prediction success metrics

## Quantifying NFL Head Coach Quality
Data minning school project with poster presentation.  <br>
Goal of project was to identify ways to quantify the quality of NFL head coaches.  The method ultimatley selected was to create predictors for head coach contract renewal as a stand in for "good" coaches.  The features of the model most predictive of contract renewal can be considered viable quantifiers of coach quality. <br>
The goal is to use these predictors for further analysis going forward

## Poker Bot
Create a tool that will provide insight into poker strategy and analytics while playing online.
Determining the best action at any given game state in poker requires a mixture of memorization and quick mental math. This program aims to reduce the need for these difficult methods and simplifies the decision process


