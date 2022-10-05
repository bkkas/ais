import pandas as pd


def statistics(input_df: pd.DataFrame, params: dict) -> pd.DataFrame:
    """
    Arguments:
        - df : tabular data (dataframe)
        - params : a dict containing parameters [full]
        - return: a dataframe containing statistical analysis of input data
    """

    # Handling the input parameters
    if params['full']:
        return input_df.describe(include='all')
    return input_df.describe()
