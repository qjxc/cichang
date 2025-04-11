import os
import numpy as np
from PyQt5 import QtWidgets, QtCore
from model.coil import Coil, generate_helix_coil
from engine.solver import MagneticFieldSolver
from data_io.data_handler import save_frame, get_frame_files, load_frame
from visualization.plotter import plot_3d_field, plot_2d_heatmap
from ui.dialogs import AddCoilDialog
import matplotlib.pyplot as plt

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("磁场仿真与可视化")
        self.coils = []  # 存储 Coil 对象
        self.init_ui()

    def init_ui(self):
        self.tab_widget = QtWidgets.QTabWidget(self)
        self.setCentralWidget(self.tab_widget)
        
        # 仿真配置标签页
        self.simulation_tab = QtWidgets.QWidget()
        self._init_simulation_tab()
        self.tab_widget.addTab(self.simulation_tab, "仿真配置")
        
        # 播放标签页
        self.playback_tab = QtWidgets.QWidget()
        self._init_playback_tab()
        self.tab_widget.addTab(self.playback_tab, "NPZ 播放")
    
    # ------------------ 仿真配置标签页 --------------------
    def _init_simulation_tab(self):
        layout = QtWidgets.QHBoxLayout(self.simulation_tab)
        
        # 左侧参数配置区域
        config_widget = QtWidgets.QWidget()
        config_layout = QtWidgets.QVBoxLayout(config_widget)
        
        # 添加线圈按钮
        self.add_coil_btn = QtWidgets.QPushButton("添加线圈")
        self.add_coil_btn.clicked.connect(self.add_coil)
        config_layout.addWidget(self.add_coil_btn)
        
        # 线圈列表显示
        self.coil_list = QtWidgets.QListWidget()
        config_layout.addWidget(self.coil_list)
        
        # 网格参数设定
        self.grid_res_edit = QtWidgets.QLineEdit("20")
        config_layout.addWidget(QtWidgets.QLabel("网格分辨率:"))
        config_layout.addWidget(self.grid_res_edit)
        
        # 轴范围设置
        self.x_range_edit = QtWidgets.QLineEdit("-10, 10")
        self.y_range_edit = QtWidgets.QLineEdit("-10, 10")
        self.z_range_edit = QtWidgets.QLineEdit("-10, 10")
        config_layout.addWidget(QtWidgets.QLabel("X 轴范围 (min, max):"))
        config_layout.addWidget(self.x_range_edit)
        config_layout.addWidget(QtWidgets.QLabel("Y 轴范围 (min, max):"))
        config_layout.addWidget(self.y_range_edit)
        config_layout.addWidget(QtWidgets.QLabel("Z 轴范围 (min, max):"))
        config_layout.addWidget(self.z_range_edit)
        
        # 生成单帧按钮（预览）和离线导出按钮
        self.preview_btn = QtWidgets.QPushButton("生成单帧预览")
        self.preview_btn.clicked.connect(self.generate_preview)
        self.export_btn = QtWidgets.QPushButton("离线导出数据")
        self.export_btn.clicked.connect(self.export_simulation)
        config_layout.addWidget(self.preview_btn)
        config_layout.addWidget(self.export_btn)
        
        layout.addWidget(config_widget, 1)
    
    def add_coil(self):
        dialog = AddCoilDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            values = dialog.get_values()
            if values:
                radius, turns, height, current = values
                points = generate_helix_coil(radius, height, turns, 100)
                coil = Coil(points, current)
                self.coils.append(coil)
                self.coil_list.addItem(f"半径: {radius}, 高度: {height}, 圈数: {turns}, 电流: {current}")
    
    def parse_range(self, text):
        try:
            parts = [float(x.strip()) for x in text.split(",")]
            if len(parts) == 2:
                return parts[0], parts[1]
        except Exception as e:
            print("解析范围错误：", e)
        return -10, 10
    
    def generate_preview(self):
        # 获取网格参数
        grid_res = int(self.grid_res_edit.text())
        grid_range = {
            'x': self.parse_range(self.x_range_edit.text()),
            'y': self.parse_range(self.y_range_edit.text()),
            'z': self.parse_range(self.z_range_edit.text())
        }
        if not self.coils:
            QtWidgets.QMessageBox.warning(self, "警告", "请先添加至少一个线圈！")
            return
        
        # 利用计算引擎计算磁场分布
        solver = MagneticFieldSolver(self.coils, grid_range, grid_res)
        grid_x, grid_y, grid_z, Bx, By, Bz = solver.solve()
        # 计算磁场幅值
        B_magnitude = (Bx**2 + By**2 + Bz**2)**0.5
        
        # 调用可视化工具进行 3D 与 2D 可视化
        plot_3d_field(self.coils, grid_x, grid_y, grid_z, Bx, By, Bz, scale=0.5)
        plot_2d_heatmap((grid_x, grid_y, grid_z), B_magnitude, axis='z')
    
    def export_simulation(self):
        # 离线导出数据（此示例中只导出单帧，可扩展为多帧动画）
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "选择导出文件夹")
        if not folder:
            return
        
        grid_res = int(self.grid_res_edit.text())
        grid_range = {
            'x': self.parse_range(self.x_range_edit.text()),
            'y': self.parse_range(self.y_range_edit.text()),
            'z': self.parse_range(self.z_range_edit.text())
        }
        solver = MagneticFieldSolver(self.coils, grid_range, grid_res)
        grid_x, grid_y, grid_z, Bx, By, Bz = solver.solve()
        filename = f"{folder}/frame_0000.npz"
        save_frame(filename, grid_x, grid_y, grid_z, Bx, By, Bz)
        QtWidgets.QMessageBox.information(self, "提示", f"数据已保存至 {filename}")
    
    # ------------------ 播放标签页 --------------------
    def _init_playback_tab(self):
        layout = QtWidgets.QVBoxLayout(self.playback_tab)
        
        # 选择数据文件夹
        folder_layout = QtWidgets.QHBoxLayout()
        self.folder_edit = QtWidgets.QLineEdit()
        folder_btn = QtWidgets.QPushButton("选择文件夹")
        folder_btn.clicked.connect(self.select_folder)
        folder_layout.addWidget(self.folder_edit)
        folder_layout.addWidget(folder_btn)
        layout.addLayout(folder_layout)
        
        # 滑块用来选择播放的帧
        self.frame_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.frame_slider.valueChanged.connect(self.show_frame)
        layout.addWidget(self.frame_slider)
        
        # 播放、暂停按钮（简单示例，仅手动控制帧）
        self.play_btn = QtWidgets.QPushButton("播放")
        self.play_btn.setCheckable(True)
        self.play_btn.clicked.connect(self.toggle_play)
        layout.addWidget(self.play_btn)
        
        # 定时器用于自动播放
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.advance_frame)
        self.current_frame_index = 0
        self.frame_files = []
    
    def select_folder(self):
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "选择数据文件夹")
        if folder:
            self.folder_edit.setText(folder)
            self.frame_files = get_frame_files(folder)
            if self.frame_files:
                self.frame_slider.setMaximum(len(self.frame_files) - 1)
                self.current_frame_index = 0
                self.show_frame(0)
    
    def show_frame(self, index):
        if not self.frame_files:
            return
        filename = self.frame_files[index]
        grid_x, grid_y, grid_z, Bx, By, Bz = load_frame(filename)
        # 使用 3D 可视化显示当前帧数据
        # 为了提高效率，这里简单调用绘图函数，实际可结合嵌入 Matplotlib 画布更新
        plot_3d_field(self.coils, grid_x, grid_y, grid_z, Bx, By, Bz, scale=0.5)
    
    def toggle_play(self):
        if self.play_btn.isChecked():
            self.timer.start(1000)  # 每秒播放一帧
        else:
            self.timer.stop()
    
    def advance_frame(self):
        if not self.frame_files:
            return
        self.current_frame_index = (self.current_frame_index + 1) % len(self.frame_files)
        self.frame_slider.setValue(self.current_frame_index)
