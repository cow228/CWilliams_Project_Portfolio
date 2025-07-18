'''
perform preprocessing steps:
1) check for nulls
2) test for normality
3) transform non normal data
4) handle outliers
'''
import load_data
import test_normality
import handle_outliers

def preprocess(df,num_features):
    '''
    combine preprocessing, normality, outliers, nulls
    :param df [dataframe] - data to preprocess
    :param feature_lists
    :param feature types 
    :return [dataframe] - preprocessed data
    '''
    # find nulls
    handle_outliers.analyze_null_values(df, False)

    # test normality
    nn_df = test_normality.normal_test_plot(df, columns=num_features, 
                                            output=False, plot=False)
    df = test_normality.normalitiy_transform(nn_df, df)
    test_normality.normal_test_plot(df, columns=num_features, output=True, plot=True)

    # handle outliers
    df = handle_outliers.handle_outliers(df, columns=num_features)

    return df

if __name__ == '__main__':
    import argparse

    # input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path to CSV')
    args = parser.parse_args()

    # load data
    data, feature_lists, feature_types = load_data.load_file(args.path)

    # preprocess
    data = preprocess(data,feature_lists['numeric'])

    # output
    new_name = args.path + '_procd'
    data.to_csv(new_name, index=False)