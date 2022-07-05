
def main():
    lenght = 3
    lista = [0,1,2]
    print_lista(lista, "", len(lista), lenght)

def print_lista(lista,prefix,n, lenght):
    if (lenght == 1):
        for j in range(n):
            if str(lista[j]) not in str(prefix):
                print(str(prefix) + str(lista[j]))
    else:
        for i in range(n):
            if str(prefix) != str(lista[i]):
                print_lista(lista, str(prefix) + str(lista[i]), n, lenght - 1)

main()