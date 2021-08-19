import streamlit as st

siteHeader = st.beta_container()
dataExploration = st.beta_container()
newFeatures = st.beta_container()
modelTraining = st.beta_container()

with siteHeader:
  st.title('Welcome to Ship Propeller Project')
  st.header('*by Nav.Eng. Edgar Villamarin*')
  link = '[Contact Info](https://grupo-villamarin.com/)'
  st.markdown(link, unsafe_allow_html=True)
  st.subheader('**mail:** <e_villamarin@grupo-villamarin.com>')
  st.text('In this project')
  
with dataExploration:
  st.header('Wagenningen Propellers')

with newFeatures:
  st.header('Kaplan Propellers')
  
with modelTraining:
  st.header('Wave Piercing Propeller') 
