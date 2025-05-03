import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QStackedWidget, QLineEdit, QTableWidget, \
    QTableWidgetItem, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
from PySide6.QtGui import QIcon
import os

# ==== 全局函数定义 ====
# 用于查找控件的函数

def find_widget(main_window, widget_type, object_name):
    """
    从主窗口中查找指定类型和名称的控件
    :param main_window: 主窗口对象
    :param widget_type: 控件类型
    :param object_name: 控件名称
    :return: 找到的控件对象，如果未找到则返回 None
    """
    return main_window.findChild(widget_type, object_name)

# 定义一个函数，用于将传入的多个表格的单元格设置为正方形
def set_square_cells(*table_widgets, size):
    """
    此函数用于将多个表格的单元格设置为正方形
    :param table_widgets: 要设置的 QTableWidget 对象，可以传入多个
    :param size: 单元格的边长
    """
    for table in table_widgets:
        if isinstance(table, QTableWidget):
            col_count = table.columnCount()
            row_count = table.rowCount()
            if col_count > 0:
                for i in range(row_count):
                    table.setRowHeight(i, size)
                for j in range(col_count):
                    table.setColumnWidth(j, size)

# 添加获取资源路径的函数
def resource_path(relative_path):
    """获取打包后资源的路径"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

if __name__ == "__main__":
    # 创建一个 QApplication 实例，用于管理 GUI 应用程序的资源和事件循环
    app = QApplication(sys.argv)

    # 创建一个 QUiLoader 实例，用于加载 UI 文件
    loader = QUiLoader()
    # 修改加载 UI 文件的路径
    ui_file_path = resource_path("MainMenu.ui")
    ui_file = QFile(ui_file_path)
    if not ui_file.open(QFile.ReadOnly):
        print(f"无法打开 UI 文件: {ui_file_path}")
        sys.exit(1)
    # 加载 UI 文件并创建主窗口对象
    main_window = loader.load(ui_file)
    # 关闭 UI 文件
    ui_file.close()

    if main_window:
        # 更改显示的位置
        main_window.move(300, 0)

        # 设置窗口图标
        icon_path = resource_path("favicon.ico")
        icon = QIcon(icon_path)
        main_window.setWindowIcon(icon)

        # 从主窗口中找到 QStackedWidget 对象，用于管理多个页面的切换
        stacked_widget = find_widget(main_window, QStackedWidget, "pages")

        # 定义一个字典，用于映射按钮名称和对应的页面索引
        button_page_map = {
            "Q1": 0,
            "Q2": 1,
            "Q3": 2,
            "Q4": 3,
            "Q5": 4
        }

        # 遍历按钮页面映射字典
        for button_name, page_idx in button_page_map.items():
            # 从主窗口中找到指定名称的按钮
            button = find_widget(main_window, QPushButton, button_name)
            # 如果按钮存在
            if button:
                # 为按钮的点击事件绑定一个 lambda 函数，用于切换到对应的页面
                button.clicked.connect(lambda _, idx=page_idx: stacked_widget.setCurrentIndex(idx))

        # 初始化各个功能模块

        # 矩阵乘法
        import matrix_multiplication
        matrix_multiplication.init_matrix_multiplication(main_window)

        # 最长公共子序列
        import longest_common_subsequence
        longest_common_subsequence.init_longest_common_subsequence(main_window)

        # 0/1背包问题
        import knapsack_problem
        knapsack_problem.init_knapsack_problem(main_window)

        # 最大字段和问题
        import max_subarray_sum
        max_subarray_sum.init_max_subarray_sum(main_window)

        # 凸多边形最优三角形剖分
        import convex_polygon_triangulation
        convex_polygon_triangulation.init_convex_polygon_triangulation(main_window)

        # 显示主窗口
        main_window.show()
        # 进入应用程序的事件循环，直到窗口关闭
        sys.exit(app.exec())
    else:
        # 如果主窗口加载失败，打印错误信息
        print("加载 UI 文件失败")