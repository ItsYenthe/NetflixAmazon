#!/usr/bin/env python
# coding: utf-8

# # Netflix & Amazon

# In[1]:


# IMDB Score voorspellen aan de hand van streamsite, genre, runtime, language etc!!!!!!!!!!!!!!!!!!!!!!!!!
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st

netflix_basis = pd.read_csv('NetflixOriginals.csv')
netflix_extra = pd.read_csv('netflix_original_movie_data.csv')
amazon_prime_basis = pd.read_csv('amazon prime movies.csv')


# In[34]:


# 2 datasets samenvoegen
netflix_merge = pd.merge(netflix_basis, netflix_extra, on = 'Title')

# Kijken hoeveel NA's er zijn
netflix_merge.isna().sum()

# Kolommen selecteren
netflix_kolommen = netflix_merge[['Title', 'Genre', 'Premiere', 'Runtime', 'IMDB Score', 'Language_x', 'Country']]

# Duplicates verwijderen
netflix = netflix_kolommen.drop_duplicates()
amazon_prime = amazon_prime_basis.drop_duplicates()

netflix.head()


# In[35]:


# Dataframe maken voor de Amazon language
new_amazon = pd.DataFrame(amazon_prime['Language'].value_counts())
new_amazon['Totaal'] = new_amazon['Language'].sum()
new_amazon['Percentage'] = new_amazon['Language']/new_amazon['Totaal']
new_amazon

# Dataframe maken voor de Netflix Language
new_netflix = pd.DataFrame(netflix['Language_x'].value_counts())
new_netflix['Totaal'] = new_netflix['Language_x'].sum()
new_netflix['Percentage'] = new_netflix['Language_x']/new_netflix['Totaal']
new_netflix

dropdown_buttons = [
    {'label': 'Amazon', 'method':'update',
    'args':[{'visible':[True, False]}, {'title':'Amazon'}]},
    {'label': 'Netflix', 'method':'update',
    'args':[{'visible':[False, True]}, {'title':'Netflix'}]},
    {'label': 'Beide', 'method':'update',
    'args':[{'visible':[True, True]}, {'title':'Beide'}]}
]

# Plotten van percentage films per taal met dropdownbox voor amazon, netflix en beide
fig = go.Figure()
fig.add_trace(go.Bar(x = new_amazon.index, y = new_amazon['Percentage'], name = 'Amazon Prime films/series'))
fig.add_trace(go.Bar(x = new_netflix.index, y = new_netflix['Percentage'], name = 'Netflix films/series'))
fig.update_layout({'updatemenus':[{'type': 'dropdown',
                                 'x':1.3, 'y':0.5,
                                 'showactive':True,
                                 'active': 0,
                                 'buttons':dropdown_buttons}]},
                  title_text = 'Aantal films/series die beschikbaar zijn via amazon of netflix, verdeeld per taal.', yaxis_tickformat="2%",
                 )
fig.update_xaxes(title_text = 'Taal')
fig.update_yaxes(title_text = 'Percentage films')
fig.show()


# In[36]:


# Wij gaan kijken naar de 5 genres die het vaakt voorkomen
netflix['Genre'].value_counts()

# Selecteren naar de data waarbij het 1 van die 5 genres is
netflix_genre = netflix.loc[(netflix['Genre'] == 'Documentary') | (netflix['Genre'] == 'Drama')| (netflix['Genre'] == 'Comedy') | 
            (netflix['Genre'] == 'Thriller') | (netflix['Genre'] == 'Romantic comedy')]


# In[74]:


# Plotten van de IMDB Scores per genre
my_scale = ['rgb(0, 171, 169)', 'rgb(0, 138, 0)', 'rgb(96, 169, 23)', 'rgb(164, 196, 0)', 'rgb(227, 200, 0)']
fig = px.box(data_frame = netflix_genre, x = 'Genre', y = 'IMDB Score', color = 'Genre', 
             color_discrete_sequence= my_scale, title = 'IMDB Scores per genre')

my_buttons = [{'label':'Boxplot', 'method':'update', 'args': [{'type': 'box'}]}, 
              {'label':'Violin', 'method':'update', 'args': [{'type': 'violin'}]}]

fig.update_layout({'updatemenus':[{'type': 'buttons', 'direction': 'down', 'x': 1.13, 'y': 0.5, 'showactive': True,
                                  'active': 0, 'buttons': my_buttons}]})

fig.show()


# In[75]:


