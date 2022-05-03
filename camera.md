

## Check Camera
* ls /dev/video0
* vcgencmd get_camera
* v4l2-ctl --list-formats-ext

```
    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_MODE, cam.CAP_MODE_YUYV)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, w)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
```
    
    if cam.isOpened():
        ret, image = cam.read()

![image](https://user-images.githubusercontent.com/29625147/166415960-cfcbff85-2996-4635-b8d5-2300d074cc4b.png)
