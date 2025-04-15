import numpy as np



def medal_tally(df):

    medal_tally = df.drop_duplicates(subset=['Team', 'NOC' , 'Games', 'Year', 'City', 'Sport','Event','Medal'])

    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver' ,'Bronze']].sort_values('Gold',ascending=False) 

    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

def fetch_medal_tally(df,years,country):
    medal_df  = df.drop_duplicates(subset=['Team', 'NOC' , 'Games', 'Year', 'City', 'Sport','Event','Medal'])
    
    flag = False
    if years == 'overall' and country == 'overall':
        new_df = medal_df
        
    if years == 'overall' and country != 'overall':
        new_df = medal_df[medal_df['region'] == country]
        flag = True
        
        
    if years != 'overall' and country == 'overall':
        new_df = medal_df[medal_df['Year'] == int(years)]
        
    if years != 'overall' and country != 'overall':
        new_df = medal_df[(medal_df['Year'] == int(years)) & (medal_df['region'] == country)]
                # medal_df[(medal_df['year'] == int(years)) & (medal_df['region'] == country)]

    if flag:
        medal = new_df.groupby('Year').sum()[['Gold', 'Silver' ,'Bronze']].sort_values('Year',ascending=True)
    else:
         medal = new_df.groupby('region').sum()[['Gold', 'Silver' ,'Bronze']].sort_values('Gold',ascending=False)
        
    medal['total'] = medal['Gold'] + medal['Silver'] + medal['Bronze']

    return medal

    
        
def country_years(df):

    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'overall')

    country = np.unique(df['region'].dropna().unique()).tolist()
    country.sort()
    country.insert(0,'overall')

    return years, country

def data_over_time(df,col):
    country_over_time = df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index()
    country_over_time.rename(columns={'Year': 'col' ,'count': 'Edition'},inplace = True)

    return country_over_time
