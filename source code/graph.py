"""
graph.py - Class đại diện cho đồ thị
"""

class Graph:
    def __init__(self, directed=False, weighted=False):
        """
        Khởi tạo đồ thị
        :param directed: Đồ thị có hướng hay không
        :param weighted: Đồ thị có trọng số hay không
        """
        self.nodes = {}  # {node_id: {'x': x, 'y': y, 'label': label}}
        self.edges = []  # [{'from': node_id, 'to': node_id, 'weight': weight}]
        self.directed = directed
        self.weighted = weighted
        self.node_counter = 0
    
    def add_node(self, x, y, label=None):
        """Thêm đỉnh vào đồ thị"""
        node_id = self.node_counter
        if label is None:
            label = str(node_id)
        self.nodes[node_id] = {'x': x, 'y': y, 'label': label}
        self.node_counter += 1
        return node_id
    
    def remove_node(self, node_id):
        """Xóa đỉnh khỏi đồ thị"""
        if node_id in self.nodes:
            del self.nodes[node_id]
            # Xóa tất cả cạnh liên quan
            self.edges = [e for e in self.edges if e['from'] != node_id and e['to'] != node_id]
            return True
        return False
    
    def add_edge(self, from_node, to_node, weight=1):
        """Thêm cạnh vào đồ thị"""
        if from_node in self.nodes and to_node in self.nodes:
            # Kiểm tra cạnh đã tồn tại chưa
            for edge in self.edges:
                if edge['from'] == from_node and edge['to'] == to_node:
                    return False  # Cạnh đã tồn tại
                if not self.directed and edge['from'] == to_node and edge['to'] == from_node:
                    return False  # Cạnh ngược đã tồn tại (đồ thị vô hướng)
            
            self.edges.append({'from': from_node, 'to': to_node, 'weight': weight})
            return True
        return False
    
    def remove_edge(self, from_node, to_node):
        """Xóa cạnh khỏi đồ thị"""
        for i, edge in enumerate(self.edges):
            if edge['from'] == from_node and edge['to'] == to_node:
                self.edges.pop(i)
                return True
            if not self.directed and edge['from'] == to_node and edge['to'] == from_node:
                self.edges.pop(i)
                return True
        return False
    
    def get_neighbors(self, node_id):
        """Lấy danh sách láng giềng của một đỉnh"""
        neighbors = []
        for edge in self.edges:
            if edge['from'] == node_id:
                neighbors.append(edge['to'])
            elif not self.directed and edge['to'] == node_id:
                neighbors.append(edge['from'])
        return neighbors
    
    def get_edge_weight(self, from_node, to_node):
        """Lấy trọng số của cạnh"""
        for edge in self.edges:
            if edge['from'] == from_node and edge['to'] == to_node:
                return edge['weight']
            if not self.directed and edge['from'] == to_node and edge['to'] == from_node:
                return edge['weight']
        return None
    
    def clear(self):
        """Xóa toàn bộ đồ thị"""
        self.nodes = {}
        self.edges = []
        self.node_counter = 0
    
    def get_adjacency_matrix(self):
        """Chuyển đổi sang ma trận kề"""
        n = len(self.nodes)
        if n == 0:
            return []
        
        # Tạo mapping từ node_id sang index
        node_ids = sorted(self.nodes.keys())
        id_to_index = {node_id: i for i, node_id in enumerate(node_ids)}
        
        # Khởi tạo ma trận
        matrix = [[0] * n for _ in range(n)]
        
        # Điền giá trị
        for edge in self.edges:
            i = id_to_index[edge['from']]
            j = id_to_index[edge['to']]
            matrix[i][j] = edge['weight'] if self.weighted else 1
            
            if not self.directed:
                matrix[j][i] = edge['weight'] if self.weighted else 1
        
        return matrix, node_ids
    
    def get_adjacency_list(self):
        """Chuyển đổi sang danh sách kề"""
        adj_list = {node_id: [] for node_id in self.nodes.keys()}
        
        for edge in self.edges:
            info = (edge['to'], edge['weight']) if self.weighted else edge['to']
            adj_list[edge['from']].append(info)
            
            if not self.directed:
                info = (edge['from'], edge['weight']) if self.weighted else edge['from']
                adj_list[edge['to']].append(info)
        
        return adj_list
    
    def get_edge_list(self):
        """Chuyển đổi sang danh sách cạnh"""
        return [
            (edge['from'], edge['to'], edge['weight']) 
            for edge in self.edges
        ]
    
    def to_dict(self):
        """Xuất đồ thị sang dictionary"""
        return {
            'nodes': self.nodes.copy(),
            'edges': self.edges.copy(),
            'directed': self.directed,
            'weighted': self.weighted,
            'node_counter': self.node_counter
        }
    
    def from_dict(self, data):
        """Nhập đồ thị từ dictionary"""
        self.nodes = data['nodes'].copy()
        self.edges = data['edges'].copy()
        self.directed = data['directed']
        self.weighted = data['weighted']
        self.node_counter = data['node_counter']
    
    def get_node_count(self):
        """Đếm số đỉnh"""
        return len(self.nodes)
    
    def get_edge_count(self):
        """Đếm số cạnh"""
        return len(self.edges)
