import pandas as pd


def statistics(input_df: pd.DataFrame, args) -> pd.DataFrame:
    """
    Arguments:
        - df : tabular data (dataframe)
        - args : a dict containing arguments from the CLI [full]
        - return: a dataframe containing statistical analysis of input data
    """

    # Handling the input parameters
    if args['full']:
        stat_df = input_df.describe(include='all')
        return stat_df
    else:
        stat_df = input_df.describe()
        return stat_df
