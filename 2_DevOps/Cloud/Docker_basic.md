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
