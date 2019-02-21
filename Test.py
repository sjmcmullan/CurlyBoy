var1 = 'true'
var2 = 'false'

if any([x not in ['true', 'false'] for x in [var1, var2]]):
    print('please enter true or false only')
else:
    print("yay")
