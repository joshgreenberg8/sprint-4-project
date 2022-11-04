# sprint-4-project
Repository for my project for Data Science Sprint 4

Chess game data from https://www.kaggle.com/datasets/datasnaek/chess?select=games.csv

The app.py app pulls data from the games.csv file using pandas and uses it to build 
some interactive data displays using streamlit and plotly_express.

The app is deployed to Render at https://chess-games-explorer.onrender.com

A notebook containing my preparation and initial exploration of the data can be found at https://github.com/joshgreenberg8/sprint-4-project/blob/main/notebooks/EDA.ipynb

Some conclusions about the data, from the notebook:

We were able to read our csv file and found that it was fairly well prepared already; there were no missing values and the duplicates were easy to find and eliminate.

We created some new columns relevant to our exploratory analysis. We attempted to identify trends by plotting our variables in appropriate ways and did find some interesting results:

* As player rating increases, fewer games are ended in the earlier rounds. 

* As player rating increases beyond 2000, there is a noticeable taper that also reduces games with higher relative turn counts. The mean looks to be around 50 turns.

* As skill level increases, the ratio of resignations to checkmates also increases.

* The rating difference between players is normally distributed with a mean near zero. The distribution of unrated games has a slightly flatter shape than the overall distribution.

* Some openings have very different win probabilities depending on skill level. For example, the Scandanavian opening is very successful for black in higher skill brackets, but lower rated players should probably try a different approach.
