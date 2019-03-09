import json


class Data:
    def __init__(self, data, size, synced=False):
        self.data = data
        self.size = size
        self.synced = synced
        self.synced_with = []

    def json_data(self):
        return {"data": self.data, "size": self.size}

    def sync_with_peer(self, peer):
        self.synced_with.append(peer)
