import numpy as np

#### Brute Force ####
def closest_pair(points):
    shortest = (euclidean(points[0], points[1]), points[0], points[1])

    for i in points:
        for j in range(1, len(points)):
            if (i != points[j]) and (euclidean(i, points[j]) < shortest[0]):
                shortest = (euclidean(i, points[j]), i, points[j])
    return shortest

def euclidean(c1, c2):
    return (((c1[0]-c2[0])**2)+((c1[1]-c2[1])**2)**.5)



# Divide and Conquer #
def closest_pair_dc(points):
    sorted(points)
    shortest = short_pair(points)
    return shortest    

def short_pair(points):
    if len(points) == 2:
        dist = (euclidean(points[0], points[1]))
    elif len(points) < 2:
        dist = float("inf")
        return (dist, points[0], points[0])
    else:
        mid = len(points) // 2
        left_set = points[:mid]
        right_set = points[mid:]
        min_left = short_pair(left_set)
        min_right = short_pair(right_set)
        p1 = max(left_set)
        p2 = min(right_set)
        dist = min(min_left[0], min_right[0], euclidean(p1, p2))
        if min_left[0] == dist:
            return (dist, min_left[1], min_left[2])
        elif min_right[0] == dist:
            return (dist, min_right[1], min_right[2])
        else:
            return (dist, p1, p2)
    return [dist, points[0], points[1]]

def calc_halves(points, start, end):
    if (end-start) != 2:
        middle_line = points[(points[start] + points[end])//2]
        left = (start, middle_line)
        right = (middle_line, end)
        return min(calc_halves(points, left[0], left[1]), calc_halves(points, right[0], right[1]))
    else:
        return (euclidean(points[start], points[end]), points[start], points[end])

def sort_by_x(points):
    return sorted

pts = []

for i in range(1, 20):
   for j in range(-20, 0):
       if tuple([i, j]) not in pts:
           pts.append(tuple([i, j]))


pts = [list(i) for i in np.random.rand(50,2)]

for i in pts:
    i[0] *= 10
    i[1] *= 10

print(closest_pair(pts))
print(closest_pair_dc(pts))
