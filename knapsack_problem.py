from PySide6.QtWidgets import QMessageBox, QLineEdit, QPushButton, QTextEdit, QTableWidget, QTableWidgetItem
from main import find_widget, set_square_cells
import re


def calculate_knapsack_problem(main_window):
    # 获取界面控件
    item_num_input = find_widget(main_window, QLineEdit, 'item_num')
    capacity_input = find_widget(main_window, QLineEdit, 'package_max')
    item_table = find_widget(main_window, QTableWidget, 'items_table')
    plan_output = find_widget(main_window, QTextEdit, 'plan_output')
    calculate_table = find_widget(main_window, QTableWidget, 'calculating_table')
    max_value_edit = find_widget(main_window, QLineEdit, 'max_value')

    try:
        # 将用户输入的物品数量转换为整数
        item_num = int(item_num_input.text())
        # 将用户输入的背包容量转换为整数
        capacity = int(capacity_input.text())
        # 用于存储每个物品的重量
        weights = []
        # 用于存储每个物品的价值
        values = []

        # 遍历物品表格获取用户输入的重量和价值
        for i in range(item_num):
            # 获取当前行的重量输入项
            weight_item = item_table.item(i, 0)
            # 获取当前行的价值输入项
            value_item = item_table.item(i, 1)
            if weight_item and value_item:
                try:
                    # 将重量输入转换为整数
                    weight = int(weight_item.text())
                    # 将价值输入转换为浮点数
                    value = float(value_item.text())
                    # 将重量添加到重量列表中
                    weights.append(weight)
                    # 将价值添加到价值列表中
                    values.append(value)
                except ValueError:
                    # 若输入格式错误，弹出警告框提示用户
                    QMessageBox.warning(main_window, "错误",
                                        f"第 {i + 1} 行物品信息输入格式错误，请确保重量为整数，价值为数字")
                    return
            else:
                # 若物品信息输入不完整，弹出警告框提示用户
                QMessageBox.warning(main_window, "错误", "物品信息输入不完整")
                return

        # 动态规划表初始化，dp[i][w] 表示考虑前 i 个物品，背包容量为 w 时的最大价值
        dp = [[0.0] * (capacity + 1) for _ in range(item_num + 1)]

        # 核心算法，使用动态规划求解背包问题
        for i in range(1, item_num + 1):
            for w in range(capacity + 1):
                # 如果当前物品的重量小于等于当前背包容量
                if weights[i - 1] <= w:
                    # 选择放入当前物品和不放入当前物品中的最大价值
                    dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
                else:
                    # 当前物品重量大于背包容量，不能放入，最大价值等于不考虑当前物品时的最大价值
                    dp[i][w] = dp[i - 1][w]

        # 填充计算表格，用于展示动态规划过程中的最大价值
        calculate_table.setRowCount(item_num)
        calculate_table.setColumnCount(capacity + 1)
        calculate_table.setHorizontalHeaderLabels([
            f"{w}" for w in range(capacity + 1)
        ])
        calculate_table.setVerticalHeaderLabels([f"物品{i}" for i in range(1, item_num + 1)])
        for i in range(item_num):
            for w in range(capacity + 1):
                # 创建表格项，显示动态规划表中的最大价值，保留两位小数
                item = QTableWidgetItem(f"{dp[i + 1][w]:.2f}")
                calculate_table.setItem(i, w, item)

        # 寻找最佳组合
        # 从动态规划表中获取考虑所有物品且背包容量为 capacity 时的最大价值
        max_value = dp[item_num][capacity]
        # 用于存储所有能达到最大价值的物品组合
        combinations = []
        # 临时存储当前正在回溯的物品组合，初始时所有物品都未被选择（值为 0）
        temp_combination = [0] * item_num

        # 定义回溯函数，用于找出所有能达到最大价值的物品组合
        # row: 当前考虑的物品编号（从 item_num 递减到 0）
        # current_w: 当前背包的剩余容量
        # combination: 当前正在考虑的物品组合
        def backtrack(row, current_w, combination):
            # 当已经考虑完所有物品（row 为 0）时
            if row == 0:
                # 计算当前组合的总价值
                total_value = sum(values[i] * combination[i] for i in range(item_num))
                # 由于浮点数计算存在精度问题，使用 abs(total_value - max_value) < 1e-6 来判断总价值是否等于最大价值
                if abs(total_value - max_value) < 1e-6:
                    # 如果总价值等于最大价值，将当前组合的副本添加到 combinations 列表中
                    # 注意要使用 copy() 方法，避免后续修改影响已添加的组合
                    combinations.append(combination.copy())
                # 回溯结束，返回上一层
                return
            # 当前正在考虑的物品编号（从 0 开始）
            current_item = row - 1
            # 不选当前物品的情况
            # 判断不选择当前物品时的最大价值是否和选择当前物品时的最大价值相同
            # 由于浮点数计算存在精度问题，使用 abs(dp[row][current_w] - dp[row - 1][current_w]) < 1e-6 进行比较
            if abs(dp[row][current_w] - dp[row - 1][current_w]) < 1e-6:
                # 如果相同，说明不选择当前物品也能达到最大价值，继续回溯考虑下一个物品
                backtrack(row - 1, current_w, combination)
            # 选当前物品的情况
            # 首先检查当前背包剩余容量是否足够放下当前物品
            if current_w >= weights[current_item]:
                # 计算选择当前物品后的预期价值
                expected_value = dp[row - 1][current_w - weights[current_item]] + values[current_item]
                # 判断选择当前物品后的预期价值是否和实际最大价值相同
                # 由于浮点数计算存在精度问题，使用 abs(dp[row][current_w] - expected_value) < 1e-6 进行比较
                if abs(dp[row][current_w] - expected_value) < 1e-6:
                    # 如果相同，说明选择当前物品也能达到最大价值
                    # 将当前物品标记为已选择（值为 1）
                    combination[current_item] = 1
                    # 继续回溯考虑下一个物品，同时更新背包剩余容量
                    backtrack(row - 1, current_w - weights[current_item], combination)
                    # 回溯完成后，将当前物品标记为未选择（值为 0），以便尝试其他组合
                    combination[current_item] = 0

        # 从最后一个物品开始回溯，初始时背包剩余容量为 capacity
        backtrack(item_num, capacity, temp_combination)

        # 整理输出
        # 将所有能达到最大价值的物品组合转换为字符串形式，每个组合的元素用空格分隔，组合之间用换行符分隔
        plan_output_text = "\n".join(" ".join(map(str, combo)) for combo in combinations)
        # 将整理好的输出文本设置到界面的文本编辑框中显示
        plan_output.setText(plan_output_text)

        # 显示最大价值
        # 如果界面上存在用于显示最大价值的文本框
        if max_value_edit:
            # 将最大价值以保留两位小数的字符串形式设置到该文本框中显示
            max_value_edit.setText(f"{max_value:.2f}")

    except ValueError as e:
        # 如果在上述过程中出现值错误（例如输入无法转换为整数或浮点数）
        # 弹出警告消息框，提示用户输入错误，并显示具体的错误信息
        QMessageBox.warning(main_window, "错误", f"输入错误: {e}")


