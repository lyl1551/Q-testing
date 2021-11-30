class buffer:
    # memory as dict = {
    #               int (state key): string (state)
    #           }
    def __init__(self):
        self.memory= {}
        self.memory_size = 0

    def store(self,activity_name, vector):
        # storing state as string?
        self.memory.setdefault(activity_name, []).append(vector)
    def show(self):
        print("current buffer:")
        print(self.memory)
        #self.memory[self.memory_size]=state
        #self.memory_size+=1
        #return self.memory_size-1