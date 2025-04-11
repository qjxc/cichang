import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # 即使不直接调用也必须导入

def plot_3d_field(coils, grid_x, grid_y, grid_z, Bx, By, Bz, scale=1):
    """
    绘制 3D 磁场矢量图并叠加线圈轨迹
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # 为了加快渲染，对网格数据进行稀疏采样
    skip = (slice(None, None, 2), slice(None, None, 2), slice(None, None, 2))
    ax.quiver(grid_x[skip], grid_y[skip], grid_z[skip], 
              Bx[skip], By[skip], Bz[skip], length=scale, color='b')
    
    for coil in coils:
        ax.plot(coil.points[:, 0], coil.points[:, 1], coil.points[:, 2], 'r-', linewidth=2)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title("3D 磁场矢量图")
    plt.show()

def plot_2d_heatmap(grid, B_magnitude, axis='z', slice_idx=None):
    """
    绘制 2D 热图，根据 axis（x, y, z）选择平面切片
    """
    if slice_idx is None:
        slice_idx = B_magnitude.shape[2] // 2  # 默认取 z 轴中间层
        
    plt.figure(figsize=(8, 6))
    if axis == 'z':
        data = B_magnitude[:, :, slice_idx]
        X, Y = grid[0][:, :, slice_idx], grid[1][:, :, slice_idx]
    elif axis == 'y':
        data = B_magnitude[:, slice_idx, :]
        X, Y = grid[0][:, slice_idx, :], grid[2][:, slice_idx, :]
    elif axis == 'x':
        data = B_magnitude[slice_idx, :, :]
        X, Y = grid[1][slice_idx, :, :], grid[2][slice_idx, :, :]
    else:
        raise ValueError("axis 必须为 'x'、'y' 或 'z'")
        
    plt.contourf(X, Y, data, cmap='jet')
    plt.colorbar()
    plt.xlabel(f"{axis.upper()} 轴切片")
    plt.title("2D 热图")
    plt.show()
