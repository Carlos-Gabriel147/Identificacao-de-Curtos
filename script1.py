import numpy as np
import time
import json
import cv2
import os

#Variáveis
ray = -1
sel  = -1
sel_jason = -1
test_trails = []
found_labels = []
remove = []
ignore = []

print("Name of circuit image with extension:")
img_name = ""
test_name = 1

while (test_name):
    print("Enter name of circuit image:")
    img_name = input("R: ")
    if (not os.path.exists(img_name)):
        print("Image not found!")
    else:
        test_name = 0

#Abertura do circuito e ajustes
img = cv2.imread(img_name)
img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
(height, width) = img.shape[:2]

#Raio escolhio pelo usuário
while ((ray<5) or (ray>100)):
    print()
    print("Ray? (5-100 pixels)")
    ray = input("R: ")
    if ray.isdigit():
        ray = int(ray)
    else:
        ray = -1

#Selecionar o tipo de circuito de entrada (negativado ou não)
while ((sel != 1) and (sel != 2)):
    print()
    sel = input("1) Black trails and white background.\n2) White trails and black background.\nR: ")
    if sel.isdigit():
        sel = int(sel)
    else:
        sel = -1

#Gerar JSON?
while ((sel_jason != 1) and (sel_jason != 2)):
    print()
    print("Generate JSON? (1-Yes, 2-No)")
    sel_jason = input("R: ")
    if sel_jason.isdigit():
        sel_jason = int(sel_jason)
    else:
        sel_jason = -1

if sel_jason == 2:
    sel_jason = 0

#Iniciar cronômetro
start_time = time.time()

print()
print("Optimizing...")

#Se sel == 1, inverte, pois preto é detectado como background e o branco label
if sel == 1:
    img = cv2.bitwise_not(img)

#Transformação
num_labels, mask, statistics, centroids = cv2.connectedComponentsWithStats(img, connectivity=8)

#Tirar cópia da da máscara para mostrar trilhas em a remoção do fundo
mask_copy = list(map(list, mask))

#Remover fundo das trilhas e deixar apenas contornos
for h in range(0+1, height-1):
    for w in range(0+1, width-1):

        if ((all((x != 0) for x in [mask[h][w], mask[h][w-1], mask[h][w+1], mask[h-1][w-1], mask[h-1][w], mask[h-1][w+1], mask[h+1][w-1], mask[h+1][w], mask[h+1][w+1]])) or
            (mask[h][w]!=0) and (mask[h+1][w]!=0) and (mask[h-1][w]!=0) and (mask[h][w+1]!=0) and (mask[h][w-1]!=0) and ((mask[h+1][w-1]==0) or (mask[h+1][w+1]==0) or (mask[h-1][w-1]==0) or (mask[h-1][w+1]==0))):
            remove.append([h, w])
            
for pos in remove:
    h, w = pos
    mask[h][w] = 0

print(f"{round(time.time()-start_time, 2)}s")
time_aux = time.time()
print("Processing...")

#Aumentar bordas em tamanho de RAY na máscara para não acontecer estouro de vetor
mask = cv2.copyMakeBorder(mask, ray, ray, ray, ray, cv2.BORDER_CONSTANT, value=(0))

#Verificar distâncias
for h in range(0, height):
    for w in range(0, width):

        #Se não for background, verificar
        if mask[h][w] != 0:

            #Capturar a região de interesse, em função da máscra que possui os valores das labels
            current_label = mask[h][w]
            region = mask[(h-ray):(h+ray+1), (w-ray):(w+ray+1)]
            
            #Achar o centro da região de interesse
            centro_y, centro_x = region.shape
            centro_y, centro_x = int(centro_y/2), int(centro_x/2)

            #Criar uma máscara da região, onde é 1 dentro do círculo e 0 fora
            region_mask = np.zeros((2*ray+1, 2*ray+1), dtype=int)
            cv2.circle(region_mask, (centro_x, centro_y), ray, 1, thickness=-1)

            #Operação AND com a máscara, tudo que estiver fora do círculo se torna background (0), e o que estiver dentro mantém valor original
            region = np.where(region_mask==1, region, 0)
            
            #Identificar as labels que estão dentro da região
            found_labels = np.unique(region).tolist()

            #Remover background e a própria trilha de teste
            found_labels.remove(0)
            found_labels.remove(current_label)
            
            #Adicionar relação de labels proximas achadas com a atual, se não tiver sido adiciona anteriormente
            if (len(found_labels) != 0):
                for x in found_labels:
                    if ([current_label, x] not in test_trails):
                        test_trails.append([current_label, x])

#Remover bordas adicionadas anteriormente
mask = mask[ray:(height+ray), ray:(width+ray)]

print(f"{round(time.time()-time_aux, 2)}s")
time_aux = time.time()
print("Organizing...")

