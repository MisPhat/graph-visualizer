Graph Visualizer - Ứng dụng trực quan hóa đồ thị
Ứng dụng Python Tkinter để trực quan hóa và thực hiện các thuật toán trên đồ thị.
📋 Tính năng
Phần Cơ Bản:

✅ Vẽ đồ thị trực quan - Canvas tương tác
✅ Lưu/Tải đồ thị - Lưu vào file JSON
✅ Đường đi ngắn nhất - Thuật toán Dijkstra
✅ Duyệt đồ thị - BFS & DFS
✅ Kiểm tra đồ thị 2 phía - Thuật toán tô màu
✅ Chuyển đổi biểu diễn - Ma trận kề ↔ Danh sách kề ↔ Danh sách cạnh

Phần Nâng Cao:

✅ Trực quan hóa các thuật toán:

7.1 Prim - Cây khung nhỏ nhất
7.2 Kruskal - Cây khung nhỏ nhất
7.3 Ford-Fulkerson - Luồng cực đại
7.4 Fleury - Chu trình Euler
7.5 Hierholzer - Chu trình Euler



🗂️ Cấu trúc file
graph-visualizer/
├── graph.py           # Class đại diện cho đồ thị
├── algorithms.py      # Các thuật toán đồ thị
├── canvas_view.py     # Giao diện Canvas vẽ đồ thị
├── ui_components.py   # Các component UI (Sidebar, Toolbar, StatusBar...)
├── main_app.py        # Controller chính của ứng dụng
└── README.md          # File này
📦 Yêu cầu

Python 3.6+
Tkinter (thường đi kèm với Python)

🚀 Cách chạy
bashpython main_app.py
📖 Hướng dẫn sử dụng
1. Tạo đồ thị:

Thêm đỉnh: Click nút "Thêm đỉnh" rồi click vào canvas
Thêm cạnh: Click nút "Thêm cạnh", click 2 đỉnh để nối
Xóa đỉnh/cạnh: Chọn chế độ xóa tương ứng
Đồ thị ngẫu nhiên: Click "Đồ thị ngẫu nhiên" để tạo tự động

2. Cấu hình:

Đồ thị có hướng: Check/uncheck checkbox
Đồ thị có trọng số: Check/uncheck checkbox

3. Chạy thuật toán:

Chọn thuật toán từ sidebar
Nhập các tham số cần thiết (đỉnh bắt đầu, đỉnh đích...)
Click nút chạy và xem animation

4. Xem biểu diễn:

Click vào các nút "Ma trận kề", "Danh sách kề", "Danh sách cạnh"
Xem kết quả trong cửa sổ popup

5. Lưu/Tải:

Lưu đồ thị: Lưu vào file JSON
Tải đồ thị: Tải từ file JSON
Import/Export: Copy/paste JSON trực tiếp

🎨 Màu sắc

Xanh dương (#2196F3): Đỉnh mặc định
Xanh lá (#4CAF50): Đỉnh đang xét/đã thêm vào MST
Vàng (#FFC107): Đỉnh trong hàng đợi/đường đi
Cam (#FF6B35): Đỉnh đã thăm
Đỏ (#F44336): Đỉnh vi phạm/cạnh bị loại
Tím (#9C27B0): Tập thứ 2 trong đồ thị 2 phía

⌨️ Phím tắt

ESC: Reset trực quan hóa

🔧 Tùy chỉnh
Bạn có thể điều chỉnh:

Tốc độ animation: Dropdown "Tốc độ" trên toolbar
Màu sắc: Sửa trong canvas_view.py (COLORS dictionary)
Kích thước đỉnh: Sửa NODE_RADIUS trong canvas_view.py

📝 Ví dụ JSON
json{
  "nodes": {
    "0": {"x": 400, "y": 200, "label": "0"},
    "1": {"x": 600, "y": 200, "label": "1"},
    "2": {"x": 500, "y": 400, "label": "2"}
  },
  "edges": [
    {"from": 0, "to": 1, "weight": 5},
    {"from": 1, "to": 2, "weight": 3},
    {"from": 0, "to": 2, "weight": 7}
  ],
  "directed": false,
  "weighted": true,
  "node_counter": 3
}
🐛 Lưu ý

Đồ thị vô hướng: Prim, Kruskal, Fleury, Hierholzer
Đồ thị có hướng: Ford-Fulkerson
BFS, DFS, Dijkstra, Bipartite: Cả hai loại đồ thị
Kéo thả đỉnh: Giữ chuột và kéo để di chuyển đỉnh
