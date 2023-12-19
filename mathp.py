import math

def calculate_intersection_area(r, R, d):
    term1 = r ** 2 * math.acos(((d ** 2 + r ** 2 - R ** 2) / (2 * d * r))%1)
    term2 = R ** 2 * math.acos(((d ** 2 + R ** 2 - r ** 2) / (2 * d * R))%1)
    term3 = 0.5 * math.sqrt(abs((-d + r + R) * (d + r - R) * (d - r + R) * (d + r + R)))

    intersection_area = term1 + term2 - term3
    return intersection_area

def circle_area(r):
    return math.pi * r ** 2