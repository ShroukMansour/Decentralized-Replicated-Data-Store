from dataStorage import DataStorage

class QueuingModule:

    def __init__(self):
        self.queue = []
        self.data_storage = DataStorage()

    def add_data(self, data):
        self.queue.append(data)
        self.sync_with_datastorage()

    def sync_with_datastorage(self):
        self.data_storage.save(self.queue)
        self.queue = []

