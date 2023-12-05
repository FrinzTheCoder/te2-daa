# generating dataset if not exists

'''
DYNAMIC PROGRAMMING
'''
# small
with open('dp_small.graph','w') as f:
    for i in range(1,3334):
        f.write(f'{3*i-1} {3*i} {3*i+1}\n')

# medium
with open('dp_medium.graph','w') as f:
    for i in range(1,33334):
        f.write(f'{3*i-1} {3*i} {3*i+1}\n')

# large
with open('dp_large.graph','w') as f:
    for i in range(1,333334):
        f.write(f'{3*i-1} {3*i} {3*i+1}\n')

'''
BRANCH AND BOUND
'''
# small
with open('bnb_small.graph','w') as f:
    f.write('100 99 0\n')
    f.write('2 3 4\n')
    for i in range(2,34):
        f.write(f'{int((i+1)/3)} {3*i-1} {3*i} {3*i+1}\n')
    for i in range(34, 101):
        f.write(f'{int((i+1)/3)}\n')

# # medium
with open('bnb_medium.graph','w') as f:
    f.write('300 299 0\n')
    f.write('2 3 4\n')
    for i in range(2,100):
        f.write(f'{int((i+1)/3)} {3*i-1} {3*i} {3*i+1}\n')
    f.write('33 299 300\n')
    for i in range(101, 301):
        f.write(f'{int((i+1)/3)}\n')

# # large
with open('bnb_large.graph','w') as f:
    f.write('900 899 0\n')
    f.write('2 3 4\n')
    for i in range(2,300):
        f.write(f'{int((i+1)/3)} {3*i-1} {3*i} {3*i+1}\n')
    f.write('100 899 900\n')
    for i in range(301, 901):
        f.write(f'{int((i+1)/3)}\n')