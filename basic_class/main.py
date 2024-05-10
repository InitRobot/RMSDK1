import connect
import solve
import Chassis_Solve
import time
import os
#import auto_aim
import RobotLiveview
#import tmp_fast2

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
	disk_mode = False
	wait = 0
	TCP.IN_OUT("robot mode free;", printing=True)
	#auto_aim.connect()
	print("connected")
	while True:
		#time.sleep(0.1)
		msg = UDP.try_get(timeout=1,printing=False)
		print(msg)
		#print(msg)
		if msg != "no_OUT":
			msg_solved = solve.solve_game_msg(msg,printing=False)
			if wait > 0:
				wait -= 1
			#print(msg_solved["keys"], "---", wait)
			if "M" in msg_solved["keys"] and wait == 0:
				#print(msg_solved["keys"], "---", wait)
				disk_mode = not disk_mode
				wait = 10
				print("mode_change")
				if not disk_mode:
					pass
			#print(msg_solved)
			
			if "E" in msg_solved["keys"]:
				print("E:auto_aim")
				#auto_aim.auto_aim()
				#os.system('cd ~/RM-yolo/RMSDK && python3 06_final.py')
			
			if disk_mode:
				degree = solve.solve_gimbal(TCP.IN_OUT("gimbal attitude ?;",printing=False),printing=False)
				wheel_output = Chassis_Solve.Disk_solve(TCP,msg_solved["keys"],degree[1],printing = False)
			elif not disk_mode:
				degree = solve.solve_gimbal(TCP.IN_OUT("gimbal attitude ?;",printing=False),printing=False)
				wheel_output = Chassis_Solve.Stright_Solve(TCP,degree[1],msg_solved["keys"],printing = False)
			#print(wheel_output)
			Chassis_Solve.move(TCP,wheel_output,printing = False)
	UDP.disconnect()
	TCP.disconnect()

def video_test():
	print("start")
	TCP = connect.TCP_connection(printing=True)
	TCP_video = connect.TCP_video(printing=True)
	UDP = connect.UDP_connection(printing=True)
	TCP.connect_enter_SDK(printing=True)
	UDP.connect(printing=True)
	TCP_video.connect(printing=True)
	TCP.IN_OUT("game_msg on;",printing=True)
	TCP.IN_OUT("stream on;",printing=True)
	robot = RobotLiveview.RobotLiveview(TCP_video)
	print("connected view")
	robot.display(TCP)
	#tmp_fast2.test()
	while True:
		pass


#------------------------
def solve(x, a, b, c, d):
    y  = ((b-d)/((a-c)**2)) * ((x-c)**2) + d
    return y

x_joints =     [0,   -1.8  , -2.5  ,  -3    , -1.7]
y_joints =     [0,   -1.45 , -2    ,  -3    , -5]
def target_xy(t,mode = 1):
    Flag_move = False
    x_t = 0
    y_t = 0
    if mode == 1:
        Flag_move = True
        point = -1
        point_1 = -1
        time_changes = [3.3,  4    ,  4.7  ,   5.5]
        x_joints =     [0,   -1.8  , -2.5  ,  -3    , -1.7]
        y_joints =     [0,   -1.45 , -2    ,  -3    , -5]
        for t_c in time_changes:
            point_1 += 1
            if t < t_c:
                point = point_1
                break
        if point != -1:
            if point == 0:
                x_t = ((1.8/3.3**2) * (t - 3.3) ** 2 - 1.8)
                y_t = ((-1.45/3.3**2) * t ** 2)
            if point == 1:
                x_t = (-0.8/0.7**2 * (t - 3.3) ** 2 - 1.8)
                y_t = ((2-1.45)/0.7**2 * (t-4) ** 2 - 2)
            if point == 2:
                x_t = solve(t, 4, -2.5, 4.7, -3)
                y_t = solve(t, 4.7, -3, 4, -2)
            if point == 3:
                x_t = solve(t, 5.5, -1.7, 4.7, -3)
                y_t = solve(t, 4.7, -3, 5.5, -5)
        else:
            x_t = x_joints[-1]
            y_t = y_joints[-1]

            
    return Flag_move,x_t,y_t

kp_x = 4
ki_x = 0.01
kd_x = 2

kp_y = 6
ki_y = 0.01
kd_y = 2
#target = 0.5
x_error_list = []
x_target_list = []
x_list = []
x_speed_list = []

y_error_list = []
y_target_list = []
y_list = []
y_speed_list = []

def auto_move():
	print("start")
	TCP = connect.TCP_connection(printing=False)
	UDP = connect.UDP_connection(printing=False)
	TCP.connect_enter_SDK(printing=False)
	UDP.connect(printing=False)
	#TCP.IN_OUT("game_msg on;",printing=False)
	#for i in range(1, 50):
	#disk_mode = False
	#wait = 0
	TCP.IN_OUT("robot mode free;", printing=True)
	TCP.IN_OUT("chassis push position on pfreq 50;",printing=False)
	#auto_aim.connect()
	print("connected")
	
	start_time = time.perf_counter()

	now_time = time.perf_counter() - start_time

	first_step_time = 3.3

	x_last_error = 0
	y_last_error = 0

	x_sum_error = 0
	y_sum_error = 0
	for i in range(1,800):
		#print(i)
		TCP.IN_OUT("chassis push position on pfreq 50;",printing=False)
		now_time = time.perf_counter() - start_time
		Flag,x_target,y_target = target_xy(now_time,mode=1)
		#x_target = ((1.7/3.3**2) * (now_time - 3.3) ** 2 - 1.7)
		x_target_list.append(x_target)
		#y_target = ((-1.45/3.3**2) * now_time ** 2)
		y_target_list.append(y_target)
		msg = Message_Delivery.try_get(timeout = 1,printing=False)
		chassis_position = []
		chassis_position = MSG_Solve.solve_chassis_position(msg,printing=False)
		#print(chassis_position)
		#chassis speed x 0.1 y 0.1 z 1;
		if chassis_position != '':
			x_error = x_target - chassis_position[0]
			x_list.append(chassis_position[0])
			x_error_list.append(x_error)
			x_speed = kp_x * x_error + kd_x * (x_error * 2 - x_last_error) + ki_x * x_sum_error
			y_error = y_target - chassis_position[1]
			y_list.append(chassis_position[1])
			y_error_list.append(y_error)
			y_speed = kp_y * y_error + kd_y * (y_error * 2 - y_last_error) + ki_y * y_sum_error
			#print("--------------",x_speed)
			x_speed_list.append(x_speed)
			y_speed_list.append(y_speed)
			TCP.IN_OUT("chassis speed x " + str(x_speed) + " y " + str(y_speed) + " z 0;",printing=False)
			#TCP.IN_OUT("chassis speed x " + str(x_speed) + " y 0 z 0;",printing=False)
			#TCP.IN_OUT("chassis speed x " + str(x_speed) + " y " + str(y_speed) + " z 0;",printing=False)
			x_sum_error += x_error
			y_sum_error += y_error
			x_last_error = x_error
			y_last_error = y_error

	second_step_time = 5
	TCP.IN_OUT("chassis speed x 0 y 0 z 0;",printing=False)
	#print(error_list)
	print('end')


if __name__ == '__main__':
	#chassis_controll()
	#video_test()
	auto_move()