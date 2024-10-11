import csv
import time
import tracemalloc
from fileinput import filename
import sys
import igraph as ig
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import csvFileMaker
# import igraphGraspi.csvFileMaker
# from build.lib.igraphGraspi.csvFileMaker import functionMemory
# from igraphGraspi.csvFileMaker import csvMaker

'''---------Function to create edges for graph in specified format --------'''
def edge(fileName):
    line = []
    n = ""
    d = ""
    dimension = 0
    with open(fileName,'r') as file:
        line = file.readline()
        splitLine = line.split()
        numBottomLayers = int(splitLine[2])
        numBottomRowVertices = int(splitLine[0])
        for i in line:
            if i != ' ':
                n += i
            elif i == ' ':
                break
        for i in reversed(line):
            if i != ' ' and i != '\n':
                d += i
            elif i == ' ':
                break

        dimension = int(d[::-1])

    num = int(n)
    edge = []
    secondToLastRow = num**2 - num
    offset = 0
    greenVertex = num**2

    for x in range(numBottomLayers):
        offset = x * numBottomLayers
        for i in range(numBottomRowVertices):
            edge.append([greenVertex,i+offset])

    for z in range(dimension):
        offset = z * (num**2)
        for y in range(num**2):
            if z < (dimension - 1):
                edge.append([y+offset,(y+offset+(num**2))])


        for x in range(0,secondToLastRow,num):
            x_num = x + num + offset
            x_offset = x+offset

            edge.append([x_offset,x_num])
            edge.append([x_offset,x_num+1])
            edge.append([x_offset,(x_offset+1)])

            for i in range(1,num):
                xi = x+i+offset
                edge.append([xi,(xi+num)])
                edge.append([(xi),(xi+(num-1))]) # right to left diagonals

                if i < num-1:
                    edge.append([xi,xi+1+num]) # left to right diagonals bottom row
                    edge.append([xi,xi+1]) # horizontal except first column
                    if x == secondToLastRow - num:
                        edge.append([secondToLastRow+i+offset,secondToLastRow+offset+i+1]) # horizontal last row except first column

    edge.append([(secondToLastRow+offset),(secondToLastRow+1+offset)]) # horizontal last row first column
    return edge

