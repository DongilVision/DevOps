
![image](https://user-images.githubusercontent.com/29625147/218292427-14b5e62f-3262-4e5b-8fc9-231ddbe75eb3.png)

* https://wiki.geekworm.com/ESPDUINO-32

### Platform io
* GPIO 번호를 PIN 번호로 사용하면 됨.
```
[platformio]
default_envs = esp32
 
;; CH340
[env:esp32]
platform = espressif32
board = esp32dev
framework = arduino
upload_port = com14
monitor_speed = 115200
monitor_port = com14
```
