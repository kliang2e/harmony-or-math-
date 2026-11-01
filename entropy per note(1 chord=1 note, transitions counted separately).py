import numpy as np
from collections import defaultdict


def read_points_from_file(filename):
    points = []
    dim = None
    with open(filename, 'r') as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            # 自动去除括号、方括号、空格
            cleaned = line.replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace(' ', '')
            try:
                point = tuple(map(int, cleaned.split(',')))
                if dim is None:
                    dim = len(point)
                elif len(point) != dim:
                    print(f"⚠️ 第 {lineno} 行维度不一致，已跳过: {line}")
                    continue
                points.append(point)
            except ValueError:
                print(f"⚠️ 第 {lineno} 行格式错误，已跳过: {line}")
    return points


def lattice_consistency_nd(points):
    if not points:
        return 0

    dim = len(points[0])
    freq = [defaultdict(int) for _ in range(dim)]

    for point in points:
        for i in range(dim):
            freq[i][point[i]] += 1

    total_error = 0
    for d in range(dim):
        d_error = 0
        d_freq = freq[d]
        grouped_points = defaultdict(list)
        for point in points:
            grouped_points[point[d]].append(point)

        for val, group in grouped_points.items():
            c_val = d_freq[val]
            local_errors = []
            for p in group:
                for j in range(dim):
                    if j == d:
                        continue
                    f_other = freq[j][p[j]]
                    local_errors.append(abs(c_val - f_other))
            if local_errors:
                d_error += np.mean(local_errors)
        total_error += d_error / len(grouped_points)

    average_error = total_error / dim
    return average_error


def main():
    print("📌 请输入点集文件路径（如 points.txt）：")
    filename = input("→ ").strip()
    try:
        points = read_points_from_file(filename)
        if not points:
            print("❌ 点集为空或读取失败。请检查格式。")
            return
        print(f"\n✅ 成功读取 {len(points)} 个 {len(points[0])} 维点。")
        error = lattice_consistency_nd(points)
        print(f"\n📊 维度结构一致性误差: {error:.4f}（越小越一致）")
    except FileNotFoundError:
        print("❌ 找不到指定文件，请检查路径。")


if __name__ == "__main__":
    main()