import abc

class Transport(abc.ABC):

    def print_specs(self):
        """aaa"""

class Sportcar(Transport):
    def __init__(self):
        self.privod = "forward drive(privod)"
        self.wheels = 4
        self.motor = "manual"
    def print_specs(self):
        print("your car is " + self.privod," with ", self.wheels," wheels and " + self.motor + "motor")
class Motorcicle(Transport):
    def __init__(self):
        self.privod = "backward drive(privod)"
        self.wheels = 2
        self.motor = "manual"
    def print_specs(self):
        print("your car is " + self.privod," with ", self.wheels," wheels and " + self.motor + "motor")


class TransportCreator(abc.ABC):
    @abc.abstractmethod
    def manifacture(self):
        """Factory"""



class SportcarCreator(TransportCreator):
    def manifacture(self):
        return Sportcar()


class MotorcicleCreator(TransportCreator):
    def manifacture(self):
        return Motorcicle()


if __name__ == "__main__":
    factory = None
    text = input("Choose vehicle to make motorcicle/sportcar: ")

    if text.lower() == "sportcar":
        factory = SportcarCreator()
    elif text.lower() == "motorcicle":
        factory = MotorcicleCreator()

    vehicle = factory.manifacture()
    vehicle.print_specs()
    