#Criar imagem com demarcação dos componentes de acordo com a máscara e cores aleatórias.
img_labels = np.zeros((height, width, 3), dtype=np.uint8)
np.random.seed(22)
colors = np.random.randint(0, 255, size=(num_labels, 3), dtype=np.uint8)
colors[0] = [30, 30, 30]

for h in range(0, height):
    for w in range(0, width):
        img_labels[h][w] = colors[mask_copy[h][w]]
        #if mask[h][w] == 0:
        #    img_labels[h][w] = [30, 30, 30]
        #else:
        #    img_labels[h][w] = [255, 255, 255]

#Organizar lista com trilhas para teste e remover valores repetidos, exemplo: [x, y] e [y, x]
test_trails.sort()

for pos, val in enumerate(test_trails):
    atual = val
    oposto = [atual[1], atual[0]]

    if oposto in test_trails:
        if atual[0] >= atual[1]:
            test_trails.remove(atual)
        else:
            test_trails.remove(oposto)

#Desenhar números de identificação de cada trilha
font = cv2.FONT_HERSHEY_DUPLEX
font_size = ((height/900) + (width/900))/2
spacing = int(font_size*20)

mask = cv2.copyMakeBorder(mask, spacing, spacing, spacing, spacing, cv2.BORDER_CONSTANT, value=(0))
mask_copy = cv2.copyMakeBorder(np.array(mask_copy), spacing, spacing, spacing, spacing, cv2.BORDER_CONSTANT, value=(0))
img_labels = cv2.copyMakeBorder(img_labels, spacing, spacing, spacing, spacing, cv2.BORDER_CONSTANT, value=(30, 30, 30))

for h in range(0, height):
    for w in range(0, width):
        if (mask[h][w] != 0) and (mask[h][w] not in ignore):
            color = (colors[mask_copy[h][w]]).tolist()
            color[0] += 35
            color[1] += 35
            color[2] += 35
            color = tuple(color)
            cv2.putText(img_labels, str(mask[h][w]), (w, h), font, font_size, color, thickness=2, lineType=cv2.LINE_AA)
            ignore.append(mask[h][w])

#Aumentar o tamanho da imagem, proporcionalmente para escrever o raio
amt_rows = int(height/10)
new_rows = np.ones((amt_rows, (width+2*spacing), 3), dtype=np.uint8)
color_rows = np.array([30, 30, 30],  dtype=np.uint8)
new_rows *= color_rows
img_labels = np.concatenate((img_labels, new_rows))

#Escrever os caractes 'R', 'a', 'y', ':' e a linha do tamanho do raio
new_heigth = height+int((0.7*amt_rows))
new_width = int(0.03*width)

cv2.putText(img_labels, 'R', (1*new_width, new_heigth), font, font_size+1, (255, 255, 255), thickness=2, lineType=cv2.LINE_AA)
cv2.putText(img_labels, 'a', (2*new_width, new_heigth), font, font_size+1, (255, 255, 255), thickness=2, lineType=cv2.LINE_AA)
cv2.putText(img_labels, 'y', (3*new_width, new_heigth), font, font_size+1, (255, 255, 255), thickness=2, lineType=cv2.LINE_AA)
cv2.putText(img_labels, ':', (4*new_width, new_heigth), font, font_size+1, (255, 255, 255), thickness=2, lineType=cv2.LINE_AA)

for w in range(new_width*5, new_width*5+ray):
    img_labels[int(0.985*new_heigth)-1][w] = [255, 255, 255]
    img_labels[int(0.985*new_heigth)][w] = [255, 255, 255]
    img_labels[int(0.985*new_heigth)+1][w] = [255, 255, 255]

#Printar numero de labels encontradas
print(f"{round(time.time()-time_aux, 2)}s")
print()
print(f"Number of labels: {num_labels-1}")

#Printar Trilhas para teste
print()
print("Trails to check:", end='')
if len(test_trails) == 0:
    print(" None!")
else:
    print("\n")
    for x in test_trails:
        print(f"[{x[0]} -> {x[1]}]")

#Escreve JSON
if (sel_jason and (len(test_trails)>0)):
    for i in range(0, len(test_trails)):
        for j in range(0, len(test_trails[0])):
            test_trails[i][j] = int(test_trails[i][j])

    dictionary = {i: lista for i, lista in enumerate(test_trails)}

    with open("data.json", "w") as archive:
        json.dump(dictionary, archive)

#Verificar saída, redimensionar apenas para visualização
img_labels = cv2.cvtColor(img_labels, cv2.COLOR_BGR2RGB)
img_labels = cv2.resize(img_labels, (1000, 600))
cv2.imwrite("identified_trails.png", img_labels)

#Finalizar cronômetro
end_time = time.time()
print()
print(f"Total running time: {round(end_time-start_time, 2)} seconds.")

#Mostrar circuito com labels identificadas
print()
print("Showing image.")
cv2.imshow('Circuito', img_labels)
cv2.waitKey(0)
print("Image closed.")
print()

cv2.destroyAllWindows()