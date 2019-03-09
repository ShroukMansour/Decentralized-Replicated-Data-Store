import json


class Data:
    def __init__(self, data, size):
        self.data = data
        self.size = size

    def json_data(self):
        return {"data": self.data, "size": self.size}
