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
<br>
Example output from the preprocessor: <br>
![Preprocessing](/Pipeline/images/Preprocessing_Output.png)
