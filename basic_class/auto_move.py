import time
import math


class Root:
    p_type_list = []  # 各阶段的移动种类；0:X,1:|,2:-,3:7,4:r,5:L,6:J
    p_parameter_list = []  # 各阶段的移动种类的参数；0:0,1:down,2:left,3:R,4:R,5:R,6:R,7:up,8:right
    p_dis_list = []  # 各阶段的移动距离
    time_cnt_list = [0]  # 各阶段累计时间

    def __init__(self, p_type, p_parameter, speed):
        self.p_type_list = p_type
        self.p_parameter_list = p_parameter
        self.speed = speed
        i = 0
        for type_ in self.p_type_list:  # 更新距离与时间
            parameter_ = self.p_parameter_list[i]
            if 2 < type_ < 7 or 9 < type_ < 13:
                dis = math.pi * parameter_ / 2
                self.p_dis_list.append(dis)
                self.time_cnt_list.append(self.time_cnt_list[len(self.time_cnt_list) - 1] + dis / speed)
            else:
                dis = self.p_parameter_list[i]
                self.p_dis_list.append(dis)
                self.time_cnt_list.append(self.time_cnt_list[len(self.time_cnt_list) - 1] + dis / speed)
            i += 1

    def get_stage(self, t):
        i = 0
        for time_stage in self.time_cnt_list:
            if time_stage > t:
                # print("end", i)
                break
            i += 1
        # print(self.time_cnt_list)
        try:
            degree = math.pi / 2 * (self.time_cnt_list[i] - t) / (self.time_cnt_list[i] - self.time_cnt_list[i - 1])
        except IndexError:
            print("IndexError")
            return False
        print("degree", degree)
        if self.p_type_list[i - 1] == 1:  # down ok
            return math.pi * 1
        elif self.p_type_list[i - 1] == 2:  # left ok
            return math.pi * 0.5
        elif self.p_type_list[i - 1] == 3:  # down 7 ok
            return math.pi - degree
        elif self.p_type_list[i - 1] == 4:  # down r ok
            return math.pi + degree
        elif self.p_type_list[i - 1] == 5:  # down l ok
            return 0.5 * math.pi + degree
        elif self.p_type_list[i - 1] == 6:  # down j ok
            return 1.5 * math.pi - degree
        elif self.p_type_list[i - 1] == 7:  # up
            return 0
        elif self.p_type_list[i - 1] == 8:  # right
            return math.pi * 1.5
        elif self.p_type_list[i - 1] == 9:  # up 7
            return 1.5 * math.pi + degree
        elif self.p_type_list[i - 1] == 10:  # up r
            return 0.5 * math.pi - degree
        elif self.p_type_list[i - 1] == 11:  # up l
            return math.pi - degree
        elif self.p_type_list[i - 1] == 12:  # up j
            return 1.5 * math.pi - degree
        print("no_move")
        return False


class Auto:
    kp_x = 4
    ki_x = 0.01
    kd_x = 2

    kp_y = 6
    ki_y = 0.01
    kd_y = 2

    # type_list = [1, 6, 4, 1, 6, 5]
    type_list = [7, 8]
    parameter_list = [1, 1]
    # parameter_list = [0.3, 2.2, 1, 0.5, 1, 0.5]
    speed = 1

    def __init__(self, tcp, printing=True):  #
        self.tcp = tcp
        self.tcp.IN_OUT("robot mode free;", printing=printing)
        # self.tcp.IN_OUT("chassis push position on pfreq 50;", printing=printing)
        self.root = Root(self.type_list, self.parameter_list, self.speed)

    def move(self, printing=True):
        moving = True
        start_time = time.perf_counter()
        while moving:
            now_time = time.perf_counter() - start_time
            print("time:-------", now_time)
            dir_ = self.root.get_stage(now_time)
            print(round(dir_ / math.pi * 180, 2))
            x = self.speed * math.sin(dir_)
            y = self.speed * math.cos(dir_)
            self.tcp.IN_OUT("chassis speed x " + str(y) + " y " + str(x) + ";", printing=printing)
            # print(result)
            print("dir", dir_)
            if not dir_:
                moving = False
            # time.sleep(0.1)
        return True


if __name__ == "__main__":
    auto = Auto()
    result = auto.move()
    print("result", result)
