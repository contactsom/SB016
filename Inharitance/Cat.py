from Inharitance.Animal import Animal


class Cat(Animal):
    def __init__(self,name,color):
        super().__init__(name)
        self.color=color

    def speak(self): # Override the function from Super/parent Class
        print(f"{self.name} meow")