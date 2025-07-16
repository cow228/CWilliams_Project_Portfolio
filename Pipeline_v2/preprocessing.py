'''
code to combine all pre-processing steps
'''
import load_data
import test_normality

def preprocess(df,feature_lists, feature_types):
    '''
    combine preprocessing, normality, outliers, nulls
    :param df [dataframe] - data to preprocess
    :param feature_lists
    :param feature types 
    :return [dataframe] - preprocessed data
    '''
    # test normality
    nn_df = test_normality.normal_test_plot(df, columns=feature_lists['numeric'], output=False, plot=False)
    df = test_normality.normalitiy_transform(nn_df, df)
    test_normality.normal_test_plot(df, columns=feature_lists['numeric'], output=True, plot=True)

if __name__ == '__main__':
    import argparse

    # input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path to CSV')
    args = parser.parse_args()

    # load data
    df, feature_lists, feature_types = load_data.load_file(args.path)