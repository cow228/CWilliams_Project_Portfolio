'''
deal with outliers in dataframe based on several options
also deals with null values
'''
import pandas as pd
import numpy as np

def handle_outliers(df, method='cap', threshold=2, drop=False, columns=None):
    """
    handel outliers by applying transformations.

    :param df [dataframe] - data to deal with
    :param method [str] - how to deal with 
    :param thresholds [int] - std's to cutoff 
    :param drop [bool] - if dropping outliers or not
    :param columns [list] - numeric columns
    :return [dataframe] - data with outliers handled
    """
    # Get numeric columns if not specified
    if columns is None:
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    else:
        numeric_cols = [col for col in columns if col in df.columns and np.issubdtype(df[col].dtype, np.number)]
    # Track outliers found
    outlier_counts = {}
    for col in numeric_cols:
        # Skip columns with all NaN values
        if df[col].isna().all():
            continue
        # Get data without NaN values
        data = df[col].dropna()
        if method == 'cap':
            # Calculate mean and standard deviation
            mean = data.mean()
            std = data.std()
            # Define lower and upper bounds
            lower_bound = mean - threshold * std
            upper_bound = mean + threshold * std
            # Identify outliers
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)].index
        elif method == 'iqr':
            # Calculate Q1, Q3 and IQR
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            # Define lower and upper bounds
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            # Identify outliers
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)].index
        else:
            raise ValueError("Method must be 'cap' or 'iqr'")
        # Store count of outliers
        outlier_counts[col] = len(outliers)
        if len(outliers) > 0:
            if drop:
                # Drop outliers
                df = df.drop(outliers)
            else:
                # Cap outliers
                df.loc[df[col] < lower_bound, col] = lower_bound
                df.loc[df[col] > upper_bound, col] = upper_bound
    # Display summary of outliers handled
    print(f"\nOutliers handled using {method} method with threshold={threshold}")
    outlier_df = pd.DataFrame({
        'Feature': list(outlier_counts.keys()),
        'Outliers Count': list(outlier_counts.values())
    })
    # Sort by count in descending order
    outlier_df = outlier_df.sort_values('Outliers Count', ascending=False)    
    print(f"{outlier_df['Outliers Count'].sum()} Outliers were handled")
    print(f"greatest affected feature: {outlier_df.iloc[0,0]}, {round(outlier_df.iloc[0,1]/len(df)*100)}% affected\n")
    return df

def analyze_null_values(df, silent=True):
    """
    Prints out how many null values per feature and what percent of rows have a null feature.
    
    param: df [dataframe] - input data
    param: siletn [bool] - whether to print results
    """
    # Calculate null values per feature
    null_counts = df.isnull().sum()
    # Calculate percentage of rows with null values per feature
    null_percentage = (null_counts / len(df)) * 100
    # Combine the information
    null_info = pd.DataFrame({
        'Null Count': null_counts,
        'Null Percentage': null_percentage
    })
    # Print the results
    if not silent:
        print("Null Values Analysis:")
    # Filter for features with null values and sort in descending order
    null_features = null_info[null_info['Null Count'] > 0].sort_values('Null Count', ascending=False)
    if not silent:
        if null_features.empty:
            print("No columns have null values.")
        else:
            print(null_features)
    # Calculate overall percentage of rows with at least one null value
    rows_with_nulls = df.isnull().any(axis=1).sum()
    percent_rows_with_nulls = (rows_with_nulls / len(df)) * 100
    if not silent:
        print(f"\nTotal rows with at least one null value: {rows_with_nulls} ({percent_rows_with_nulls:.2f}%)")
    # Print rows with null values if any exist
    if rows_with_nulls > 0:
        if not silent:
            print("\nRows with null values:")
        rows_with_null_values = df[df.isnull().any(axis=1)]
        if not silent:
            rows_with_null_values.to_csv('null_values.csv')
    else:
        if not silent:
            print("\nNo rows contain null values.")
    if null_counts.sum() == 0:
        print("No null values found")
