# using singleton pattern for storing global variables (r, G, M)
class _EarthParameters:
    _self = None

    def __new__(cls, *args, **kwargs):
        if not cls._self:
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        self.r = 6.371 * 10**6       # radius of earth
        self.G = 6.67 * 10 ** (-11)  # gravitational constant
        self.M = 5.97 * 10 ** 24     # mass of earth


earth = _EarthParameters()


# class computes gravitational acceleration on earth depending on altitude
class ComputeGravAcc:

    def __init__(self):
        self.altitude = float(input("Enter altitude in meters: "))
        self.grav_acc = earth.G * earth.M / ((earth.r + self.altitude) ** 2)


grav1 = ComputeGravAcc()

print(grav1.grav_acc)
