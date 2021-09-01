import streamlit as st
import pandas as pd
import numpy as np
import base64 
#import plotly.figure_factory as ff
#import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib
import numpy.matlib
siteHeader = st.container()
dataExploration = st.container()
newFeatures = st.container()
modelTraining = st.container()

def get_table_download_link_csv(df,PD,AEAO,z):
    """
    To download the wage propeller open water characteristics
    """
    #csv = df.to_csv(index=False)
    csv = df.to_csv().encode()
    #b64 = base64.b64encode(csv.encode()).decode() 
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="Propeller_Resutls.csv" target="_blank">Download Results file</a>'
    return href

def plot_propeller(Data,PD,AEAO,z):
  import matplotlib.pyplot as plt
  head=list(Data.columns)
  fig=plt.figure(figsize=(7,3))
  #fig,ax=plt.subplots(figsize=(7,3))
  #ax.plot(Data['J'],Data['KT'],'k',Data['J'],10*Data['KQ'],'r',Data['J'],Data['no'])
  plt.plot(Data['J'],Data['KT'],'k',Data['J'],10*Data['KQ'],'r',Data['J'],Data['no'])
  plt.title('B-serie'+'  '+'z:'+' '+str(z)+'  '+'AEAO:'+' '+str(AEAO)+'  '+'PD:'+' '+str(PD))
  plt.legend(['Kt','10*Kq','no'])
  plt.grid()
  plt.xlabel('Advanced Coefficient   J')
  plt.ylabel('Kt,10*Kq,no')
  #plt.title('B-serie'+'  '+'z:'+' '+str(z)+'  '+'AEAO:'+' '+str(AE/AO)+'  '+'PD:'+' '+str(P/D))
  #plt.xlabel('Advanced Coefficient   J')
  #plt.ylabel('Kt,10*Kq,no')
  #plt.title('B-serie'+'  '+'z:'+' '+str(z)+'  '+'AEAO:'+' '+str(AE/AO)+'  '+'PD:'+' '+str(P/D))
  #plt.grid()
  #ax.set_xlabel('Advanced Coefficient   J')
  #ax.set_ylabel('Kt,10*Kq,no')
  #ax.set_title('B-serie'+'  '+'z:'+' '+str(z)+'  '+'AEAO:'+' '+str(AE/AO)+'  '+'PD:'+' '+str(P/D))
  #ax.plot.grid()
  return fig

def plot_propeller_kaplan(Data,PD,FileID):
  import matplotlib.pyplot as plt
  head=list(Data.columns)
  fig=plt.figure(figsize=(7,3))
  plt.plot(Data['J'],Data['KT'],'k',Data['J'],Data['KTn'],'g',Data['J'],10*Data['KQ'],'r',Data['J'],Data['no'])
  plt.title('Kaplan 19A'+'  '+str(FileID)+'  '+'PD:'+' '+str(PD))
  plt.legend(['Kt','Ktn','10*Kq','no'])
  plt.grid()
  plt.xlabel('Advanced Coefficient   J')
  plt.ylabel('Kt,10*Kq,no')
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
  KQ= sum(mat1['WagCTorque_stuv']*((ja)**mat1['WagTorque_s'])*PD**mat1['WagTorque_t']*AEAO**mat1['WagTorque_u']*z**mat1['WagTorque_v'])
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
  if z>2 and z<7 and PD> 0.5 and PD<1.4 and AEAO>0.3 and AEAO<1.05:
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


def kaplan(FileID,PD,J):
  """
  Determine the KT: Thrust coefficient, KQ: Torque coefficient, no= open water efficiency for a 
  different values of advance coefficient J, for wagennigen propellers.
  Reference Coefficient:
  https://repository.tudelft.nl/islandora/object/uuid:b8cd2238-1cd7-4a64-a74e-73f4dcdf35d4/datastream/OBJ/download
  FileID: Name of the data file coefficient, Ka375,Ka455,Ka470,Ka575
  """
  File='Coefficients/'+str(FileID)+'.csv'
  ka=pd.read_csv(File)
  heads=list(ka.columns)
  #factor=np.ones((7,7))
  R=np.ones((7,1))
  Ja=np.ones((7,1))
  for x in range(0,7,1):
    R[x,0]=PD**x
    Ja[x,0]=J**x
  for x in range(0,len(heads),1):
    globals()[f'A{x}']=np.array(ka[heads[x]])
    globals()[f'A{x}']=np.matlib.reshape(globals()[f'A{x}'],(7,7))
  KT=float(np.matmul(np.transpose(np.matmul(A0,Ja)),R))
  KQ=float(np.matmul(np.transpose(np.matmul(A1,Ja)),R))
  KTN=float(np.matmul(np.transpose(np.matmul(A2,Ja)),R))
  return KT,KTN,KQ

