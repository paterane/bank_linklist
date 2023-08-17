import pymongo

Com = pymongo.MongoClient('localhost', 27017)
db = Com['bank']
col = db['users']


class Linklist:
    def __init__(self, start:bool=True):
        self.__next = None
        if start:
            uList:list = col.find({}, {'_id':0})
            for profile in uList:
                self.loadCol(profile)

    def terminate(self):
        db.drop_collection(col)
        current = self.__next
        while current != None:
            col.insert_one(current.data)
            current = current.__next

    def loadCol(self, col:dict):
        current = self.__next
        if current == None:
            self.__next = Node(col)
        else:
            current.loadCol(col)  


    def insertCol(self, data:dict):
        current = self.__next
        if current == None:
            self.__next = Node(data)
        else:
            current.insertCol(data)
    
    def deleteCol(self, data:dict):
        current = self.__next
        if current != None:
            if current.existed(data):
                self.__next = current.__next
            else:
                current.deleteCol(data)

    def searchCol(self, data:dict):
        current = self.__next
        if current != None:
            if current.existed(data):
                return current.data
            else:
                return  current.searchCol(data)
        else:
            return {}

    def updateCol(self, search:dict, update:dict):
        current = self.__next
        if current != None:
            if current.existed(search):
                self.__next.data.update(update)
                return self.__next.data
            else:
                return current.updateCol(search, update)
        else:
            return {}

    def existed(self, data:dict):
        found:bool = False
        for ukey in data.keys():
            for dkey in self.data.keys():
                if ukey == dkey:
                    if data[ukey] == self.data[dkey]:
                        found = True
                        break
            else:
                found = False
        return found

class Node(Linklist):
    def __init__(self, data:dict):
        self.data:dict = data
        super().__init__(start=False)




# Module Test
if __name__ == "__main__":
    db = Linklist()
    db.insertCol({'name': 'Peter'})
    db.insertCol({'name': 'Merry'})
    db.insertCol({'name': 'katty'})
    db.deleteCol({'name': 'Merry'})
    db.insertCol({'name': 'Rano'})
    found = db.searchCol({'name': 'Peter'})
    db.updateCol({'name': 'Rano'}, {'age': 21})
    col = db.searchCol({'name': 'Rano'})
    print()