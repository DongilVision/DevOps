
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
        st.sidebar.write("path=%s, md=%s, rd=%s"%( self.path, self.md, self.rdir))
        st.sidebar.write(filelist)

    def getFirst(self, Path=None):
        self.rdir = self.home+self.path
        return Path+'/First'

                 
    def showDir(self, param):
        self.parse(param)
        (dir_list, file_list) = self.getList()


       
        url_all = ''
        st.sidebar.write("DIRLIST------------------")
        url = "?path=%s"%('')
        url_all += redirect_url(url,'/',color="#002255")
        ## st.sidebar.markdown(url_all,unsafe_allow_html=True)

        subpath = self.path[1:].split('/') # 무조건 / 로 시작
        #st.sidebar.write(subpath)
        ##url_all = ''
        url_path = ''
        for name in subpath:
            url_path += '/'+name
            url = "?path=%s"%( url_path)
            url_all += redirect_url(url,name+'/',color="#002255")
        st.sidebar.markdown(url_all,unsafe_allow_html=True)



        url_all = ''
        for x in dir_list:
            url = "?path=%s"%( self.path+'/'+x)
            url_all += redirect_url(url,x,color="#005522")
        st.sidebar.markdown(url_all,unsafe_allow_html=True)

        st.sidebar.write("FILE_LIST------------------")
        url_all = ''
        for x in file_list:
            url = "?md=%s"%(self.path+'/'+x)
            url_all += redirect_url(url,x )
        st.sidebar.markdown(url_all,unsafe_allow_html=True)
        dname = os.path.dirname(self.home+self.md)
        fname = os.path.basename(self.home+self.md)
        st.sidebar.write("dd=%s, ff=%s cd=%s"%( dname, fname, os.getcwd()))
        # mdview(self.home+self.md)
        mdview(dname, fname)

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
    base = 'http://div.iptime.org:58282'
    base = 'http://192.168.2.51:8501'
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
            
            
    

