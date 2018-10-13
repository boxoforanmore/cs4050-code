import random


def quick_sort_no_recur(lst):
    pass


def quick_sort(lst):
    partition(lst, 0, len(lst)-1)

def partition(lst, start, end):
    if (end - start + 1) <= 15:
        insertion_sort(lst, start, end)
        return
    else:
        mid = (start+end)//2
        if lst[end] < lst[start]:
            lst[end], lst[start] = lst[start], lst[end]
        if lst[end] < lst[mid]:
            lst[mid], lst[end] = lst[end], lst[mid]
        if lst[start] < lst[mid]:
            lst[start], lst[mid] = lst[mid], lst[start]

        pivot = lst[start]

        i = start
        j = end - 1

        while (i <= j):
            while (lst[i] < pivot):
                i += 1
            while (lst[j] > pivot):
                j -= 1
            if (i <= j):
                lst[i], lst[j] = lst[j], lst[i]
                i += 1
                j -= 1
        if start < j:
            partition(lst, start, mid)
        if i < end:
            partition(lst, mid, end)

def insertion_sort(lst, low, high):
    print("hi, it's me")
    for i in range(low, high):
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
    while index1 < len(random_list):
        if lst[index1] > lst[index1 + 1]:
            return index1
        index1 += 1
    return None

random_list = random.sample(range(10000), 500)
print(random_list)
quick_sort(random_list)
print(random_list)
print(is_sorted(random_list))
if not is_sorted(random_list):
    print(random_list[0:not_sorted_index(random_list)+1])
