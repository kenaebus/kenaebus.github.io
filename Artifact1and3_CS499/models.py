class Animal:
    def __init__(self, name, animalType, gender, age, weight, acquisitionDate, acquisitionCountry, trainingStatus, reserved, inServiceCountry):
        self.name = name
        self.animalType = animalType
        self.gender = gender
        self.age = age
        self.weight = weight
        self.acquisitionDate = acquisitionDate
        self.acquisitionCountry = acquisitionCountry
        self.trainingStatus = trainingStatus
        self.reserved = reserved
        self.inServiceCountry = inServiceCountry

    def to_dict(self):
        return self.__dict__

class Dog(Animal):
    def __init__(self, name, gender, age, weight, acquisitionDate, acquisitionCountry, trainingStatus, reserved, inServiceCountry, breed):
        super().__init__(name, "Dog", gender, age, weight, acquisitionDate, acquisitionCountry, trainingStatus, reserved, inServiceCountry)
        self.breed = breed    # no underscore

    def to_dict(self):
        return self.__dict__


class Monkey(Animal):
    def __init__(self, name, gender, age, weight, acquisitionDate, acquisitionCountry, trainingStatus, reserved, inServiceCountry, tailLength, species, height, bodyLength):
        super().__init__(name, "Monkey", gender, age, weight, acquisitionDate, acquisitionCountry, trainingStatus, reserved, inServiceCountry)
        self.tailLength = tailLength    # no underscore
        self.species = species
        self.height = height
        self.bodyLength = bodyLength

    def to_dict(self):
        return self.__dict__


def animal_from_doc(doc):
    if doc['animalType'] == 'Dog':
       return Dog(
            name=doc["name"],
            gender=doc["gender"],
            age=doc["age"],
            weight=doc["weight"],
            acquisitionDate=doc["acquisitionDate"],
            acquisitionCountry=doc["acquisitionCountry"],
            trainingStatus=doc["trainingStatus"],
            reserved=doc["reserved"],
            inServiceCountry=doc["inServiceCountry"],
            breed=doc["breed"]
        )
    elif doc["animalType"] == "Monkey":
        return Monkey(
            name=doc["name"],
            gender=doc["gender"],
            age=doc["age"],
            weight=doc["weight"],
            acquisitionDate=doc["acquisitionDate"],
            acquisitionCountry=doc["acquisitionCountry"],
            trainingStatus=doc["trainingStatus"],
            reserved=doc["reserved"],
            inServiceCountry=doc["inServiceCountry"],
            tailLength=doc["tailLength"],
            species=doc["species"],
            height=doc["height"],
            bodyLength=doc["bodyLength"]
        )
    else:
        return Animal(
            name=doc["name"],
            animalType=doc["animalType"],
            gender=doc["gender"],
            age=doc["age"],
            weight=doc["weight"],
            acquisitionDate=doc["acquisitionDate"],
            acquisitionCountry=doc["acquisitionCountry"],
            trainingStatus=doc["trainingStatus"],
            reserved=doc["reserved"],
            inServiceCountry=doc["inServiceCountry"]
        )