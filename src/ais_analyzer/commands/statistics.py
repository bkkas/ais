import pandas as pd
from .statistics_data.mmsi_country import mmsi_map

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
        # Outputs each country represented from mmsi, and how many rows the dataset includes from that
        # mmsi = pd.read_excel("statistics_data/mmsikos1.xlsx")
        mmsi = pd.DataFrame(mmsi_map.items(), columns=["Digit", "Allocated to"])
        mmsi = mmsi.rename(columns={'Allocated to' : 'country'})

        unique_ais = pd.DataFrame({"nr_unique_ships" : input_df["mmsi"].unique()})
        unique_ais["Digit"] = unique_ais["nr_unique_ships"].astype("str").str[:-6].astype("int")

        ais_digits = pd.DataFrame({'Digit': input_df["mmsi"].astype("str").str[:-6].astype("int")})
        ais_counts = pd.DataFrame(data = ais_digits.value_counts(), columns = ["nr_rows"]).reset_index()

        # del ais
        try:
            ships_country = pd.merge(mmsi, unique_ais, on='Digit')
        except:
            print("mmsi does not point to country")

        del unique_ais
        del ais_digits

        nr_of_ships_by_country = pd.DataFrame(data = ships_country.groupby('country')['nr_unique_ships'].nunique().reset_index())

        del ships_country

        mmsi_count = ais_counts.merge(mmsi, on='Digit')
        nr_of_rows_by_countries = mmsi_count.groupby(mmsi_count['country']).aggregate(sum).reset_index().drop(columns = "Digit")

        del mmsi
        del mmsi_count

        data = nr_of_ships_by_country.merge(nr_of_rows_by_countries, on="country")

        del nr_of_ships_by_country
        del nr_of_rows_by_countries

        return data
    elif args['mmsi']:
        # outputs a Dataframe of information about each unique ship, based on mmsi
        occurence = input_df.sort_values(by=["timestamp_utc"]).loc[: ,["mmsi", "timestamp_utc"]]

        first_oc = occurence.groupby(by=["mmsi"]).first().reset_index()
        first_oc["last_oc"] = occurence.groupby(by=["mmsi"]).last().reset_index().loc[:,"timestamp_utc"]

        del occurence


        first_oc = first_oc.rename(columns={"timestamp_utc" : "first_oc"})

        df_lenght = pd.DataFrame(input_df.loc[: ,["mmsi","length"]].groupby(by=["mmsi"]).first().reset_index())
        count_rows = input_df["mmsi"].value_counts().reset_index()
        count_rows.columns = ["mmsi", "count_rows"]
        df_lenght = df_lenght.merge(count_rows, on="mmsi")

        del count_rows

        result = first_oc.merge(df_lenght, how="inner")

        del df_lenght
        del first_oc

        return result

    elif args['complete']:
        # outputs one row with information about the whole dataset
        one_line = pd.DataFrame(input_df["mmsi"].unique()).count()
        one_line = pd.DataFrame(one_line, columns=["mmsi_count"])

        unique_ais = input_df.groupby(by=["mmsi"]).first().reset_index()

        one_line["avg_length"] = unique_ais.length.mean()
        one_line["max_length"] = unique_ais.length.max()
        one_line["min_length"] = unique_ais.length.min()

        one_line["start_date"] = input_df.timestamp_utc.sort_values().min()
        one_line["end_date"] = input_df.timestamp_utc.sort_values().max()

        one_line["median_lon"] = input_df.lon.median()
        one_line["median_lat"] = input_df.lat.median()

        return one_line

    else:
        stat_df = input_df.describe()
        return stat_df
