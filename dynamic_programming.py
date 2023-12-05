# Kode ini diambil dari sumber berikut:
# https://www.geeksforgeeks.org/vertex-cover-problem-dynamic-programming-solution-for-tree/

# Python3 implementation for the above approach

import time

def addEdge(adj, x, y):
	adj[x].append(y)
	adj[y].append(x)


def dfs(adj, dp, src, par):
	for child in adj[src]:
		if child != par:
			dfs(adj, dp, child, src)

	for child in adj[src]:
		if child != par:
			# not including source in the vertex cover
			dp[src][0] = dp[child][1] + dp[src][0]

			# including source in the vertex cover
			dp[src][1] = dp[src][1] + min(dp[child][1], dp[child][0])


def minSizeVertexCover(adj, N):
	dp = [[0 for j in range(2)] for i in range(N+1)]
	for i in range(1, N+1):
		# 0 denotes not included in vertex cover
		dp[i][0] = 0

		# 1 denotes included in vertex cover
		dp[i][1] = 1

	dfs(adj, dp, 1, -1)

	# printing minimum size vertex cover
	print(min(dp[1][0], dp[1][1]))

'''
SEGMENT: SMALL DATASET (10.000)
'''
N = 10000
adj = [[] for i in range(N+1)]

with open('dp_small.graph') as f:
	for i in range(1, 3334):
		vertex_adjacency = f.readline().split()
		addEdge(adj, i, int(vertex_adjacency[0]))
		addEdge(adj, i, int(vertex_adjacency[1]))
		addEdge(adj, i, int(vertex_adjacency[2]))

print("Minimum Size Vertex Cover (Small): ",end="")
start = time.time()
minSizeVertexCover(adj, N)
print(f"Time needed: {time.time()-start}")

'''
SEGMENT: LARGE DATASET (1.000.000)
'''
N = 1000000
adj = [[] for i in range(N+1)]

with open('dp_large.graph') as f:
	for i in range(1, 333334):
		vertex_adjacency = f.readline().split()
		addEdge(adj, i, int(vertex_adjacency[0]))
		addEdge(adj, i, int(vertex_adjacency[1]))
		addEdge(adj, i, int(vertex_adjacency[2]))

print("Minimum Size Vertex Cover (Large): ",end="")
minSizeVertexCover(adj, N)