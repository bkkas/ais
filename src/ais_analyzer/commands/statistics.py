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
    elif args['country']:
        mmsi = pd.read_excel("statistics_data/mmsikos.xlsx")
        digits = pd.DataFrame({'numbs': input_df["mmsi"].astype("str").str[:-6].astype("int")})

        counts = pd.DataFrame(data = digits.value_counts()).reset_index()
        counts.columns = ["Digit", "Count"]
        mmsi_count = pd.merge(mmsi, counts, on='Digit')

        nr_of_rows_by_countries = mmsi_count.groupby(mmsi_count['Allocated to']).aggregate(sum).reset_index().drop(columns = "Digit")
        return nr_of_rows_by_countries
     elif args['']:

    else:
        stat_df = input_df.describe()
        return stat_df
