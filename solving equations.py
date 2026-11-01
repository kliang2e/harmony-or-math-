import math
import os


def find_zero_solutions(range_n, range_xy, epsilon=1e-6):
    solutions = []

    for n in range_n:
        if n <= 0:
            continue
        a = math.log(n)
        for x in range_xy:
            for y in range_xy:
                if x <= 0 or y <= 0:
                    continue

                term1 = a * (1 / y - 1 / x)
                term2 = (1 / x * math.log(1 / x) - 1 / y * math.log(1 / y))
                b = term1 + term2

                if abs(b) < epsilon:
                    solutions.append((x, y, n))  # (x, y, n) format for compatibility

    return solutions


# Define the ranges
range_n = range(1, 51)  # Increase range to find more precise matches
range_xy = range(1, 101)  # Try x, y = 1 to 100

solutions = find_zero_solutions(range_n, range_xy)

# Write output to a file in a format compatible with your program
filename = "solutions.txt"
filepath = os.path.abspath(filename)
print(f"Saving results to: {filepath}")

with open(filename, "w", encoding="gb18030") as f:
    if solutions:
        for x, y, n in solutions:
            f.write(f"({x},{y},{n})\n")
    else:
        f.write("No solutions found.\n")

print("✅ Done! Solutions where b ≈ 0 have been saved.")