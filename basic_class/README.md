# README

## class TCP_connect

用于TCP相关连接，断开，消息接收等功能

### def connect

与机器人控制命令端口建立 TCP 连接

### def disconnect

与机器人控制命令端口断开 TCP 连接

### def IN

检测并向机器发送message

### def try_get_message

这个函数默认等待5秒钟，如果在这个时间内没有收到机器人的返回结果，就会立即返回'no_OUT'。如果收到了机器人的返回结果，就会解码并返回结果字符串。

### def OUT

检测机器回复

### def IN_OUT

检测并向机器发送message，检测机器回复

### def connect_enter_SDK

与机器人控制命令端口建立 TCP 连接，并进入SDK模式控制

## class UDP_connect

用于UCP相关连接，断开，消息接收等功能

### def connect

与机器人控制命令端口建立 UDP 连接

### def disconnect

与机器人控制命令端口断开UDP 连接

### def try_get

这个函数默认等待5秒钟，如果在这个时间内没有收到机器人的返回结果，就会立即返回'no_OUT'。如果收到了机器人的返回结果，就会解码并返回结果字符串。

### def solve_game

用于解析赛事数据推送

### def solve_key

用于从赛事数据推送中获得键位

### solve_key_name

将获得键位转换为真实名称

### def solve_gimbal

### def solve_chassis_position

# 使用示例：

以下为连接TCP,UDP获取赛事引擎数据的示例

```python
TCP = TCP_connection(printing=True)

UDP = UDP_connection(printing=True)

TCP.connect_enter_SDK()

UDP.connect()

TCP.IN_OUT("game_msg on;")

for i in range(1, 1000):
	msg = UDP.try_get()
	
	msg_solved = solve_game(msg)
	
	keys = solve_key(msg_solved)
	
	keyname = solve_key_name(keys)
	
	print("keynames:", keyname)

UDP.disconnect()

TCP.disconnect()
```

# 日志

- 20240420
    - 12:44 完成
        - class TCP_connection
    - 13:12 完成
        - class UDP_connect
        - def solve_game
        - def solve_key
        - solve_key_name
        - def solve_gimbal
        - def solve_chassis_position
    - 13:31完成样例代码
