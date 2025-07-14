'''
import data file and perform preprocessing steps:
1) check for nulls
2) test for normality
3) transform non normal data
4) handle outliers
'''
import load_data
import test_normality

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path to CSV')
    args = parser.parse_args()

    df, feature_lists, feature_types = load_data.load_file(args.path)
    test_normality.normal_test_plot(df, columns=feature_lists['numeric'], output=True, plot=True)
