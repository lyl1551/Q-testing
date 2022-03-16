# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cmd_out = os.popen("uiautomator2 current")
    cmd_out.readline()  # {
    cmd_out.readline()  # package
    new_activity_name = cmd_out.readline().strip()
    new_activity_name = new_activity_name[13:len(new_activity_name) - 1]
    print(new_activity_name)
    new_activity_name = new_activity_name[new_activity_name.rfind(".") + 1:]
    if new_activity_name.endswith("\""):
        new_activity_name = new_activity_name[:-1]
    print("current activity = " + new_activity_name)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
