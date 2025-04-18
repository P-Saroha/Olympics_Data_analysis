import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
from plotly.figure_factory import create_distplot

###########################################################################################################
df = preprocessor.preprocessor()

st.sidebar.header('Olympics Analysis')
#############################################################################################################
list = st.sidebar.radio(
    "Select an Option",
    ("Medal Tally","Overall Analysis","Country wise Analysis","Athletes wise Analysis") 
)

# st.dataframe(df)
#############################################################################################################
if list == 'Medal Tally':
    st.sidebar.header("Medal Tally") 
    years,country = helper.country_years(df)
    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)


    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)

    if selected_year == 'overall' and selected_country == 'overall':
        st.title('OverAll Tally')
    
    if selected_year == 'overall' and selected_country != 'overall':
        st.title(selected_country + " Overall Performance")

    if selected_year != 'overall' and selected_country == 'overall':
        st.title('Medal Tally in ' + str(selected_year)+ " Olympics")

    if selected_year != 'overall' and selected_country != 'overall':
        st.title(selected_country + " Performance in " + str(selected_year) + " Olympic")

    st.dataframe(medal_tally)

############################################################################################################
if list == "Overall Analysis":
    editions = df['Year'].nunique() - 1
    city = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes_name = df['Name'].nunique()
    nations = df['region'].nunique()


    st.title("Top Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Total Olympics Held (Till 2016)")
        st.title(editions)

    with col2:
        st.header("Host Cities")
        st.title(city)

    with col3:
        st.header("Different Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header("Unique Events")
        st.title(events)

    with col2:
        st.header("Participating Athletes")
        st.title(athletes_name)

    with col3:
        st.header("Participating Countries")
        st.title(nations)

    nation_over_time = helper.data_over_time(df,'region')
    st.title("Number of Participating Country over years in Olympics")
    fig = px.line(nation_over_time, x= 'region', y = 'No of years')
    st.plotly_chart(fig)

    event_over_time = helper.data_over_time(df,'Event')
    st.title("Events over years in Olympics")
    fig = px.line(event_over_time, x= 'Event', y = 'No of years')
    st.plotly_chart(fig)

    Athletes_over_time = helper.data_over_time(df,'Name')
    st.title("Number of Athletes over years in Olympics")
    fig = px.line(Athletes_over_time, x= 'Name', y = 'No of years')
    st.plotly_chart(fig)

    st.title("Number of Events Over Time")

    
    fig ,ax = plt.subplots(figsize=(20, 12))
    x = df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(
        x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),
        annot=True, fmt='d', cmap='YlGnBu', linewidths=0.5, linecolor='gray', cbar_kws={'shrink': 0.8}
    )
    plt.title('Events per Sport by Year')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

############################################################################################################
if list == "Country wise Analysis":

    st.sidebar.title("Country wise Analysis")
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)
    country_medal = helper.year_wise_medal(df,selected_country)

    fig = px.line(country_medal, x = 'Year', y = 'Medal')
    st.title( selected_country + " Medal Tally Over The Years")
    st.plotly_chart(fig)

    pt = helper.best_sport_country(df,selected_country)

    st.title( selected_country + " Strong In The Following Sports")
    fig ,ax = plt.subplots(figsize=(20, 12)) 
    ax = sns.heatmap(pt,annot = True)
    st.pyplot(fig)


    st.title("Top Athletes of "+ selected_country)
    top_at_country = helper.most_successful_countrywise(df,selected_country)
    st.table(top_at_country)

###################################################################################################################
if list == "Athletes wise Analysis":
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age")
    st.plotly_chart(fig)

#############################################################################################################
    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

##################################################################################################
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)

    temp_df = helper.weight_v_height(df, selected_sport)

    fig, ax = plt.subplots()
    ax = sns.scatterplot(data=temp_df, x='Weight', y='Height', hue='Medal', style='Sex', s=60)

    st.pyplot(fig)


    st.title("Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

