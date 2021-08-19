import streamlit as st
import pandas as pd
#import plotly.figure_factory as ff
#import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

siteHeader = st.container()
dataExploration = st.container()
newFeatures = st.container()
modelTraining = st.container()

with siteHeader:
  st.title('Welcome to Ship Propeller Project')
  st.header('by Nav.Eng. Edgar Villamarin')
  link = '[Contact Info](https://grupo-villamarin.com/)'
  st.markdown(link, unsafe_allow_html=True)
  #st.subheader('**mail:** <e_villamarin@grupo-villamarin.com>')
  st.text('The aim of this project is present a data base for a propeller')
with dataExploration:
  st.header('Wagenningen Propellers')

with newFeatures:
  st.header('Kaplan Propellers')
  
with modelTraining:
  st.header('Wave Piercing Propeller')
  ha=pd.read_csv('Coefficients/ka365.csv')
  st.table(ha)
  fig=plt.plot(ha['Axy 3-65'],ha['Axy 3-65'])
  st.pyplot(fig)
