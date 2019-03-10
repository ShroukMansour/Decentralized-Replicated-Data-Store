import time
import random

class DataStorage:

    def __init__(self):
        self.hard_disk_sim = []

    def save(self, data):
        time.sleep(random.randint(0, 2))
        self.hard_disk_sim.append(data)
        print("---------> data", data[0].data, " with size ", data[0].size)

    def get_all_data(self):
        return self.hard_disk_sim




