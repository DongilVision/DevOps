
### Python Check ( Root )
```
apt-get update -y
apt-get upgrade -y
apt autoremove
apt-get upgrade python3
python3 --version
pip3 --version
alias python=python3
```

### Docker Check
``` 
docker ps
docker-compose -v
sudo usermod -aG docker jjy
sudo chmod 666 /var/run/docker.sock
```
### Dockerfile Build
* https://github.com/ultralytics/ultralytics/tree/main/docker
```
t=ultralytics/ultralytics:latest && sudo docker build -f docker/Dockerfile -t $t . && sudo docker push $t
t=ultralytics/ultralytics:latest && sudo docker pull $t && sudo docker run -it --ipc=host --gpus all $t
t=ultralytics/ultralytics:latest && sudo docker pull $t && sudo docker run -it --ipc=host --gpus all -v "$(pwd)"/datasets:/usr/src/datasets $t
```
