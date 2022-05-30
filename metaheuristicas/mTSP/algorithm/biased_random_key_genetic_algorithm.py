from random import uniform 

def decoder(instance, S):
    pass

def create_solutions(instance, p):
    S = []
    for i in range(p):
        key = [0] * len(instance.points)
        for j in range(len(instance.points)):
            key[j] = uniform(0, 1)

        element = {
            'key': key,
            'key_sorted': key.sort(),
            'fo': -1
            }
        S.append(element)
    return S

def BRKGA(instance, BRKGAMax, p):
    while BRKGAMax > 0:
        BRKGAMax -= 1
        S = create_solutions(instance, p)
        decoder(instance, S)
        print(S)



    