# Running time kolom omzetten naar tijden !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11
for time in amazon_prime[0:5]['Running Time']:
    pd.Timedelta(time)
    amazon_prime['Running Time'] = amazon_prime['Running Time'].replace(time, pd.Timedelta(time))

amazon_prime.head(10)


# In[76]:


# Nieuwe kolom in netflix met runtime per groep 
bins= [0,51,101,151,251]
labels = ['0-50','51-100','101-150','151-250']
netflix['Runtime_group'] = pd.cut(netflix['Runtime'], bins=bins, labels=labels, right=False)


# In[77]:


# Visualisatie van runtime van de (Netflix)films tegen de IMDB scores !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
fig = go.Figure()
for runtime in netflix['Runtime_group']:
    df = netflix[netflix["Runtime_group"] == runtime]
    fig.add_trace(go.Box(x = df['Runtime_group'], y = df['IMDB Score'], name = runtime))
    
sliders = [{'steps':[
    {'label':'all', 'method': 'update', 'args': [{'visible': [True, True, True, True]}, {'title': 'Runtime'}]},
    {'label':'0-50 minuten', 'method': 'update', 'args': [{'visible': [True, False, False, False]}, {'title': 'Runtime van 0-50 minuten'}]},
    {'label':'51-100 minuten', 'method': 'update', 'args': [{'visible': [False, True, False, False]}, {'title': 'Runtime van 51-100 minuten'}]},
    {'label':'101-150 minuten', 'method': 'update', 'args': [{'visible': [False, False, True, False]}, {'title': 'Runtime van 101-150 minuten'}]},
    {'label':'151-250 minuten', 'method': 'update', 'args': [{'visible': [False, False, False, True]}, {'title': 'Runtime van 151-250 minuten'}]},
]}]

fig.update_xaxes(title_text = 'Runtime (minuten)')
fig.update_yaxes(title_text = 'IMDB Score')
fig.update_layout({'sliders': sliders})
fig.show()


# In[ ]:





# In[90]:


# Als Slider niet werkt, dan kan ik hier dropdown doen voor scatter, bar en boxplot van runtime tegen IMDB
fig = go.Figure()

dropdown_buttons_2 = [
    {'label': 'Scatter', 'method':'update',
    'args':[{'visible':[True, False, False]}, {'title':'Scatterplot van de runtime tegen de IMDB Score'}]},
    {'label': 'Boxplot', 'method':'update',
    'args':[{'visible':[False, True, False]}, {'title':'Boxplot van de runtime tegen de IMDB Score'}]},
    {'label': 'Barplot', 'method':'update',
    'args':[{'visible':[False, False, True]}, {'title':'Barplot van de runtime tegen de IMDB Score'}]}    
]

fig.add_trace(go.Scatter(x = netflix['Runtime'], y = netflix['IMDB Score'], name = 'Sctterplot', mode = 'markers', marker = dict(color = 'rgb(0, 171, 169)')))

fig.add_trace(go.Box(x = netflix['Runtime_group'], y = netflix['IMDB Score'], name = 'Boxplot'))

fig.add_trace(go.Bar(x = netflix['Runtime_group'], y = netflix['IMDB Score'], name = 'Barplot'))


fig.update_layout({'updatemenus':[{'type': 'dropdown',
                                 'x':1.13, 'y':0.5,
                                 'showactive':True,
                                 'active': 0,
                                 'buttons':dropdown_buttons_2}]})

fig.update_xaxes(title_text = 'Runtime (minuten)')
fig.update_yaxes(title_text = 'IMDB Score')
fig.show()


# In[31]:


# Scatterplot van de Netflix IMDB Scores per runtime
fig = px.scatter(data_frame = netflix, x = 'Runtime', y = 'IMDB Score', 
             color_discrete_sequence= ['rgb(0, 171, 169)'], title = 'IMDB Scores per runtime')

fig.show()

# Boxplot van de Netflix IMDB Scores per runtime groep
my_scale = ['rgb(0, 171, 169)', 'rgb(0, 138, 0)', 'rgb(96, 169, 23)', 'rgb(164, 196, 0)', 'rgb(227, 200, 0)', 'rgb(247, 241, 156)']
fig = px.box(data_frame = netflix, x = 'Runtime_group', y = 'IMDB Score', color = 'Runtime_group', 
             color_discrete_sequence= my_scale, title = 'IMDB Scores per runtime')

fig.show()


# In[9]:


amazon_prime.head()


# In[10]:


# OOK NOG NIEUWE KOLOMMEN MAKEN EN DIE GEBRUIKEN !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

