from Inharitance.Animal import Animal


class Dog(Animal):
    def __init__(self,name,breed):
        super().__init__(name)
        self.breed=breed

    def speak(self): # Override the function from Super/parent Class
        print(f"{self.name} Bark")