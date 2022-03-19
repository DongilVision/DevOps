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