'''------- Labeling the color of the vertices -------'''
def vertexColors(fileName):
    labels = []
    with open(fileName, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            for char in line:
                if char == '1':
                    labels.append('white')
                elif char == '0':
                    labels.append('black')
    return labels

'''********* Constructing the Graph **********'''
def generateGraph(file):
    edges = edge(file)
    labels = vertexColors(file)

    f = open(file, 'r')
    line = f.readline()
    line = line.split()

    g = ig.Graph(n=int(line[0]) * int(line[1]), edges=edges, directed=False, vertex_attrs={'color': labels})
    # g = ig.Graph(n=int(line[0]) * int(line[1]) + 1, edges=edges, directed=False, vertex_attrs={'color': labels})
    g.vs[int(line[0]) * int(line[1])]['color'] = 'blue'
    add_red_node(g, file)
    # g.vs[int(line[0]) * int(line[1]) +1]['color'] = 'red'

    return g

def visual2D(g):
    layout = g.layout('kk')
    fig, ax = plt.subplots()
    # ax.invert_yaxis() # reverse starting point of graph (vertex 0)

    ig.plot(g, target=ax, layout=layout,vertex_size=25,margin=5)

    ''' ---- generate the labels of each vertex value ---- '''
    for i, (x, y) in enumerate(layout):
        g.vs['label']=[i for i in range(len(g.vs))]
        ax.text(
            x, y - 0.2,
            g.vs['label'][i],
            fontsize=12,
            color='black',
            ha='right',  # Horizontal alignment
            va='top'  # Vertical alignment
        )

    plt.show()

def visual3D(g):
    edges = g.get_edgelist()
    num_vertices = len(g.vs)
    grid_size = int(np.round(num_vertices ** (1/3)))

    # Generate 3D coordinates (layout) for the vertices
    x, y, z = np.meshgrid(range(grid_size), range(grid_size), range(grid_size))
    coords = np.vstack([x.ravel(), y.ravel(), z.ravel()]).T

    # Plot the graph in 3D using matplotlib
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot vertices
    ax.scatter(coords[:, 0], coords[:, 1], coords[:, 2], c=g.vs['color'], s=100)

    # Plot edges
    for e in edges:
        start, end = e
        ax.plot([coords[start][0], coords[end][0]],
                [coords[start][1], coords[end][1]],
                [coords[start][2], coords[end][2]], 'black')

    # Add labels to the vertices
    for i, (x, y, z) in enumerate(coords):
        ax.text(x, y, z, str(i), color='black')

    plt.show()



'''********* Filtering the Graph **********'''
def filterGraph(graph):
    edgeList = graph.get_edgelist()
    keptEdges = []

    for edge in edgeList:
        currentNode = edge[0]
        toNode = edge[1]
        if(graph.vs[currentNode]['color'] == graph.vs[toNode]['color']):
            keptEdges.append(edge)
        elif(graph.vs[currentNode]['color'] == 'blue' or graph.vs[toNode]['color'] == 'blue'):
            keptEdges.append(edge)
        elif (graph.vs[currentNode]['color'] == 'red' or graph.vs[toNode]['color'] == 'red'):
            keptEdges.append(edge)

    filteredGraph = graph.subgraph_edges(keptEdges,delete_vertices = False)

    return filteredGraph

'''********* Shortest Path **********'''
def shortest_path(graph):
    numVertices = graph.vcount()
    ccp = graph.connected_components()
    listOfShortestPaths = {}
    blueVertex = numVertices-2

    for c in ccp:
        if graph.vs[c]['color'] == 'black':
            for x in c:
                if graph.vs[x]['color'] == 'black' or graph.vs[x]['color'] == 'blue':
                    listOfShortestPaths[x] = graph.get_shortest_paths(blueVertex,x,output="vpath")[0]

    return listOfShortestPaths

def add_red_node(g, file):
    # print("in red node")
    g.add_vertex()
    f = open(file, 'r')
    line = f.readline()
    splitLine = line.split()
    numTopRowVertices = int(splitLine[0])
    endOfVertexCount = g.vcount() - 3
    g.vs[g.vcount()-1]['color'] = 'red'
    redNode = g.vs[g.vcount()-1]
    while(numTopRowVertices != 0 ):
        g.add_edge(endOfVertexCount,redNode)
        endOfVertexCount -= 1
        numTopRowVertices -= 1

def run_all_three_functions(filename, graph):
    GC_total_time, FG_total_time, SP_total_time = 0,0,0

    start = time.time()
    generateGraph(filename)
    GC_total_time += time.time() - start

    start = time.time()
    filterGraph(graph)
    FG_total_time += time.time() - start

    start = time.time()
    shortest_path(graph)
    SP_total_time += time.time() - start

    GC_mem, FG_mem, SP_mem = 0, 0, 0

    tracemalloc.start()
    generateGraph(filename)
    stats = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    GC_mem = stats[1] - stats[0]

    tracemalloc.start()
    filterGraph(graph)
    stats = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    FG_mem = stats[1] - stats[0]

    tracemalloc.start()
    shortest_path(graph)
    stats = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    SP_mem = stats[1] - stats[0]

    total_mem = GC_mem + FG_mem + SP_mem

    return GC_total_time, FG_total_time, SP_total_time, total_mem

def main():
    is_2D = True
    correct_input = False
    if sys.argv[2] == '2d':
        is_2D = True
        correct_input = True
    elif sys.argv[2] == '3d':
        is_2D = False
        correct_input = True

    if correct_input == False:
        print("Did not specify if 2d or 3d please try again")
        return 1

    g = generateGraph(sys.argv[1])  # utilizing the test file found in 2D-testFiles folder
    if is_2D:
        visual2D(g)
        filteredGraph = filterGraph(g)
        visual2D(filteredGraph)
        print(shortest_path(g))
        with open('Python-Igraph_2D_Test_Results.csv', 'w', newline='') as file:
            field = ["n", " n2", " Graph creation", " Connected Components", " Shortest Path", " total", " Memory Usage"]
            writer = csv.writer(file)
            f = "{:<5} {:<8} {:<24} {:<24} {:<24} {:<24} {:<24}".format(*field)
            writer.writerow([f])
            x = 0
            n = 0
            n_2 = 0
            dimensions = 2
            data = run_all_three_functions(sys.argv[1], g)
            n = 10
            n_2 = n * n
            total_time = data[0] + data[1] + data[3]
            row = f"{n:<5} {n_2:<8} {data[0]:<24} {data[1]:<24} {data[2]:<24} {total_time:<24} {data[3]:<24}"
            writer.writerow([row])

    else:
        visual3D(g)
        filteredGraph = filterGraph(g)
        visual3D(filteredGraph)


if __name__ == '__main__':
    main()
