from collections import defaultdict, Counter
import math

def load_points_from_file(filename):
    points = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip().replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace(' ', '')
            if line:
                try:
                    point = tuple(map(int, line.split(',')))
                    points.append(point)
                except:
                    pass
    return points

def load_solutions_from_file(filename):
    solutions = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip().replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace(' ', '')
            try:
                triplet = tuple(map(int, line.split(',')))
                if len(triplet) == 3:
                    solutions.append(triplet)
            except:
                continue
    return solutions

def get_slices(dim):
    if dim < 3:
        return [[0], [1]]
    else:
        return [list(range(dim - 1)), list(range(1, dim))]

def count_occurrences(points):
    return Counter(points)

def total_error(points, solutions):
    dim = len(points[0])
    point_counter = count_occurrences(points)
    slices = get_slices(dim)

    total_error = 0
    for fixed_dims in slices:
        varying_dims = [i for i in range(dim) if i not in fixed_dims]
        grouped = defaultdict(list)

        for p in points:
            key = tuple(p[i] for i in fixed_dims)
            grouped[key].append(p)

        count_table = defaultdict(int)
        for group in grouped.values():
            for p in group:
                varying = tuple(p[i] for i in varying_dims)
                count_table[varying] += 1

        for pt, freq in point_counter.items():
            key_fixed = tuple(pt[i] for i in fixed_dims)
            key_varying = tuple(pt[i] for i in varying_dims)
            xval = len(grouped.get(key_fixed, []))
            yval = count_table.get(key_varying, 0)
            n = math.ceil(freq / 2)
            query = (xval, yval, n)
            err = min(sum(abs(a - b) for a, b in zip(query, sol)) for sol in solutions)
            total_error += err

    return total_error

def main():
    pts_file = input("📁 请输入点集文件路径：").strip()
    sol_file = input("📁 请输入解集文件路径：").strip()

    points = load_points_from_file(pts_file)
    solutions = load_solutions_from_file(sol_file)

    if not points or not solutions:
        print("❌ 输入文件格式错误或内容为空。")
        return

    total_err = total_error(points, solutions)
    print(f"✅ 点集大小: {len(points)}")
    print(f"📊 总误差: {total_err}")

if __name__ == "__main__":
    main()