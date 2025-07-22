'''
perform preprocessing steps:
1) check for nulls
2) test for normality
3) transform non normal data
4) handle outliers
'''
import os
import load_data
import test_normality
import handle_outliers

def preprocess(df,num_features, stat_name):
    '''
    combine preprocessing, normality, outliers, nulls
    :param df [dataframe] - data to preprocess
    :param feature_lists
    :param feature types 
    :return [dataframe] - preprocessed data
    '''
    # find nulls
    handle_outliers.analyze_null_values(df.copy(), stat_name, False)

    # test normality
    nn_df = test_normality.normal_test_plot(df.copy(), columns=num_features,
                                            output=False, plot=False)
    num_df = test_normality.normalitiy_transform(nn_df, df.copy())
    test_normality.normal_test_plot(num_df, columns=num_features, output=True, plot=True, stat_name=stat_name)

    # handle outliers
    num_df = handle_outliers.handle_outliers(num_df, columns=num_features)

    # merge adjusted numeric columns with original
    for col in num_df.columns:
        df[col] = num_df[col]

    return df

if __name__ == '__main__':

    for stat in ['rec', 'rush', 'pass']:
        # target id
        target = 'ffpts_target'
        
        # load data
        file_name = stat + '_stats.csv'
        # file_path = os.path.join('..', 'files', file_name) #only works when executing from Preprocessing directory
        file_path = os.path.join('import_files', file_name)
        print(file_path)
        data, feature_lists, feature_types = load_data.load_file(file_path)

        # seperate target
        features_data = data.drop(columns=[target])
        if target in feature_lists['numeric']:
            feature_lists['numeric'].remove(target)
        target_data = data[target]

        # preprocess
        features_data = preprocess(features_data,feature_lists['numeric'], stat)

        # recombine
        features_data['target'] = target_data

        # output
        file_name = stat + '_proc.csv'
        file_path = os.path.join('preproc_files', file_name)
        features_data.to_csv(file_path, index=False)