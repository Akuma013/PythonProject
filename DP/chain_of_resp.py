import math
# for structure was taken the code from https://www.geeksforgeeks.org/chain-of-responsibility-python-design-patterns/
# but code is fully changed with different example (shapes area/volume handler)
class AbstractHandler(object):

    """Parent class of all concrete handlers"""
    side_length = int(input("Enter side length: "))
    def __init__(self, nxt):
        """change or increase the local variable using nxt"""

        self._nxt = nxt

    def handle(self, request):

        """It calls the processRequest through given request"""

        handled = self.processRequest(request)

        """case when it is not handled"""

        if not handled:
            self._nxt.handle(request)

    def processRequest(self, request):

        """throws a NotImplementedError"""

        raise NotImplementedError('First implement it !')


class TriangleArea(AbstractHandler):

    """Concrete Handler # 1: Child class of AbstractHandler"""

    def processRequest(self, request):

        '''return True if request is handled '''

        if request == "triangle":
            print("This is {} handling request '{}'".format(self.__class__.__name__, request))
            print(f"The area of triangle with side {self.side_length} is {self.side_length**2* math.sqrt(3)/4}")
            return True


class SquareArea(AbstractHandler):

    """Concrete Handler # 2: Child class of AbstractHandler"""

    def processRequest(self, request):

        '''return True if the request is handled'''

        if request == "square":
            print("This is {} handling request '{}'".format(self.__class__.__name__, request))
            print(f"The area of square with side {self.side_length} is {self.side_length ** 2}")
            return True


class CubeVolume(AbstractHandler):

    """Concrete Handler # 3: Child class of AbstractHandler"""

    def processRequest(self, request):

        '''return True if the request is handled'''

        if request == "cube":
            print("This is {} handling request '{}'".format(self.__class__.__name__, request))
            print(f"The volume of a cube with side {self.side_length} is {self.side_length ** 3}")
            return True

class DefaultHandler(AbstractHandler):

    """Default Handler: child class from AbstractHandler"""

    def processRequest(self, request):

        """Gives the message that the request is not handled and returns true"""

        print("This is {} telling you that request '{}' has no handler right now.".format(self.__class__.__name__,
                                                                                          request))
        return True


class User:

    """User Class"""

    def __init__(self):

        """Provides the sequence of handles for the users"""

        initial = None

        self.handler = TriangleArea(SquareArea(CubeVolume(DefaultHandler(initial))))

    def agent(self, user_request):

        """Iterates over each request and sends them to specific handles"""

        for request in user_request:
            self.handler.handle(request)

"""main method"""

if __name__ == "__main__":

    """Create a client object"""
    user = User()

    """Create requests to be processed"""

    requests = ["triangle", "circle", "square", "cube", "hexagon"]

    """Send the requests one by one, to handlers as per the sequence of handlers defined in the Client class"""
    user.agent(requests)