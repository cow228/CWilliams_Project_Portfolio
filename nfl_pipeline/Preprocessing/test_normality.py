'''
test whether each feature is normally distributed.  Plot results of non-normal features
'''
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

def normal_test_plot(df, columns=None, output=False, plot=False, stat_name=None):
    """
    Performs normality tests on all numeric features.
    - Uses Shapiro-Wilk test if there are fewer than 5000 rows
    - Uses D'Agostino-Pearson test otherwise
    Also calculates skewness and kurtosis for each feature.
    
    :param df [dataframe] - input dataframe
    :param columns [list[str]] - list of numeric columns
    :param output [bool] - selection to output result table
    :param plot [bool] - slection to output result plot
    """
    # Initialize lists to store results
    features = []
    test_results = []
    skewness = []
    kurtosis_values = []
    test_name = []
    p_values = []
    # Determine which test to use based on sample size
    if len(df) < 5000:
        test_type = "Shapiro-Wilk"
        if output:
            print(f"Testing Normality with Shapiro-Wilk test (n={len(df)} < 5000)")
    else:
        test_type = "D'Agostino-Pearson"
        if output:
            print(f"Testing Normality with D'Agostino-Pearson test (n={len(df)} >= 5000)")
    # Perform tests for each numeric feature
    for col in columns:
        # Get data without NaN values
        data = df[col].dropna()
        # Calculate skewness and kurtosis
        skew = stats.skew(data)
        kurt = stats.kurtosis(data)
        # Perform normality test
        if test_type == "Shapiro-Wilk":
            # Shapiro-Wilk test
            _, p = stats.shapiro(data)
        else:
            # D'Agostino-Pearson test
            _, p = stats.normaltest(data)
        # Store results
        features.append(col)
        test_results.append("Normal" if p > 0.05 else "Not Normal")
        skewness.append(skew)
        kurtosis_values.append(kurt)
        test_name.append(test_type)
        p_values.append(p)
    # Create DataFrame with results
    normality_df = pd.DataFrame({
        'Feature': features,
        'Test': test_name,
        'Result': test_results,
        'p-value': p_values,
        'Skewness': skewness,
        'Kurtosis': kurtosis_values
    })
    # Display results
    non_normal_df = normality_df[normality_df['Result']=='Not Normal'].copy()

    if plot:
        n_features = len(non_normal_df)
        if n_features > 0:
            # Calculate number of rows and columns for subplots
            n_cols = min(3, n_features)
            n_rows = (n_features + n_cols - 1) // n_cols
            # Create subplots
            _, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5 * n_rows))
            axes = axes.flatten() if n_features > 1 else [axes]
            # Plot each non-normal feature in its own subplot
            for i, (_, row) in enumerate(non_normal_df.iterrows()):
                feature = row['Feature']
                sns.histplot(df[feature].dropna(), bins=30, kde=True, ax=axes[i])
                axes[i].set_title(f'{feature}')
                axes[i].set_xlabel('Value')
                axes[i].set_ylabel('Frequency')
            # Hide any unused subplots
            for j in range(i+1, len(axes)):
                axes[j].set_visible(False)
            plt.tight_layout()
            file_path = os.path.join('preproc_files', stat_name+'_non_norm.png')
            plt.savefig(file_path)
            
        else:
            print("No non-normal features to plot.")

    if output:
        print("\nNormality Test Results:")
        print(non_normal_df)

    return non_normal_df

def normalitiy_transform(non_normal_df, data_df, method='auto'):
    """
    Apply appropriate transformations to normalize features identified as non-normal.
    : 
    """   
    # Track transformations applied
    transformations = {}
    
    # Process each non-normal feature
    for _, row in non_normal_df.iterrows():
        feature = row['Feature']
        skewness = row['Skewness']
            
        # Get data without NaN values
        data = data_df[feature].dropna()
        
        # Choose transformation method
        if method == 'auto':
            # Select transformation based on skewness
            if abs(skewness) > 1:
                if skewness > 0:
                    transform_method = 'log'
                else:
                    transform_method = 'sqrt'
            else:
                transform_method = 'box-cox' if all(data > 0) else 'yeo-johnson'
        else:
            transform_method = method
            
        # Apply transformation
        try:
            if transform_method == 'log':
                # Handle negative values if present
                if data.min() <= 0:
                    min_val = data.min()
                    shift = abs(min_val) + 1 if min_val <= 0 else 0
                    data = np.log(data + shift)
                    transformations[feature] = f"log(x + {shift})"
                else:
                    data = np.log(data)
                    transformations[feature] = "log(x)"
                    
            elif transform_method == 'sqrt':
                # Handle negative values if present
                if data.min() < 0:
                    min_val = data.min()
                    shift = abs(min_val) + 1
                    data = np.sqrt(data + shift)
                    transformations[feature] = f"sqrt(x + {shift})"
                else:
                    data = np.sqrt(data)
                    transformations[feature] = "sqrt(x)"
                    
            elif transform_method == 'box-cox':
                # Box-Cox requires all positive values
                if data.min() <= 0:
                    min_val = data.min()
                    shift = abs(min_val) + 1
                    transformed, lambda_val = stats.boxcox(data + shift)
                    data = transformed
                    transformations[feature] = f"box-cox(x + {shift}, λ={lambda_val:.4f})"
                else:
                    transformed, lambda_val = stats.boxcox(data)
                    # Create a temporary series with the right index
                    temp_series = pd.Series(index=data.index, dtype='float64')
                    # Use .loc to properly set values and avoid SettingWithCopyWarning
                    temp_series.loc[data.index] = transformed
                    data = temp_series
                    transformations[feature] = f"box-cox(x, λ={lambda_val:.4f})"
                    
            elif transform_method == 'yeo-johnson':
                # Yeo-Johnson works with negative values
                transformed, lambda_val = stats.yeojohnson(data)
                # Create a temporary series with the right index
                temp_series = pd.Series(index=data.index, dtype='float64')
                # Use .loc to properly set values and avoid SettingWithCopyWarning
                temp_series.loc[data.index] = transformed
                data = temp_series
                transformations[feature] = f"yeo-johnson(x, λ={lambda_val:.4f})"
        
        except Exception as e:
            print(f"Error transforming {feature}: {str(e)}")
            continue
    
        # change data_col with normal value
        data_df[feature] = data

    print(f"Applied normality correction to {len(non_normal_df)} features")
    return data_df
