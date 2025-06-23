from abc import ABC, abstractmethod

class ComputerBuilder(ABC):
    @abstractmethod
    def add_cpu(self):
        pass
    @abstractmethod
    def add_memory(self):
        pass
    @abstractmethod
    def add_disk(self):
        pass
    @abstractmethod
    def add_gpu(self):
        pass
    @abstractmethod
    def get_product(self):
        pass

class GamingPCBuilder(ComputerBuilder):
    def __init__(self):
        self.reset()

    def reset(self):
        self._comuter = Computer()

    def add_cpu(self):
        self._comuter.add("AMD Ryzen 9800X3D")

    def add_memory(self):
        self._comuter.add("32GB DDR5 RAM 5600MHz")

    def add_gpu(self):
        self._comuter.add("Nvidia RTX 5090")

    def add_disk(self):
        self._comuter.add("Samsung Nvme 2T ssd drive")

    def get_product(self):
        product = self._comuter
        self.reset()
        return product

class Computer:
    def __init__(self):
        self.parts = []

    def add(self, part):
        self.parts.append(part)

    def show_parts(self):
        print("Computer's parts: ", ", ".join(self.parts))


class ComputerDirector:
    def __init__(self):
        self._builder = None
        self._builder: ComputerBuilder

    @property
    def builder(self) -> ComputerBuilder:
        return self._builder

    @builder.setter
    def builder(self, builder: ComputerBuilder):
        self._builder = builder

    def build_basic_computer(self):
        self.builder.add_cpu()
        self.builder.add_disk()

    def build_gaming_computer(self):
        self.builder.add_cpu()
        self.builder.add_gpu()
        self.builder.add_disk()


if __name__ == "__main__":
    director = ComputerDirector()
    builder = GamingPCBuilder()
    director.builder = builder

    print("Building Basic Computer:")
    director.build_basic_computer()
    builder.get_product().show_parts()

    print("\nBuilding Gaming Computer:")
    director.build_gaming_computer()
    builder.get_product().show_parts()

    print("\nCustom Build:")
    builder.add_cpu()
    builder.add_gpu()
    builder.get_product().show_parts()
