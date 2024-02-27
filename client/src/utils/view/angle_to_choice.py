import math

# 定义弧度范围
RAD_45 = math.pi / 4
RAD_135 = 3 * math.pi / 4
RAD_225 = 5 * math.pi / 4
RAD_315 = 7 * math.pi / 4


def classify_angle_with_radians(a, b):
    """根据AB线与X轴的角度（以弧度为单位）返回相应的值。"""
    # 计算向量AB的坐标差
    dx = b[0] - a[0]
    dy = b[1] - a[1]

    # 计算角度，使用atan2可以处理dx为0的情况，并且得到的是[-π, π]范围内的角度
    angle_rad = math.atan2(dy, dx)

    # 将角度调整到[0, 2π)范围内
    if angle_rad < 0:
        angle_rad += 2 * math.pi

    # 根据角度范围返回对应的值
    if RAD_135 <= angle_rad < RAD_225:
        return 1
    elif RAD_45 <= angle_rad < RAD_135:
        return 2
    elif RAD_225 <= angle_rad < RAD_315:
        return 3
    else:  # 角度在315度到360度或者0度到45度
        return 4


if __name__ == "__main__":
    # 示例A点和B点的坐标
    a = (0.0, 0.0)  # A点坐标
    b = (-1, 0)  # B点坐标

    # 调用函数并打印结果
    result = classify_angle_with_radians(a, b)
    print(result)
