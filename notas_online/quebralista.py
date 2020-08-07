#!/usr/bin/env python3

from pprint import pprint

turmas = ('6A','6B','7A','8A','9A','1A','2A','3A')

with open('lista_completa') as file:
    lista = file.read().replace('\n',',')
    lista = lista.split('|')

    count = 0
    for row in lista:
        with open(turmas[count], 'w') as new_file:
            print(row, end='', file=new_file)
        count += 1
