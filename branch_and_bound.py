# Kode ini diambil dari sumber berikut (dengan modifikasi):
# https://github.com/sangyh/minimum-vertex-cover

# UNTUK MENJALANKAN KODE, GUNAKAN:
# python branch_and_bound.py -inst bnb_small.graph
# python branch_and_bound.py -inst bnb_medium.graph
# python branch_and_bound.py -inst bnb_large.graph

# JANGAN LUPA UNTUK lakukan 'pip install networkx' KARENA
# PROGRAM PERLU MODUL TERSEBUT

import argparse
import networkx as nx
import operator
import time
import tracemalloc
from math import ceil

# FUNCTION FOR PARSING INPUT FILES
def parse(datafile):
	adj_list = []
	with open(datafile) as f:
		num_vertices, num_edges, weighted = map(int, f.readline().split())
		for i in range(num_vertices):
			adj_list.append(map(int, f.readline().split()))
	return adj_list

# USE THE ADJACENCY LIST TO CREATE A GRAPH
def create_graph(adj_list):
	G = nx.Graph()
	for i in range(len(adj_list)):
		for j in adj_list[i]:
			G.add_edge(i + 1, j)
	return G

# BRANCH AND BOUND FUNCTION to find minimum VC of a graph
"""The algorithm is summarized as follows:

Every vertex is considered as having one of two states: 1 or 0
State 1---> Vertex is a part of Vertex Cover (VC) 
State 0---> Vertex is not a part of Vertex Cover (VC) whihc means all its neighbors HAVE to be in VC

Frontier Set: contains the set of candiadate vertices for a subproblem. Each entry is a tuple list comprising of (vertex ID, state, parent in searching tree) 

CurG: subproblem of current graph after removing explored nodes 
CurVC: Current VC found in particular instance of search
OptVC: Best (i.e. minimum) value of |CurVC| at any given point form start

Bounds to Solutions:
Upper Bound: Initially set to number of nodes and updated to size of current solution (i.e. size of minimum vertex cover found in search)

Lower bound: |Current VC| + LB(CurG)
LB(CurG)=sum of edges in CurG / maximum node degree in CurG

Stages of Implementation:
1) Choose candidate node (vi)
	Each search is started from the node with highest degree in CurG, as it represents the most promising node to be included in the VC. This node is stored in the last index of Frontier set, and accessed using Frontier.pop().

	Appened (vi,1) and (vi,0) to CurVC as a tuple= (vertex,state)


2)  If State==1: Remove from CurG 
	This removes the node and its edges from CurG
	
	If state==0, Add all neighbors of vi to CurVC and remove vi from CurG

3) Consider CurG
	If No more edges in CurG-->Candidate solution is found (CurVC accounts for all edges). 
		Check to see if |CurVC| lesser than |OptVC| (and update OptVC if true, otherwise backtrack to find new path) 
	Else Update Lower bound and prune as necessary.
		If Lowerbound<Upperbound, solution is possible
			Append next highest degree node in CurG to Frontier set 
		Else, there is no better solution in this search sapce, so can be pruned from CurG. Backtrack to find new path.

4) Backtracking
	After reaching the end of a path, we need to backtrack to consider a new path. To do this, we have to undo the changes made to CurG and CurVC, which is where the parent item of each tuple in Frontier is handy.
	
	If the parent node is in the VC, then 
		we remove the last few elements from CurVC that were added after teh parent node was discovered and add the corresponing nodes+edges back to CurG. This basically 'undoes the mistakes' to CurG...
	Else then the parent must be (-1,-1) i.e. start of the graph or root node
		Reset CurG to G and CurVC to empty 

When Frontier Set==empty, the whole graph and all possible solutions have been examined.G

End
"""

