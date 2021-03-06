# Q-testing

## 运行方式

#### System Requirements

- Python: 3.8

- Android SDK: API 20 (make sure `adb` and `aapt` commands are available)

- uiautomator2

  ```
  pip3 install -U uiautomator2
  ```

#### Mobile Requirments

- atx-agent（需连接至电脑端）

  ```
  python3 -m uiautomator2 init
  ```

#### Running

将移动设备连接至电脑，切换至待测应用界面

删除./output/tree和./output/xml下所有文件，仅保留两个文件夹

```
python my_qlearning.py
```



## 运行视频链接：

 https://box.nju.edu.cn/f/410a3682bc9b454fb104/ 

视频太长，没做字幕。建议使用AI字幕软件提高观看体验



## 模块介绍

#### environment

用于强化学习中的重置探索(reset)，由于论文中未提及探索的重置，因此暂未使用

#### memory

按Activity_name分类进行存储，存储当前Activity中所有已知的各不相似的状态

#### extractor

parsexml:    将提取的xml文件解析成控件树（如{{{}}{}}）

write():    在./output/tree中按Activity_name保存控件树

#### output

/xml下存储了每次探索捕获的页面原始xml文件

/tree下按Activity_name保存了所有不相似的控件树

#### agent

**【位于my_qlearning中的一个class】**

self.q_table: 机器人采用Q-learning策略所需要的q_table

self.buffer: 存储（Activitiy_name,vector）的内存部分

learn(): 依据【奖励、新旧Activity名称、新旧状态、action】来更新Q-table

pick_action(): 根据ε-greedy策略，选择出一个执行的动作

#### my_qlearning

代码执行模块，利用了上述4个模块（除environment）

代码细致讲解见视频or见代码注释



#### test.xml

能从移动端获取的xml样例

#### dumpPhone-release.apk

一个可安装的apk文件，可以用于代码运行（安装后打开，再运行代码）

#### 工具复现ppt.pptx

用于视频讲解的ppt，简要介绍了论文内容