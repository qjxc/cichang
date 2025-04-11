import numpy as np

MU0 = 4 * np.pi * 1e-7

def compute_magnetic_field(coil, grid_x, grid_y, grid_z):
    """
    根据 Biot-Savart 定律计算指定 coil 在网格上产生的磁场（分量计算均为批量向量化运算）
    """
    Bx = np.zeros_like(grid_x)
    By = np.zeros_like(grid_y)
    Bz = np.zeros_like(grid_z)
    
    for i in range(len(coil.ds)):
        segment = coil.ds[i]
        point = coil.points[i]
        # 利用广播计算每个网格点与当前线段起点的差向量
        rx = grid_x - point[0]
        ry = grid_y - point[1]
        rz = grid_z - point[2]
        r_squared = rx**2 + ry**2 + rz**2 + 1e-12  # 防止除零
        
        # 计算 ds × r（交叉乘积）
        dBx = (segment[1] * rz - segment[2] * ry) / (r_squared ** (3/2))
        dBy = (segment[2] * rx - segment[0] * rz) / (r_squared ** (3/2))
        dBz = (segment[0] * ry - segment[1] * rx) / (r_squared ** (3/2))
        
        Bx += MU0 * coil.current * dBx
        By += MU0 * coil.current * dBy
        Bz += MU0 * coil.current * dBz
        
    return Bx, By, Bz