def BnB(G):
	#RECORD START TIME AND MEMORY
	start_time=time.time()
	
	times=[]    #list of times when solution is found, tuple=(VC size,delta_time)

	# INITIALIZE SOLUTION VC SETS AND FRONTIER SET TO EMPTY SET
	OptVC = []
	CurVC = []
	Frontier = []
	neighbor = []

	# ESTABLISH INITIAL UPPER BOUND
	UpperBound = G.number_of_nodes()
	print('Initial UpperBound:', UpperBound)

	CurG = G.copy()  # make a copy of G
	# sort dictionary of degree of nodes to find node with highest degree
	v = find_maxdeg(CurG)

	# APPEND (V,1,(parent,state)) and (V,0,(parent,state)) TO FRONTIER
	Frontier.append((v[0], 0, (-1, -1)))  # tuples of node,state,(parent vertex,parent vertex state)
	Frontier.append((v[0], 1, (-1, -1)))

	while Frontier!=[]:
		(vi,state,parent)=Frontier.pop() #set current node to last element in Frontier
		
		backtrack = False


		#print(parent[0])
		# print('Neigh',vi,neighbor)
		# print('Remaining no of edges',CurG.number_of_edges())

		
		
		#print(parent[0])
		# print('Neigh',vi,neighbor)
		# print('Remaining no of edges',CurG.number_of_edges())

		
		if state == 0:  # if vi is not selected, state of all neighbors=1
			neighbor = CurG.neighbors(vi)  # store all neighbors of vi
			for node in list(neighbor):
				CurVC.append((node, 1))
				CurG.remove_node(node)  # node is in VC, remove neighbors from CurG
		elif state == 1:  # if vi is selected, state of all neighbors=0
			CurG.remove_node(vi)  # vi is in VC,remove node from G
		else:
			pass

		CurVC.append((vi, state))
		CurVC_size = VC_Size(CurVC)

		if CurG.number_of_edges() == 0:  # end of exploring, solution found
			if CurVC_size < UpperBound:
				OptVC = CurVC.copy()
				print('Current Opt VC size', CurVC_size)
				UpperBound = CurVC_size
				times.append((CurVC_size,time.time()-start_time))
			backtrack = True
				
		else:   #partial solution
			CurLB = Lowerbound(CurG) + CurVC_size
			if CurLB < UpperBound:  # worth exploring
				vj = find_maxdeg(CurG)
				Frontier.append((vj[0], 0, (vi, state)))#(vi,state) is parent of vj
				Frontier.append((vj[0], 1, (vi, state)))
			else:
				# end of path, will result in worse solution,backtrack to parent
				backtrack=True

		if backtrack==True:
			if Frontier != []:	#otherwise no more candidates to process
				nextnode_parent = Frontier[-1][2]	#parent of last element in Frontier (tuple of (vertex,state))

				# backtrack to the level of nextnode_parent
				if nextnode_parent in CurVC:
					
					id = CurVC.index(nextnode_parent) + 1
					while id < len(CurVC):	#undo changes from end of CurVC back up to parent node
						mynode, mystate = CurVC.pop()	#undo the addition to CurVC
						CurG.add_node(mynode)	#undo the deletion from CurG
						
						# find all the edges connected to vi in Graph G
						# or the edges that connected to the nodes that not in current VC set.
						
						curVC_nodes = list(map(lambda t:t[0], CurVC))
						for nd in G.neighbors(mynode):
							if (nd in CurG.nodes()) and (nd not in curVC_nodes):
								CurG.add_edge(nd, mynode)	#this adds edges of vi back to CurG that were possibly deleted

				elif nextnode_parent == (-1, -1):
					# backtrack to the root node
					CurVC.clear()
					CurG = G.copy()
				else:
					print('error in backtracking step')

	return OptVC,times

#TO FIND THE VERTEX WITH MAXIMUM DEGREE IN REMAINING GRAPH
def find_maxdeg(g):
	deglist = g.degree()
	deglist_sorted = sorted(deglist, reverse=True, key=operator.itemgetter(
		1))  # sort in descending order of node degree
	v = deglist_sorted[0]  # tuple - (node,degree)
	return v

#EXTIMATE LOWERBOUND
def Lowerbound(graph):
	lb=graph.number_of_edges() / find_maxdeg(graph)[1]
	lb=ceil(lb)
	return lb


def ceil(d):
    """
        return the minimum integer that is bigger than d
    """ 
    if d > int(d):
        return int(d) + 1
    else:
        return int(d)
    

#CALCULATE SIZE OF VERTEX COVER (NUMBER OF NODES WITH STATE=1)
def VC_Size(VC):
	# VC is a tuple list, where each tuple = (node_ID, state, (node_ID, state)) vc_size is the number of nodes which has state == 1

	vc_size = 0
	for element in VC:
		vc_size = vc_size + element[1]
	return vc_size

##################################################################
# MAIN BODY OF CODE

def main(inputfile):
	#READ INPUT FILE INTO GRAPH
	adj_list = parse(inputfile)	
	# CONSTRUCT THE GRAPH BASED ON ADJACENT LIST

	datafile = inputfile
	adj_list = parse(datafile)
	g = create_graph(adj_list)

	print('No of nodes in G:', g.number_of_nodes(),
		  '\nNo of Edges in G:', g.number_of_edges())

	start = time.time()
	tracemalloc.start()
	Sol_VC,times = BnB(g)
	end = time.time()
	mem = tracemalloc.get_traced_memory()
	tracemalloc.stop()

	#DELETE FALSE NODES (STATE=0) IN OBTAINED SoL_VC
	for element in Sol_VC:
		if element[1]==0:
			Sol_VC.remove(element)

	print('Minimum Size Vertex:', VC_Size(Sol_VC))
	print(f"Time needed: {end-start}")
	print(f"Memory needed: {mem[1]}")
	print()

if __name__ == '__main__':
	#create parser; example: python bnb.py --datafile ../Data/karate.graph --cutoff_time 200
	parser=argparse.ArgumentParser(description='Input parser for BnB')
	parser.add_argument('-inst',action='store',type=str,required=True,help='Inputgraph datafile')
	args=parser.parse_args()

	graph_file = args.inst

	main(graph_file)