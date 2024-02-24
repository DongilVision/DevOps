
# checklist

[] ssh 접속이 되는가?
[] 사용자 id 와 파일시스템이 일치하는가?
[] git 업데이트는 잘되는가?
[] 자동재기동되는가?

# basic-include
```
FROM ubuntu:22.04
 
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul

RUN apt-get update \
    && apt-get install -y tzdata \
    && apt-get install -y python3 pip git \
    && apt-get install -y net-tools iputils-ping dnsutils \
    && apt-get install -y vim git curl wget sudo unzip \
    && apt-get install -y gnupg software-properties-common 

RUN pip install --upgrade pip


```
# SSH-VSCODE

```
# *************************************************************************************
#   2. SSHD / 권한시스템
#      기동방법 : /usr/sbin/sshd -D &
#      id를   uid=1001(jjy) gid=1001(jjy) groups=1001(jjy),998(docker)
#      암호 root
# *************************************************************************************

RUN apt-get install -y openssh-server

RUN echo 'root:1234' | chpasswd
RUN sed -ri 's/^#?PermitRootLogin\s+.*/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config
RUN sed -i "s/^#Port 22/Port 22/g" /etc/ssh/sshd_config

RUN mkdir -p /var/run/sshd \
    && mkdir -p /root/.ssh \
    && chmod 700 /root/.ssh \
    && ssh-keygen -A

EXPOSE 22

```
# USER-ADD

```
# *************************************************************************************
# #  7. `pwd` 사용할때는 반드시 계정일치 필요
# 사용자 /유저/그룹 등록
# USER = jjy  host_gid = 2014 host_uid = 2014
# docker run --rm -it aainka/webdesk:0.1 /bin/bash
# *************************************************************************************

ARG USER=jjy
RUN echo "${USER} ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/${USER} \
    && chmod 0440 /etc/sudoers.d/${USER}

ARG USER_ID=1001
ARG GROUP_ID=1001
RUN groupadd -g $GROUP_ID $USER \
    && useradd -s /bin/bash -u $USER_ID -g $GROUP_ID -m $USER
 
RUN echo "${USER}:1234" | chpasswd


```
