import os
import numpy as np

def save_frame(filename, grid_x, grid_y, grid_z, Bx, By, Bz):
    """
    将当前帧数据压缩保存为 NPZ 文件
    """
    np.savez_compressed(filename, grid_x=grid_x, grid_y=grid_y, grid_z=grid_z, Bx=Bx, By=By, Bz=Bz)

def load_frame(filename):
    """
    读取 NPZ 文件中的帧数据
    """
    data = np.load(filename)
    return (data['grid_x'], data['grid_y'], data['grid_z'],
            data['Bx'], data['By'], data['Bz'])

def get_frame_files(folder):
    """
    获取指定文件夹下所有 NPZ 数据文件的排序列表
    """
    files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.npz')]
    return sorted(files)
