'''
Find feature corelations to target
'''
import os
import feature_imp_cl
import pandas as pd

if __name__ == '__main__':
    import argparse

    # input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--features', help='number of features to show', default=15, type=int)
    args = parser.parse_args()
    
    # feature correlation
    for stat in ['rec', 'rush', 'pass']:
        # load data
        file_name = stat + '_proc.csv'
        path = file_path = os.path.join('preproc_files', file_name)
        data = pd.read_csv(path)
        # analyse data
        data_fts = feature_imp_cl.Data_features(data, 'target', stat)
        data_fts.plot_target_correlation(args.features)
        print('done with', stat, 'features')
    