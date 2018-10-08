def count_sort_dict(array):
    count = dict()
    for index in range(len(array)):
        if array[index] not in count:
            count[array[index]] = 0
        count[array[index]] += 1
    total = 0
    index = 0
    for key in count:
        oldCount = count[key]
        count[key] = total
        total += oldCount
    output = ["" for _ in range(len(array))]
    for index in range(len(array)):
        output[count[array[index]]] = array[index]
        count[array[index]] += 1
    return output

def count_sort(array):
    count = [0 for _ in range(len(array))]
    for index in range(len(array)):
        count[int(array[index])] += 1

    total = 0
    for index in range(len(count)):
        oldCount = count[index]
        count[index] = total
        total += oldCount

    output = [0 for _ in range(len(array))]
    for index in range(len(array)):
        output[count[int(array[index])]] = array[index]
        count[int(array[index])] += 1
    return output

items2 = [0, 3, 1 ,5, 1,5 , 6, 4, 6,4, 6,4]
items1 = ["a", "b", "c", "a", "d", "g", "q", "a", "e"]
print(count_sort(items2))
