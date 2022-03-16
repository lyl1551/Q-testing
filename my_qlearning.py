import os

import numpy as np
import random
import time
from environment import my_env
from memory import memory_buffer
from vector_extractor import my_extractor
from collections import defaultdict

import uiautomator2 as u2


class Q_Learning_Agent:
    def __init__(self):
        # 在主界面触发back会退出待测软件
        self.system_actions = ["volume_up", "volume_down", "back"]
        self.learning_rate = 0.99
        self.discount_factor = 0.9
        self.epsilon = 0.2
        # <<1>> q_table = ∅
        # self.q_table = {}
        self.q_table = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        '''
        三重字典:
        structure:
            qtable = {
                activity_name1:{
                    [int] state1:{ 
                              (key = count)
                        [int] action1:(s,a)Reward1
                              action2:(s,a)Reward2
                    }
                    state2:{ key = count
                        action1:
                        ...
                    }
                }
                activity_name2:{
                    state1:{ key = count
                        action1:(s,a)Reward1
                        action2:(s,a)Reward2
                    }
                    state2:{ key = count
                        action1:
                        ...
                    }
                }
            
            }
        '''

        # <<2>> memory buffer = ∅
        self.memory_buffer = memory_buffer.buffer()
        '''
        structure:
            memory = {
                activity1: [vector1, vector2, vector3]
                activity2: [vector1, vector2, vector3]
            }
        '''

    def learn(self, activity_name, new_activity_name, state_key, next_state_key, action, reward):
        state_key = int(state_key)
        next_state_key = int(next_state_key)
        action = int(action)
        # 原始公式：
        # new_q = old_q + self.learning_rate *
        #   (reward + self.discount_factor * max(self.q_table[activity_name][next_state_key]) - old_q)
        # 把第一次执行的1000奖励值去掉
        if self.q_table[activity_name][state_key][action] == 1000:
            print("delete first time execute reward")
            self.q_table[activity_name][state_key][action] = 0

        old_q = self.q_table[activity_name][state_key][action]
        future = 0
        if self.q_table.__contains__(new_activity_name):
            if self.q_table[new_activity_name].__contains__(next_state_key):
                future = max(self.q_table[new_activity_name][next_state_key].values())
            else:
                future = 1000
        else:
            future = 1000
        new_q = old_q + self.learning_rate * (reward + self.discount_factor * future - old_q)
        self.q_table[activity_name][state_key][action] = new_q

    # 在指定的activity和state下，选择出一个动作
    def pick_action(self, activity, state, ui_event_num):
        """
                action              probability
        Q(s,a) with max reward          1-ε
            random UI event             ε/2
            random system event         ε/2

        """
        random_number = np.random.rand()
        if random_number < self.epsilon:
            if random_number < self.epsilon / 2:
                # choose random UI_event
                action = str(np.random.randint(1, ui_event_num))
            else:
                # choose random system_event
                action = self.system_actions[np.random.randint(0, 2)]
        else:
            # choosing from q_table
            max_value = max(self.q_table[activity][state].values())
            candidate_list = []
            # find the state_key with max reward
            for key, value in self.q_table[activity][state].items():
                if value == max_value:
                    candidate_list.append(key)
            action = str(candidate_list[np.random.randint(0, len(candidate_list))])
        return action


