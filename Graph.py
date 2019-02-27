import sys

# This class implements the Shortest Paths in a Network - the minimum binary heap and the Dijkstra's Algorithm implementation...
class Heap:
    heap=[]


    def parent(self,i):
        return int((i - 1) / 2)

    def left_child(self,i):
        return int(2*i+1)

    def right_child(self,i):
        return int(2*i+2)

    def insert(self,vertex):
        self.heap.append(vertex)
        pos = len(self.heap)-1
        while not (pos == 0) and self.heap[self.parent(pos)][1] > self.heap[pos][1]:
            self.heap[pos], self.heap[self.parent(pos)] = self.heap[self.parent(pos)],self.heap[pos]
            pos = self.parent(pos)

    def pop(self):
        top = self.heap[0]
        self.heap[0]=self.heap[-1]
        self.heap.pop(-1)
        self.heapify(0)
        return top

    def heapify(self,pos):
        l = self.left_child(pos)
        r = self.right_child(pos)
        minimum = None
        if l < len(self.heap) and self.heap[l][1] < self.heap[pos][1]:
            minimum = l
        if r < len(self.heap) and self.heap[r][1] < self.heap[l][1]:
            minimum = r
        if minimum is not None :
            self.heap[pos],self.heap[minimum] = self.heap[minimum],self.heap[pos]
            self.heapify(minimum)

    def decrease_value(self,vertex):
        index = 0
        for value in self.heap:
            if value[0] == vertex[0]:
                break
            index+=1
        self.heap[index]=vertex
        while index > 0 and self.heap[index][1] < self.heap[self.parent(index)][1]:
            self.heap[self.parent(index)], self.heap[index] = self.heap[index], self.heap[self.parent(index)]
            index = self.parent(index)

# This class implements the initiation or creation of the vertex of the graph; and also the up and down operation...
class Vertex:
    _name = ""
    _is_up = True

    def __init__(self, name, is_up=True):
        self._name = name
        self._is_up = is_up

    def __repr__(self):
        return self._name

    def __index__(self):
        return hash(self._name)

    def __hash__(self):
        return hash(self._name)

    def __eq__(self, other):
        return (self._name == other._name)

    def is_up(self):
        return self._is_up

    def get_name(self):
        return self._name

# This class implements the initiation or creation of the edges of the graph; and also the up and down operation...
class Edge:
    _from = None
    _to = None
    _is_up = True
    _value = 0

#Initialization
    def __init__(self, from_src, to_dest, value, is_up=True):
        self._from = from_src
        self._to = to_dest
        self._value = value
        self._is_up = is_up

    def __hash__(self):
        return hash(self._from._name + self._to._name)

    def __repr__(self):
        return self._from._name + self._to._name

    def __eq__(self, other):
        return (self._from._name + self._to._name == other._from._name + other._to._name)

    def get_from(self):
        return self._from

    def get_to(self):
        return self._to

    def get_value(self):
        return self._value

    def is_up(self):
        return self._is_up

# Reads the imputs from a file and outputs to another txt file depending upon the commands...
class Graph:
    node_dict = {}  # name:obj_ref
    edge_dict = {}  # from+to:obj_ref
    adjecency_list = {}  # src_object_ref:{dest_obj_ref, edge_obj_ref}

#This function adds the new edge to graph
    def add_edge(self, from_src, to_dest, value):
        if from_src + to_dest in self.edge_dict:
            self.edge_dict[from_src + to_dest]._value = value
        else:
            if from_src not in self.node_dict:
                node = Vertex(from_src)
                self.node_dict[node.get_name()] = node
            if to_dest not in self.node_dict:
                node = Vertex(to_dest)
                self.node_dict[node.get_name()] = node
            edge = Edge(self.node_dict[from_src], self.node_dict[to_dest], value)
            self.edge_dict[from_src + to_dest] = edge
            if self.node_dict[from_src]._name not in self.adjecency_list:
                self.adjecency_list[from_src] = [[to_dest, from_src + to_dest]]
            else:
                self.adjecency_list.get(from_src).append([to_dest, from_src + to_dest])


    def delete_edge_given_src_dest(self, from_src, to_dest):
        for i in range(len(self.adjecency_list[from_src])):
            if (self.adjecency_list[from_src][i][0] == to_dest):
                self.adjecency_list[from_src].pop(i)
                break
        self.edge_dict.pop(from_src+to_dest)

    def delete_edge(self,from_src,to_dest):
        self.delete_edge_given_src_dest(from_src, to_dest)

