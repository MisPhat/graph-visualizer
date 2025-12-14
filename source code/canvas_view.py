"""
canvas_view.py - Giao diện Canvas để vẽ đồ thị
"""

import tkinter as tk
from tkinter import Canvas
import math


class GraphCanvas(Canvas):
    """Canvas để vẽ và tương tác với đồ thị"""
    
    # Cấu hình màu sắc
    COLORS = {
        'node_default': '#2196F3',
        'node_selected': '#4CAF50',
        'node_visiting': '#FFC107',
        'node_visited': '#FF6B35',
        'node_conflict': '#F44336',
        'node_bipartite_0': '#2196F3',
        'node_bipartite_1': '#9C27B0',
        'edge_default': '#90CAF9',
        'edge_selected': '#FFC107',
        'edge_mst': '#4CAF50',
        'edge_rejected': '#F44336',
        'background': '#0A1929',
        'text': '#E3F2FD',
    }
    
    NODE_RADIUS = 25
    ARROW_SIZE = 12
    
    def __init__(self, parent, graph, **kwargs):
        super().__init__(parent, bg=self.COLORS['background'], 
                        highlightthickness=0, **kwargs)
        self.graph = graph
        self.node_colors = {}
        self.edge_colors = {}
        self.selected_node = None
        
        # Bind events
        self.bind('<Button-1>', self.on_click)
        self.bind('<B1-Motion>', self.on_drag)
        self.bind('<ButtonRelease-1>', self.on_release)
        
        self.dragging_node = None
        
    def draw_all(self):
        """Vẽ toàn bộ đồ thị"""
        self.delete('all')
        
        # Vẽ lưới nền
        self.draw_grid()
        
        # Vẽ cạnh trước
        for edge in self.graph.edges:
            self.draw_edge(edge)
        
        # Vẽ đỉnh sau
        for node_id, node_data in self.graph.nodes.items():
            self.draw_node(node_id, node_data)
    
    def draw_grid(self):
        """Vẽ lưới nền"""
        width = self.winfo_width()
        height = self.winfo_height()
        grid_size = 20
        
        for i in range(0, width, grid_size):
            self.create_line(i, 0, i, height, fill='#132F4C', width=1)
        
        for i in range(0, height, grid_size):
            self.create_line(0, i, width, i, fill='#132F4C', width=1)
    
    def draw_node(self, node_id, node_data):
        """Vẽ một đỉnh"""
        x, y = node_data['x'], node_data['y']
        r = self.NODE_RADIUS
        
        # Lấy màu
        color = self.node_colors.get(node_id, self.COLORS['node_default'])
        
        # Vẽ shadow
        self.create_oval(x - r + 2, y - r + 2, x + r + 2, y + r + 2,
                        fill='#000000', outline='', tags=f'node_{node_id}')
        
        # Vẽ hình tròn
        self.create_oval(x - r, y - r, x + r, y + r,
                        fill=color, outline='#90CAF9', width=2,
                        tags=f'node_{node_id}')
        
        # Vẽ label
        self.create_text(x, y, text=node_data['label'],
                        fill='white', font=('Arial', 12, 'bold'),
                        tags=f'node_{node_id}')
    
    def draw_edge(self, edge):
        """Vẽ một cạnh"""
        from_node = self.graph.nodes.get(edge['from'])
        to_node = self.graph.nodes.get(edge['to'])
        
        if not from_node or not to_node:
            return
        
        x1, y1 = from_node['x'], from_node['y']
        x2, y2 = to_node['x'], to_node['y']
        
        # Tính toán điểm bắt đầu và kết thúc (tránh vẽ vào trong node)
        dx = x2 - x1
        dy = y2 - y1
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance == 0:
            return
        
        r = self.NODE_RADIUS
        start_x = x1 + (dx / distance) * r
        start_y = y1 + (dy / distance) * r
        end_x = x2 - (dx / distance) * r
        end_y = y2 - (dy / distance) * r
        
        # Lấy màu
        edge_key = (edge['from'], edge['to'])
        color = self.edge_colors.get(edge_key, self.COLORS['edge_default'])
        
        # Vẽ đường thẳng
        self.create_line(start_x, start_y, end_x, end_y,
                        fill=color, width=2, tags='edge')
        
        # Vẽ mũi tên nếu là đồ thị có hướng
        if self.graph.directed:
            angle = math.atan2(dy, dx)
            arrow_points = [
                end_x, end_y,
                end_x - self.ARROW_SIZE * math.cos(angle - math.pi/6),
                end_y - self.ARROW_SIZE * math.sin(angle - math.pi/6),
                end_x - self.ARROW_SIZE * math.cos(angle + math.pi/6),
                end_y - self.ARROW_SIZE * math.sin(angle + math.pi/6)
            ]
            self.create_polygon(arrow_points, fill=color, outline=color, tags='edge')
        
        # Vẽ trọng số nếu có
        if self.graph.weighted:
            mid_x = (start_x + end_x) / 2
            mid_y = (start_y + end_y) / 2
            
            # Background cho text
            self.create_rectangle(mid_x - 15, mid_y - 10, mid_x + 15, mid_y + 10,
                                fill=self.COLORS['background'], outline='', tags='edge')
            
            self.create_text(mid_x, mid_y, text=str(edge['weight']),
                           fill='#FFC107', font=('Arial', 10, 'bold'), tags='edge')
    
    def find_node_at(self, x, y):
        """Tìm đỉnh tại vị trí (x, y)"""
        for node_id, node_data in self.graph.nodes.items():
            nx, ny = node_data['x'], node_data['y']
            distance = math.sqrt((x - nx)**2 + (y - ny)**2)
            if distance <= self.NODE_RADIUS:
                return node_id
        return None
    
    def on_click(self, event):
        """Xử lý sự kiện click chuột"""
        node_id = self.find_node_at(event.x, event.y)
        if node_id is not None:
            self.dragging_node = node_id
    
    def on_drag(self, event):
        """Xử lý sự kiện kéo chuột"""
        if self.dragging_node is not None:
            self.graph.nodes[self.dragging_node]['x'] = event.x
            self.graph.nodes[self.dragging_node]['y'] = event.y
            self.draw_all()
    
    def on_release(self, event):
        """Xử lý sự kiện thả chuột"""
        self.dragging_node = None
    
    def set_node_color(self, node_id, color_key):
        """Đặt màu cho đỉnh"""
        if color_key in self.COLORS:
            self.node_colors[node_id] = self.COLORS[color_key]
        else:
            self.node_colors[node_id] = color_key
        self.draw_all()
    
    def set_edge_color(self, from_node, to_node, color_key):
        """Đặt màu cho cạnh"""
        if color_key in self.COLORS:
            self.edge_colors[(from_node, to_node)] = self.COLORS[color_key]
        else:
            self.edge_colors[(from_node, to_node)] = color_key
        self.draw_all()
    
    def reset_colors(self):
        """Reset tất cả màu về mặc định"""
        self.node_colors = {}
        self.edge_colors = {}
        self.draw_all()
    
    def highlight_path(self, path, color='node_visiting'):
        """Làm nổi bật một đường đi"""
        for i, node_id in enumerate(path):
            self.set_node_color(node_id, color)
            if i < len(path) - 1:
                self.set_edge_color(path[i], path[i+1], 'edge_selected')
    
    def get_canvas_center(self):
        """Lấy tâm của canvas"""
        width = self.winfo_width()
        height = self.winfo_height()
        return width // 2, height // 2
