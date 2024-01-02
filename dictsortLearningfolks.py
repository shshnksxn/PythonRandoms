dict1 = { 'a':5,'b': [1,2,{'a':100,'b':100}], 'dict 2' : {'a':3,'b':5}}

Solution: 
dict1 = { 'a':5,'b': [1,2,{'a':100,'b':100}], 'dict 2' : {'a':3,'b':5}}
def recurse(dict):
     if type(dict) == type({}):
        for key in dict:
            recurse(dict[key])
    elif type(dict) == type([]):
        for element in dict:
            if type(element) == type({}):
               recurse(element)
            else:
                print element
    else:
        print dict
recurse(dict1)
