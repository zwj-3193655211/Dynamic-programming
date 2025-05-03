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
    start = 0
    current_max = 0
    max_sum = 0
    max_start = 0
    max_end = 0
    table.setRowCount(n)
    table.setColumnCount(3)  # 设置列数为3
    table.setHorizontalHeaderLabels(["尾数值", "最大值", "起点"])  # 调整表头标签
    history = []

    for i in range(n):
        if arr[i] > current_max + arr[i]:
            current_max = arr[i]
            start = i
        else:
            current_max += arr[i]
        if current_max > max_sum:
            max_sum = current_max
            max_start = start
            max_end = i
        history.append((current_max, start))  # 记录每一步的最大值和起始位置

    max_sum_output.setText(str(max_sum))
    putout_str.setText(str(arr[max_start:max_end + 1]))

    for i in range(n):
        table.setItem(i, 0, QTableWidgetItem(str(arr[i])))
        table.setItem(i, 1, QTableWidgetItem(str(history[i][0])))  # 填充每一步的最大值
        table.setItem(i, 2, QTableWidgetItem(str(history[i][1])))  # 填充每一步的起始位置
    set_square_cells(table, size=80)


def init_max_subarray_sum(main_window):
    # 这里可以添加初始化最大子段和问题功能的代码
    push_button = find_widget(main_window, QPushButton, "Start_3")
    if push_button:
        push_button.clicked.connect(lambda: calculate_max_subarray_sum(main_window))