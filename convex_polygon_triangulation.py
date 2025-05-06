from PySide6.QtWidgets import QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QTextEdit
from PySide6.QtCore import Qt
from main import find_widget, set_square_cells


# 生成权重表格的函数
def generate_weight_table(main_window):
    dot_num_input = find_widget(main_window, QLineEdit, "dot_num")
    input_weight_table = find_widget(main_window, QTableWidget, "input_weight")
    try:
        dot_num = int(dot_num_input.text())
        if dot_num < 3:
            QMessageBox.warning(main_window, "输入错误", "顶点数必须大于等于 3！")
            return
        input_weight_table.setRowCount(dot_num)
        input_weight_table.setColumnCount(dot_num)
        for i in range(dot_num):
            for j in range(dot_num):
                if i >= j:
                    item = QTableWidgetItem("0")
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    input_weight_table.setItem(i, j, item)
        set_square_cells(input_weight_table, size=40)
    except ValueError:
        QMessageBox.warning(main_window, "输入错误", "请输入有效的整数！")


# 解决凸多边形三角剖分问题的函数（关键修改：记录所有最优分割点）
def solve_convex_polygon_triangulation(weights):
    n = len(weights)
    m = [[0] * n for _ in range(n)]
    # s矩阵存储所有可能的最优分割点（列表形式）
    s = [[[] for _ in range(n)] for _ in range(n)]

    for length in range(2, n):  # 子问题规模从2开始（对应边数，顶点数=length+1）
        # 遍历所有可能的起点
        for i in range(n - length):
            j = i + length
            m[i][j] = float('inf')
            # 遍历断点k，找到最优分割点
            for k in range(i + 1, j):
                # 计算三角形权重分割三角形的权值，要去除重复边！
                weight_ijk = weights[i][j]
                if j - k == 1:
                    weight_ijk += weights[j][k]
                if k - i == 1:
                    weight_ijk += weights[i][k]
                current_cost = m[i][k] + m[k][j] + weight_ijk

                if current_cost < m[i][j]:
                    # 发现更小代价，清空列表并记录新的分割点
                    m[i][j] = current_cost
                    s[i][j] = [k]
                elif current_cost == m[i][j]:
                    # 代价相同，添加新的分割点
                    s[i][j].append(k)

    return m, s


# 获取完整连线组合的函数
def get_connections(s_table, start, end):
    all_connections = []
    if start < end - 1:  # 至少需要3个顶点才能形成三角形
        # 遍历所有可能的最优分割点
        for k in s_table[start][end]:
            # 递归获取左右子问题的所有连接组合
            left_conns = get_connections(s_table, start, k)
            right_conns = get_connections(s_table, k, end)

            # 处理左子问题可能的空结果（当子问题只有两个顶点时）
            left_conns = left_conns if left_conns else [[]]
            right_conns = right_conns if right_conns else [[]]

            # 组合所有可能的左右连接
            for l_conn in left_conns:
                for r_conn in right_conns:
                    # 添加当前分割的两条边（start-k 和 k-en），非相邻点才连线
                    if abs(start - k) != 1:
                        new_conn = l_conn + r_conn + [(start, k)]
                    else:
                        new_conn = l_conn + r_conn
                    if abs(k - end) != 1:
                        new_conn += [(k, end)]
                    all_connections.append(new_conn)
    else:
        # 基础情况：无法分割（少于3个顶点），返回空连接
        return [[]]

    return all_connections


# 计算凸多边形三角剖分的函数
def calculate_convex_polygon_triangulation(main_window):
    input_weight_table = find_widget(main_window, QTableWidget, "input_weight")
    min_sum_output = find_widget(main_window, QLineEdit, "min_sum")
    table_min = find_widget(main_window, QTableWidget, "table_min")
    output_connection = find_widget(main_window, QTextEdit, "output_connection")

    dot_num = input_weight_table.rowCount()
    weights = [[0] * dot_num for _ in range(dot_num)]
    for i in range(dot_num):
        for j in range(dot_num):
            if i < j:
                try:
                    weights[i][j] = float(input_weight_table.item(i, j).text())
                    weights[j][i] = weights[i][j]
                except (AttributeError, ValueError):
                    QMessageBox.warning(main_window, "输入错误", "请输入有效的权值！")
                    return

    m, s = solve_convex_polygon_triangulation(weights)
    min_sum = m[0][dot_num - 1]
    min_sum_output.setText(str(min_sum))

    # 填充最小代价表格
    table_min.setRowCount(dot_num)
    table_min.setColumnCount(dot_num)
    for i in range(dot_num):
        for j in range(i, dot_num):
            item = QTableWidgetItem(str(m[i][j]))
            table_min.setItem(i, j, item)
    set_square_cells(table_min, size=40)

    if output_connection:
        # 获取所有最优解连接组合
        conn_list = get_connections(s, 0, dot_num - 1)
        output_text = ""
        for idx, conn in enumerate(conn_list, 1):
            # 去重处理（避免相同连接不同顺序的重复解，可根据需求调整）
            unique_conn = list(set(conn))  # 转换为集合去重，再转回列表
            output_text += f"最优解{idx}（代价：{min_sum}）："
            # 排序连接以保证显示顺序一致
            for c in sorted(unique_conn, key=lambda x: (x[0], x[1])):
                output_text += f"({c[0] + 1}, {c[1] + 1}) "
            output_text += "\n"
        output_connection.setText(output_text)


# 初始化函数
def init_convex_polygon_triangulation(main_window):
    defined_btn = find_widget(main_window, QPushButton, "defined")
    start_btn = find_widget(main_window, QPushButton, "Start_4")
    if defined_btn:
        defined_btn.clicked.connect(lambda: generate_weight_table(main_window))
    if start_btn:
        start_btn.clicked.connect(lambda: calculate_convex_polygon_triangulation(main_window))