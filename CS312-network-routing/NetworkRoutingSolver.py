#!/usr/bin/python3


from CS312Graph import *
import time
import numpy as np
import heapq

# class MinHeap(object):
#     def __init__(self):
#         self.__array = []
#         self.__last_index = -1
#         self.distances = dict()

#     def insert(self, item, value):
#         """ 
#             Append item on the back of the heap, 
#             sift upwards if heap property is violated.
#         """
#         self.__array.append(item)
#         self.distances[item.node_id] = value
#         self.__last_index += 1
#         self.__siftup(self.__last_index)

#     def del_min(self):
#         """ 
#             Pop root element from the heap (if possible),
#             put last element as new root and sift downwards till
#             heap property is satisfied.

#         """
#         if self.__last_index == -1:
#             raise IndexError("Can't pop from empty heap")
#         root_node = self.__array[0]
#         if self.__last_index > 0:  # more than one element in the heap
#             self.__array[0] = self.__array[self.__last_index]
#             self.__siftdown(0)
#         self.__last_index -= 1
#         return root_node

#     def heapify(self, input_list):
#         """
#             each leaf is a trivial subheap, so we may begin to call
#             Heapify on each parent of a leaf.  Parents of leaves begin
#             at index n/2.  As we go up the tree making subheaps out
#             of unordered array elements, we build larger and larger
#             heaps, joining them at the i'th element with Heapify,
#             until the input list is one big heap.
#         """
#         n = len(input_list)
#         self.__array = input_list
#         self.__last_index = n-1
#         for index in reversed(range(n//2)):
#             self.__siftdown(index)

#     def __siftdown(self, index): #v3
#         current_node = self.__array[index]
#         current_value = self.distances[current_node.node_id]

#         left_child_index = 2 * index + 1
#         if left_child_index > self.__last_index:
#             left_child_index, left_child_value = None, None
#         else:
#             left_child_value = self.distances[self.__array[left_child_index].node_id]

#         right_child_index = 2 * index + 2
#         if right_child_index > self.__last_index:
#             right_child_index, right_child_value = None, None
#         else:
#             right_child_value = self.distances[self.__array[right_child_index].node_id]
#         # the following works because if the right_child_index is not None, then the left_child
#         # is also not None => property of a complete binary tree, else left will be returned.
#         best_child_index, best_child_value = (left_child_index, left_child_value)

#         if right_child_index is not None:
#             left_child = self.__array[left_child_index]
#             right_child = self.__array[right_child_index]
#             if self.comparer(right_child, left_child):
#                 best_child_index, best_child_value = (right_child_index, right_child_value)
#         if best_child_index is not None:
#             best_child = self.__array[best_child_index]
#             if self.comparer(best_child, current_node):
#                 self.distances[current_node.node_id], self.distances[best_child.node_id] =\
#                     best_child_value, current_value
#                 self.__siftdown(best_child_index)
#         return

#     def __siftup(self, index):
#         current_node = self.__array[index]
#         parent_index = (index - 1) >> 1
#         parent_node = self.__array[parent_index]
#         if index > 0:
#             if self.comparer(current_node, parent_node):
#                 self.distances[parent_node.node_id], self.distances[current_node.node_id] =\
#                     self.distances[current_node.node_id], self.distances[parent_node.node_id]
#                 self.__siftup(parent_index)
#         return

#     def __get_parent(self, index):
#         if index == 0:
#             return None, None
#         parent_index =  (index - 1) // 2
#         return parent_index

#     def __get_left_child(self, index):
#         left_child_index = 2 * index + 1
#         if left_child_index > self.__last_index:
#             return None, None
#         return left_child_index, self.__array[left_child_index]

#     def __get_right_child(self, index):
#         right_child_index = 2 * index + 2
#         if right_child_index > self.__last_index:
#             return None, None
#         return right_child_index, self.__array[right_child_index]

#     def __repr__(self):
#         return str(self.__array[:self.__last_index+1])

#     def __eq__(self, other):
#         if isinstance(other, MinHeap):
#             return self.__array == other.__array
#         if isinstance(other, list):
#             return self.__array == other
#         return NotImplemented

#     def comparer(self, node1, node2):
#         return self.distances[node1.node_id] < self.distances[node2.node_id]

#     def is_empty(self):
#         return len(self.__array) == 0

