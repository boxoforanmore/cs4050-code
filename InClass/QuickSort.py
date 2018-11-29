import random
from copy import deepcopy

def quick_sort_no_recur(lst):
    stack = list()
    start = 0
    end = len(lst) - 1

    stack.append((start, end))

    while(len(stack) != 0):
        top = stack.pop(len(stack)-1)
        if((abs(top[1] - top[0]) + 1) <= 15):
            insertion_sort(lst, top[0], top[1])
            continue
        else:
            end = top[1]
            start = top[0]
            mid = (start+end)//2

            if lst[end] < lst[start]:
                lst[end], lst[start] = lst[start], lst[end]
            if lst[end] < lst[mid]:
                lst[end], lst[mid] = lst[mid], lst[mid]
            if lst[start] < lst[mid]:
                lst[mid], lst[start] = lst[start], lst[mid]
            pivot = lst[start]

            i = start

            for j in range(i+1, end+1):
                if (lst[j] <= pivot):
                    i += 1
                    lst[i], lst[j] = lst[j], lst[i]

            lst[start], lst[i] = lst[i], lst[start]

            stack.append((start, i-1))
            stack.append((i+1, end))


def quick_sort(lst):
    partition(lst, 0, len(lst)-1)

def partition(lst, start, end):
    if (end - start + 1) <= 15:
        insertion_sort(lst, start, end)
        return
    elif start < end:
        mid = (start+end)//2
        if lst[end] < lst[start]:
            lst[end], lst[start] = lst[start], lst[end]
        if lst[end] < lst[mid]:
            lst[mid], lst[end] = lst[end], lst[mid]
        if lst[start] < lst[mid]:
            lst[start], lst[mid] = lst[mid], lst[start]

        pivot = lst[start]

        i = start + 1
        j = end

        while (i <= j):
            while (lst[i] < pivot):
                i += 1
            while (lst[j] > pivot):
                j -= 1
            if (i <= j):
                lst[i], lst[j] = lst[j], lst[i]
                i += 1
                j -= 1
        lst[start], lst[j] = lst[j], lst[start]
        if start < j:
            partition(lst, start, j-1)
        if i < end:
            partition(lst, i, end)

def find_kth(lst, k):
     new_list = deepcopy(lst)
     partition(new_list, 0, len(new_list)-1)
     for pos, item in enumerate(new_list):
         #print(f"{item}, {k}")
         if item == k:
             return pos
     return -1

def quick_sort_three_way(lst):
    partition_three_way(lst, 0, len(lst)-1)
    pass

def partition_three_way(lst, start, end):
    if (end - start + 1) <= 15:
        insertion_sort(lst, start, end)
        return
    elif start < end:
        mid = (start+end)//2
        if lst[end] < lst[start]:
            lst[end], lst[start] = lst[start], lst[end]
        if lst[end] < lst[mid]:
            lst[mid], lst[end] = lst[end], lst[mid]
        if lst[start] < lst[mid]:
            lst[start], lst[mid] = lst[mid], lst[start]
    pivot = lst[start]
    low = int(start)
    hi = int(end)
    i = low + 1
    
    while (i < hi) and (len(lst) not in (i, hi)):
        if (lst[i] < pivot):
            lst[low], lst[i] = lst[i], lst[low]
            low += 1
            i += 1
        elif (lst[i] > pivot):
            lst[hi], lst[i] = lst[i], lst[hi]
            hi += 1
        else:
            i += 1

    #print(lst)

    partition_three_way(lst, 0, low-1)
    partition_three_way(lst, hi+1, end)

def insertion_sort(lst, low, high):
    ##print(f"low: {low}, high:{high}")
    if low == high:
        return
    for i in range(low, high+1):
        j = i - 1 
        while(j >= 0) and (lst[j] > lst[j+1]):
            temp = lst[j+1]
            lst[j+1] = lst[j]
            lst[j] = temp
            j = j-1 
    return lst

def is_sorted(lst):
    if (len(lst)==1) or (len(lst)==0):
        return True
    if len(lst)==2:
        if lst[0] > lst[1]:
            return False
        return True
    return is_sorted(lst[:2]) and is_sorted(lst[1:len(lst)])

def not_sorted_index(lst):
    index1 = 0
    while index1 < len(lst):
        if lst[index1] > lst[index1 + 1]:
            return index1
        index1 += 1
    return None

lst1 = random.sample(range(10000), 500)
lst2 = deepcopy(lst1)

print()
print("Recursive quicksort")
quick_sort(lst1)
print(f"Is Sorted: {is_sorted(lst1)}")
print()
print()
print("Non-recursive quicksort")
quick_sort_no_recur(lst2)
print(f"Is Sorted: {is_sorted(lst2)}")
print()


'''
lst = random.sample(range(10000), 500)
lst2 = deepcopy(lst)
lst3 = random.sample(range(500), 500)
print(lst)
quick_sort(lst)
print(lst)
print(f"lst is sorted: {is_sorted(lst)}")
if not is_sorted(lst):
    print(lst[0:not_sorted_index(lst)+2])
print()
quick_sort_no_recur(lst2)
print(lst2)
print(f"lst2 is sorted: {is_sorted(lst2)}")
if not is_sorted(lst2):
    print(lst2[0:not_sorted_index(lst2)+2])
pos = find_kth(lst3, 30)
print(pos)

lst4 = random.sample(range(10000), 500)
print(lst4)
quick_sort_three_way(lst4)
print(f"lst is sorted: {is_sorted(lst4)}")
if not is_sorted(lst4):
    print(lst4[0:not_sorted_index(lst4)+2])
print(lst4)
'''
