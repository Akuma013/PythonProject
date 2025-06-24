import abc


class AbstractCar(abc.ABC):

    def print_specs(self):
        pass


class Sportcar(AbstractCar):
    def __init__(self):
        self.privod = "forward drive(privod)"
        self.wheels = 4
        self.motor = "manual"

    def print_specs(self):
        print("your car is " + self.privod," with ", self.wheels," wheels and " + self.motor + " motor")


class TruckCar(AbstractCar):
    def __init__(self):
        self.privod = "full drive(privod)"
        self.wheels = 4
        self.motor = "auto"

    def print_specs(self):
        print("your truck is " + self.privod, " with ", self.wheels, " wheels and " + self.motor + " motor")

class AbstractMotorcycle(abc.ABC):

    def print_specs(self):
        pass

class SportBike(AbstractMotorcycle):
    def __init__(self):
        self.privod = "backward drive(privod)"
        self.wheels = 2
        self.motor = "manual"
    def print_specs(self):
        print("your bike is " + self.privod," with ", self.wheels," wheels and " + self.motor + "motor ")

class ElectroBike(AbstractMotorcycle):
    def __init__(self):
        self.privod = "backward drive(privod)"
        self.wheels = 2
        self.motor = "electric"
    def print_specs(self):
        print("your bike is " + self.privod," with ", self.wheels," wheels and " + self.motor + "motor ")


class AbstractManifacturer(abc.ABC):
    @abc.abstractmethod
    def manifacture_car(self):
        pass
    @abc.abstractmethod
    def manifacture_motorcycle(self):
        pass


class ManifactureSportVehicles(AbstractManifacturer):
    def manifacture_car(self):
        return Sportcar()

    def manifacture_motorcycle(self):
        return SportBike()


class ManifactureBasicVehicles(AbstractManifacturer):
    def manifacture_car(self):
        return TruckCar()

    def manifacture_motorcycle(self):
        return ElectroBike()


def run(factory: AbstractManifacturer):
    car = factory.manifacture_car()
    motorcycle = factory.manifacture_motorcycle()
    car.print_specs()
    motorcycle.print_specs()


if __name__ == "__main__":
    factory = None
    text = input("Choose vehicles to make sport/basic: ")

    if text.lower() == "sport":
        factory = ManifactureSportVehicles()
    elif text.lower() == "basic":
        factory = ManifactureBasicVehicles()

    run(factory)

