from PySide6.QtWidgets import QMessageBox, QLineEdit, QPushButton, QTextEdit, QTableWidget, QTableWidgetItem
from main import find_widget, set_square_cells
import re

# 解析输入字符串为列表
def parse_input(input_str):
    """
    使用正则表达式分割输入字符串，支持空格、中文逗号、英文逗号，
    并将分割后的部分进一步拆分为单个字符
    """
    # 去除字符串两端空白字符，然后按 [ ,，] 这些分隔符分割，并过滤掉空字符串
    return [char for part in re.split(r'[ ,，]+', input_str.strip()) if part for char in part]

# 计算最长公共子序列
def find_lcs(X, Y):
    """
    计算两个序列 X 和 Y 的最长公共子序列的长度和所有可能的最长公共子序列
    :param X: 第一个序列
    :param Y: 第二个序列
    :return: 最长公共子序列的长度和所有可能的最长公共子序列组成的列表
    """
    m, n = len(X), len(Y)
    # 初始化一个 (m + 1) * (n + 1) 的二维数组 table，元组的第一个元素表示长度，第二个元素表示回溯信息
    table = [[(0, 0)] * (n + 1) for _ in range(m + 1)]

    # 填充 table 数组
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # 如果 X 的第 i 个元素和 Y 的第 j 个元素相等
            if X[i - 1] == Y[j - 1]:
                length = table[i - 1][j - 1][0] + 1
                # 记录回溯信息为 1，表示从左上角来
                backtrack = 1
            # 如果 X 的前 i - 1 个元素和 Y 的前 j 个元素的最长公共子序列长度
            # 大于 X 的前 i 个元素和 Y 的前 j - 1 个元素的最长公共子序列长度
            elif table[i - 1][j][0] > table[i][j - 1][0]:
                length = table[i - 1][j][0]
                # 记录回溯信息为 2，表示从上方来
                backtrack = 2
            # 如果 X 的前 i - 1 个元素和 Y 的前 j 个元素的最长公共子序列长度
            # 小于 X 的前 i 个元素和 Y 的前 j - 1 个元素的最长公共子序列长度
            elif table[i - 1][j][0] < table[i][j - 1][0]:
                length = table[i][j - 1][0]
                # 记录回溯信息为 3，表示从左方来
                backtrack = 3
            # 如果两者相等，意味着有两条路线
            else:
                length = table[i - 1][j][0]  # 或者 table[i][j - 1][0]，因为它们相等
                # 记录回溯信息为 4，表示有两条路线（上方和左方）
                backtrack = 4
            table[i][j] = (length, backtrack)

    lcs_length = table[m][n][0]
    lcs_sequences = []
    stack = [(m, n, [])]
    # 使用栈进行回溯操作
    while stack:
        # 从栈中取出当前位置 (i, j) 以及当前已构建的子序列 current_seq
        i, j, current_seq = stack.pop()
        # 如果已经回溯到边界（i 或 j 为 0 ），说明找到了一条可能的最长公共子序列
        if i == 0 or j == 0:
            # 将当前子序列反转并添加到结果列表 lcs_sequences 中
            lcs_sequences.append(current_seq[::-1])
        # 如果回溯信息为 1，说明当前位置是从左上角来的，即当前字符是公共子序列的一部分
        elif table[i][j][1] == 1:
            # 将当前字符添加到已构建的子序列中，并将新状态 (i - 1, j - 1) 压入栈中
            stack.append((i - 1, j - 1, current_seq + [X[i - 1]]))
        # 如果回溯信息为 2，说明当前位置是从上方来的，即当前字符不是公共子序列的一部分
        elif table[i][j][1] == 2:
            # 不添加当前字符，直接将新状态 (i - 1, j) 压入栈中
            stack.append((i - 1, j, current_seq))
        # 如果回溯信息为 3，说明当前位置是从左方来的，即当前字符不是公共子序列的一部分
        elif table[i][j][1] == 3:
            # 不添加当前字符，直接将新状态 (i, j - 1) 压入栈中
            stack.append((i, j - 1, current_seq))
        # 如果回溯信息为 4，说明当前位置有两条路径（上方和左方）
        elif table[i][j][1] == 4:
            # 分别将上方和左方的状态压入栈中，继续回溯
            stack.append((i - 1, j, current_seq))
            stack.append((i, j - 1, current_seq))

    # 去重操作
    unique_lcs_sequences = []
    for seq in lcs_sequences:
        if len(seq) == lcs_length and seq not in unique_lcs_sequences:
            unique_lcs_sequences.append(seq)

    return lcs_length, unique_lcs_sequences, table

# 计算并更新界面
def calculate_lcs(main_window):
    """
    从界面获取输入，计算最长公共子序列，并更新界面显示结果
    :param main_window: 主窗口对象
    """
    input1 = find_widget(main_window, QLineEdit, 'input1')
    input2 = find_widget(main_window, QLineEdit, 'input2')
    length_output = find_widget(main_window, QLineEdit, 'length')
    text_output = find_widget(main_window, QTextEdit, 'StringOutput')
    table_output = find_widget(main_window, QTableWidget, 'tableWidget')

    X = parse_input(input1.text())
    Y = parse_input(input2.text())

    lcs_length, lcs_sequences, table = find_lcs(X, Y)
    length_output.setText(str(lcs_length))

    sequence_text = "\n".join([" ".join(seq) for seq in lcs_sequences])
    text_output.setText(sequence_text)

    if table_output:  # 先确保获取到了table_output组件
        m = len(X) + 1
        n = len(Y) + 1
        table_output.setRowCount(m)
        table_output.setColumnCount(n)

        # 设置水平表头
        horizontal_headers = [' '] + Y
        table_output.setHorizontalHeaderLabels(horizontal_headers)
        # 设置垂直表头
        vertical_headers = [' '] + X
        table_output.setVerticalHeaderLabels(vertical_headers)
        for i in range(0, m):
            for j in range(0, n):
                length, backtrack = table[i][j]
                cell_text = f"{length},{backtrack}"
                item = QTableWidgetItem(cell_text)
                table_output.setItem(i, j, item)
        set_square_cells(table_output, size=35)


# 初始化绑定
def init_longest_common_subsequence(main_window):
    """
    初始化按钮点击事件的绑定，使得点击按钮时调用 calculate_lcs 函数
    :param main_window: 主窗口对象
    """
    calculate_btn = find_widget(main_window, QPushButton, 'Start')
    if calculate_btn:
        calculate_btn.clicked.connect(lambda: calculate_lcs(main_window))
        '''calculate_lcs 函数需要一个参数 main_window，而 clicked 信号在触发时并不会传递任何参数。
        因此，我们不能直接将 calculate_lcs 函数传递给 connect 方法，
        因为它需要一个参数。使用 lambda 表达式可以捕获 main_window 变量，
        并在按钮点击时调用 calculate_lcs 函数。'''