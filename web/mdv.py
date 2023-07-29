
import streamlit as st
import os
 
from streamlit.components.v1 import html

def script():
    html(f"""<script src="https://use.fontawesome.com/releases/v5.2.0/js/all.js"></script>""")

def redirect_button(url: str, text: str= None, color="#FD504D"):
    st.markdown(
    f"""
     <a href="{url}" target="_self">
        <div style="
            display: inline-block;
            padding: 2px 10px 2px 10px ;
            margin: 3px;
            color: #FFFFFF;
            background-color: {color};
            border-radius: 3px;
            text-decoration: none;">
            {text}
        </div>
    </a>
    """,
    unsafe_allow_html=True
    )

def redirect_url(url: str, text: str= None, color="#FD504D"):
    str =   f"""
    
     <a href="{url}" target="_self">
        <div style="
            display: inline-block;
            padding: 1px 5px 1px 5px ;
            margin: 2px 1px 0px 0px;
            color: #FFFFFF;
            background-color: {color};
            border-radius: 4px;
            text-decoration: none;">
            {text}
        </div>
    </a>
    """ 
    return str

def mdview(filename):
    tab1, tab2 = st.tabs([filename,"editor"])
    sline = ''
    with tab1:
        #'pages/project.md'
        with open(filename) as f:
            for line in f:
                sline += line
            
        st.markdown(sline,unsafe_allow_html=True)
    
    with tab2:
        # response_dict = code_editor(sline,lang="python",theme="dark")
        btn = st.button("Update")
        txt = st.text_area(label="편집내용", value=sline, height=500)
        if btn:
            with open(filename, "w") as file:
                file.write(txt)


def mdfirst(path):
    file_list = os.listdir(path)
    for x in file_list:
        if 'pycache' in x:
            continue
        if os.path.isdir(x):
            continue
        if ".md" in x:
            return x
    return None

def mdlist(path):
    url_all =''
    # st.sidebar.write("cwd = "+path)
    ## 현재 디렉토리 표시
    updir = path
    count = 10
    base = 'http://div.iptime.org:58282'
    base = 'http://192.168.2.51:8501'
    while updir != '.':
        url = "%s?path=%s"%(base,updir)
        url_all = redirect_url(url,'/'+os.path.basename(updir),color="#888888") + url_all
        updir = os.path.dirname(updir)
        count -=1
        if count < 0:
            break
    if count < 10:
        url = "%s?path=%s"%(base,updir)
        url_all = redirect_url(url,"..",color="#888888") + url_all
        st.sidebar.markdown(url_all,unsafe_allow_html=True)
       
    
    # subdir 표시


    url_all =''
    file_list = os.listdir(path)
    for x in file_list:
        if 'pycache' in x:
            continue
        if os.path.isdir(path+'/'+x):
            url = "%s?path=%s"%(base,path+'/'+x)
            url_all += redirect_url(url,x,color="#222222")
    #         url_all += url +'\n'
    st.sidebar.markdown(url_all,unsafe_allow_html=True)
    
    for x in file_list:
        if 'pycache' in x:
            continue
        if os.path.isdir(x):
            continue
        if ".md" in x:
            url = "%s?md=%s"%(base,path+'/'+x)
            url_all = redirect_url(url,x)
            st.sidebar.markdown(url_all,unsafe_allow_html=True)
            
            
    

