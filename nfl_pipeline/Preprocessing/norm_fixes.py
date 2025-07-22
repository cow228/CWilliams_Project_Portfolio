"""
manual programed fixes for non normal data
"""
import pandas as pd

def binomize (df, col):
    """
    take columns and turn into two categories at median
    """
    median_value = df[col].median()
    df[col] = ((df[col] > median_value).astype(int)).astype('category')
    return df

def deciles (df, col):
    """
    converts into deciles
    """
    df[col] = (pd.qcut(df[col], q=10, labels=False) + 1).astype('category')
    return df

def kill (df, col):
    '''
    removes column
    '''
    df.drop(columns=[col], inplace=True)
    return df

def cutoff(df, col, cutoff_point, high_low='low'):
    """
    cuts off values at a certain threshold
    """
    if high_low == 'low':
        df.loc[df[col]<cutoff_point,col] = cutoff_point
    elif high_low == 'high':
        df.loc[df[col]>cutoff_point,col] = cutoff_point
    else: 
        print('error during cutoff: high/low not specified')
    return df

def exec_fix_list(df):
    """
    apply list of methods to given df and return it
    """
    fix_list = [
        [kill,'passing_drop_pct'],
        [binomize,'offense_pct'],
        [binomize,'draft_pos_decay'],
        [binomize,'fpts_gained'],
        [binomize,'fpts_lost'],
        [cutoff,['coach_td_prob', 0.3]],
        [cutoff,['coach_first_down', 14]],
        [cutoff,['coach_3d_pct', 0.25]],
        [kill,'receiving_drop_pct'],
        [kill,'draft_number']
    ]

    for fix in fix_list:
        fix_fn = fix[0]
        if isinstance(fix[1],list):
            param1 = fix[1][0]
            param2 = fix[1][1]
            if param1 in df.columns:
                df = fix_fn(df, param1, param2)
        else:
            param1 = fix[1]
            if param1 in df.columns:
                df = fix_fn(df, param1)

    return df

if __name__ == '__main__':
    # pass fixes
    df = pd.read_csv('import_files/pass_stats.csv')
    df = exec_fix_list(df)
    df.to_csv('import_files/pass_stats.csv',index=False)
    # rec fixes
    df = pd.read_csv('import_files/rec_stats.csv')
    df = exec_fix_list(df)
    df.to_csv('import_files/rec_stats.csv',index=False)
    # rush fixes
    df = pd.read_csv('import_files/rush_stats.csv')
    df = exec_fix_list(df)
    df.to_csv('import_files/rush_stats.csv',index=False)






