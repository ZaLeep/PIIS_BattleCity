import numpy as np

def trans(number, m = []):
    if len(m) != 0:
        map = m
    else:
        map = np.loadtxt("digitmap" + str(number) + ".txt", delimiter = ",", dtype = "i")
    Map = []
    for i in range(len(map)):
        line = []
        for j in range(len(map[i])):
            line.append(map[i][j])
            line.append(map[i][j])
        Map.append(line)
        Map.append(line)
    np.savetxt("Map" + str(number) + ".txt", Map, delimiter = ",")