# RoboBot - Control and configure your robot with ease

RoboBot is a application developed in Python what enables you to create a robot configuration and control the robot in a 3D environment. The robot configuration file exists as a `yaml` file that defines the axis of rotation and linked body parts. the 3D file are loaded as `.STL` files.

## Yaml config file
```yaml
name: "ServoBot"
arm_length: 100.8
origin_point: [0, 54.875, 0]

parts:
  - part:
    type: "body"
    name: "base"
    rotation: [0, 180, 0]
    position: [-15, 20, -25.375]
    lock_position: [1, 1, 1]
    lock_rotation: [1, 1, 1]
    link: 0

  - part:
    type: "body"
    name: "servo"
    rotation: [0, 0, 0]
    position: [0, 1.8, -5.375]
    lock_position: [1, 1, 1]
    lock_rotation: [1, 1, 1]
    link: 0

  - part:
    type: "body"
    name: "rotate"
    rotation: [0, 0, 0]
    position: [13, 33, 5.375]
    lock_position: [1, 1, 1]
    lock_rotation: [1, 0, 1]
    link: 0

  - part:
    ...
```

## Project

### init project with UV
```bash
uv sync
```

### start project

```bash
cd ./code/main
python ./main.py
```

## Screenshots
![img lenna](https://github.com/JessevanVuuren/RoboBot/blob/master/imgs/img1.PNG?raw=true)

![img lenna](https://github.com/JessevanVuuren/RoboBot/blob/master/imgs/img2.PNG?raw=true)