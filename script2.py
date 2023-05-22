import numpy as np
import json
import sys
import os
import shutil

if not os.path.exists("data.json"):
    print("Json file not find!")
    sys.exit()

with open('data.json', 'r') as arquivo:
    data = json.load(arquivo)

test_trails = [data[str(key)] for key in range(len(data))]
amt_test_trails = len(test_trails)
unique_trails = np.unique(np.array(test_trails))
amt_trails = len(unique_trails)
pins_trails = {}
main_code = ''
line = "//-------------------------------------//\n"

#Verificar o número máximo de trilhas
if(amt_trails>52):
    print("Max number of trails exceeded! (54)");
    sys.exit(1)

#Criar uma dicionário que relacione as trilhas com os pinos digitais
for indice, valor in enumerate(unique_trails):
    pins_trails[valor] = 'D' + str(indice+2)

#Criar sublistas para cada conjunto de trilhas começando por X
sub_lists = []
firts_indexs = []

for sb in test_trails:
    fi = sb[0]
    if fi not in firts_indexs:
        firts_indexs.append(fi)
        sub_lists.append([sb])
    else:
        index = firts_indexs.index(fi)
        sub_lists[index].append(sb)

#Adicionar as definições dos pinos
for i in range(2, 53):
    main_code += f"#define D{i} {i}\n"

#Adicionar vetores principais, teste de trilhas e marcador de curtos
main_code += f"#define DIM {amt_test_trails}\n"
main_code += "\n"
main_code += "int cont = 0;\n"
main_code += "\n"
main_code += "int marker[DIM][2] = {\n"

#Vetor marcador
for i in range(0, amt_test_trails):
    main_code += "{0, 0}"
    if i < (amt_test_trails-1):
        main_code += ','
    main_code += "\n"
main_code += "};\n"
main_code += "\n"

#Vetor de testes
main_code += "int test_trails[DIM][2] = {\n"
for index, value in enumerate(test_trails):
    main_code += f"{{{value[0]}, {value[1]}}}"
    if index < (amt_test_trails-1):
        main_code += ','
    main_code += "\n"
main_code += "};\n"
main_code += "\n"

#Vetor de trilhas únicas
main_code += f"int unique_trails[{amt_trails}] = "
main_code += '{'
for index, value in enumerate(unique_trails):
    main_code += str(int(value))
    if index < (len(unique_trails)-1):
        main_code += ','
main_code += "};\n"
main_code += "\n"

#Função de checar curto
main_code += "int testPin(int pin, int pos){\n"
main_code += "  if (!digitalRead(pin)){\n"
main_code += "    while(1){\n"
main_code += "      if(marker[cont][0]==0 && marker[cont][1]==0){\n"
main_code += "        marker[cont][0] = test_trails[pos][0];\n"
main_code += "        marker[cont][1] = test_trails[pos][1];\n"
main_code += "        cont++;\n"
main_code += "        break;\n"
main_code += "      }else{\n"
main_code += "        cont++;\n"
main_code += "      }\n"
main_code += "    }\n"
main_code += "  }\n"
main_code += "}\n"
main_code += "\n"

#Setup, definir modos
main_code += "void setup(){\n"
main_code += "  Serial.begin(115200);\n"
for i in range(2, 53):
    main_code += f"  pinMode(D{i}, INPUT_PULLUP);\n"
main_code += "}\n"
main_code += "\n"

#Início do loop
main_code += "void loop(){\n"
main_code += "\n"
main_code += "  delay(1000);\n"
main_code += "\n"

#Printar relação de trilhas e pinos digitais
main_code += '  Serial.println("Trails -> Digital Pins");\n'
main_code += "  for(int i; i < sizeof(unique_trails)/sizeof(unique_trails[0]); i++){\n"
main_code += "    Serial.print(unique_trails[i]);\n"
main_code += '    Serial.print(" -> ");\n'
main_code += "    Serial.print('D');\n"
main_code += "    Serial.println(i+2);\n"
main_code += "  }\n"

main_code += "\n"
main_code += line
main_code += "\n"

#Partes pricipais, alterar modo dos pinos e testar
aux = 0
for index, value in enumerate(sub_lists):

    main_code += f"  pinMode({pins_trails[value[0][0]]}, OUTPUT);\n"
    main_code += f"  digitalWrite({pins_trails[value[0][0]]}, LOW);\n"
    main_code += "\n"

    for x in range(0, len(value)):
        main_code += f"  testPin({pins_trails[value[x][1]]}, {aux});\n"
        aux += 1;

    main_code += "\n"
    main_code += f"  digitalWrite({pins_trails[value[0][0]]}, HIGH);\n"
    main_code += f"  pinMode({pins_trails[value[0][0]]}, INPUT_PULLUP);\n"

    main_code += "\n"
    main_code += line
    main_code += "\n"


#Print final dos curtos
main_code += "  if(cont==0){\n"
main_code += '    Serial.println("No shorts!");\n'
main_code += "  }else{\n"
main_code += '    Serial.println("Shorts founds:");\n'
main_code += "    for(int x=0; x<cont; x++){\n"
main_code += '      Serial.print("Trails ");\n'
main_code += "      for(int y=0; y<2; y++){\n"
main_code += "        Serial.print(marker[x][y]);\n"
main_code += "        if(y==0){\n"
main_code += '          Serial.print(" and ");\n'
main_code += "        }\n"
main_code += "      }\n"
main_code += "      Serial.println();\n"
main_code += "    }\n"
main_code += "  }\n"
main_code += "\n"
main_code += "  while(1){\n"
main_code += "    delay(10);\n"
main_code += "  }\n"
main_code += "}"

dir_name = "file"

#Excluir pasta se já existir, criar se não
if os.path.exists("file"):
    shutil.rmtree("file")

#Criar uma pasta
os.mkdir(dir_name)

#Criar o arquivo ino dentro da pasta
file_name = "file.ino"
path = os.path.join(dir_name, file_name)
with open(path, 'w') as file:
    file.write(main_code)

#Mostrar as relações de trilhas e pinos
print()
print("Trail -> Digital Pin:")
for index, value in pins_trails.items():
    print(f"{index} -> {value}")
print()
print("-> .ino file created!")
print()
