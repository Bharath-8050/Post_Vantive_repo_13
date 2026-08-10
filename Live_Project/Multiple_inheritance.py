class Car:
    def Maruthi(self):
        print("Maruthi")
    def A(self):
        print("B")

class Music:
    def dol(self):
        print("Dol")
    def A(self):
        print("A")

class Fish(Car,Music):
    def fresh_fish(self):
        print("Emporrot")

fish = Fish()
music = Music()
car = Car()


fish.fresh_fish()
fish.dol()
fish.Maruthi()
fish.A()

