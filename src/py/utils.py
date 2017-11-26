import errno
import os
import tushare


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def get_df_index_by_col_value(df, key, value):
    return df.loc[df[key]==value].index