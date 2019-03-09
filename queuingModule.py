from dataStorage import DataStorage
from data import Data
class QueuingModule:

    def __init__(self, data_storage):
        self.queue = []
        self.data_storage = data_storage

    def add_data(self, data, synced=False):
        self.queue.append(Data(data['data'], data['size'], synced))
        self.sync_with_datastorage()

    def sync_with_datastorage(self):
        self.data_storage.save(self.queue)
        self.queue = []

