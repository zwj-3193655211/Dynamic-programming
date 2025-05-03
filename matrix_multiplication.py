from PySide6.QtWidgets import QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from main import find_widget, set_square_cells


# 定义一个函数，用于根据用户输入的矩阵数量生成矩阵维度输入表格
def generate_dim_table(main_window):
    matrix_count_input = find_widget(main_window, QLineEdit, "matrix_count_input")
    matrix_dim_table = find_widget(main_window, QTableWidget, "matrix_dim_table")
    try:
        # 将用户输入的矩阵数量转换为整数
        matrix_count = int(matrix_count_input.text())
        # 检查矩阵数量是否小于 2，如果是，显示错误消息框
        if matrix_count < 2:
            QMessageBox.warning(main_window, "输入错误", "矩阵数量必须大于等于 2！")
            return
        # 设置矩阵维度输入表格的行数
        matrix_dim_table.setRowCount(matrix_count)
        # 设置矩阵维度输入表格的列数
        matrix_dim_table.setColumnCount(2)
        # 设置矩阵维度输入表格的水平表头标签
        matrix_dim_table.setHorizontalHeaderLabels(["行", "列"])
        # 调用 set_square_cells 函数，将矩阵维度输入表格的单元格设置为正方形
        set_square_cells(matrix_dim_table, size=43)
    except ValueError:
        # 如果用户输入的不是有效的整数，显示错误消息框
        QMessageBox.warning(main_window, "输入错误", "请输入有效的整数！")


# 定义一个函数，用于根据用户输入的矩阵维度计算矩阵连乘的最小乘法次数和最优分割点
def calculate_matrices(main_window):
    matrix_dim_table = find_widget(main_window, QTableWidget, "matrix_dim_table")
    m_table = find_widget(main_window, QTableWidget, "m_table")
    s_table = find_widget(main_window, QTableWidget, "s_table")
    # 初始化一个空列表，用于存储矩阵的维度信息
    dimensions = []
    # 按行遍历矩阵维度输入表格的每一行
    for row in range(matrix_dim_table.rowCount()):
        try:
            # 获取当前行第一列的文本并转换为整数，表示矩阵的行数
            rows = int(matrix_dim_table.item(row, 0).text())
            # 获取当前行第二列的文本并转换为整数，表示矩阵的列数
            cols = int(matrix_dim_table.item(row, 1).text())
            # 检查是否为第一个矩阵，如果不是，检查当前矩阵的行数是否等于前一个矩阵的列数
            if row > 0 and rows != dimensions[-1]:
                QMessageBox.warning(main_window, "输入错误", "矩阵无法连乘，当前矩阵的行数与前一个矩阵的列数不匹配！")
                return
            # 如果是第一行，将行数添加到维度列表中
            if row == 0:
                dimensions.append(rows)
            # 将列数添加到维度列表中
            dimensions.append(cols)
        except (AttributeError, ValueError):
            # 如果获取或转换文本时出现异常，显示错误消息框
            QMessageBox.warning(main_window, "输入错误", "请输入有效的矩阵维度！")
            return


    # 如果维度列表中的元素数量大于 1
    if len(dimensions) > 1:
        # 调用 solve_matrix_multiplication 函数，计算最小乘法次数和最优分割点
        m, s = solve_matrix_multiplication(dimensions)
        # 计算矩阵的数量
        # 虽然前面已经有用户输入的矩阵数量，但是这里有dimensions的长度，可以不额外调用用户输入的矩阵数量
        n = len(dimensions) - 1
        # 设置最小乘法次数表格的行数
        m_table.setRowCount(n)
        # 设置最小乘法次数表格的列数
        m_table.setColumnCount(n)
        # 设置最优分割点表格的行数
        s_table.setRowCount(n)
        # 设置最优分割点表格的列数
        s_table.setColumnCount(n)
        # 遍历每一行
        for i in range(n):
            # 遍历每一列
            for j in range(n):
                # 将最小乘法次数表格中的值添加到 m_table 中
                m_table.setItem(i, j, QTableWidgetItem(str(m[i + 1][j + 1])))
                # 将最优分割点表格中的值添加到 s_table 中
                s_table.setItem(i, j, QTableWidgetItem(str(s[i + 1][j + 1])))
        # 调用 set_square_cells 函数，将最小乘法次数表格和最优分割点表格的单元格设置为正方形
        set_square_cells(m_table, s_table, size=43)


def solve_matrix_multiplication(dimensions):
    """
    计算矩阵连乘的最小乘法次数和最优分割点
    :param dimensions: 矩阵维度列表，例如 [p0, p1, p2, ..., pn]，表示矩阵 A1 的维度为 p0 x p1，A2 的维度为 p1 x p2，以此类推
    :return: 最小乘法次数矩阵 m 和最优分割点矩阵 s
    """
    n = len(dimensions)

    # 创建一个二维数组 m 来存储子问题的最优解，默认值为 0，避免了初始化的麻烦
    m = [[0] * n for _ in range(n)]
    # 创建一个二维数组 s 来记录最优分割点
    s = [[0] * n for _ in range(n)]

    # l 表示 l个矩阵连乘，从 2 开始，因为 1 时不存在连乘
    for l in range(2, n):
        for i in range(1, n - l + 1):
            j = i + l - 1
            m[i][j] = float('inf')# 初始化 m[i][j] 为正无穷大
            for k in range(i, j):
                # 计算代价
                q = m[i][k] + m[k + 1][j] + dimensions[i - 1] * dimensions[k] * dimensions[j]
                if q < m[i][j]:
                    m[i][j] = q
                    s[i][j] = k

    return m, s


def init_matrix_multiplication(main_window):
    generate_table_btn = find_widget(main_window, QPushButton, "generate_table_btn")
    calculate_btn = find_widget(main_window, QPushButton, "calculate_btn")
    # 如果生成表格按钮存在
    if generate_table_btn:
        # 为生成表格按钮的点击事件绑定 generate_dim_table 函数
        generate_table_btn.clicked.connect(lambda: generate_dim_table(main_window))

    # 如果计算按钮存在
    if calculate_btn:
        # 为计算按钮的点击事件绑定 calculate_matrices 函数
        calculate_btn.clicked.connect(lambda: calculate_matrices(main_window))