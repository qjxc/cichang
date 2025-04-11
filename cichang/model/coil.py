import numpy as np

class Coil:
    def __init__(self, points: np.ndarray, current: float):
        self.points = points
        self.current = current
        # 预计算各离散线段的差分 ds
        self.ds = np.diff(points, axis=0)

def generate_helix_coil(radius: float, height: float, turns: int, points_per_turn: int, center=(0, 0, 0)):
    """
    生成螺旋线圈的离散点
    """
    theta = np.linspace(0, 2 * np.pi * turns, turns * points_per_turn)
    z = np.linspace(0, height, turns * points_per_turn)
    x = radius * np.cos(theta) + center[0]
    y = radius * np.sin(theta) + center[1]
    points = np.stack((x, y, z + center[2]), axis=-1)
    return points
