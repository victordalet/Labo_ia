import json


class Data:
    def __init__(self,src):
        self.src = src

    def get_data(self):
        with open(self.src) as read_file:
            data = json.load(read_file)
        print(data)
        return data

    def give_data(self,data):
        with open(self.src , "w") as fp:
            json.dump(data,fp)

