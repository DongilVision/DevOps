# Redmine Install
* 공식사이트 이용
* https://hub.docker.com/_/redmine
* db를 먼저 Install하고 , Redmine을 설치한다.
* https://c804c131bc30.gitbooks.io/redmine/content/chapter1.html

### 설정
개발종류
사용자
역활
```
WSL에 설치 (23.2.8)
apt update
apt install nfs-common
mount -t nfs 192.168.2.55:/vol2 /NAS2
http://172.25.33.236:53000/projects : 도커주소로 접속된다.(기동시 변경되니 주의바람)
```
```
version: '3.7'
# https://hub.docker.com/_/redmine
services:

  mysql:
    image: mysql:8.0.32
    restart: always
    container_name: mysql_4_redmine
    ports:
      - 53306:3306 # HOST:CONTAINER
    environment:
      MYSQL_ROOT_PASSWORD: 20142014
    command:
      - --character-set-server=utf8mb4
      - --collation-server=utf8mb4_unicode_ci
      #- --bind="0.0.0.0"
    volumes:
      - /NAS2/JJY_TASK/mysql_repo:/var/lib/mysql

  redmine:
    image: redmine
    container_name: redmine_4_jjy
    restart: always
    
    environment:
      REDMINE_DB_MYSQL: 172.25.33.236
      REDMINE_DB_PORT: 53306 
      REDMINE_DB_USERNAME: root
      REDMINE_DB_PASSWORD: 20142014
      REDMINE_DB_DATABASE: redmine
      REDMINE_SECRET_KEY_BASE: supersecretkey
    volumes:
     - /NAS2/redmine/files:/usr/src/redmine/files
     - /NAS2/redmine/plugins:/usr/src/redmine/plugins
     - /NAS2/redmine/themess:/usr/src/redmine/themes
    ports:
      - 53000:3000
   



```

```
version: '3.7'
# https://hub.docker.com/_/redmine
services:

  redmine:
    image: redmine
    restart: always
    
    environment:
      REDMINE_DB_MYSQL: 192.168.2.51
      REDMINE_DB_PORT: 53236 
      REDMINE_DB_USERNAME: root
      REDMINE_DB_PASSWORD: 20142014
      REDMINE_DB_DATABASE: redmine
      REDMINE_SECRET_KEY_BASE: supersecretkey
    volumes:
     - /NAS2/redmine/files:/usr/src/redmine/files
     - /NAS2/redmine/plugins:/usr/src/redmine/plugins
     - /NAS2/redmine/themess:/usr/src/redmine/themes
    ports:
      - 53000:3000
   

  mysql:
    image: mysql:8.0.32
    restart: always
    container_name: mysql_jjy_only
    ports:
      - 53236:3306 # HOST:CONTAINER
    environment:
      MYSQL_ROOT_PASSWORD: 20142014
    command:
      - --character-set-server=utf8mb4
      - --collation-server=utf8mb4_unicode_ci
      - --bind="0.0.0.0"
    volumes:
      - /NAS2/JJY_TASK/mysql_repo:/var/lib/mysql
 ```