def input_items(main_window):
    # 获取物品数量输入框
    item_num_input = find_widget(main_window, QLineEdit, 'item_num')
    # 获取背包容量输入框
    capacity_input = find_widget(main_window, QLineEdit, 'package_max')
    try:
        # 将用户输入的背包容量转换为整数
        capacity = int(capacity_input.text())
        # 将用户输入的物品数量转换为整数
        item_num = int(item_num_input.text())
        if item_num <= 0 or capacity <= 0:
            # 若物品数量或背包容量小于等于 0，弹出警告框提示用户
            QMessageBox.warning(main_window, "错误", "物品数量和背包容量必须大于0")
            return
        # 获取物品表格
        item_table = find_widget(main_window, QTableWidget, 'items_table')
        # 设置物品表格的行数为物品数量
        item_table.setRowCount(item_num)
        # 设置物品表格的列数为 2（重量和价值）
        item_table.setColumnCount(2)
        # 设置物品表格的列标题
        item_table.setHorizontalHeaderLabels(['重量', '价值'])
        # 设置物品表格单元格的大小
        set_square_cells(item_table, size=47)
    except ValueError:
        # 若输入无法转换为整数，弹出警告框提示用户
        QMessageBox.warning(main_window, "错误", "请输入有效的数字")


def init_knapsack_problem(main_window):
    # 获取定义按钮
    push_button = find_widget(main_window, QPushButton, 'define')
    if push_button:
        # 为定义按钮绑定点击事件，点击时调用 input_items 函数
        push_button.clicked.connect(lambda: input_items(main_window))
    # 获取开始按钮
    start_btn = find_widget(main_window, QPushButton, 'Start_2')
    if start_btn:
        # 为开始按钮绑定点击事件，点击时调用 calculate_knapsack_problem 函数
        start_btn.clicked.connect(lambda: calculate_knapsack_problem(main_window))
