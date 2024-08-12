from Person import Person

def createPerson():
    try:
        person = Person('Pablo', 'Pérez', 26, 'Male')
        person.greet()
    except ValueError as error:
        print(error)

createPerson()