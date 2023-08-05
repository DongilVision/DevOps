
import streamlit as st
import os
import markdown
import re
import base64
from pathlib import Path
from streamlit_option_menu import option_menu
# pip install streamlit-option-menu
from streamlit_js_eval import streamlit_js_eval
import webbrowser

 
from streamlit.components.v1 import html

def script():
    html(f"""<script src="https://use.fontawesome.com/releases/v5.2.0/js/all.js"></script>""")

def redirect_button(url: str, text: str= None, color="#FD504D"):
    st.markdown(
    f"""
     <a href="{url}" target="_self">
        <div style="
            display: inline-block;
            padding: 2px 10px 0px 10px ;
            margin: 30px 30px 30px 30px;
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
            margin: 2px 1px 5px 0px;
            color: #FFFFFF;
            background-color: {color};
            border-radius: 4px;
            text-decoration: none;">
            {text}
        </div>
    </a>
    """ 
    return str

# path는 논리적 위치 : fpath 물리적주소
class Navi:
    def __init__(self, home):
        self.home = home

    def parse(self, param):
        (self.path, self.md) = ( '', None ) # 논리구조임.

        if 'path' in param:
            self.path = str(param['path'][0])
            # self.md = self.getFirst(self.path)
        else:
            if 'md' in param:
                self.md = str(param['md'][0])
                self.path= os.path.dirname(self.md)
            else :
                self.path=''
                # self.md = self.getFirst(self.path)
        self.rdir = self.home+self.path
        (dirlist, filelist) = self.getList()
        if self.md == None and len(filelist)>0:
            self.md = self.path+'/'+ filelist[0]
        # st.sidebar.write("path=%s, md=%s, rd=%s"%( self.path, self.md, self.rdir))
        # st.sidebar.write(filelist)

    def getFirst(self, Path=None):
        self.rdir = self.home+self.path
        return Path+'/First'

                 
    def showDir(self, param):
        self.parse(param)
        (dir_list, file_list) = self.getList()

        subpath = self.path[1:].split('/') # 무조건 / 로 시작
        url_all = ''
        url_path = ''
        if len(subpath) > 0 :
            url = "?path=%s"%('')
            url_all += redirect_url(url,'/',color="#ff8c00")
        for name in subpath:
            if len(name) == 0:
                continue
            url_path += '/'+name
            url = "?path=%s"%( url_path)
            url_all += redirect_url(url,name,color="#ff8c00")
        st.sidebar.markdown(url_all,unsafe_allow_html=True)

        with st.sidebar:
            if len(dir_list) > 0:
                choice_dir = option_menu(None,dir_list,
                    on_change=self.on_change_dir, key='menu_dir',
                    styles={
                        "container": {"margin":"0px", "padding": "0px", "font-size": "14px","background-color": "#ff8c00"},
                        "menu-title": {"font-size": "14px"},
                        "menu-icon":{"font-size":"14px"},
                        "icon": {"color": "black", "font-size": "8px"},
                        "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px","Padding":"0px", "--hover-color": "#555555"},
                        "nav-link-selected": {"background-color": "#222222"},
                        })
            if len(file_list) > 0:
                choice = option_menu(None,file_list,
                    styles={
                        "container": {"margin":"0px", "padding": "0px", "font-size": "14px","background-color": "#2e8b57"},
                        "menu-title": {"font-size": "14px"},
                        "menu-icon":{"font-size":"14px"},
                        "icon": {"color": "black", "font-size": "8px"},
                        "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px","Padding":"0px", "--hover-color": "#555555"},
                        "nav-link-selected": {"background-color": "#222222"},
                        })
                self.md = self.path+'/'+choice
                dname = os.path.dirname(self.home+self.md)
                fname = os.path.basename(self.home+self.md)
                # st.sidebar.write("dd=%s, ff=%s cd=%s"%( dname, fname, os.getcwd()))
                # mdview(self.home+self.md)
        if len(file_list) > 0:
            mdview(dname, fname)

    def on_change_dir(self,key):
        selection = st.session_state[key]
        url = "?path=%s"%( self.path+'/'+selection)
        # self.open_page(url)
        self.nav_to(url)
        st.write(f"Selection chage to {url}")

    def nav_to(self,url):
        nav_script = """
            <meta http-equiv="refresh" content="0; url='%s'">
        """ % (url)
        st.write(nav_script, unsafe_allow_html=True)


    def getList(self):
        dir_list = []
        file_list = []
        f_list = os.listdir(self.rdir)
        for x in f_list:
            if self._contains(['pycache','.git','.jpg','.png','web'],x):
                continue
            else:
                if os.path.isdir(self.rdir+'/'+x):
                    dir_list.append(x)
                else:
                    file_list.append(x)
        return ( dir_list, file_list)

    def _contains(self,list, name):
        for x in list:
            if x in name:
                return True
        return False


# 디버그를 위하여 현재 디렉토리 show

def mdlist(home,path):
    url_all =''
    # st.sidebar.write("cwd = "+path)
    ## 현재 디렉토리 표시
    updir = path
    count = 10
    # base = 'http://div.iptime.org:58282'
    # base = 'http://192.168.2.51:8501'
    if path == None:
        updir = home
    else:
        updir = home+'/'+path
    while updir != home:
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

def mdview(rpath, filename):
    xdir = os.getcwd();
    os.chdir(rpath)
    # st.sidebar.write("CWD = "+os.getcwd())
    tab1, tab2 = st.tabs([filename,"editor"])
    sline = ''
    with tab1:
        with open(filename) as f:
            for line in f:
                sline += line
        imgline = markdown_insert_images(sline) 
        st.markdown(imgline,unsafe_allow_html=True)
    with tab2:
        # response_dict = code_editor(sline,lang="python",theme="dark")
        btn = st.button("Update")
        txt = st.text_area(label="편집내용", value=sline, height=500)
        if btn:
            with open(filename, "w") as file:
                file.write(txt)
    os.chdir(xdir)


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

# -----------------------------------------------------------------------------

def markdown_images(markdown):
    # example image markdown:
    # ![Test image](images/test.png "Alternate text")
    # images = re.findall(r'(!\[(?P<image_title>[^\]]+)\]\((?P<image_path>[^\)"\s]+)\s*([^\)]*)\))', markdown)
    images = re.findall(r'(!\[(?P<image_title>[^\]]*)\]\((?P<image_path>[^\)"\s]+)\s*([^\)]*)\))', markdown)
    return images


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def img_to_html(img_path, img_alt):
    img_format = img_path.split(".")[-1]
    img_html = f'<img src="data:image/{img_format.lower()};base64,{img_to_bytes(img_path)}" alt="{img_alt}" style="max-width: 100%;">'

    return img_html


def markdown_insert_images(markdown):
    images = markdown_images(markdown)

    for image in images:
        image_markdown = image[0]
        image_alt = image[1]
        image_path = image[2]
        if os.path.exists(image_path):
            markdown = markdown.replace(image_markdown, img_to_html(image_path, image_alt))
    return markdown



























    
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
            
            
    

