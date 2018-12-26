from enum import Enum


class Material(Enum):
    TRADITIONAL = "Traditional"
    DIGITAL = "Digital"

    @staticmethod
    def get_all():
        return [e.value for e in Material]


class Artist:
    def __init__(self, name, material, country):
        self.name = name
        self.country = country
        self.material = material

    def print(self):
        print(f'Name : {self.name}')
        print(f'Material: {"self.material.value"}')
        print(f'Country : {self.country}')
