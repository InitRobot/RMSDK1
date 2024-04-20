import socket
import sys

import select


class TCP_connection:
	# USB 模式下，机器人默认 IP 地址为 192.168.42.2, 控制命令端口号为 40923
	host = "192.168.42.2"
	port = 40923
	printing = True
	connection = False
	
	def __init__(self, printing=True):
		self.printing = printing
	
	def connect(self):  # 与机器人控制命令端口建立 TCP 连接
		self.address = (self.host, int(self.port))
		self.TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if self.printing:
			print("Connecting_TCP...")
		
		self.TCP_socket.connect(self.address)
		self.connection = True
		if self.printing:
			print("TCP_Connected!")
	
	def disconnect(self):  # 与机器人控制命令端口断开 TCP 连接
		if not self.connection:
			if self.printing:
				print("You Haven't Connected Yet")
			return
		if self.printing:
			print("TCP_disconnecting...")
		self.TCP_socket.shutdown(socket.SHUT_WR)
		self.TCP_socket.close()
		if self.printing:
			print("TCP_disconnected!")
	
	def IN(self, message):  # 检测并向机器发送message
		if not self.connection:
			if self.printing:
				print("You Haven't Connected Yet")
			return
		if (str(type(message)) == "<class 'str'>") and (message[-1] == ';'):
			if self.printing:
				print('IN:', message)
			self.TCP_socket.send(message.encode('utf-8'))
		else:
			if self.printing:
				print('please input str that ends with ";"')
	
	def try_get_message(self, timeout=5):  # 这个函数默认等待5秒钟，如果在这个时间内没有收到机器人的返回结果，就会立即返回'no_OUT'。如果收到了机器人的返回结果，就会解码并返回结果字符串。
		if not self.connection:
			if self.printing:
				print("You Haven't Connected Yet")
			return
		result = ''
		try:
			# 设置超时时间
			ready = select.select([self.TCP_socket], [], [], timeout)
			if ready[0]:
				# 如果有可读数据，接收并解码
				buf = self.TCP_socket.recv(1024)
				result = buf.decode('utf-8')
			else:
				result = 'no_OUT'
		except socket.error as e:
			if self.printing:
				print("Error receiving :", e)
			sys.exit(1)
		return result
	
	def OUT(self, timeout=5):  # 检测机器回复
		if not self.connection:
			if self.printing:
				print("You Haven't Connected Yet")
			return
		result = ''
		result = self.try_get(timeout)
		if self.printing:
			print("OUT:", result)
		return result
	
	def IN_OUT(self, message, timeout=5):  # 检测并向机器发送message，检测机器回复
		if not self.connection:
			if self.printing:
				print("You Haven't Connected Yet")
			return
		result = ''
		self.IN(message, printing=self.printing)
		result = self.OUT(timeout=timeout, printing=self.printing)
		return result
	
	def connect_enter_SDK(self, timeout=5):  # 与机器人控制命令端口建立 TCP 连接，并进入SDK模式控制
		if not self.connection:
			if self.printing:
				print("You Haven't Connected Yet")
			return
		self.connect_TCP(printing=self.printing)
		self.IN_OUT("command;", timeout=timeout, printing=self.printing)
		self.IN_OUT("quit;", timeout=timeout, printing=self.printing)  # 以免图传卡住
		self.IN_OUT("command;", timeout=timeout, printing=self.printing)


class UDP_connection:
	# USB 模式下，机器人默认 IP 地址为 192.168.42.2, 消息推送端口号为 40924
	host = "0.0.0.0"
	port = 40924
	printing = True
	connection = False
	
	def __init__(self, printing=True):
		self.printing = printing
	
	def connect(self):  # 与机器人控制命令端口建立 UDP 连接
		self.address = (self.host, int(self.port))
		self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		
		if self.printing:
			print("Connecting_UDP...")
		
		self.udp_socket.bind(self.address)
		
		if self.printing:
			print("UDP_Connected!")
	
	def disconnect(self):
		if self.printing:
			print("UDP disconnecting...")
		self.udp_socket.close()
		if self.printing:
			print("UDP disconnected!")
	
	def try_get(self, timeout=5):  # 这个函数默认等待5秒钟，如果在这个时间内没有收到机器人的返回结果，就会立即返回'no_OUT'。如果收到了机器人的返回结果，就会解码并返回结果字符串。
		result = ''
		try:
			# 设置超时时间
			ready = select.select([self.udp_socket], [], [], timeout)
			# print(ready)
			if ready[0]:
				# 如果有可读数据，接收并解码
				# print("hearing...")
				buf = self.udp_socket.recv(1024)
				result = buf.decode('utf-8')
			else:
				result = 'no_OUT'
		
		except socket.error as e:
			if self.printing:
				print("Error receiving :", e)
			
			sys.exit(1)
		
		if self.printing:
			print(result)
		
		return result


def solve_game(msg, printing=True):  # 用于解析赛事数据推送
	result = ''
	if msg[0:14] == 'game msg push ' and msg[-1] == ';':
		# print('right_start')
		info = msg[15:-2]
		# print(info)
		info_list = info.split(', ')
		# print(info_list)
		info_list_int = [int(i) for i in info_list]
		# print(info_list_int)
		result = info_list_int
	else:
		if printing:
			print('please give a game msg push')
	return result


def solve_key(msg, printing=True):  # 用于从赛事数据推送中获得键位
	result = []
	key_n = msg[6]
	if printing:
		print(key_n)
	if key_n != 0:
		keys = msg[0 - key_n:]
		if printing:
			print(keys)
			print(type(keys))
		result = keys
	return result


def solve_key_name(keys):  # 将获得键位转换为真实名称
	result = []
	key_name_list = []
	for key in keys:
		if key >= 48 and key <= 90:
			key_name_list.append(chr(key))
		elif key == 8:
			key_name_list.append("Space")
		elif key == 9:
			key_name_list.append("Tab")
		elif key == 16:
			key_name_list.append("Shift")
		elif key == 17:
			key_name_list.append("Ctrl")
		elif key == 18:
			key_name_list.append("Alt")
		elif key == 20:
			key_name_list.append("Caps")
	result = key_name_list
	return result


def solve_gimbal(msg, printing=True):
	result = ''
	if msg[-1] == ';':
		if printing:
			print('right_start')
		info = msg[:-2]
		if printing:
			print(info)
		info_list = info.split(' ')
		if printing:
			print(info_list)
		info_list_int = [float(i) for i in info_list]
		if printing:
			print(info_list_int)
		result = info_list_int
	else:
		if printing:
			print('please give a gimbal msg push')
	return result


def solve_chassis_position(msg, printing=True):
	result = ''
	if msg[0:22] == 'chassis push position ' and msg[-1] == ';':
		# print('right_start')
		info = msg[22:-3]
		if printing:
			print(info)
		info_list = info.split(' ')
		if printing:
			print(info_list)
		info_list_float = []
		for i in info_list:
			if printing:
				print(i)
			if i != "-0.000" and i != "0.000":
				if printing:
					print("float")
				if i[0] == '-':
					info_list_float.append(-float(i[1:]))
				else:
					info_list_float.append(float(i))
			else:
				info_list_float.append(0)
		if printing:
			print(info_list_float)
		result = info_list_float
	else:
		if printing:
			print('please give a chassis push position push')
	return result


"""
以下为连接TCP,UDP获取赛事引擎数据的示例
"""
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

# -------以上为示例--------
