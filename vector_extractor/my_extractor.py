# 提取xml树，然后转化成树编辑距离
import re
import os


class extractor:
    # 解析xml，返回树
    def parsexml(self, count):
        file = open("C:/lyl/Q-testing/output/xml/" + count + ".xml", "r+")
        tree = file.read()
        tree = re.sub(r"<node", "{", tree)
        tree = re.sub(r"/>", "}", tree)
        tree = re.sub(r"</node>", "}", tree)
        tree = re.sub(r"[^{}]", "", tree)
        file.close()
        return tree
    # 保存树
    def write(self, count, act_name, tree):
        if not (os.path.exists("C:/lyl/Q-testing/output/tree/" + act_name + "/")):
            os.mkdir("C:/lyl/Q-testing/output/tree/" + act_name + "/")
        target = open("C:/lyl/Q-testing/output/tree/" + act_name + "/" + count + ".txt", "w+")
        print("tree= " + tree)
        target.write(tree)
        target.close()

