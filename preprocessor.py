import pandas as pd
import numpy as np

df_alt = pd.read_csv("athlete_events.csv")
df_reg = pd.read_csv("noc_regions.csv")

def preprocessor():

    global df_alt,df_reg

    ## extracting summer only
    df_alt = df_alt[df_alt["Season"] == 'Summer']

    # Merging data of noc_regions.csv with df_alt
    df = df_alt.merge(df_reg,on='NOC',how='left')

    # droping duplicates value from the data
    df.drop_duplicates(inplace = True)

    ## doing OHE on Medals
    dummies = pd.get_dummies(df['Medal'], dtype=int)

    df = pd.concat([df, dummies], axis=1)

    return df

