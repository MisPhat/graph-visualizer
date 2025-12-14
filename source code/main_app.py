"""
main_app.py - Controller chính của ứng dụng
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import json
import math
import time

from graph import Graph
from algorithms import GraphAlgorithms
from canvas_view import GraphCanvas
from ui_components import Sidebar, Toolbar, StatusBar, InfoPanel, InputDialog


class GraphVisualizerApp:
    """Ứng dụng trực quan hóa đồ thị"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Visualizer - Python Tkinter")
        self.root.geometry("1400x800")
        
        # Graph và state
        self.graph = Graph()
        self.mode = 'add_node'
        self.selected_node = None
        self.animation_speed = 500
        self.is_animating = False
        
        # Setup UI
        self.setup_styles()
        self.setup_ui()
        
        # Bind keyboard shortcuts
        self.root.bind('<Escape>', lambda e: self.reset_visualization())
    
    def setup_styles(self):
        """Thiết lập style cho ttk widgets"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colors
        bg_dark = '#0A1929'
        bg_surface = '#132F4C'
        bg_surface_light = '#1E4976'
        text_color = '#E3F2FD'
        accent_color = '#FF6B35'
        primary_color = '#2196F3'
        
        # Configure styles
        style.configure('Sidebar.TFrame', background=bg_surface)
        style.configure('Toolbar.TFrame', background=bg_surface, relief='flat')
        style.configure('StatusBar.TFrame', background=bg_surface)
        
        style.configure('Title.TLabel', background=bg_surface, foreground=text_color,
                       font=('Arial', 18, 'bold'))
        style.configure('Subtitle.TLabel', background=bg_surface, foreground='#90CAF9',
                       font=('Arial', 9))
        style.configure('Section.TLabel', background=bg_surface, foreground=accent_color,
                       font=('Arial', 10, 'bold'))
        style.configure('Label.TLabel', background=bg_surface, foreground='#90CAF9',
                       font=('Arial', 9))
        style.configure('Status.TLabel', background=bg_surface, foreground='#90CAF9',
                       font=('Arial', 9))
        
        style.configure('TButton', background=bg_surface_light, foreground=text_color,
                       borderwidth=1, relief='flat', font=('Arial', 9))
        style.map('TButton', background=[('active', primary_color)])
        
        style.configure('Custom.TCheckbutton', background=bg_surface, foreground=text_color,
                       font=('Arial', 9))
        
        style.configure('TEntry', fieldbackground=bg_dark, foreground=text_color,
                       borderwidth=1, relief='flat')
        
        style.configure('TCombobox', fieldbackground=bg_dark, foreground=text_color,
                       background=bg_surface_light, borderwidth=1)
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True)
        
        # Sidebar
        self.sidebar = Sidebar(main_frame, self)
        self.sidebar.pack(side='left', fill='y', padx=0, pady=0)
        
        # Right panel
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Toolbar
        self.toolbar = Toolbar(right_panel, self)
        self.toolbar.pack(side='top', fill='x', pady=0)
        
        # Canvas
        canvas_frame = ttk.Frame(right_panel)
        canvas_frame.pack(side='top', fill='both', expand=True)
        
        self.canvas = GraphCanvas(canvas_frame, self.graph, width=800, height=600)
        self.canvas.pack(fill='both', expand=True)
        self.canvas.bind('<Button-1>', self.on_canvas_click)
        
        # Status bar
        self.status_bar = StatusBar(right_panel)
        self.status_bar.pack(side='bottom', fill='x')
        
        # Initial draw
        self.root.after(100, self.canvas.draw_all)
    
    def update_graph_type(self):
        """Cập nhật loại đồ thị"""
        self.graph.directed = self.sidebar.directed_var.get()
        self.graph.weighted = self.sidebar.weighted_var.get()
        self.canvas.draw_all()
        self.update_status("Đã cập nhật loại đồ thị")
    
    def set_mode_add_node(self):
        """Chế độ thêm đỉnh"""
        self.mode = 'add_node'
        self.selected_node = None
        self.update_status("Chế độ: Thêm đỉnh - Click vào canvas")
    
    def set_mode_add_edge(self):
        """Chế độ thêm cạnh"""
        self.mode = 'add_edge'
        self.selected_node = None
        self.update_status("Chế độ: Thêm cạnh - Click 2 đỉnh")
    
    def set_mode_remove_node(self):
        """Chế độ xóa đỉnh"""
        self.mode = 'remove_node'
        self.selected_node = None
        self.update_status("Chế độ: Xóa đỉnh - Click vào đỉnh cần xóa")
    
    def set_mode_remove_edge(self):
        """Chế độ xóa cạnh"""
        self.mode = 'remove_edge'
        self.selected_node = None
        self.update_status("Chế độ: Xóa cạnh - Click 2 đỉnh")
    
    def on_canvas_click(self, event):
        """Xử lý click vào canvas"""
        if self.is_animating:
            return
        
        clicked_node = self.canvas.find_node_at(event.x, event.y)
        
        if self.mode == 'add_node':
            if clicked_node is None:
                node_id = self.graph.add_node(event.x, event.y)
                self.canvas.draw_all()
                self.update_counts()
                self.update_status(f"Đã thêm đỉnh {node_id}")
        
        elif self.mode == 'add_edge':
            if clicked_node is not None:
                if self.selected_node is None:
                    self.selected_node = clicked_node
                    self.canvas.set_node_color(clicked_node, 'node_selected')
                    self.update_status(f"Đã chọn đỉnh {clicked_node}, click đỉnh thứ 2")
                else:
                    if self.selected_node != clicked_node:
                        weight = 1
                        if self.graph.weighted:
                            weight = simpledialog.askinteger("Trọng số", 
                                                            "Nhập trọng số cạnh:",
                                                            initialvalue=1,
                                                            minvalue=1)
                            if weight is None:
                                weight = 1
                        
                        if self.graph.add_edge(self.selected_node, clicked_node, weight):
                            self.update_status(f"Đã thêm cạnh {self.selected_node} → {clicked_node}")
                        else:
                            self.update_status("Cạnh đã tồn tại!")
                    
                    self.canvas.reset_colors()
                    self.selected_node = None
                    self.update_counts()
        
        elif self.mode == 'remove_node':
            if clicked_node is not None:
                self.graph.remove_node(clicked_node)
                self.canvas.draw_all()
                self.update_counts()
                self.update_status(f"Đã xóa đỉnh {clicked_node}")
        
        elif self.mode == 'remove_edge':
            if clicked_node is not None:
                if self.selected_node is None:
                    self.selected_node = clicked_node
                    self.canvas.set_node_color(clicked_node, 'node_selected')
                    self.update_status(f"Đã chọn đỉnh {clicked_node}, click đỉnh thứ 2")
                else:
                    if self.graph.remove_edge(self.selected_node, clicked_node):
                        self.update_status(f"Đã xóa cạnh {self.selected_node} → {clicked_node}")
                    else:
                        self.update_status("Không tìm thấy cạnh!")
                    
                    self.canvas.reset_colors()
                    self.selected_node = None
                    self.update_counts()
    
    def clear_graph(self):
        """Xóa toàn bộ đồ thị"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa toàn bộ đồ thị?"):
            self.graph.clear()
            self.canvas.draw_all()
            self.update_counts()
            self.update_status("Đã xóa toàn bộ đồ thị")
    
    def generate_random_graph(self):
        """Tạo đồ thị ngẫu nhiên"""
        dialog = InputDialog(self.root, "Tạo đồ thị ngẫu nhiên", [
            {'name': 'nodes', 'label': 'Số đỉnh:', 'default': '8'},
            {'name': 'edges', 'label': 'Số cạnh:', 'default': '12'}
        ])
        self.root.wait_window(dialog)
        
        if dialog.result:
            try:
                num_nodes = int(dialog.result['nodes'])
                num_edges = int(dialog.result['edges'])
                
                self.graph.clear()
                
                # Tạo các đỉnh theo hình tròn
                cx, cy = self.canvas.get_canvas_center()
                radius = min(self.canvas.winfo_width(), self.canvas.winfo_height()) // 2 - 100
                
                for i in range(num_nodes):
                    angle = 2 * math.pi * i / num_nodes
                    x = cx + radius * math.cos(angle)
                    y = cy + radius * math.sin(angle)
                    self.graph.add_node(x, y)
                
                # Tạo các cạnh ngẫu nhiên
                import random
                added_edges = 0
                max_attempts = num_edges * 10
                attempts = 0
                
                while added_edges < num_edges and attempts < max_attempts:
                    from_node = random.randint(0, num_nodes - 1)
                    to_node = random.randint(0, num_nodes - 1)
                    
                    if from_node != to_node:
                        weight = random.randint(1, 10) if self.graph.weighted else 1
                        if self.graph.add_edge(from_node, to_node, weight):
                            added_edges += 1
                    
                    attempts += 1
                
                self.canvas.draw_all()
                self.update_counts()
                self.update_status(f"Đã tạo đồ thị với {num_nodes} đỉnh và {added_edges} cạnh")
            
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")
    
    def run_bfs(self):
        """Chạy thuật toán BFS"""
        try:
            start = int(self.sidebar.start_node_var.get())
            if start not in self.graph.nodes:
                messagebox.showerror("Lỗi", "Đỉnh bắt đầu không tồn tại!")
                return
            
            self.is_animating = True
            self.canvas.reset_colors()
            
            def callback(node_id, state):
                if state == 'visiting':
                    self.canvas.set_node_color(node_id, 'node_visiting')
                elif state == 'queued':
                    self.canvas.set_node_color(node_id, 'node_selected')
                elif state == 'visited':
                    self.canvas.set_node_color(node_id, 'node_visited')
                self.root.update()
                time.sleep(self.animation_speed / 1000)
            
            order = GraphAlgorithms.bfs(self.graph, start, callback)
            self.update_status(f"BFS hoàn thành: {' → '.join(map(str, order))}")
            messagebox.showinfo("BFS", f"Thứ tự duyệt:\n{' → '.join(map(str, order))}")
            
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập đỉnh hợp lệ!")
        finally:
            self.is_animating = False
    
    def run_dfs(self):
        """Chạy thuật toán DFS"""
        try:
            start = int(self.sidebar.start_node_var.get())
            if start not in self.graph.nodes:
                messagebox.showerror("Lỗi", "Đỉnh bắt đầu không tồn tại!")
                return
            
            self.is_animating = True
            self.canvas.reset_colors()
            
            def callback(node_id, state):
                if state == 'visiting':
                    self.canvas.set_node_color(node_id, 'node_visiting')
                elif state == 'visited':
                    self.canvas.set_node_color(node_id, 'node_visited')
                self.root.update()
                time.sleep(self.animation_speed / 1000)
            
            order = GraphAlgorithms.dfs(self.graph, start, callback)
            self.update_status(f"DFS hoàn thành: {' → '.join(map(str, order))}")
            messagebox.showinfo("DFS", f"Thứ tự duyệt:\n{' → '.join(map(str, order))}")
            
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập đỉnh hợp lệ!")
        finally:
            self.is_animating = False
    
    def run_dijkstra(self):
        """Chạy thuật toán Dijkstra"""
        try:
            source = int(self.sidebar.source_node_var.get())
            target = int(self.sidebar.target_node_var.get())
            
            if source not in self.graph.nodes or target not in self.graph.nodes:
                messagebox.showerror("Lỗi", "Đỉnh không tồn tại!")
                return
            
            self.is_animating = True
            self.canvas.reset_colors()
            
            def callback(node_id, state, distance):
                if state == 'visiting':
                    self.canvas.set_node_color(node_id, 'node_visiting')
                elif state == 'visited':
                    self.canvas.set_node_color(node_id, 'node_visited')
                self.root.update()
                time.sleep(self.animation_speed / 1000)
            
            path, distance = GraphAlgorithms.dijkstra(self.graph, source, target, callback)
            
            if path:
                self.canvas.highlight_path(path)
                self.update_status(f"Đường đi ngắn nhất: {' → '.join(map(str, path))}, độ dài: {distance}")
                messagebox.showinfo("Dijkstra", 
                                  f"Đường đi ngắn nhất:\n{' → '.join(map(str, path))}\n\nĐộ dài: {distance}")
            else:
                messagebox.showinfo("Dijkstra", "Không có đường đi!")
            
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập đỉnh hợp lệ!")
        finally:
            self.is_animating = False
    
    def check_bipartite(self):
        """Kiểm tra đồ thị 2 phía"""
        if len(self.graph.nodes) == 0:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
        
        self.is_animating = True
        self.canvas.reset_colors()
        
        def callback(node_id, state, color):
            if state == 'visiting':
                color_key = 'node_bipartite_0' if color == 0 else 'node_bipartite_1'
                self.canvas.set_node_color(node_id, color_key)
            elif state == 'colored':
                color_key = 'node_bipartite_0' if color == 0 else 'node_bipartite_1'
                self.canvas.set_node_color(node_id, color_key)
            elif state == 'conflict':
                self.canvas.set_node_color(node_id, 'node_conflict')
            self.root.update()
            time.sleep(self.animation_speed / 1000)
        
        is_bipartite, coloring = GraphAlgorithms.check_bipartite(self.graph, callback)
        
        if is_bipartite:
            messagebox.showinfo("Kết quả", "Đây LÀ đồ thị 2 phía!")
            self.update_status("Đồ thị 2 phía - Các tập được tô màu xanh và tím")
        else:
            messagebox.showinfo("Kết quả", "Đây KHÔNG PHẢI là đồ thị 2 phía!")
            self.update_status("Không phải đồ thị 2 phía - Các đỉnh đỏ vi phạm")
        
        self.is_animating = False
    
    def run_prim(self):
        """Chạy thuật toán Prim"""
        if self.graph.directed:
            messagebox.showwarning("Cảnh báo", "Thuật toán Prim chỉ áp dụng cho đồ thị vô hướng!")
            return
        
        if len(self.graph.nodes) == 0:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
        
        self.is_animating = True
        self.canvas.reset_colors()
        
        def callback(node_id, state, from_node, to_node, weight):
            if state == 'added':
                self.canvas.set_node_color(node_id, 'node_visiting')
                self.canvas.set_edge_color(from_node, to_node, 'edge_mst')
                self.root.update()
                time.sleep(self.animation_speed / 1000)
        
        mst_edges, total_weight = GraphAlgorithms.prim(self.graph, callback)
        
        messagebox.showinfo("Prim's Algorithm",
                          f"Cây khung nhỏ nhất\n\nSố cạnh: {len(mst_edges)}\nTổng trọng số: {total_weight}")
        self.update_status(f"Prim hoàn thành - Tổng trọng số: {total_weight}")
        
        self.is_animating = False
    
    def run_kruskal(self):
        """Chạy thuật toán Kruskal"""
        if self.graph.directed:
            messagebox.showwarning("Cảnh báo", "Thuật toán Kruskal chỉ áp dụng cho đồ thị vô hướng!")
            return
        
        if len(self.graph.nodes) == 0:
            messagebox.showwarning("Cảnh báo", "Đồ thị rỗng!")
            return
        
        self.is_animating = True
        self.canvas.reset_colors()
        
        def callback(node_id, state, from_node, to_node, weight):
            if state == 'checking':
                self.canvas.set_edge_color(from_node, to_node, 'node_visiting')
            elif state == 'added':
                self.canvas.set_edge_color(from_node, to_node, 'edge_mst')
                self.canvas.set_node_color(from_node, 'node_visiting')
                self.canvas.set_node_color(to_node, 'node_visiting')
            elif state == 'rejected':
                self.canvas.set_edge_color(from_node, to_node, 'edge_rejected')
            self.root.update()
            time.sleep(self.animation_speed / 1000)
        
        mst_edges, total_weight = GraphAlgorithms.kruskal(self.graph, callback)
        
        messagebox.showinfo("Kruskal's Algorithm",
                          f"Cây khung nhỏ nhất\n\nSố cạnh: {len(mst_edges)}\nTổng trọng số: {total_weight}")
        self.update_status(f"Kruskal hoàn thành - Tổng trọng số: {total_weight}")
        
        self.is_animating = False
    
    def run_ford_fulkerson(self):
        """Chạy thuật toán Ford-Fulkerson"""
        if not self.graph.directed:
            messagebox.showwarning("Cảnh báo", "Thuật toán Ford-Fulkerson cần đồ thị có hướng!")
            return
        
        dialog = InputDialog(self.root, "Ford-Fulkerson", [
            {'name': 'source', 'label': 'Đỉnh nguồn:', 'default': '0'},
            {'name': 'sink', 'label': 'Đỉnh đích:', 'default': str(len(self.graph.nodes) - 1)}
        ])
        self.root.wait_window(dialog)
        
        if dialog.result:
            try:
                source = int(dialog.result['source'])
                sink = int(dialog.result['sink'])
                
                if source not in self.graph.nodes or sink not in self.graph.nodes:
                    messagebox.showerror("Lỗi", "Đỉnh không tồn tại!")
                    return
                
                self.is_animating = True
                self.canvas.reset_colors()
                
                def callback(path, state, flow, iterations):
                    if state == 'path_found':
                        for i in range(len(path) - 1):
                            self.canvas.set_edge_color(path[i], path[i+1], 'edge_selected')
                        self.root.update()
                        time.sleep(self.animation_speed / 1000)
                        self.canvas.reset_colors()
                
                max_flow = GraphAlgorithms.ford_fulkerson(self.graph, source, sink, callback)
                
                messagebox.showinfo("Ford-Fulkerson",
                                  f"Luồng cực đại: {max_flow}")
                self.update_status(f"Ford-Fulkerson hoàn thành - Luồng cực đại: {max_flow}")
                
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ!")
            finally:
                self.is_animating = False
    
    def run_fleury(self):
        """Chạy thuật toán Fleury"""
        if self.graph.directed or len(self.graph.nodes) == 0:
            messagebox.showwarning("Cảnh báo", "Thuật toán Fleury chỉ áp dụng cho đồ thị vô hướng!")
            return
        
        self.is_animating = True
        self.canvas.reset_colors()
        
        def callback(circuit, state, edge):
            if state == 'edge_added':
                self.canvas.set_edge_color(edge['from'], edge['to'], 'edge_selected')
                self.root.update()
                time.sleep(self.animation_speed / 1000)
        
        circuit = GraphAlgorithms.fleury(self.graph, callback)
        
        if circuit:
            self.canvas.highlight_path(circuit)
            messagebox.showinfo("Fleury's Algorithm",
                              f"Chu trình Euler:\n{' → '.join(map(str, circuit))}")
            self.update_status(f"Fleury hoàn thành - Tìm thấy chu trình Euler")
        else:
            messagebox.showinfo("Fleury's Algorithm",
                              "Đồ thị không có chu trình Euler!\n(Cần tất cả đỉnh có bậc chẵn)")
            self.update_status("Không có chu trình Euler")
        
        self.is_animating = False
    
    def run_hierholzer(self):
        """Chạy thuật toán Hierholzer"""
        if self.graph.directed or len(self.graph.nodes) == 0:
            messagebox.showwarning("Cảnh báo", "Thuật toán Hierholzer chỉ áp dụng cho đồ thị vô hướng!")
            return
        
        self.is_animating = True
        self.canvas.reset_colors()
        
        def callback(data, state):
            self.root.update()
            time.sleep(self.animation_speed / 2000)
        
        circuit = GraphAlgorithms.hierholzer(self.graph, callback)
        
        if circuit:
            self.canvas.highlight_path(circuit)
            messagebox.showinfo("Hierholzer's Algorithm",
                              f"Chu trình Euler:\n{' → '.join(map(str, circuit))}")
            self.update_status(f"Hierholzer hoàn thành - Tìm thấy chu trình Euler")
        else:
            messagebox.showinfo("Hierholzer's Algorithm",
                              "Đồ thị không có chu trình Euler!\n(Cần tất cả đỉnh có bậc chẵn)")
            self.update_status("Không có chu trình Euler")
        
        self.is_animating = False
    
    def show_representation(self, rep_type):
        """Hiển thị biểu diễn đồ thị"""
        content = ""
        
        if rep_type == 'matrix':
            matrix, node_ids = self.graph.get_adjacency_matrix()
            if not matrix:
                messagebox.showinfo("Ma trận kề", "Đồ thị rỗng!")
                return
            
            content = "MA TRẬN KỀ\n\n"
            content += "    " + "  ".join(str(i).rjust(2) for i in node_ids) + "\n"
            for i, row in enumerate(matrix):
                content += f"{node_ids[i]:2d} [{' '.join(str(v).rjust(2) for v in row)}]\n"
        
        elif rep_type == 'list':
            adj_list = self.graph.get_adjacency_list()
            if not adj_list:
                messagebox.showinfo("Danh sách kề", "Đồ thị rỗng!")
                return
            
            content = "DANH SÁCH KỀ\n\n"
            for node_id in sorted(adj_list.keys()):
                neighbors = adj_list[node_id]
                if self.graph.weighted:
                    neighbor_str = ", ".join(f"{n}({w})" for n, w in neighbors)
                else:
                    neighbor_str = ", ".join(str(n) for n in neighbors)
                content += f"{node_id}: {neighbor_str if neighbor_str else '(rỗng)'}\n"
        
        elif rep_type == 'edges':
            edge_list = self.graph.get_edge_list()
            if not edge_list:
                messagebox.showinfo("Danh sách cạnh", "Không có cạnh!")
                return
            
            content = "DANH SÁCH CẠNH\n\n"
            arrow = "→" if self.graph.directed else "—"
            for from_node, to_node, weight in edge_list:
                if self.graph.weighted:
                    content += f"{from_node} {arrow} {to_node} ({weight})\n"
                else:
                    content += f"{from_node} {arrow} {to_node}\n"
        
        InfoPanel(self.root, f"Biểu diễn đồ thị - {rep_type}", content)
    
    def save_graph(self):
        """Lưu đồ thị vào file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.graph.to_dict(), f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Thành công", "Đã lưu đồ thị!")
                self.update_status(f"Đã lưu: {filename}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu file: {str(e)}")
    
    def load_graph(self):
        """Tải đồ thị từ file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.graph.from_dict(data)
                self.sidebar.directed_var.set(self.graph.directed)
                self.sidebar.weighted_var.set(self.graph.weighted)
                self.canvas.draw_all()
                self.update_counts()
                messagebox.showinfo("Thành công", "Đã tải đồ thị!")
                self.update_status(f"Đã tải: {filename}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể tải file: {str(e)}")
    
    def import_graph(self):
        """Import đồ thị từ JSON"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Import JSON")
        dialog.geometry("500x400")
        
        text = tk.Text(dialog, wrap=tk.WORD)
        text.pack(fill='both', expand=True, padx=10, pady=10)
        
        def do_import():
            try:
                data = json.loads(text.get('1.0', 'end'))
                self.graph.from_dict(data)
                self.sidebar.directed_var.set(self.graph.directed)
                self.sidebar.weighted_var.set(self.graph.weighted)
                self.canvas.draw_all()
                self.update_counts()
                dialog.destroy()
                messagebox.showinfo("Thành công", "Đã import đồ thị!")
                self.update_status("Đã import từ JSON")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Dữ liệu JSON không hợp lệ: {str(e)}")
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Import", command=do_import).pack(side='right', padx=5)
        ttk.Button(btn_frame, text="Hủy", command=dialog.destroy).pack(side='right', padx=5)
    
    def export_graph(self):
        """Export đồ thị ra JSON"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Export JSON")
        dialog.geometry("500x400")
        
        text = tk.Text(dialog, wrap=tk.WORD)
        text.pack(fill='both', expand=True, padx=10, pady=10)
        text.insert('1.0', json.dumps(self.graph.to_dict(), indent=2, ensure_ascii=False))
        text.config(state='disabled')
        
        def copy_to_clipboard():
            self.root.clipboard_clear()
            self.root.clipboard_append(text.get('1.0', 'end'))
            messagebox.showinfo("Thành công", "Đã copy vào clipboard!")
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Copy", command=copy_to_clipboard).pack(side='right', padx=5)
        ttk.Button(btn_frame, text="Đóng", command=dialog.destroy).pack(side='right', padx=5)
    
    def reset_visualization(self):
        """Reset trực quan hóa"""
        self.is_animating = False
        self.canvas.reset_colors()
        self.update_status("Đã reset")
    
    def update_speed(self, event=None):
        """Cập nhật tốc độ animation"""
        self.animation_speed = int(self.toolbar.speed_var.get())
    
    def update_status(self, text):
        """Cập nhật thanh trạng thái"""
        self.status_bar.update_status(text)
    
    def update_counts(self):
        """Cập nhật số lượng đỉnh và cạnh"""
        self.status_bar.update_counts(
            self.graph.get_node_count(),
            self.graph.get_edge_count()
        )


def main():
    root = tk.Tk()
    app = GraphVisualizerApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
