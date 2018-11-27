import random

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

def short_pair2(points):
    if len(points) == 2:
        return (euclidean(points[0], points[1]), points[0], points[1])
    elif len(points) < 2:
        return (float("inf"), (0, 0), (0, 0))
    else:
        mid = len(points) // 2
        left_set = points[:mid]
        right_set = points[mid:]
        min_set = min(short_pair(left_set), short_pair(right_set))
        

def sort_by_ys(points):
    for i in points:
        i[0], i[1] = i[1], i[0]
    points = sorted(points)
    for i in points:
        i[0], i[1] = i[1], i[0]
    return points

def short_pair3(x_points, y_points, low, hi):
    # Limit from checking a point against itself
    if (hi-low) < 2:
        return (float("inf"), (0, 0), (0, 0))

    # Search left and right partitions
    mid = (hi+low) // 2
    left_set = x_points[:mid]
    right_set = x_points[mid:]
    min_set = min(short_pair(left_set), short_pair(right_set))

    # Points sorted by y coordinates
    y_points = sort_by_ys(x_points)    

    # Find middle band (those that are a certain distance (the minimum distance found for either side) away from the middle point
    middle = x_points[mid]
    mid_band = [point for point in y_points[low:hi] if (abs(point[0]-middle[0]) < min_set[0])]

    # Searching the middle area
    for index, p1 in enumerate(mid_band):
        for j in range(index+1, len(mid_band)):
            p2 = mid_band[j]

            # Look for the closest y points given that they are not the same or the same as the mid set
            if (abs(p1[1]-p2[1]) < min_set[0]) and ((min_set[1], min_set[2]) not in (p1, p2)) and (euclidean(p1, p2) != 0):
                min_set = min(min_set, (euclidean(p1, p2), p1, p2))
            else:
                continue
    return min_set

def closest_pair_3(points):
    points = sorted(points)
    return short_pair3(points, points, 0, len(points))

pts = []

'''
for i in range(1, 20):
   for j in range(-20, 0):
       if tuple([i, j]) not in pts:
           pts.append(tuple([i, j]))
'''
tup_lo = -100
tup_hi = 100

pts = [[random.randint(tup_lo, tup_hi), random.randint(tup_lo, tup_hi)] for _ in range(100)]

#pts = [list(i) for i in np.random.rand(50,2)]

'''
for i in pts:
    i[0] *= 10
    i[1] *= 10
'''

print(closest_pair(pts))
print(closest_pair_dc(pts))
print(closest_pair_3(pts))
