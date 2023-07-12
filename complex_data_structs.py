# 1 List of person dicts with name, age and list of hobbies
persons = [ {'name': 'Bob', 'age': 32, 'hobbies': ['puzzles', 'food']},
           {'name': 'Pat', 'age': 21, 'hobbies': ['gaming', 'books']},
           {'name': 'Mat', 'age': 22, 'hobbies': ['sleep']} ] 
# 2 Use list comprhension to convert this to a list of names
names = [person['name'] for person in persons ]
print(names)
# 3 Check wheter all persons are older than 20
greater_ages = all([person['age']> 19 for person in persons])
print("All older than 20: ", greater_ages)
# 4 Copy so that you can safely edit the name of the first person
copy_persons = [person.copy() for person in persons]
copy_persons[0]['name'] = "Hector"
print(persons)
print()
print(copy_persons)
# Unpack into diff variables out of the dict
p1, p2, p3 = persons
print(f'p1: {p1}\np2: {p2}\np3: {p3}\n')