class MinHeap(object):
    def __init__(self):
        self.h = []
        self.items = {}
        self.counter = 0

    def is_empty(self):
        return not self.counter > 0

    def insert(self, item, priority):
        if item in self.items:
            self.remove(item)
        entry = [priority, item, True]
        self.counter += 1
        self.items[item] = entry
        heapq.heappush(self.h, entry)

    def remove(self, item):
        entry = self.items[item]
        entry[-1] = False
        self.counter -= 1

    def del_min(self):
        while self.h:
            _, item, is_active = heapq.heappop(self.h)
            if is_active:
                self.counter -= 1
                del self.items[item]
                return item

class ArrayQueue(object):
    """
    Implementation of a priority queue using a python list
    """
    def __init__(self):
        self.q = []
        self.distances = dict()

    def is_empty(self):
        return len(self.q) == 0

    def insert(self, node, dist):
        if not self.distances.get(node.node_id):
            self.q.append(node)
        self.distances[node.node_id] = dist

    def decrease_key(self, item, new_key):
        self.distances[item.node_id] = new_key

    def del_min(self):
        # Find index of smallest item
        min_index = 0
        for i in range(1, len(self.q)):
            if self.distances[self.q[i].node_id]\
             < self.distances[self.q[min_index].node_id]:
                min_index = i
        item = self.q[min_index]
        self.q.remove(item)

        return item

    def __str__(self):
        return str([node.node_id for node in self.q])

class NetworkRoutingSolver:
    def __init__( self ):
        pass

    def initializeNetwork( self, network ):
        # assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        """
        Method used after runnning computeShortestPaths (Dijkstra's) to
        get the actual node to node path from sourceIndex to destIndex
        
        Parameters:
        ___________
            destIndex (int): The index of the desired node to end up at
        
        Returns:
        ________
            dict: Dictionary containing the total cost to get to destIndex 
                from sourceIndex (float) and the associated nodes passed
                through along the way (list)
        """
        self.dest = destIndex
      # print(destIndex)

        path_edges = []
        dest_node = self.network.nodes[self.dest]
        current = dest_node.node_id
        # print("Source index", self.source+1)
        # print("Current index", current+1)
        while current != self.source:
            if not self.parents.get(current):
              # print("NO PATH EXISTS")
                break
            edge = self.parents[current]
            path_edges.append( (edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)) )
            current = edge.src.node_id
            # print("Current index", current+1)

        return {'cost':self.distances[self.dest], 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap=False ):
        """
        Implementation of Dijkstra's Algorithm to compute the shortest
        paths from the given srcIndex node to all other nodes in the graph.
        
        Parameters:
        ___________
            srcIndex (int): The index of the desired starting node
            use_heap (bool): Whether or not to use a minHeap
        
        Returns:
        ________
            float: Time the algorithm took to run
        """
        self.source = srcIndex
        t1 = time.time()

        # print(self.network)
        # print()

        self.distances = dict()
        self.parents = dict()
        N = len(self.network.nodes)
        
        for i in range(N):
            self.distances[i] = np.inf

        if use_heap:    
            self.pq = MinHeap()
        else:
            self.pq = ArrayQueue()

        self.distances[srcIndex] = 0
        self.pq.insert(self.network.nodes[srcIndex], self.distances[srcIndex])
        
        while not self.pq.is_empty():
            closest_node = self.pq.del_min()
            # print("Visiting", closest_node.node_id, "node")
            
            for edge in closest_node.neighbors:
                dest, w = edge.dest, edge.length
                # print()
                # print("Checking edge from", edge.src.node_id, "to", dest.node_id)
                # print(self.distances[closest_node.node_id] + w, self.distances[dest.node_id])
                if self.distances[closest_node.node_id] + w < self.distances[dest.node_id]:
                    self.distances[dest.node_id] = self.distances[closest_node.node_id] + w

                    self.pq.insert(dest, self.distances[dest.node_id])
                    self.parents[dest.node_id] = edge

                #   # print("Adding/Updating", dest.node_id, self.distances[dest.node_id], "to priority queue")
                #   # print("Adding/Updating", dest.node_id, edge, "to parents map")
                #   # print("Adding/Updating", dest.node_id, self.distances[closest_node.node_id] + w)
                # print("CURRENT PRIORITY QUEUE NODES", self.pq)
                # print("CURRENT DISTANCES", self.distances)
            
        #   # print()

        # print(self.distances)
        # print()
        # print(self.parents)
        # print()

        t2 = time.time()
        return (t2-t1)

def test_graph():
    nodes = []
    edges = []
    for i in range(10):
        nodes.append(CS312GraphNode(i, (i,i)))
    for i in range(9):   
        edges.append(CS312GraphEdge(nodes[i], nodes[i+1], i+1))

    graph = CS312Graph(nodes, edges)

  # print(graph.getNodes())
    