if __name__ == "__main__":
    # 暂时没做自动清空
    # env = my_env.qt_Environment()
    agent = Q_Learning_Agent()
    ext = my_extractor.extractor()
    d = u2.connect()
    # How long (in seconds) will wait for a new command from the client
    # before assuming the client quit and ending the uiautomator service
    # set to 2 hour
    d.set_new_command_timeout(7200)
    '''
    print("starting apk")
    apk_path = "C:/Users/LYL/Desktop/Qtesting/dumpPhone-release.apk"
    os.system("adb install " + apk_path)
    print("please open app manually")
    time.sleep(10)
    '''
    '''
    暂未实现自动化打开软件
    '''
    '''
    cmd_out = os.popen("uiautomator2 current")
    cmd_out.readline(); #第一行的{
    package_name = cmd_out.readline().strip()[13:len(cmd_out.readline().strip())-2]
    print("package name = "+package_name)
    activity_name = cmd_out.readline().strip()[13:len(cmd_out.readline().strip())-2]
    print()
    cmd_out.readlines()
    os.system("adb shell am start " + package_name)
    '''

    # xml count = total state number = 已探索的总状态数
    xml_count = 0
    new_activity_name = ""
    old_activity_name = ""
    new_tree = ""
    current_state = 0

    # <<3>> state, activity = getCurrentState()
    # get xml structure
    xml_path = "./output/xml/" + str(xml_count) + ".xml"
    xml = d.dump_hierarchy()
    file = open(xml_path, "w", encoding="utf-8")
    file.write(xml)
    file.close()
    # get new_activity_name
    cmd_out = os.popen("uiautomator2 current")
    cmd_out.readline()  # {
    cmd_out.readline()  # package
    new_activity_name = cmd_out.readline().strip()
    new_activity_name = new_activity_name[13:len(new_activity_name) - 1]
    new_activity_name = new_activity_name[new_activity_name.rfind(".") + 1:]
    if new_activity_name.endswith("\""):
        new_activity_name = new_activity_name[:-1]
    print("current activity = " + new_activity_name)
    cmd_out.readlines()

    # <<4>> vector = extractVectors(state)
    # vector = current state
    vector = current_state
    # 将提取的xml转化为树,如{{}{{}}}
    new_tree = ext.parsexml(str(vector))
    ext.write(str(vector), new_activity_name, new_tree)
    # <<5>> memoryBuffer = mB ∪ (activity, vector)
    # 在buffer中存储该activity和对应vector
    agent.memory_buffer.store(new_activity_name, vector)
    agent.memory_buffer.show()

    current_state = xml_count
    next_state = xml_count
    print("starting loop")
    # <<6>> while !timeout:
    for i in range(0, 10):
        '''
        还没确定什么时候reset，如何reset
        if(i == 100):
            state_key = env.reset()
        '''
        # 没有设置break出while循环的条件: 1）timeout 2)reset
        # 需要手动停止 或者把最后一行的break的注释去掉
        while True:
            time.sleep(2)
            for j in range(0, 4):
                print()

            # <<7>> state t = state t+1
            # current_state = next_state

            # <<8>> A = getOrInferEvents(Q_table, state t)
            # element = list[]，暂时只实现了点击
            element = d(clickable=True)
            print("element =")
            for n in range(0, len(element)):
                print(element[n].get_text())
            ele_size = len(element)
            print("element number:" + str(ele_size))

            if ele_size == 0:
                d.press("back")
                continue
            else:
                current_state = next_state

            # 如果是新状态，就需要更新Q-table
            # 如果是已有状态，就不需要更新，直接在下一步里找
            if current_state == xml_count:
                for i in range(0, ele_size):
                    agent.q_table[new_activity_name][current_state][i] = 1000
                # agent.q_table.setdefault(new_activity_name, {})
                # state_dict = {}
                # # 第一次做 unexecuted actions 的奖励 = 1000，做完被归零
                # for i in range(0, ele_size):
                #     state_dict[i] = 1000
                # agent.q_table[new_activity_name][current_state] = state_dict
            print("Q-table:")
            print(agent.q_table[new_activity_name][current_state])

            while True:
                try:
                    # <<9>> action t = getAction(Q_table, state t)
                    # action = "1" or "volume_up",类型为string
                    action = agent.pick_action(new_activity_name, current_state, ele_size)

                    # <<10>> state t+1, activity t+1 = execute(action)

                    # 如果是UI event，就直接点击对应的widget
                    if action.isdigit():
                        print("picking ui event:" + action)
                        element[int(action)].click()
                    # 如果是系统事件，则press
                    else:
                        print("picking system event:")
                        d.press(action)
                    break
                except:
                    print("UIOBJECT NOT FOUND, RETRYING...")
                    time.sleep(1)

            xml_count = xml_count + 1
            # 保存跳转前的activity name
            old_activity_name = new_activity_name
            # 获得新状态的new_activity_name
            cmd_out = os.popen("uiautomator2 current")
            cmd_out.readline()  # {
            cmd_out.readline()  # package
            new_activity_name = cmd_out.readline().strip()
            new_activity_name = new_activity_name[13:len(new_activity_name) - 1]
            new_activity_name = new_activity_name[new_activity_name.rfind(".") + 1:]
            if new_activity_name.endswith("\""):
                new_activity_name = new_activity_name[:-1]
            print("current activity = " + new_activity_name)
            cmd_out.readlines()
            # 获得新的xml
            xml_path = "./output/xml/" + str(xml_count) + ".xml"
            xml = d.dump_hierarchy()
            file = open(xml_path, "w", encoding="utf-8")
            file.write(xml)
            file.close()

            # <<11>> new_vector = extractVectors(new_state)
            vector = xml_count
            new_tree = ext.parsexml(str(xml_count))
            print("similarity calculation")

            # <<12>> for all(activity t+1, vector)∈ Memory buffer:
            # <<13>>     distance = calculate_distance(vector, new_vector)
            # <<14>>     similarity = min(similarity, distance)
            # <<15>>     end for
            # <<16>> if similarity >= threshold:
            # <<17>>     reward = small reward
            # <<18>> else :
            # <<19>>     memoryBuffer = mB ∪ (activity t+1, new_vector)
            # <<20>>     reward = large_reward
            # <<21>> end if

            # 应该放在这里的相似度对比
            similarity = 0
            max_sim = 0
            reward = 0
            potential_skip_obj = ""
            # 比较当前activity中所有tree与当前tree的相似度
            # 如果Activity文件夹都不存在，说明是新的Activity，直接存储
            # if not (os.path.exists("C:/lyl/Q-testing/output/tree/" + new_activity_name + "/")):
            #     os.mkdir("C:/lyl/Q-testing/output/tree/" + new_activity_name + "/")
            if not (os.path.exists("./output/tree/" + new_activity_name + "/")):
                os.mkdir("./output/tree/" + new_activity_name + "/")
                agent.memory_buffer.store(new_activity_name, vector)
                ext.write(str(vector), new_activity_name, new_tree)
                next_state = xml_count
                reward = 500
                print("New activity found!")
            # 如果Activity文件夹存在，就先对比，再考虑是否进行存储
            else:
                print("No new activity, calculating similarity")
                for root, dirs, files in os.walk("./output/tree/" + new_activity_name):
                    for trees in files:
                        existing_tree_file = open("./output/tree/" + new_activity_name + "/" + trees)
                        compared_tree = existing_tree_file.readline().strip()
                        existing_tree_file.close()
                        cmd_out = os.popen("python -m apted -t " + new_tree + " " + compared_tree)
                        edit_distance = int(cmd_out.readline().strip())
                        print("get edit_distance:" + str(edit_distance))
                        # 相似度 = 1 - d/max(n1,n2)，n1n2节点数 = 处理后树的长度除2
                        # 相似度需要与编辑距离同步更新
                        # ??? 究竟是最小的还是最大的
                        # a)最大相似度都小于x 【暂用】
                        # b)最小相似度都大于x
                        similarity = 1 - (2 * edit_distance) / max(len(new_tree), len(compared_tree))
                        # print("similarity = " + str(similarity))
                        if similarity > max_sim:
                            potential_skip_obj = trees
                            max_sim = similarity
                print("max similarity = " + str(max_sim))
                if max_sim < 1:
                    agent.memory_buffer.store(new_activity_name, vector)
                    ext.write(str(vector), new_activity_name, new_tree)
                    next_state = xml_count
                    reward = 500
                else:
                    # potential_skip_obj = "0.txt"
                    next_state = int(potential_skip_obj[0:len(potential_skip_obj) - 4])
                    reward = -500

            # print current info
            agent.memory_buffer.show()
            print("old act = " + old_activity_name)
            print("new act = " + new_activity_name)
            print("old state = " + str(current_state))
            print("new state = " + str(next_state))
            print("action = " + action)
            print("reward = " + str(reward))
            print("xml count = " + str(xml_count))

            # <<21>>
            # update q_table
            if action.isdigit():
                agent.learn(old_activity_name, new_activity_name, current_state, next_state, action, reward)
                print("learning...")
            print("Q-table:")
            print(agent.q_table)

            # if done:
            #    break
            # break
