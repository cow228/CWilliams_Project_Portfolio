'''
Find feature corelations to target
'''
import feature_imp_cl
import load_data
import subprocess

if __name__ == '__main__':
    import argparse

    # input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path to CSV')
    parser.add_argument('target', help='column name of target feature')
    parser.add_argument('process', help='t/f if you want to preprocess the data')
    args = parser.parse_args()

    # perform preprocessing if necessary
    path = args.path
    if args.process:
        subprocess.run(['python','preprocessing.py '+args.path])
        path = args.path+'_procd'

    # load data
    data, feature_lists, feature_types = load_data.load_file(path)
    
    # feature correlation
    data_fts = feature_imp_cl.Data_features(data, args.target)
    data_fts.plot_target_correlation()
    