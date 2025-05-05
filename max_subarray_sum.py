from PySide6.QtWidgets import QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QTextEdit
from main import find_widget, set_square_cells
import re


def calculate_max_subarray_sum(main_window):
    """
    计算最大子段和问题的结果并更新界面显示
    :param main_window: 主窗口对象
    """
    input_arr = find_widget(main_window, QLineEdit, "input_arr")
    max_sum_output = find_widget(main_window, QLineEdit, "max_sum")
    putout_str = find_widget(main_window, QTextEdit, "putout_str")
    table = find_widget(main_window, QTableWidget, "table_max")
    str_arr = input_arr.text()
    try:
        arr = [float(x) for x in re.split(r'[ ,，]+', str_arr.strip()) if x]
    except ValueError:
        QMessageBox.warning(main_window, "输入错误", "请输入有效的数字序列！")
        return
    n = len(arr)
    current_max = 0
    max_sum = -float('inf')
    max_starts = []  # 存储所有可能的起始位置
    max_ends = []  # 存储所有可能的结束位置
    current_start = 0  # 当前子数组的起始位置
    table.setRowCount(n)
    table.setColumnCount(3)  # 设置列数为3
    table.setHorizontalHeaderLabels(["尾数值", "最大值", "起点"])  # 调整表头标签
    history = []

    for i in range(n):
        # 如果当前元素大于当前最大值加上当前元素，则重新开始新的子数组
        if arr[i] >= current_max + arr[i]:
            current_max = arr[i]
            current_start = i
        else:
            current_max += arr[i]

        # 如果当前最大值大于全局最大值，更新全局最大值和相关位置
        if current_max > max_sum:
            max_sum = current_max
            max_starts = [current_start]
            max_ends = [i]
        # 对于有相同部分的字段，保留最短的那个
        elif current_max == max_sum and current_start not in max_starts:
            max_starts.append(current_start)
            max_ends.append(i)

        history.append((current_max, current_start))  # 记录每一步的最大值和起始位置

    max_sum_output.setText(str(max_sum))
    # 收集所有可能的子数组
    sub_arrays = []
    for start, end in zip(max_starts, max_ends):
        sub_arrays.append(arr[start:end + 1])

    # 去除重复的子数组
    unique_sub_arrays = []
    for sub_arr in sub_arrays:
        if sub_arr not in unique_sub_arrays:
            unique_sub_arrays.append(sub_arr)

    # 将所有子数组转换为字符串并格式化输出
    output_text = "\n".join([str(sub_arr) for sub_arr in unique_sub_arrays])
    putout_str.setText(output_text)

    for i in range(n):
        table.setItem(i, 0, QTableWidgetItem(str(arr[i])))
        table.setItem(i, 1, QTableWidgetItem(str(history[i][0])))
        table.setItem(i, 2, QTableWidgetItem(str(history[i][1]+1)))
    set_square_cells(table, size=80)


def init_max_subarray_sum(main_window):
    push_button = find_widget(main_window, QPushButton, "Start_3")
    if push_button:
        push_button.clicked.connect(lambda: calculate_max_subarray_sum(main_window))
