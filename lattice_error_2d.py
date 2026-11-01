
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
                    if len(point) == 2:
                        points.append(point)
                except:
                    pass
    return points

def load_solutions_from_file(filename):
    solutions = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip().replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace(' ', '')
            if line:
                try:
                    triplet = tuple(map(int, line.split(',')))
                    if len(triplet) == 3:
                        solutions.append(triplet)
                except:
                    pass
    return solutions

def count_occurrences(points):
    return Counter(points)

def prepare_lookup_tables(points):
    count_by_x = defaultdict(int)
    count_by_y = defaultdict(int)
    for x, y in points:
        count_by_x[x] += 1
        count_by_y[y] += 1
    return count_by_x, count_by_y

def find_closest_solution(triplet, solution_set):
    min_dist = float('inf')
    for sol in solution_set:
        dist = sum(abs(a - b) for a, b in zip(triplet, sol))
        if dist < min_dist:
            min_dist = dist
    return min_dist

def total_error_against_solution(points, solution_set):
    count_by_point = count_occurrences(points)
    count_by_x, count_by_y = prepare_lookup_tables(points)

    total_error = 0
    for (x, y), freq in count_by_point.items():
        xval = count_by_x[x]
        yval = count_by_y[y]
        n = math.ceil(freq / 2)
        query_triplet = (xval, yval, n)
        err = find_closest_solution(query_triplet, solution_set)
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

    total_err = total_error_against_solution(points, solutions)
    print(f"✅ 点集大小: {len(points)}")
    print(f"📊 总误差: {total_err}")

if __name__ == "__main__":
    main()
