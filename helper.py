import numpy as np
import plotly.express as px


def medal_tally(df):

    medal_tally = df.drop_duplicates(subset=['Team', 'NOC' , 'Games', 'Year', 'City', 'Sport','Event','Medal'])

    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver' ,'Bronze']].sort_values('Gold',ascending=False) 

    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

##########################################################################################################
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

    
######################################################################################################        
def country_years(df):

    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'overall')

    country = np.unique(df['region'].dropna().unique()).tolist()
    country.sort()
    country.insert(0,'overall')

    return years, country
###########################################################################################################
def data_over_time(df,col):
    country_over_time = df.drop_duplicates(['Year',col])['Year'].value_counts().reset_index()
    country_over_time.rename(columns={'count': col ,'Year': 'No of years' },inplace = True)

    return country_over_time

#########################################################################################################
def most_successful(df, sport):
    # Remove rows without a medal
    temp_df = df.dropna(subset=['Medal'])

    # Filter by specific sport if not 'Overall'
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    # Count medals per athlete and get top 15
    top_athletes = temp_df['Name'].value_counts().head(20).reset_index()
    top_athletes.columns = ['Name', 'Medals']  # Rename columns

    # Merge with main dataframe to get sport and region info
    top_athletes = top_athletes.merge(df, on='Name', how='left')[
        ['Name', 'Medals', 'Sport', 'region']
    ].drop_duplicates('Name')  # Avoid duplicate rows

    return top_athletes

##########################################################################################################
def year_wise_medal(df,country):
    new_df = df.dropna(subset=['Medal'])
    new_df.drop_duplicates(subset=['Team', 'NOC' , 'Games', 'Year', 'City', 'Sport','Event','Medal'],inplace = True)

    reg_df = new_df[new_df['region']== country]
    final_df = reg_df.groupby('Year').count()['Medal'].reset_index()

    return final_df
###############################################################################################################
def best_sport_country(df,country):
    new_df = df.dropna(subset=['Medal'])
    new_df.drop_duplicates(subset=['Team', 'NOC' , 'Games', 'Year', 'City', 'Sport','Event','Medal'],inplace = True)

    reg_df = new_df[new_df['region']== country]

    pt = reg_df.pivot_table(index = 'Sport' , columns = 'Year', values = 'Medal', aggfunc = 'count' ).fillna(0)
    return pt
##################################################################################################################
def most_successful_countrywise(df, country):
    # Remove rows without a medal
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    # Count medals per athlete and get top 15
    top_athletes = temp_df['Name'].value_counts().head(15).reset_index()
    top_athletes.columns = ['Name', 'Medals']  # Rename columns

    # Merge with main dataframe to get sport and region info
    top_athletes = top_athletes.merge(df, on='Name', how='left')[
        ['Name', 'Medals', 'Sport']
    ].drop_duplicates('Name')  

    return top_athletes

#####################################################################################
def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

#######################################################################################
def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final