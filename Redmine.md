
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
