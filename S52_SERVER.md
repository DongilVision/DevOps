#52번 서버 사용법

---
## 데이타베이스
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
* 비정상시 점검 : root disk 부족, NAS 마운트 상태
### 종료
* cd /home/jjy/project/DIV_Platform/busan
* docker-compose down

---
## GPU Container

### 설정
* /home/jjy/project/DIV_Platform/cuda-0-common
* div52.yaml
* content dir : /home/jjy/user0
* 드라이버 업데이트 필요.