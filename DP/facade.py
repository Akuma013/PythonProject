class TV:
     def on(self):
         print("TV is ON")

     def off(self):
         print("TV is OFF")


class DVDPlayer:
     def on(self):
        print("DVD Player is ON")

     def play(self, movie):
         print(f"Playing movie: {movie}")

     def off(self):
         print("DVD Player is OFF")


class SoundSystem:
     def on(self):
         print("Sound system is ON")

     def set_volume(self, level):
         print(f"Volume set to {level}")

     def off(self):
         print("Sound system is OFF")


# Facade

class HomeTheaterFacade:
     def __init__(self):
         self.tv = TV()
         self.dvd = DVDPlayer()
         self.sound = SoundSystem()

     def watch_movie(self, movie):
         print("Starting movie...")
         self.tv.on()
         self.sound.on()
         self.sound.set_volume(5)
         self.dvd.on()
         self.dvd.play(movie)

     def end_movie(self):
         print("Shutting down the movie theater...")
         self.tv.off()
         self.dvd.off()
         self.sound.off()


home_theater = HomeTheaterFacade()
home_theater.watch_movie("Harry Potter")
home_theater.end_movie()

