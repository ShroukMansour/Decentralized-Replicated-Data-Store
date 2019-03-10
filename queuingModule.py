import random

from dataStorage import DataStorage
from data import Data
class QueuingModule:

    def __init__(self, data_storage):
        self.queue = []
        self.data_storage = data_storage
        self.total_amount = 30
        self.avail_amount = self.total_amount

    def add_data(self, data, synced=False):
        if data['size'] <= self.avail_amount:
            self.avail_amount -= data['size']
            for item in data['data']:
                self.queue.append(Data(item['data'], item['size'], synced))
                self.sync_with_datastorage()
        else:
            print('---Sorry queue is full wait for some time')

    def sync_with_datastorage(self):
        self.data_storage.save(self.queue)
        self.queue = []
        self.avail_amount = self.total_amount

    def get_avail_amount(self):
        return self.avail_amount

