class Student(object):
    def __init__(self, age:int, name:str) -> None:
        self.age = age
        self.name = name


class Institute(object):
    def presentInstitute(self):
        print('Study at the Law Institute 112.\n')

class Law(Student, Institute):
    def instroduce(self):
        greeting = f'\nHello, I\'m {self.name}, I have {self.age} years old and I study Law.'
        print(greeting)

student = Law(26, 'Paul')
student.instroduce()
student.presentInstitute()