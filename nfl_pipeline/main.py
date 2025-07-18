'''
Find feature corelations to target
'''
import feature_imp_cl
import Preprocessing.load_data as load_data
import subprocess

if __name__ == '__main__':
    import argparse

    # input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path to CSV')
    parser.add_argument('target', help='column name of target feature')
    args = parser.parse_args()

    # load data
    data, feature_lists, feature_types = load_data.load_file(args.path)
    
    # feature correlation
    data_fts = feature_imp_cl.Data_features(data, args.target)
    data_fts.plot_target_correlation()
    