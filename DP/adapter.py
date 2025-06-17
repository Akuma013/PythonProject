class MetricSys:
    def __init__(self, speed):
        self.speed = speed

    def showSpeed_kph(self):
        return self.speed


class ImperialSys:
    def __init__(self, speed):
        self.speed = speed

    def showSpeed_mph(self):
        return self.speed


class Adapter(ImperialSys, MetricSys):
    def showSpeed_kph(self):
        self.speed = self.speed * 1.60934
        return self.speed


metricSys = MetricSys(399)
print("Your speed is " + str(metricSys.showSpeed_kph()) + "kph")

# not adapted class will show speed in mph
ImperialSys = ImperialSys(250)
print("Your speed is " + str(ImperialSys.showSpeed_mph()) + "mph")

# using adapter DP to convert speed to metric system (kph)
Adapter = Adapter(250)
print("Your speed is " + str(Adapter.showSpeed_kph()) + "kph")
