import os
from uiautomator import Device


class qt_Environment():
    def __init__(self):
        1

    def reset(self):
        cmd = 'return to the beginning ? how ? '
        cmd = ''
        os.system(cmd)
        state_key = 1
        return state_key

    def step(self, action):
        Device.click()
        return 0

    def parse_state(self, state):
        # ignore things like text
        return state
