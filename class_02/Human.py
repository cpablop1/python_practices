class Human(): # We created the Human class
    def __init__(self, age:int, name:str, profession:str) -> None: # We define the age and name attribute
        self.age = age
        self.name = name
        self.profession = profession
    # We define a method to present
    def introduce(self):
        greeting = '\nHello I {}, I have {} years old end my profession is {}\n'
        print(greeting.format(self.name, self.age, self.profession))


person = Human(26, 'Pablo', 'Developer') # Person is an instance of the Human class

person.introduce()