def curve_kt_kq_kaplan(FileID,PD):
  """
  Determine the KT: Thrust coefficient, KQ: Torque coefficient, no= open water efficiency for a 
  different values of advance coefficient J, for kapla in a duct 19A propellers.
  """
  if  PD> 0.5 and PD<1.4:
    j=np.arange(0,2,0.001)
    kt=[]
    ktn=[]
    kq=[]
    ne=[]
    jn=0
    for x in range(0,len(j),1):
      kt1,ktn1,kq1=kaplan(FileID,PD,j[x])
      if kt1>0 and kq1>0:
        kt.append(kt1)
        kq.append(kq1)
        ktn.append(ktn1)
        ne.append((j[x]/(2*3.1416))*(kt1/kq1))
        jn=jn+1
    j=j[0:jn]
    villamarin=pd.DataFrame()
    villamarin['J']=j
    villamarin['KT']=kt
    villamarin['KTn']=ktn
    villamarin['KQ']=kq
    villamarin['no']=ne
  else:
    return print('Check aplication limits')
  return villamarin



with siteHeader:
  st.title('Welcome to Ship Propeller Project')
  st.header('by Nav.Eng. Edgar Villamarin')
  link = '[Personal Website](https://grupo-villamarin.com/)'
  st.markdown(link, unsafe_allow_html=True)
  #st.subheader('**mail:** <e_villamarin@grupo-villamarin.com>')
  st.markdown('''Dear network, the aim of this project is make available
  open-water characteristics for ship propeller design and selection,
  for a wide range of propllers series in this web app
  At the moment, the classic B-series are available here.
  I hope for the future to upgrade the
  app with other propeller series, hence,
  if you have other propeller series data availble,
  I would be grateful shared with me the information via mail <e_villamarin@grupo-villamarin.com>''')
       
with dataExploration:
  st.header('Wagenningen Propellers')
  st.text('The polynomials equation for thrust:')
  st.latex(r''' K_{T}= \sum_{s,t,u,v}^{} C^TJ^s(P/D)^t(A_{E}/A_{O})^uZ^v ''')
  st.text('The polynomials equation for torque:')
  st.latex(r''' K_{Q}= \sum_{s,t,u,v}^{} C^QJ^s(P/D)^t(A_{E}/A_{O})^uZ^v ''')
  st.text('The open-water efficiency of the propeller is:')
  st.latex(r''' n_{O}= \frac{JK_{T}}{2\pi K_{Q}}''')
  
  PD=st.number_input('Select the Pitch/Diameter',min_value=0.6,max_value=1.4,step=0.1)#,min_value=0.5,max_value=1.4,value=1,step=0.1)
  AEAO=st.number_input('Select the Expanded area coefficient',min_value=0.35,max_value=1.05,step=0.05)
  z=st.number_input('Select the number of propellers',min_value=3,max_value=7,step=1)
  #PD=1.2
  #AEAO=0.7
  #z=3
  ready=st.checkbox('READY')
  if ready==True:
    st.write('**Calculating...**')
    st.write('For other combination of parameters, first mark uncheck ')
    villamarin=curve_kt_kq(PD,AEAO,z)
  #st.write(villamarin)
    fig=plot_propeller(villamarin,PD,AEAO,z)
    st.pyplot(fig)
    st.markdown(get_table_download_link_csv(villamarin,PD,AEAO,z), unsafe_allow_html=True)
    
with newFeatures:
  st.header('Kaplan Propellers')
  st.text('The polynomials equation for thrust:')
  st.latex(r''' K_{T}= \sum_{i=0}^{i=n} \sum_{j=0}^{j=n} A_{i,j}(P/D)^iJ^j''')
  st.text('The polynomials equation for thrust with nozzle:')
  st.latex(r''' K_{TN}= \sum_{i=0}^{i=n} \sum_{j=0}^{j=n} B_{i,j}(P/D)^iJ^j''')
  st.text('The polynomials equation for torque:')
  st.latex(r''' K_{Q}= \sum_{i=0}^{i=n} \sum_{j=0}^{j=n} C_{i,j}(P/D)^iJ^j''')
  st.text('The Kaplan propeller characteristics are specfic for 19A Nozzle')
  SelectPropeller=st.selectbox('Select the Kaplan propeller type',('ka365','ka455','ka470','ka575'))
  PD1=st.number_input('Select Pitch and Diameter Ratio',min_value=0.6,max_value=1.2,step=0.1) 
  SelectPropeller=str(SelectPropeller)
  ready1=st.checkbox('START')
  if ready1==True:
    st.write('**Calculating...**')
    st.write('For other combination of parameters, first mark uncheck ')
    villamarin1=curve_kt_kq_kaplan(SelectPropeller,PD1)
    st.write(villamarin1)
    fig=plot_propeller_kaplan(villamarin1,PD1,SelectPropeller)
    st.pyplot(fig)
    st.markdown(get_table_download_link_csv(villamarin1,PD,'',''), unsafe_allow_html=True)
    
#with modelTraining:
  #st.header('Wave Piercing Propeller')
  #ha=pd.read_csv('Coefficients/ka365.csv')
  #st.table(ha)
  #fig,ax=plt.subplots(figsize=(7, 3))
  #ax.plot(ha['Axy 3-65'],ha['Axy 3-65'])
  #st.pyplot(fig)