#This function prints the grapgh with DOWN vertex and edge 
    def print_graph(self):
        def compare(a, b):
            return str.lower(a[0]._name[:1]) < str.lower(b[0]._name[:1])

        keys = [key for key in self.node_dict.keys()]
        sorted_keys = sorted(keys, key=str.lower)
        for key_str in sorted_keys:
            key = self.node_dict[key_str]
            values = self.adjecency_list.get(key_str,[])
            temp_dict = {}
            for value in values:
                temp_dict[value[0]] = self.edge_dict[value[1]]._value
            temp_sorted_keys = sorted(temp_dict.keys(), key=str.lower)
            #if len(temp_sorted_keys)>0:
            msg = ""
            if not self.node_dict[key_str]._is_up:
                msg=" DOWN"
            print(key_str+msg)
            for temp_key in temp_sorted_keys:
                msg=""
                if not self.edge_dict[key_str+temp_key]._is_up:
                    msg = " DOWN"
                print("  " + temp_key + " " + str(temp_dict[temp_key])+msg)


    def reachable_from(self,from_src):
        if not self.node_dict[from_src]._is_up :
            return None
        queue = []
        queue.append(from_src)
        reachable = []
        while(len(queue) != 0 ):
            top = queue.pop(0)
            if top not in reachable:
                reachable.append(top)
            for adjecent_vertex in self.adjecency_list[top]:
                if adjecent_vertex[0] not in reachable and self.node_dict[adjecent_vertex[0]]._is_up and self.edge_dict[adjecent_vertex[1]]._is_up:
                    queue.append(adjecent_vertex[0])
        return reachable

#This function prints all the vertices reachable from the given vertex
    def reachable(self):
        ans = []
        for key in sorted(self.node_dict.keys(),key=str.lower):
            ans.append(self.reachable_from(key))
        return ans


#This function finds out the shortest path from source vertex to destination vertex
    def path(self,src,dest):
        dist = {}
        visited = []
        parent_path = {}
        solution_path = []
        min_heap = Heap()
        vertices = self.node_dict.keys()
        for vertex in vertices:
            if vertex == src:
                min_heap.insert([vertex, 0])
                dist[vertex] = 0
            else:
                min_heap.insert([vertex,1000])
                dist[vertex] = 1000

        parent_path[src]=None

        while len(min_heap.heap) != 0:
            closest_vertex = min_heap.pop()
            visited.append(closest_vertex)
            if closest_vertex[0] not in self.adjecency_list:
                continue
            for adjecent_vertex in self.adjecency_list[closest_vertex[0]]:
                if self.edge_dict[adjecent_vertex[1]]._is_up == True and self.node_dict[adjecent_vertex[0]]._is_up:
                    vertex_name = adjecent_vertex[0]
                    if vertex_name not in visited and self.edge_dict[adjecent_vertex[1]]._value + dist[closest_vertex[0]] < dist[adjecent_vertex[0]]:
                        dist[adjecent_vertex[0]] = self.edge_dict[adjecent_vertex[1]]._value+dist[closest_vertex[0]]
                        min_heap.decrease_value([adjecent_vertex[0],dist[adjecent_vertex[0]]])
                        parent_path[adjecent_vertex[0]]=closest_vertex[0]

        child = dest
        solution_path.append(dest)
        while parent_path[child] is not None:
            solution_path.append(parent_path[child])
            child = parent_path[child]
        return round(dist[dest],2), solution_path

# This is the main function which implements the required Project-2 operations specified in input file
def main():
    graph = Graph()
    with open(sys.argv[1]) as input_file:
        lines = input_file.readlines()
        for line in lines:
            splited_line = line.split()
            graph.add_edge(splited_line[0], splited_line[1], float(splited_line[2]))
            graph.add_edge(splited_line[1], splited_line[0], float(splited_line[2]))
    #graph.edge_dict["HealthEducation"]._is_up = False
    #graph.node_dict["Belk"]._is_up = False

    #print(graph.path("Education", "Belk"))
    while True:
        try:
            input_command = input()
        except EOFError:
            break
        if input_command == "print":
            graph.print_graph()
            print("")
        elif input_command.split()[0] == "addedge":
            src = input_command.split()[1]
            dest = input_command.split()[2]
            val = input_command.split()[3]
            graph.add_edge(src , dest, float(val))

        elif input_command.split()[0] == "deleteedge":
            src = input_command.split()[1]
            dest = input_command.split()[2]
            graph.delete_edge(src,dest)

        elif input_command.split()[0] == "edgedown":
            src = input_command.split()[1]
            dest = input_command.split()[2]
            graph.edge_dict[src+dest]._is_up=False

        elif input_command.split()[0] == "edgeup":
            src = input_command.split()[1]
            dest = input_command.split()[2]
            graph.edge_dict[src+dest]._is_up=True

        elif input_command.split()[0] == "vertexup":
            src = input_command.split()[1]
            graph.node_dict[src]._is_up=True

        elif input_command.split()[0] == "vertexdown":
            src = input_command.split()[1]
            graph.node_dict[src]._is_up=False

        elif input_command.split()[0] == "path":
            src = input_command.split()[1]
            dest = input_command.split()[2]
            dist,path = graph.path(src, dest)
            for vertex in reversed(path):
                print(vertex+" ", end='')
            print(dist)
            print("")

        elif input_command.split()[0] == "reachable":
            ans = graph.reachable()
            for row in ans:
                if row is not None:
                    print(row[0])
                    for vertex in sorted(row[1:],key=str.lower):
                        print("  "+vertex)
            print("")

        elif input_command == "quit":
            break

#Calls main function
if __name__ == "__main__":
    main()