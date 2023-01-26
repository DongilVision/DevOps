#52번 서버 사용법

# 데이타베이스서버
### 설정
* 호스트 : 192.168.2.52
* 포트: 3306 (보안문제있음)
* 계정: root:dongilxxxx (설립연도)
* 실제위치: /NAS2/docker_maria_db
* 설정화일
  * cd /home/jjy/project/DIV_Platform/
  * compose.yml 참고.
  * /NAS2/docker_maria_db:/var/lib/mysql
  * ./docker_mysql/my.conf:/usr/local/etc/my.cnf

### 점검
* docker ps | grep local_mariadb
### 시작
* cd /home/jjy/project/DIV_Platform/busan
* docker-compose up -d
### 종료
* cd /home/jjy/project/DIV_Platform/busan
* docker-compose down