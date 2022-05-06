import pandas as pd
import streamlit as st
from PIL import Image
import sqlite3

st.title('Final Project')
image = Image.open('Logo-KDT-JU.webp')
st.image(image)

con = sqlite3.connect('excel_database.db') # Connect

selects = {'country': 'SELECT * FROM countries',
   'participants': 
           '''SELECT p.shortName, p.name, p.activityType, p.organizationURL, COUNT(*) as projects, SUM(p.ecContribution) as total_grants
            FROM  participants p, projects pr, countries c
            WHERE p.projectID = pr.projectID AND c.Acronym = p.country AND c.Country = '{}'
            GROUP BY p.name ORDER BY SUM(p.ecContribution) DESC''',
    'grants':
           '''SELECT pr.year, SUM(p.ecContribution) as total_grants
            FROM  participants p, projects pr, countries c
            WHERE p.projectID = pr.projectID AND c.Acronym = p.country AND c.Country = '{}'
            GROUP BY pr.year'''
}

countries = pd.read_sql(selects['country'], con)
selection = st.selectbox('', list(countries['Country']))

grants = pd.read_sql(selects['grants'].format(selection), con)
st.bar_chart(grants)
print('')
chart = pd.read_sql(selects['participants'].format(selection), con)
st.dataframe(chart)
