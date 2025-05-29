from collections import deque
from typing import List

class Solution:
    def maxTargetNodes(self, edges1: List[List[int]], edges2: List[List[int]], k: int) -> List[int]:
        n = len(edges1) + 1
        m = len(edges2) + 1
        
        def build_graph(edges, size):
            graph = [[] for _ in range(size)]
            for u,v in edges:
                graph[u].append(v)
                graph[v].append(u)
            return graph
        
        graph1 = build_graph(edges1, n)
        graph2 = build_graph(edges2, m)
        
        # BFS to get shortest distances from one node to all others
        def bfs(start, graph):
            dist = [-1]*len(graph)
            dist[start] = 0
            queue = deque([start])
            while queue:
                u = queue.popleft()
                for w in graph[u]:
                    if dist[w] == -1:
                        dist[w] = dist[u] + 1
                        queue.append(w)
            return dist
        
        # Precompute all distances in Tree1
        dist1 = [bfs(i, graph1) for i in range(n)]
        # Precompute all distances in Tree2
        dist2 = [bfs(j, graph2) for j in range(m)]
        
        # Precompute reachable counts in Tree1 for each node within distance k
        reachable1 = [sum(1 for d in dist1[i] if d != -1 and d <= k) for i in range(n)]
        
        # For each node j in Tree2, precompute number of nodes within distance d
        # We'll use this for d = 0 to max dist (<= k-1) because connection edge adds 1
        max_dist2 = k - 1
        reachable2_counts = []
        for j in range(m):
            count_within = [0]*(max_dist2+1)
            for d in dist2[j]:
                if d != -1 and d <= max_dist2:
                    count_within[d] += 1
            # prefix sums to quickly get number of nodes within distance d
            for x in range(1, max_dist2+1):
                count_within[x] += count_within[x-1]
            reachable2_counts.append(count_within)
        
        answer = []
        for i in range(n):
            max_nodes = 0
            # nodes reachable in Tree1 from i (within k)
            base_count = reachable1[i]
            
            # Try connecting i to each node j in Tree2
            for j in range(m):
                # reachable nodes in Tree2 within k-1 from j, because edge i-j adds 1 distance
                count_in_tree2 = reachable2_counts[j][max_dist2] if max_dist2 >= 0 else 0
                total = base_count + count_in_tree2
                if total > max_nodes:
                    max_nodes = total
            answer.append(max_nodes)
        
        return answer
