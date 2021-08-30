#!/usr/bin/env python
# coding: utf-8

# In[1]:



import sys
print(sys.version)


# In[2]:


#pip install cx_Oracle


# In[3]:


import os
os.chdir("C:\Oracle\instantclient_19_9")


# In[4]:


import cx_Oracle
print("Connected to Oracle Client Version ")
cx_Oracle.clientversion()


# In[5]:



ORACLE_CONNECT = "DRIVRTEST2/ivrtest2@(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(COMMUNITY=TCP)(PROTOCOL=TCP)(HOST=ocdnt16kcl-scan.test.intranet)(PORT=1521))(ADDRESS=(COMMUNITY=TCP)(PROTOCOL=TCP)(HOST=ocomt46tcl-scan.dev.qintra.com)(PORT=1521)))(CONNECT_DATA=(FAILOVER_MODE=(TYPE=session)(METHOD=basic)(RETRIES=180)(DELAY=5))(SERVER=dedicated)(SERVICE_NAME=gendb01t_failover)))"
orcl = cx_Oracle.connect(ORACLE_CONNECT)
print("Connected to Oracle: " + orcl.version)


#also include environment


# In[6]:


# Inputs

import pandas as pd
import numpy as np

#Path for CSV File
csv_input_path= "C:\\Users\\ab17766\\Desktop\\CareerVillage.org"


# Creation of DataFrame
#print("Reading the inputs from the spreadsheet")
df1=pd.read_csv(csv_input_path + "/KPI_Trace_Inputs.csv")
#df1.head(1)


# In[7]:


ucid = df1.at[0,'UCID']
ucid = ucid.strip('"')
#ucid


# In[8]:


#ani = df1['ANI'] 
kpicr = df1.at[0,'KPI']

#ucid = input("Enter the UCID that has to be validated : ") 
#ani = input("Enter your ANI for the corresponding UCID : ") 
#kpicr = input("Enter the KPI/Call reason that has to be validated : ") 

#print(ucid) 
#print(ani) 
#print(kpicr) 


# In[9]:




KPI_query = "select * from kpi_log where ucid like '{}' order by time_stamp".format(ucid)
df_KPI = pd.read_sql(KPI_query, con=orcl)
#print("This is the KPI Log that we see in the DB ")
#df_KPI.head()


# In[10]:



df_KPI = df_KPI[['MENU', 'CALL_REASON']]
#print("The columns that are necessary for us in the KPI Log : ")
#df_KPI.head(50)


# In[11]:


#Validate_KPI_query = "select * from kpi_log where menu like '33132' and call_reason like 'RR_FiberMigrationInfo_%' order by time_stamp asc"
#df_validate_KPI = pd.read_sql(Validate_KPI_query, con=orcl)
#df_validate_KPI.head()


# In[12]:


#print("The row that we are validating in the KPI Log : ")
#df_KPI[df_KPI['CALL_REASON'].str.contains(kpicr)]


# In[13]:


#df_KPI[df_KPI['CALL_REASON'].str.contains('RR_Skip_SelfHelp_131 TCHNLGY:')].any()


# In[14]:


import numpy as np
df_KPI['Test_Result'] = np.where((df_KPI['CALL_REASON'] == kpicr),'PASS', 'FAIL')
print("Result for the validation of KPI/Call reason in KPI Log : ")
#df_KPI1 = df_KPI['Test_Result'].str.contains('PASS')
df_KPI1 = df_KPI[df_KPI['Test_Result'].str.contains('PASS')]

#df_KPI2 = df_KPI1['Test_Result']
#val = df_KPI2.iat[0,0]
val = df_KPI1['Test_Result'].values[0]
#print("val is : ", val)

if val == 'PASS':
    print("PASS")
else:
    print("FAIL")





#df_KPI[df_KPI['Test_Result'].str.contains('PASS')]
#df_KPI = df_KPI['Test_Result'].str.contains('PASS')

#idx = np.where((df['Salary_in_1000']>=100) & (df['Age']< 60) & (df['FT_Team'].str.startswith('S')))

#df_KPI[(df_KPI['MENU'] == 33132) & (df_KPI['CALL_REASON'] == "RR_FiberMigrationInfo_OfferMigration")]


# In[15]:


#pip install beautifulsoup4


# In[16]:


#pip install lxml


# In[17]:


import xml.etree.ElementTree as ET


# In[18]:



Trace_query = "select * from trace_log where ucid like '{}' order by time_stamp".format(ucid)
df_Trace = pd.read_sql(Trace_query, con=orcl)
#print("This is what we see in the db when we execute a query : " )
#df_Trace.head()


# In[19]:


df_Trace['CALL_RECORD']= df_Trace['CALL_RECORD'].apply(lambda x: x.read())
#print("This is the Trace Log that we see in the DB : \n \n")
#print(df_Trace['CALL_RECORD'].values.tolist())


# In[20]:


import os.path
from os import path


# In[21]:


x = path.exists("trace.xml")
#print("Trace log is saved in the path : ", x)


# In[22]:


with open('Trace.xml', 'w') as f:  # Writing in XML file
    for line in df_Trace['CALL_RECORD']:
        f.write(line)


# In[23]:


#input_path= "C:\\Users\\ab17766\\Desktop"
tree = ET.parse("trace.xml")
root = tree.getroot()

tag = root.tag
#print(tag)


# In[24]:


import re


#FromState = input("Enter the state that has to be validated : ") 
#ToState = input("Enter the GoTo state : ")

FromState = df1.at[0,'From State']
ToState = df1.at[0,'To State']



print("From state :", FromState)
print("Go to state :", ToState)


# In[25]:


from bs4 import BeautifulSoup 

# Reading the data inside the xml 

# file to a variable under the name  
# data 
##The below query is for trial
##with open('C:\\Users\\ab17766\\Desktop\\abc.xml', 'r') as f: 
   ## data = f.read() 
    
with open('Trace.xml', 'r') as f: 
    data = f.read() 
  
  
# Passing the stored data inside 
# the beautifulsoup parser, storing 
# the returned object  
Bs_data = BeautifulSoup(data, "xml") 
  
# Finding all instances of tag  
# `ST` 
b_ST = Bs_data.find_all('ST') 
  
 
# Using find() to extract attributes  
# of the first instance of the tag 
State = Bs_data.find('ST', {'nm':FromState}) 

print("The element that we are validating in the Trace Log :  \n \n")
print(State) 


# In[26]:


Fromstate = State.find('Update') 
print("State to be validated is : ", Fromstate) 


# In[27]:




Output = State.find('output') 
print ("Output is: \n \n", Output ) 


# In[28]:


Update = State.find('Next') 
print ("Update info is: \n \n", Update ) 


# In[29]:



OSDM_Response = State.find('OSDM_Response') 
print ("OSDM Response is : \n \n", OSDM_Response ) 


# In[30]:


#print(ToState)
GoToState = State.find("ToState") 
print ("GoTo state is: \n \n", GoToState ) 


# In[ ]:




