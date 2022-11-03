'''
Sprint 4 Project
WebApp to explore chess game data (sourced from Lichess, via Kaggle)
'''

# import libraries
import pandas as pd
import streamlit as st
import plotly_express as px

#load the data into a DataFrame using pandas
games_df = pd.read_csv('./games.csv')
games_df.info()

# drop duplicates
games_df.drop_duplicates(inplace=True)

# add rating_difference column by determining difference between white's and black's ratings
games_df['rating_difference'] = games_df['white_rating'] - games_df['black_rating']

# add avg_rating column by determining average between white's and black's ratings
games_df['avg_rating'] = (games_df['white_rating'] + games_df['black_rating']) / 2

# define a function to reduce the complexity of the opening name
def get_opening(opening_name):
    ''' This function will take a game instance from the games_df dataframe and return a shortened version of the opening_name
    
        parameters:
        opening_name - a row from the games_df dataframe

        returns:
        opening (string) - the generalized name of the opening played
        '''    
    return opening_name.split(':')[0]

# define a function to determine skill_level by grouping rating scores into categories
def get_skill_level(rating):
    ''' This function will take a game instance from the games_df dataframe and return a classifying string
    
        parameters:
        game - a row from the games_df dataframe
        
        returns:
        skill_level (string) - the rating classification for players in the game
    '''
    if rating <= 1400:
        return 'beginner'
    elif 1400 < rating <= 1600:
        return 'intermediate'
    elif 1600 < rating <= 1800:
        return 'advanced'
    else:
        return 'master'

# define a function to determine time control by grouping time increments into categories
def get_time_control(increment):
    ''' This function will take a game instance from the games_df dataframe and return a classifying string
    
        parameters:
        game - a row from the games_df dataframe
        
        returns:
        time_control (string) - the time control type for the game
    '''
    time = int(increment.split('+')[0])

    if time < 5:
        return 'bullet'
    elif 5 <= time < 10:
        return 'blitz'
    elif 10 <= time < 30:
        return 'rapid'
    else:
        return 'classic'
    
# create new columns by applying the above functions    
games_df['opening'] = games_df['opening_name'].apply(get_opening)
games_df['skill_level'] = games_df['avg_rating'].apply(get_skill_level)
games_df['time_control'] = games_df['increment_code'].apply(get_time_control)

st.write('''
    # Chess Game Data Explorer
    ## Data Science Sprint 4 Project
    ### Made by Josh Greenberg)
    '''

st.header('Total turns played in a game vs. Average rating of the players')

# generate a scatter plot of average player rating vs. total turns, colored by time control
fig = px.scatter(games_df, x='avg_rating', y='turns', color='time_control',  title='Chess Game Total Turns vs. Average Player Rating',
    labels=dict(avg_rating='Average Player Rating', turns='Total Turns', time_control='Time Control'), opacity=.75)

# use streamlit to display the plot
st.write(fig)

st.header('Rating difference between players')
st.write('(positive values indicate white is higher rated)')

# create a checkbox to allow the use filter for games where 'rated' is True
rated_only = st.checkbox("Include only rated games")

# create a copy of our data that we can filter if the user chooses to do so
filter_df = games_df
if rated_only:
    filter_df = games_df[games_df['rated']]

# generate a histogram of the rating difference on the filtered data
fig = px.histogram(filter_df, x='rating_difference', nbins=250, range_x=[-500,500],
    labels=dict(rating_difference='Rating difference (white - black)'), title='Rating Differential Between Players')

# use streamlit to display fig
st.write(fig)

st.header('View winner color frequency by opening and skill level')

# generate a list of the 20 most popular openings
top_openings = games_df['opening'].value_counts()[:20]
openings = list(top_openings.index.unique())

# create an enhanced list with a 'Select all' option
openings_2 = openings[:]
openings_2.append('Select all')

# allow the user to select an opening, defaults on 'Select all'
opening = st.selectbox("Select an opening", openings_2, openings_2.index('Select all'))

# if the user choose 'Select all', we need to pass the whole list to our filter
if opening == 'Select all':
    opening = openings

# get a list of the skill levels available to choose from
skill_levels = list(games_df['skill_level'].unique())

# create an enhanced list with a 'Select all' option
skill_levels_2 = skill_levels[:]
skill_levels_2.append('Select all')

# allow the user to select a skill level, defaults on 'Select all'
skill_level = st.selectbox("Select a skill level", skill_levels_2, skill_levels_2.index('Select all'))

# if the user chooses 'Select all', we need to pass the whole list to our filter
if skill_level == 'Select all':
    skill_level = skill_levels

# filter our data per users choices
q_string = 'opening in @opening and skill_level in @skill_level'
filter_df = games_df.query(q_string)

# generate the histogram of winner color, in a consistent order with plotly express
fig = px.histogram(filter_df, x='winner', category_orders={'winner':['white','black','draw']}, 
        labels=dict(winner='Winner'), title='Winning Color')

# display the figure with streamlit
st.write(fig)