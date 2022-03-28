
원래는 docker conatiner 내에서 nvidia GPU를 사용하기 위해 nvidia-docker 혹은 nvidia-docker2를 따로 설치해줘야했다. 하지만 docker 19.03 버전부터는 docker 자체적으로 nvidia GPU를 지원하고 nvidia-docker는 사용하지 않는다.
* docker run ... --gpus "device=1,2,3" ...
* docker run ... --gpus all ... 
* https://conservatory.tistory.com/12

# Official Docker docs.

* https://docs.docker.com/get-docker/
* https://docs.docker.com/engine/install/ubuntu/ (Installation for Ubuntu)
* https://docs.docker.com/compose/install/ ( Installation Compose )


---
# DOCKER 설치
* https://docs.docker.com/engine/install/ubuntu/ # 공식설치

apt-get update  
apt-get remove docker docker-engine docker.io containerd runc  
apt-get install -y apt-transport-https ca-certificates curl   gnupg lsb-release  

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
... 중략
apt-get update  
apt-get install docker-ce docker-ce-cli containerd.io  

---
# DOCKER-COMPOSE 설치

@버전확인
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

@Docker 권한
sudo usermod -aG docker $USER
visudo

# docker dns 안될경우, 특히 apt-update 않될때.
docker build --network=host -t div/uhome:0.1 .  
호스트 쪽의 dns를 사용하도록 한다.  

# Docker 내부 시간 (KST설정)
```
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul
RUN apt-get update
RUN apt-get install tzdata
RUN apt-get install -y vim git curl net-tools iputils-ping
```
