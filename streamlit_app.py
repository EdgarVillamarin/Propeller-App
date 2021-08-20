import streamlit as st
import pandas as pd
import numpy as np
#import plotly.figure_factory as ff
#import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib
siteHeader = st.container()
dataExploration = st.container()
newFeatures = st.container()
modelTraining = st.container()

def plot_propeller(Data,PD,AEAO,z):
  head=list(Data.columns)
  fig,ax=plt.subplots(figsize=(7,3))
  ax.plot(Data['J'],Data['KT'],'k',Data['J'],10*Data['KQ'],'r',Data['J'],Data['no'])
  ax.set_xlabel('Advanced Coefficient J')
  ax.set_ylabel('Kt,10*Kq,no')
  ax.set_title('B-serie'+'z:'+str(z)+'AEAO:'+str(AEAO)+'PD:'+str(PD))
  return fig
  
def wage(ja,PD,AEAO,z):
  """
  Reference: Barnitsas, M.M., Ray, D. and Kinley, P. (1981).
  KT, KQ and Efficiency Curves for the Wageningen B-Series Propellers
  http://deepblue.lib.umich.edu/handle/2027.42/3557
  """
  mat = pd.read_csv('Coefficients/Empuje_Wage.csv')
  mat1=pd.read_csv('Coefficients/Torque_Wage.csv')
  KT = sum(mat['WagCThrust_stuv']*((ja)**mat['WagThrust_s'])*PD**mat['WagThrust_t']*AEAO**mat['WagThrust_u']*z**mat['WagThrust_v'])
  KQ= sum(mat['WagCTorque_stuv']*((ja)**mat['WagTorque_s'])*PD**mat['WagTorque_t']*AEAO**mat['WagTorque_u']*z**mat['WagTorque_v'])
  KT=float(KT)
  KQ=float(KQ)
  return KT,KQ

def curve_kt_kq(PD,AEAO,z):
  """
  Determine the KT: Thrust coefficient, KQ: Torque coefficient, no= open water efficiency for a 
  different values of advance coefficient J.
  Author: Nav. Eng. Edgar Villamarin
  mail: e_villamarin@grupo-villamarin.com
  """
  if z>2 and z<7 and PD> 0.5 and PD<1.4 and AEAO>0.35 and AEAO<1.40:
    j=np.arange(0,2,0.001)
    kt=[]
    kq=[]
    ne=[]
    jn=0
    for x in range(0,len(j),1):
      kt1,kq1=wage(j[x],PD,AEAO,z)
      if kt1>0 and kq1>0:
        kt.append(kt1)
        kq.append(kq1)
        ne.append((j[x]/(2*3.1416))*(kt1/kq1))
        jn=jn+1
    j=j[0:jn]
    villamarin=pd.DataFrame()
    villamarin['J']=j
    villamarin['KT']=kt
    villamarin['KQ']=kq
    villamarin['no']=ne
  else:
    return print('Check aplication limits')
  return villamarin


with siteHeader:
  st.title('Welcome to Ship Propeller Project')
  st.header('by Nav.Eng. Edgar Villamarin')
  link = '[Contact Info](https://grupo-villamarin.com/)'
  st.markdown(link, unsafe_allow_html=True)
  #st.subheader('**mail:** <e_villamarin@grupo-villamarin.com>')
  st.text('The aim of this project is present a data base for a propeller')
with dataExploration:
  st.header('Wagenningen Propellers')
  PD=1.2
  AEAO=0.7
  z=3
  villamarin=curve_kt_kq(PD,AEAO,z)
  st.write(villamarin)
  fig=plot_propeller(villamarin,PD,AEAO,z)
  st.pyplot(fig)
#with newFeatures:
 # st.header('Kaplan Propellers')
  
#with modelTraining:
  #st.header('Wave Piercing Propeller')
  #ha=pd.read_csv('Coefficients/ka365.csv')
  #st.table(ha)
  #fig,ax=plt.subplots(figsize=(7, 3))
  #ax.plot(ha['Axy 3-65'],ha['Axy 3-65'])
  #st.pyplot(fig)
