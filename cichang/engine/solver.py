from concurrent.futures import ThreadPoolExecutor
import numpy as np
from model.physics import compute_magnetic_field

class MagneticFieldSolver:
    def __init__(self, coils: list, grid_range: dict, grid_resolution: int = 20):
        self.coils = coils
        self.grid_range = grid_range
        self.grid_resolution = grid_resolution
        self._init_grid()
        
    def _init_grid(self):
        # 根据 grid_range 设置各轴采样点
        xr = np.linspace(*self.grid_range['x'], self.grid_resolution)
        yr = np.linspace(*self.grid_range['y'], self.grid_resolution)
        zr = np.linspace(*self.grid_range['z'], self.grid_resolution)
        self.grid_x, self.grid_y, self.grid_z = np.meshgrid(xr, yr, zr, indexing='ij')
        # 初始化磁场分量为零
        self.Bx = np.zeros_like(self.grid_x)
        self.By = np.zeros_like(self.grid_y)
        self.Bz = np.zeros_like(self.grid_z)
    
    def solve(self):
        # 使用多线程同时计算各线圈的磁场贡献
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(compute_magnetic_field, coil, self.grid_x, self.grid_y, self.grid_z)
                       for coil in self.coils]
            for future in futures:
                dBx, dBy, dBz = future.result()
                self.Bx += dBx
                self.By += dBy
                self.Bz += dBz
        return self.grid_x, self.grid_y, self.grid_z, self.Bx, self.By, self.Bz
