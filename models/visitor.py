class Visitor:
    def __init__(self, name, services):
        self.name = name
        self.services = services

    def print(self):
        print(f'Visitor name : {self.name}')
        print('Visitor services : ')
        for service in self.services:
            print(service)