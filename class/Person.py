class Person():
    def __init__(self, name:str, last_name:str, age:int, gender:str):
        self.name = str(name)
        self.last_name = str(last_name)
        try:
            self.age = int(age)
        except ValueError:
            raise ValueError(f'\n{age} is an incorrect data type, it must be an integer.\n')
        self.gender = str(gender)

    def greet(self) -> str:
        print(f'\nWelcome {self.name} {self.last_name}')
        print(f'I see you are {self.age} years old and you are a man.\n')