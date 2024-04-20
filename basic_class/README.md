# README

### class：TCP_connect

用于TCP相关连接，断开，消息接收等功能

##### def connect

与机器人控制命令端口建立 TCP 连接

##### def disconnect

与机器人控制命令端口断开 TCP 连接

##### def IN

检测并向机器发送message

##### def try_get_message

这个函数默认等待5秒钟，如果在这个时间内没有收到机器人的返回结果，就会立即返回'no_OUT'。如果收到了机器人的返回结果，就会解码并返回结果字符串。

##### def OUT

检测机器回复

##### def IN_OUT

检测并向机器发送message，检测机器回复

##### def connect_enter_SDK

与机器人控制命令端口建立 TCP 连接，并进入SDK模式控制





# 日志

- 20240420
  - 12:44 完成class TCP_connection