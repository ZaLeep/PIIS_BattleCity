import numpy as np

map = np.loadtxt("digitmap3.txt", delimiter = ",", dtype = "i")
Map = []
for i in range(len(map)):
    line = []
    for j in range(len(map[i])):
        print(map[i][j])
        line.append(map[i][j])
        line.append(map[i][j])
    Map.append(line)
    Map.append(line)
print(Map)
np.savetxt("Map3.txt", Map, delimiter = ",")