import numpy as np
import time
import json
import sys

print("Ready? (Enter any key)")
input("")

start = time.time()

with open('data.json', 'r') as arquivo:
    data = json.load(arquivo)

test_trails = [data[str(key)] for key in range(len(data))]
unique_trails = np.unique(np.array(test_trails))
amt_trails = len(unique_trails)
pins_trails = {}

#Verificar o número máximo de trilhas
if(amt_trails>54):
    print("Max number of trails exceeded! (54)");
    sys.exit(1)

#Criar uma dicionário que relacione as trilhas com os pinos digitais
for indice, valor in enumerate(unique_trails):
    pins_trails[valor] = 'D' + str(indice+2)

sub_lists = []
firts_indexs = []

for sub_list in test_trails:
    first_index = sub_list[0]
    if first_index not in firts_indexs:
        firts_indexs.append(first_index)
        sub_lists.append([sub_list])
    else:
        index = firts_indexs.index(first_index)
        sub_lists[index].append(sub_list)

for x in sub_lists:
    print(x)
