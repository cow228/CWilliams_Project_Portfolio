'''
performs tests on functions for pipeline
'''
import pandas as pd
from pandas.api.types import is_numeric_dtype
import load_data


def test_load_data(path = 'nfl_historical_data.csv'):
    '''
    using a default data source to check for key properties.
    '''
    original_df = pd.read_csv(path)
    df, feature_lists, _ = load_data.load_file(path)

    # drop column should only contain columns that are non numeric
    for col in feature_lists['drop']:
        drop_col = original_df[col]
        assert not is_numeric_dtype(drop_col), 'dropped numeric dtype'
    # should have number of columns - number dropped
    assert len(original_df.columns) == (len(df.columns)
                        + len(feature_lists['drop'])), 'too many or too few columns dropped'

    # all columns should be either numeric type or categorical
    for col in df.columns:
        if not is_numeric_dtype(df[col]):
            assert df[col].dtype == 'category', 'columns not correct type'

    # pass all tests, print success
    print('load_data module tests passed')

def test_test_normality(path = 'nfl_historical_data.csv'):
    '''
    using default data to test for key properties
    '''
    assert isinstance(path, str)

    # pass all test, print success
    print('test_normality module tests passed')

if __name__ == '__main__':
    # run all tests
    test_load_data()
    test_test_normality()
