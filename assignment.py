# ASSIGNMENT - SECTION 4
#
# persons = [{'name': 'Arnav', 'age': 18, 'hobbies': 'guitar, cricket'},
#           {'name': 'Avni', 'age': 13, 'hobbies': 'music, dance'},
#           {'name': 'Mo', 'age': 45, 'hobbies': 'cooking, family'}]
#
# print(persons)
#
# person_names = [p['name'] for p in (persons)]
# print(person_names)
#
# age_check = all(p['age'] > 20 for p in persons)
# print(age_check)
#
#
# persons_copy = [person.copy() for person in persons]
# persons_copy[0]['name'] = 'Munnu'
# print(persons_copy)
# print(persons)
# a, b, c = persons
# print(a)
# print(b)
# print(c)




# ASSIGNMENT - SECTION 5
#
# def normal_function(func):
#     print(func(5))
#
# normal_function(lambda p: 2*p)
#
#
# def normal_function2(func, *args):
#     for arg in args:
#         print(func(arg))
#
# normal_function2(lambda p: 2*p, 4, 9, 2, 3)
#
#
# def normal_function3(func, *args):
#     for arg in args:
#         print('Result: {:^20.2f} '.format(func(arg)))
#
# normal_function3(lambda p: 2*p, 4, 9, 2, 3)




#ASSIGNMENT - SECTION 6
#
# import random as rn
# import datetime as dt
#
# n1 = rn.random()
# n2 = rn.uniform(1,10)
# print(n1, n2)
#
# unique_value = dt.datetime.now()
# ru = str(n1) + str(unique_value)
# print(ru)


# ASSIGNMENT - SECTION 7
# 1) Write a short Python script which queries the user for input (infinite loop with exit possibility) and writes the input to a file.

# import json
# import pickle

# input_list = []

# script = True
# while script:
#     inp = input('1. More input, 2. Output data, 3. End  ')

#     if inp == '1':
#         user_input = input('Enter data: ')
#         input_list.append(user_input)
#         with open('assignment.p', mode = 'wb') as f:
#           f.write(pickle.dumps(input_list))  
#         #   f.write('\n')

#     elif inp == '2':
#         with open('assignment.p', mode = 'rb') as f:
#             file_content = pickle.loads(f.read())
#             for line in file_content:
#                 print(line)

#     elif inp == '3':
#         script = False

# class Food:
#     def __init__(self, name, kind):
#         self.name = name
#         self.kind = kind

#     def describe(self):
#         print('Name: {}, Kind: {}'.format(self.name, self.kind))

# banana = Food('Banana', 'fruit')
# chicken = Food('Chicken', 'meat')

# banana.describe()
# chicken.describe()

    

    


