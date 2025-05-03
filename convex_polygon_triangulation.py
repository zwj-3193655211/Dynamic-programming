from PySide6.QtWidgets import QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QTextEdit
from PySide6.QtCore import Qt
from main import find_widget, set_square_cells

# 生成权重表格的函数
def generate_weight_table(main_window):
    # 从主窗口中查找名为 "dot_num" 的 QLineEdit 控件，用于输入顶点数
    dot_num_input = find_widget(main_window, QLineEdit, "dot_num")
    # 从主窗口中查找名为 "input_weight" 的 QTableWidget 控件，用于输入权重
    input_weight_table = find_widget(main_window, QTableWidget, "input_weight")
    try:
        # 将输入的顶点数转换为整数
        dot_num = int(dot_num_input.text())
        # 检查顶点数是否小于 3，如果小于 3 则弹出警告框
        if dot_num < 3:
            QMessageBox.warning(main_window, "输入错误", "顶点数必须大于等于 3！")
            return
        # 设置输入权重表格的行数和列数为顶点数
        input_weight_table.setRowCount(dot_num)
        input_weight_table.setColumnCount(dot_num)
        # 遍历表格的每一个单元格
        for i in range(dot_num):
            for j in range(dot_num):
                # 当 i 大于等于 j 时，将单元格的值设为 0，并将其设置为不可编辑
                if i >= j:
                    item = QTableWidgetItem("0")
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    input_weight_table.setItem(i, j, item)
        # 设置表格单元格为正方形，大小为 40
        set_square_cells(input_weight_table, size=40)
    except ValueError:
        # 如果输入的顶点数无法转换为整数，弹出警告框
        QMessageBox.warning(main_window, "输入错误", "请输入有效的整数！")

# 解决凸多边形三角剖分问题的函数，使用动态规划算法
def solve_convex_polygon_triangulation(weights):
    # 获取权重矩阵的长度，即顶点数
    n = len(weights)
    # 初始化 m 矩阵，用于存储子问题的最优解
    m = [[0] * n for _ in range(n)]
    # 初始化 s 矩阵，用于记录最优分割点
    s = [[0] * n for _ in range(n)]

    # l 表示子问题中多边形的边数差，即子问题规模
    for l in range(2, n):
        # 遍历所有可能的起始顶点
        for i in range(n - l):
            # 计算对应的结束顶点
            j = i + l
            # 初始化 m[i][j] 为无穷大
            m[i][j] = float('inf')
            # 遍历所有可能的分割点
            for k in range(i + 1, j):
                # 计算当前分割点下的代价
                q = m[i][k] + m[k][j] + weights[i][k] + weights[k][j] + weights[i][j]
                # 如果当前代价小于 m[i][j]，更新 m[i][j] 和 s[i][j]
                if q < m[i][j]:
                    m[i][j] = q
                    s[i][j] = k
    # 返回 m 矩阵和 s 矩阵
    return m, s

# 获取完整的连线组合的函数
def get_connections(s_table, start, end):
    # 初始化连线组合列表
    all_connections = []
    # 当起始顶点小于结束顶点减 1 时，进行递归计算
    if start < end - 1:
        # 获取最优分割点
        k = s_table[start][end]
        # 递归计算左半部分的连线组合
        left_connections = get_connections(s_table, start, k)
        # 递归计算右半部分的连线组合
        right_connections = get_connections(s_table, k, end)
        # 如果左半部分没有连线组合，将其初始化为空列表
        if not left_connections:
            left_connections = [[]]
        # 如果右半部分没有连线组合，将其初始化为空列表
        if not right_connections:
            right_connections = [[]]
        # 遍历左半部分和右半部分的连线组合，生成新的连线组合
        for l_conn in left_connections:
            for r_conn in right_connections:
                new_conn = l_conn + r_conn + [(start, k), (k, end)]
                all_connections.append(new_conn)
    else:
        # 如果起始顶点大于等于结束顶点减 1，返回空列表
        return [[]]
    # 返回所有连线组合
    return all_connections

