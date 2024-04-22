import connect
import solve
import Chassis_Solve

def example():
	"""
	以下为连接TCP,UDP获取赛事引擎数据的示例
	"""
	print("start")
	TCP = connect.TCP_connection(printing=False)
	UDP = connect.UDP_connection(printing=False)
	TCP.connect_enter_SDK(printing=False)
	UDP.connect(printing=False)
	TCP.IN_OUT("game_msg on;",printing=False)
	#for i in range(1, 50):
	while True:
		msg = UDP.try_get(timeout=1,printing=False)
		#print(msg)
		if msg != "no_OUT":
			msg_solved = solve.solve_game_msg(msg,printing=False)
			print(msg_solved)
	UDP.disconnect()
	TCP.disconnect()

	# -------以上为示例--------
'''
			msg_solved = solve.solve_game(msg,printing=False)
			if msg_solved[0] == 0:
				keys = solve.solve_key(msg_solved,printing=False)
				keyname = solve.solve_key_name(keys,printing=False)
				print("keynames:", keyname)
			elif msg_solved[0] == 1:
				print("Unknow:",msg_solved)
			else:
				print("-----???-----",msg_solved)'''

def chassis_controll():
	print("start")
	TCP = connect.TCP_connection(printing=False)
	UDP = connect.UDP_connection(printing=False)
	TCP.connect_enter_SDK(printing=False)
	UDP.connect(printing=False)
	TCP.IN_OUT("game_msg on;",printing=False)
	#for i in range(1, 50):
	while True:
		msg = UDP.try_get(timeout=1,printing=False)
		#print(msg)
		if msg != "no_OUT":
			msg_solved = solve.solve_game_msg(msg,printing=False)
			print(msg_solved)
			wheel_output = Chassis_Solve.Stright_Solve(msg_solved["keys"],printing = True)
			Chassis_Solve.move(TCP,wheel_output,printing = True)
	UDP.disconnect()
	TCP.disconnect()


if __name__ == '__main__':
	example()