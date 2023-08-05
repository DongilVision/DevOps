import streamlit as st
import webbrowser
import os
from mdv import Navi
import subprocess
 
#from st_pages import Page, Section, add_page_title, show_pages

st.set_page_config(layout="wide")

 
padding_top = 10

st.markdown(f"""
    <style>
        .reportview-container .main .block-container{{
            padding-top: {padding_top}rem;
        }}
    </style>""",
    unsafe_allow_html=True,
) 
 
# st.write(st.experimental_get_query_params())
#{"show_map": ["True"], "selected": ["asia", "america"]}
#com.mdlist(".")
param = st.experimental_get_query_params()

nav = Navi('..')

# st.markdown("""
#   <style>
#     .css-o18uir.e16nr0p33 {
#       margin-top: -75px;
#     }
#   </style>
# """, unsafe_allow_html=True)
# # st.markdown(
# #     f"""
#         <style>
#                .block-container {
#                     padding-top: 1rem;
#                     padding-bottom: 0rem;
#                     padding-left: 5rem;
#                     padding-right: 5rem;
#                 }
#         </style>
#     """, unsafe_allow_html=True)
# st.markdown(f"""
#   <style>
#     .block-container {{
#       padding-top: 2rem;
#     }}
#   </style>
# """, unsafe_allow_html=True)
st.sidebar.image('DIT.png')
st.sidebar.title('Dongil Vision Archive')

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

 




 
    
     