# 计算凸多边形三角剖分的函数
def calculate_convex_polygon_triangulation(main_window):
    # 从主窗口中查找名为 "input_weight" 的 QTableWidget 控件，用于输入权重
    input_weight_table = find_widget(main_window, QTableWidget, "input_weight")
    # 从主窗口中查找名为 "min_sum" 的 QLineEdit 控件，用于显示最小和
    min_sum_output = find_widget(main_window, QLineEdit, "min_sum")
    # 从主窗口中查找名为 "table_min" 的 QTableWidget 控件，用于显示最小代价表格
    table_min = find_widget(main_window, QTableWidget, "table_min")
    # 从主窗口中查找名为 "output_connection" 的 QTextEdit 控件，用于显示连线组合
    output_connection = find_widget(main_window, QTextEdit, "output_connection")
    # 获取输入权重表格的行数，即顶点数
    dot_num = input_weight_table.rowCount()
    # 初始化权重矩阵
    weights = [[0] * dot_num for _ in range(dot_num)]
    # 遍历输入权重表格的每一个单元格
    for i in range(dot_num):
        for j in range(dot_num):
            # 当 i 小于 j 时，获取单元格的值并转换为浮点数
            if i < j:
                try:
                    weights[i][j] = float(input_weight_table.item(i, j).text())
                    # 由于权重矩阵是对称的，将对称位置的值也设为相同
                    weights[j][i] = weights[i][j]
                except (AttributeError, ValueError):
                    # 如果单元格的值无法转换为浮点数，弹出警告框
                    QMessageBox.warning(main_window, "输入错误", "请输入有效的权值！")
                    return

    # 调用 solve_convex_polygon_triangulation 函数计算最小代价和最优分割点
    m, s = solve_convex_polygon_triangulation(weights)
    # 获取凸多边形三角剖分的最小和
    min_sum = m[0][dot_num - 1]
    # 将最小和显示在对应的 QLineEdit 控件中
    min_sum_output.setText(str(min_sum))

    # 设置最小代价表格的行数和列数
    table_min.setRowCount(dot_num - 1)
    table_min.setColumnCount(dot_num - 1)
    # 遍历最小代价表格的每一个单元格，将最小代价填入
    for i in range(dot_num - 1):
        for j in range(i + 1, dot_num - 1):
            table_min.setItem(i, j, QTableWidgetItem(str(m[i][j + 1])))
    # 设置表格单元格为正方形，大小为 40
    set_square_cells(table_min, size=40)

    # 如果存在输出连线组合的 QTextEdit 控件
    if output_connection:
        # 调用 get_connections 函数获取所有连线组合
        conn_list = get_connections(s, 0, dot_num - 1)
        # 初始化输出文本
        output_text = ""
        # 遍历所有连线组合，将其格式化为文本
        for idx, conn in enumerate(conn_list, 1):
            output_text += f"最优解{idx}："
            for c in conn:
                output_text += f"({c[0] + 1},{c[1] + 1}) "  # 假设界面显示从 1 开始编号
            output_text += "\n"
        # 将输出文本显示在对应的 QTextEdit 控件中
        output_connection.setText(output_text)

# 初始化凸多边形三角剖分功能的函数
def init_convex_polygon_triangulation(main_window):
    # 从主窗口中查找名为 "defined" 的 QPushButton 控件，用于定义顶点数
    defined_btn = find_widget(main_window, QPushButton, "defined")
    # 从主窗口中查找名为 "Start_4" 的 QPushButton 控件，用于开始计算
    start_btn = find_widget(main_window, QPushButton, "Start_4")
    # 如果存在定义按钮，为其点击事件绑定 generate_weight_table 函数
    if defined_btn:
        defined_btn.clicked.connect(lambda: generate_weight_table(main_window))
    # 如果存在开始按钮，为其点击事件绑定 calculate_convex_polygon_triangulation 函数
    if start_btn:
        start_btn.clicked.connect(lambda: calculate_convex_polygon_triangulation(main_window))