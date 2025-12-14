"""
ui_components.py - Các component UI
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json


class Sidebar(ttk.Frame):
    """Sidebar chứa các điều khiển"""
    
    def __init__(self, parent, controller):
        super().__init__(parent, style='Sidebar.TFrame')
        self.controller = controller
        self.setup_ui()
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        # Title
        title_label = ttk.Label(self, text="Graph Visualizer",
                               style='Title.TLabel')
        title_label.pack(pady=(10, 5), padx=10)
        
        subtitle_label = ttk.Label(self, text="Python Tkinter",
                                  style='Subtitle.TLabel')
        subtitle_label.pack(pady=(0, 15), padx=10)
        
        # Scrollable container
        canvas = tk.Canvas(self, bg='#132F4C', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Sidebar.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Graph Configuration
        self.create_section(scrollable_frame, "⚙ CẤU HÌNH ĐỒ THỊ")
        
        self.directed_var = tk.BooleanVar()
        self.weighted_var = tk.BooleanVar()
        
        ttk.Checkbutton(scrollable_frame, text="Đồ thị có hướng",
                       variable=self.directed_var,
                       command=self.controller.update_graph_type,
                       style='Custom.TCheckbutton').pack(anchor='w', padx=20, pady=2)
        
        ttk.Checkbutton(scrollable_frame, text="Đồ thị có trọng số",
                       variable=self.weighted_var,
                       command=self.controller.update_graph_type,
                       style='Custom.TCheckbutton').pack(anchor='w', padx=20, pady=2)
        
        # Basic Operations
        self.create_section(scrollable_frame, "📊 THAO TÁC CƠ BẢN")
        
        ttk.Button(scrollable_frame, text="➕ Thêm đỉnh",
                  command=self.controller.set_mode_add_node).pack(fill='x', padx=10, pady=2)
        
        ttk.Button(scrollable_frame, text="🔗 Thêm cạnh",
                  command=self.controller.set_mode_add_edge).pack(fill='x', padx=10, pady=2)
        
        ttk.Button(scrollable_frame, text="❌ Xóa đỉnh",
                  command=self.controller.set_mode_remove_node).pack(fill='x', padx=10, pady=2)
        
        ttk.Button(scrollable_frame, text="✂️ Xóa cạnh",
                  command=self.controller.set_mode_remove_edge).pack(fill='x', padx=10, pady=2)
        
        ttk.Button(scrollable_frame, text="🗑️ Xóa toàn bộ",
                  command=self.controller.clear_graph).pack(fill='x', padx=10, pady=2)
        
        # Traversal Algorithms
        self.create_section(scrollable_frame, "🔍 THUẬT TOÁN DUYỆT")
        
        ttk.Button(scrollable_frame, text="BFS - Duyệt theo chiều rộng",
                  command=self.controller.run_bfs).pack(fill='x', padx=10, pady=2)
        
        ttk.Button(scrollable_frame, text="DFS - Duyệt theo chiều sâu",
                  command=self.controller.run_dfs).pack(fill='x', padx=10, pady=2)
        
        ttk.Label(scrollable_frame, text="Đỉnh bắt đầu:",
                 style='Label.TLabel').pack(anchor='w', padx=20, pady=(5, 0))
        
        self.start_node_var = tk.StringVar(value="0")
        ttk.Entry(scrollable_frame, textvariable=self.start_node_var,
                 width=15).pack(anchor='w', padx=20, pady=2)
        
        # Shortest Path
        self.create_section(scrollable_frame, "🎯 ĐƯỜNG ĐI NGẮN NHẤT")
        
        ttk.Button(scrollable_frame, text="Dijkstra Algorithm",
                  command=self.controller.run_dijkstra).pack(fill='x', padx=10, pady=2)
        
        ttk.Label(scrollable_frame, text="Từ đỉnh:",
                 style='Label.TLabel').pack(anchor='w', padx=20, pady=(5, 0))
        
        self.source_node_var = tk.StringVar(value="0")
        ttk.Entry(scrollable_frame, textvariable=self.source_node_var,
                 width=15).pack(anchor='w', padx=20, pady=2)
        
        ttk.Label(scrollable_frame, text="Đến đỉnh:",
                 style='Label.TLabel').pack(anchor='w', padx=20, pady=(5, 0))
        
        self.target_node_var = tk.StringVar(value="1")
        ttk.Entry(scrollable_frame, textvariable=self.target_node_var,
                 width=15).pack(anchor='w', padx=20, pady=2)
        
        # Bipartite Check
        self.create_section(scrollable_frame, "🔲 KIỂM TRA ĐỒ THỊ")
        
        ttk.Button(scrollable_frame, text="Kiểm tra đồ thị 2 phía",
                  command=self.controller.check_bipartite).pack(fill='x', padx=10, pady=2)
        
        # Advanced Algorithms
        self.create_section(scrollable_frame, "🚀 THUẬT TOÁN NÂNG CAO")
        
        ttk.Button(scrollable_frame, text="Prim - Cây khung nhỏ nhất",
                  command=self.controller.run_prim).pack(fill='x', padx=10, pady=2)
        
        ttk.Button(scrollable_frame, text="Kruskal - Cây khung nhỏ nhất",
                  command=self.controller.run_kruskal).pack(fill='x', padx=10, pady=2)
        
        ttk.Button(scrollable_frame, text="Ford-Fulkerson - Luồng cực đại",
                  command=self.controller.run_ford_fulkerson).pack(fill='x', padx=10, pady=2)
        
        ttk.Button(scrollable_frame, text="Fleury - Chu trình Euler",
                  command=self.controller.run_fleury).pack(fill='x', padx=10, pady=2)
        
        ttk.Button(scrollable_frame, text="Hierholzer - Chu trình Euler",
                  command=self.controller.run_hierholzer).pack(fill='x', padx=10, pady=2)
        
        # Representation
        self.create_section(scrollable_frame, "📋 BIỂU DIỄN ĐỒ THỊ")
        
        ttk.Button(scrollable_frame, text="Ma trận kề",
                  command=lambda: self.controller.show_representation('matrix')).pack(fill='x', padx=10, pady=2)
        
        ttk.Button(scrollable_frame, text="Danh sách kề",
                  command=lambda: self.controller.show_representation('list')).pack(fill='x', padx=10, pady=2)
        
        ttk.Button(scrollable_frame, text="Danh sách cạnh",
                  command=lambda: self.controller.show_representation('edges')).pack(fill='x', padx=10, pady=2)
        
        # Save/Load
        self.create_section(scrollable_frame, "💾 LƯU/TẢI ĐỒ THỊ")
        
        ttk.Button(scrollable_frame, text="💾 Lưu đồ thị",
                  command=self.controller.save_graph).pack(fill='x', padx=10, pady=2)
        
        ttk.Button(scrollable_frame, text="📂 Tải đồ thị",
                  command=self.controller.load_graph).pack(fill='x', padx=10, pady=2)
        
        ttk.Button(scrollable_frame, text="📥 Import JSON",
                  command=self.controller.import_graph).pack(fill='x', padx=10, pady=2)
        
        ttk.Button(scrollable_frame, text="📤 Export JSON",
                  command=self.controller.export_graph).pack(fill='x', padx=10, pady=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_section(self, parent, title):
        """Tạo một section với tiêu đề"""
        ttk.Label(parent, text=title, style='Section.TLabel').pack(
            anchor='w', padx=10, pady=(15, 5))


class Toolbar(ttk.Frame):
    """Toolbar trên cùng"""
    
    def __init__(self, parent, controller):
        super().__init__(parent, style='Toolbar.TFrame')
        self.controller = controller
        self.setup_ui()
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        ttk.Button(self, text="⟲ Reset",
                  command=self.controller.reset_visualization).pack(side='left', padx=5)
        
        ttk.Button(self, text="🎲 Đồ thị ngẫu nhiên",
                  command=self.controller.generate_random_graph).pack(side='left', padx=5)
        
        ttk.Separator(self, orient='vertical').pack(side='left', fill='y', padx=10)
        
        ttk.Label(self, text="Tốc độ:", style='Label.TLabel').pack(side='left', padx=5)
        
        self.speed_var = tk.StringVar(value="500")
        speed_combo = ttk.Combobox(self, textvariable=self.speed_var,
                                   values=['50', '200', '500', '1000', '2000'],
                                   width=10, state='readonly')
        speed_combo.pack(side='left', padx=5)
        speed_combo.bind('<<ComboboxSelected>>', self.controller.update_speed)


class StatusBar(ttk.Frame):
    """Thanh trạng thái"""
    
    def __init__(self, parent):
        super().__init__(parent, style='StatusBar.TFrame')
        self.setup_ui()
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        self.status_label = ttk.Label(self, text="Sẵn sàng",
                                     style='Status.TLabel')
        self.status_label.pack(side='left', padx=10)
        
        self.node_count_label = ttk.Label(self, text="Đỉnh: 0",
                                         style='Status.TLabel')
        self.node_count_label.pack(side='right', padx=10)
        
        self.edge_count_label = ttk.Label(self, text="Cạnh: 0",
                                         style='Status.TLabel')
        self.edge_count_label.pack(side='right', padx=10)
    
    def update_status(self, text):
        """Cập nhật trạng thái"""
        self.status_label.config(text=text)
    
    def update_counts(self, nodes, edges):
        """Cập nhật số lượng đỉnh và cạnh"""
        self.node_count_label.config(text=f"Đỉnh: {nodes}")
        self.edge_count_label.config(text=f"Cạnh: {edges}")


class InfoPanel(tk.Toplevel):
    """Panel hiển thị thông tin"""
    
    def __init__(self, parent, title, content):
        super().__init__(parent)
        self.title(title)
        self.geometry("500x400")
        self.configure(bg='#0A1929')
        
        # Make it stay on top
        self.transient(parent)
        
        # Title
        title_label = tk.Label(self, text=title, bg='#132F4C', fg='#FF6B35',
                              font=('Arial', 14, 'bold'), pady=10)
        title_label.pack(fill='x')
        
        # Content
        text_widget = scrolledtext.ScrolledText(self, wrap=tk.WORD,
                                               bg='#132F4C', fg='#E3F2FD',
                                               font=('Courier', 10),
                                               padx=10, pady=10)
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        text_widget.insert('1.0', content)
        text_widget.config(state='disabled')
        
        # Close button
        close_btn = ttk.Button(self, text="Đóng", command=self.destroy)
        close_btn.pack(pady=10)


class InputDialog(tk.Toplevel):
    """Dialog nhập liệu"""
    
    def __init__(self, parent, title, fields):
        super().__init__(parent)
        self.title(title)
        self.configure(bg='#0A1929')
        self.transient(parent)
        self.result = None
        
        self.entries = {}
        
        for field in fields:
            frame = ttk.Frame(self, style='Sidebar.TFrame')
            frame.pack(fill='x', padx=20, pady=5)
            
            label = ttk.Label(frame, text=field['label'], style='Label.TLabel')
            label.pack(side='left', padx=5)
            
            entry = ttk.Entry(frame, width=20)
            entry.insert(0, field.get('default', ''))
            entry.pack(side='right', padx=5)
            
            self.entries[field['name']] = entry
        
        # Buttons
        btn_frame = ttk.Frame(self, style='Sidebar.TFrame')
        btn_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(btn_frame, text="OK", command=self.ok).pack(side='right', padx=5)
        ttk.Button(btn_frame, text="Hủy", command=self.cancel).pack(side='right', padx=5)
        
        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (self.winfo_width() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")
        
        self.grab_set()
    
    def ok(self):
        """Xác nhận"""
        self.result = {name: entry.get() for name, entry in self.entries.items()}
        self.destroy()
    
    def cancel(self):
        """Hủy"""
        self.destroy()
