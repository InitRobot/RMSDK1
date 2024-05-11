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
            if 2 < type_ < 7:
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
            return False
        if self.p_type_list[i - 1] == 1:
            return math.pi * 1
        elif self.p_type_list[i - 1] == 2:
            return math.pi * 0.5
        elif self.p_type_list[i - 1] == 3:
            return 2 * math.pi - 1 / math.tan(degree)
        elif self.p_type_list[i - 1] == 4:
            return 1 / math.tan(degree)
        elif self.p_type_list[i - 1] == 5:
            return math.pi - 1 / math.tan(degree)
        elif self.p_type_list[i - 1] == 6:
            return math.pi + 1 / math.tan(degree)
        elif self.p_type_list[i - 1] == 7:
            return 0
        elif self.p_type_list[i - 1] == 8:
            return math.pi * 1.5
        return False


class Auto:
    kp_x = 4
    ki_x = 0.01
    kd_x = 2

    kp_y = 6
    ki_y = 0.01
    kd_y = 2

    type_list = [1]
    parameter_list = [0.5]
    speed = 0.5

    def __init__(self, tcp, printing=True):  #
        self.tcp = tcp
        self.tcp.IN_OUT("robot mode free;", printing=printing)
        #self.tcp.IN_OUT("chassis push position on pfreq 50;", printing=printing)
        self.root = Root(self.type_list, self.parameter_list, self.speed)

    def move(self, printing=True):
        moving = True
        start_time = time.perf_counter()
        while moving:
            now_time = time.perf_counter() - start_time
            # print("time:-------", now_time)
            dir_ = self.root.get_stage(now_time)
            print(dir_)
            x = self.speed * math.sin(dir_)
            y = self.speed * math.cos(dir_)
            self.tcp.IN_OUT("chassis move x " + str(x) + " y " + str(y) + ";", printing=printing)
            if not dir_:
                moving = False
            # time.sleep(0.1)
        return True


if __name__ == "__main__":
    auto = Auto()
    result = auto.move()
    print("result", result)
