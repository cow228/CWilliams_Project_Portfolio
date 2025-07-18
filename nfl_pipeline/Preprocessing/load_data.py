'''
import data file and extract feature types.
'''
import pandas as pd
from pandas.api.types import is_numeric_dtype

def check_feature_type(column):
    '''
    check feature types.

    :param column [pandas series] - column of dataframe
    :return datatype [string] - column data type
    '''
    # calculate values to test if non categorical types should be converted
    classes = column.nunique()
    avg_class_mem = len(column)/classes

    # check data type
    # if the data can reasonably be considered categorical convert it
    # reasonable if it has on average 3 members per class and less than 25 classes
    if (avg_class_mem>3) and (classes<25):
        datatype = 'categorical'
        column = column.astype('category')
        if classes == 2:
            datatype = 'binary'
    elif is_numeric_dtype(column):
        datatype = 'numeric'
    # if it isn't one of these acceptable types drop it
    else:
        datatype = 'drop'

    return datatype, column

def asses_df_features(dataframe):
    '''
    check each column of a dataframe and output feature type lists. remove unacceptable types.

    :param dataframe [dataframe] - df to check
    :return dataframe [dataframe] - updated df
    :return feature_types [dict] - each column with feature type
    :return feature_lists [dict] - lists labeled for each type: numeric, categorical, binary
    '''
    # prepare output lists
    feature_types = {}
    feature_lists = {'numeric': [], 'categorical': [], 'binary': [], 'drop': {}}

    for col in dataframe.columns:
        datatype, new_col = check_feature_type(dataframe[col])
        # replace column if needed
        dataframe[col] = new_col
        # drop unacceptable columns
        if datatype == 'drop':
            feature_lists['drop'][col] = dataframe[col].dtype
            dataframe.drop(columns=[col], inplace=True)
            continue
        # update lists
        feature_lists[datatype].append(col)
        feature_types[col] = datatype

    return dataframe, feature_lists, feature_types

def load_file(path, drops=False):
    '''
    load file based on input path and define feature types.

    :param path [string] - file path
    :return [dataframe]
    :return [dict] - dict of lists containing feature types
    :return [dict] - list of features organized by type (included droped features)
    '''
    # load dataframe and unify column names
    print(path)
    data = pd.read_csv(path)
    data.columns = data.columns.str.replace(' ', '_')

    # drop columns if needed
    if drops:
        data.drop(columns=drops, inplace=True)

    # check feature types and drop unacceptable ones
    return asses_df_features(data)
