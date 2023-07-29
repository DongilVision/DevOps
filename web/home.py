import streamlit as st
import webbrowser
import os
from mdv import Navi
import subprocess
 
#from st_pages import Page, Section, add_page_title, show_pages

st.set_page_config(layout="wide")

 
 
# st.write(st.experimental_get_query_params())
#{"show_map": ["True"], "selected": ["asia", "america"]}
#com.mdlist(".")
param = st.experimental_get_query_params()

nav = Navi('..')

nav.showDir(param)


# path = home
# if 'path' in param:
#     path = str(param['path'][0])

# fname = path+'/'+mdv.mdfirst(path)
# if 'md' in param :
#     fname = str(param['md'][0])
#     path= os.path.dirname(fname)

# ## 디렉토리 목록보이기
# mdv.mdlist(home,None)
# if fname != None:
#     mdv.mdview(fname)

if st.sidebar.button("GIT PUSH"):
    x = subprocess.run('/usr/bin/sh ./git_push.sh', shell=True, capture_output=True, text=True)
    #st.write("action push" +x)
    st.sidebar.write("Result.  "+x.stdout)




 
    
     