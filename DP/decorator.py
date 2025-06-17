class SandwichMaker:
    def make_sandwich(self):
        return "Making a basic sandwich"


class SandwichDecorator:
    _sandwich_maker: SandwichMaker = None

    def __init__(self, sandwich_maker):
        self._sandwich_maker = sandwich_maker

    def make_sandwich(self):
        return self._sandwich_maker.make_sandwich()


class SauceDecorator(SandwichDecorator):
    def make_sandwich(self):
        return self._sandwich_maker.make_sandwich() + " with sauce"


class TomatoDecorator(SandwichDecorator):
    def make_sandwich(self):
        return self._sandwich_maker.make_sandwich() + " with tomato"


class OnionDecorator(SandwichDecorator):
    def make_sandwich(self):
        return self._sandwich_maker.make_sandwich() + " with onion"


sandwich_maker = SandwichMaker()

sandwich_with_sauce = SauceDecorator(sandwich_maker)

sandwich_with_sauce_tomato = TomatoDecorator(sandwich_with_sauce)

sandwich_with_sauce_tomato_onion = OnionDecorator(sandwich_with_sauce_tomato)

print(sandwich_with_sauce_tomato_onion.make_sandwich())

