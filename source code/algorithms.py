from collections import deque
import heapq


class GraphAlgorithms:
    
    @staticmethod
    def bfs(graph, start_node, callback=None):
        if start_node not in graph.nodes:
            return []
        
        visited = set()
        queue = deque([start_node])
        visited.add(start_node)
        order = []
        
        while queue:
            current = queue.popleft()
            order.append(current)
            
            if callback:
                callback(current, 'visiting')
            
            neighbors = graph.get_neighbors(current)
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    if callback:
                        callback(neighbor, 'queued')
            
            if callback:
                callback(current, 'visited')
        
        return order
    
    @staticmethod
    def dfs(graph, start_node, callback=None):
        if start_node not in graph.nodes:
            return []
        
        visited = set()
        order = []
        
        def dfs_visit(node):
            visited.add(node)
            order.append(node)
            
            if callback:
                callback(node, 'visiting')
            
            neighbors = graph.get_neighbors(node)
            for neighbor in neighbors:
                if neighbor not in visited:
                    dfs_visit(neighbor)
            
            if callback:
                callback(node, 'visited')
        
        dfs_visit(start_node)
        return order
    
    @staticmethod
    def dijkstra(graph, source, target, callback=None):
        if source not in graph.nodes or target not in graph.nodes:
            return None, float('inf')
        
        dist = {node: float('inf') for node in graph.nodes}
        prev = {node: None for node in graph.nodes}
        dist[source] = 0
        
        pq = [(0, source)]
        visited = set()
        
        while pq:
            current_dist, u = heapq.heappop(pq)
            
            if u in visited:
                continue
            
            visited.add(u)
            
            if callback:
                callback(u, 'visiting', dist[u])
            
            if u == target:
                break
            
            neighbors = graph.get_neighbors(u)
            for v in neighbors:
                if v not in visited:
                    weight = graph.get_edge_weight(u, v)
                    alt = dist[u] + weight
                    
                    if alt < dist[v]:
                        dist[v] = alt
                        prev[v] = u
                        heapq.heappush(pq, (alt, v))
            
            if callback:
                callback(u, 'visited', dist[u])
        
        if dist[target] == float('inf'):
            return None, float('inf')
        
        path = []
        current = target
        while current is not None:
            path.append(current)
            current = prev[current]
        path.reverse()
        
        return path, dist[target]
    
    @staticmethod
    def check_bipartite(graph, callback=None):
        if len(graph.nodes) == 0:
            return True, {}
        
        color = {node: -1 for node in graph.nodes}
        
        for start_node in graph.nodes:
            if color[start_node] == -1:
                queue = deque([start_node])
                color[start_node] = 0
                
                while queue:
                    u = queue.popleft()
                    
                    if callback:
                        callback(u, 'visiting', color[u])
                    
                    neighbors = graph.get_neighbors(u)
                    for v in neighbors:
                        if color[v] == -1:
                            color[v] = 1 - color[u]
                            queue.append(v)
                        elif color[v] == color[u]:
                            if callback:
                                callback(u, 'conflict', color[u])
                                callback(v, 'conflict', color[v])
                            return False, color
                    
                    if callback:
                        callback(u, 'colored', color[u])
        
        return True, color
    
    @staticmethod
    def prim(graph, callback=None):
        if len(graph.nodes) == 0 or graph.directed:
            return [], 0
        
        start_node = list(graph.nodes.keys())[0]
        visited = set([start_node])
        mst_edges = []
        total_weight = 0
        
        edges = []
        for neighbor in graph.get_neighbors(start_node):
            weight = graph.get_edge_weight(start_node, neighbor)
            heapq.heappush(edges, (weight, start_node, neighbor))
        
        while edges and len(visited) < len(graph.nodes):
            weight, u, v = heapq.heappop(edges)
            
            if v in visited:
                continue
            
            visited.add(v)
            mst_edges.append((u, v, weight))
            total_weight += weight
            
            if callback:
                callback(v, 'added', u, v, weight)
            
            for neighbor in graph.get_neighbors(v):
                if neighbor not in visited:
                    w = graph.get_edge_weight(v, neighbor)
                    heapq.heappush(edges, (w, v, neighbor))
        
        return mst_edges, total_weight
    
    @staticmethod
    def kruskal(graph, callback=None):
        if len(graph.nodes) == 0 or graph.directed:
            return [], 0
        
        parent = {node: node for node in graph.nodes}
        rank = {node: 0 for node in graph.nodes}
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x, y):
            px, py = find(x), find(y)
            if px == py:
                return False
            if rank[px] < rank[py]:
                parent[px] = py
            elif rank[px] > rank[py]:
                parent[py] = px
            else:
                parent[py] = px
                rank[px] += 1
            return True
        
        edges = sorted(graph.edges, key=lambda e: e['weight'])
        
        mst_edges = []
        total_weight = 0
        
        for edge in edges:
            u, v, w = edge['from'], edge['to'], edge['weight']
            
            if callback:
                callback(None, 'checking', u, v, w)
            
            if union(u, v):
                mst_edges.append((u, v, w))
                total_weight += w
                
                if callback:
                    callback(None, 'added', u, v, w)
                
                if len(mst_edges) == len(graph.nodes) - 1:
                    break
            else:
                if callback:
                    callback(None, 'rejected', u, v, w)
        
        return mst_edges, total_weight
    
    @staticmethod
    def ford_fulkerson(graph, source, sink, callback=None):
        if source not in graph.nodes or sink not in graph.nodes:
            return 0
        
        residual = {}
        for node in graph.nodes:
            residual[node] = {}
        
        for edge in graph.edges:
            u, v, w = edge['from'], edge['to'], edge['weight']
            residual[u][v] = w
            if v not in residual or u not in residual[v]:
                residual[v][u] = 0
        
        def bfs_find_path(source, sink):
            visited = set([source])
            queue = deque([(source, [source])])
            
            while queue:
                node, path = queue.popleft()
                
                for neighbor in residual[node]:
                    if neighbor not in visited and residual[node][neighbor] > 0:
                        visited.add(neighbor)
                        new_path = path + [neighbor]
                        
                        if neighbor == sink:
                            return new_path
                        
                        queue.append((neighbor, new_path))
            
            return None
        
        max_flow = 0
        iterations = 0
        
        while True:
            path = bfs_find_path(source, sink)
            if not path:
                break
            
            flow = min(residual[path[i]][path[i+1]] for i in range(len(path)-1))
            
            for i in range(len(path)-1):
                u, v = path[i], path[i+1]
                residual[u][v] -= flow
                residual[v][u] += flow
            
            max_flow += flow
            iterations += 1
            
            if callback:
                callback(path, 'path_found', flow, iterations)
            
            if iterations > 100:
                break
        
        return max_flow
    
    @staticmethod
    def fleury(graph, callback=None):
        if graph.directed or len(graph.nodes) == 0:
            return None
        
        degrees = {node: len(graph.get_neighbors(node)) for node in graph.nodes}
        for degree in degrees.values():
            if degree % 2 != 0:
                return None
        
        remaining_edges = graph.edges.copy()
        circuit = [list(graph.nodes.keys())[0]]
        
        while remaining_edges:
            current = circuit[-1]
            neighbors = []
            
            for edge in remaining_edges:
                if edge['from'] == current:
                    neighbors.append((edge['to'], edge))
                elif edge['to'] == current:
                    neighbors.append((edge['from'], edge))
            
            if not neighbors:
                break
            
            next_node, chosen_edge = neighbors[0]
            circuit.append(next_node)
            remaining_edges.remove(chosen_edge)
            
            if callback:
                callback(circuit, 'edge_added', chosen_edge)
        
        if remaining_edges:
            return None
        
        return circuit
    
    @staticmethod
    def hierholzer(graph, callback=None):
        if graph.directed or len(graph.nodes) == 0:
            return None
        
        degrees = {node: len(graph.get_neighbors(node)) for node in graph.nodes}
        for degree in degrees.values():
            if degree % 2 != 0:
                return None
        
        adj = {node: [] for node in graph.nodes}
        for edge in graph.edges:
            adj[edge['from']].append(edge['to'])
            adj[edge['to']].append(edge['from'])
        
        start = list(graph.nodes.keys())[0]
        stack = [start]
        circuit = []
        
        while stack:
            v = stack[-1]
            if adj[v]:
                u = adj[v].pop()
                adj[u].remove(v)
                stack.append(u)
                
                if callback:
                    callback(stack, 'exploring')
            else:
                circuit.append(stack.pop())
                
                if callback:
                    callback(circuit, 'backtrack')
        
        circuit.reverse()
        return circuit
