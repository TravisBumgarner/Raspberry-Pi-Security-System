import os

class File_Manager():
    def __init__(self,offline_directory):
        self.offline_directory = offline_directory
        offline_file_list = [f for f in os.listdir(offline_directory) if os.path.isfile(os.path.join(offline_directory, f))]
        self.queue = offline_file_list
        self.last_pop = None
        self.size = len(self.queue)

    def print_file_list(self):
        print(self.queue)

    def enqueue(self,file_name):
        self.queue.insert(0,file_name)
        self.size += 1

    def dequeue(self):
        if self.size != 0:
            self.last_pop = self.queue.pop()
            f_src = os.path.abspath(self.offline_directory) + "/" + self.last_pop
            os.remove(f_src)
            self.size -= 1

    def get_next(self):
        return self.queue[-1]





