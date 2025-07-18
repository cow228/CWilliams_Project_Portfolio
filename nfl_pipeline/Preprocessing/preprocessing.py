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
    handle_outliers.analyze_null_values(df, stat_name, False)

    # test normality
    nn_df = test_normality.normal_test_plot(df, columns=num_features, 
                                            output=False, plot=False)
    df = test_normality.normalitiy_transform(nn_df, df)
    test_normality.normal_test_plot(df, columns=num_features, output=True, plot=True, stat_name=stat_name)

    # handle outliers
    df = handle_outliers.handle_outliers(df, columns=num_features)

    return df

if __name__ == '__main__':

    for stat in ['rec', 'rush', 'pass']:
        # load data
        file_name = stat + '_stats.csv'
        # file_path = os.path.join('..', 'files', file_name) #only works when executing from Preprocessing directory
        file_path = os.path.join('files', file_name)
        # abs_path = file_path.resolve()
        print(file_path)
        data, feature_lists, feature_types = load_data.load_file(file_path)

        # preprocess
        data = preprocess(data,feature_lists['numeric'], stat)

        # output
        file_name = stat + '_proc.csv'
        file_path = os.path.join('files', file_name)
        data.to_csv(file_path, index=False)