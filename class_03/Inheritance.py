class Student(): # We create the parent class
    def __init__(self, age:int, name:str) -> None:
        self.age = age
        self.name = name

class Law(Student): # We crate a child class, this class inherits from the parent class
    def introduce(self):
        greeting = f'\nHello, I am {self.name}, I have {self.age} years old and I study law.\n'
        print(greeting)


student = Law(26, 'Pablo')

student.introduce()