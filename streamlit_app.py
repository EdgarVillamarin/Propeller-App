import streamlit as st
import webbrowser
siteHeader = st.beta_container()
dataExploration = st.beta_container()
newFeatures = st.beta_container()
modelTraining = st.beta_container()

with siteHeader:
  st.title('Welcome to Ship Propeller Project')
  st.header('by [Nav.Eng. Edgar Villamarin](www.grupo-villamarin.com)')
  st.subheader('mail: e_villamarin@hotmail.com')
  st.text('In this project')


url = 'www.grupo-villamarin.com'

if st.button('Open browser'):
    webbrowser.open_new_tab(url)
