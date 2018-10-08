import unittest
import timeit
import random
from copy import deepcopy

list_length = 25000
list_range = 1000000

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

def shell_sort(lst):
    gaps = []
    x = 1 
    gaps.append(x)
    while x < (len(lst)):
        x = x * 2 
        gaps.insert(0, (x*3) + 1)
    for gap in gaps:
        for index in range(gap, len(lst)):
            temp = lst[index]
            index2 = int(index)
            while (index2 >= gap) and (lst[index2-gap] > temp):
                lst[index2] = lst[index2-gap]
                index2 -= gap 
            lst[index2] = temp
    return lst 

    pass

def shell_sort_book(lst):
    gaps = []
    x = 1
    gaps.append(x)
    while x < (len(lst)):
        x = (x*3) + 1
        gaps.insert(0, (x*3) + 1)
    for gap in gaps:
        for index in range(gap, len(lst)):
            temp = lst[index]
            index2 = int(index)
            while (index2 >= gap) and (lst[index2-gap] > temp):
                lst[index2] = lst[index2-gap]
                index2 -= gap
            lst[index2] = temp
    return lst

def insertion_sort(lst):
    for i in range(1, len(lst)):
        j = i - 1 
        while(j >= 0) and (lst[j] > lst[j+1]):
            temp = lst[j+1]
            lst[j+1] = lst[j]
            lst[j] = temp
            j = j-1 
    return lst

def quick_sort(lst):
    quick_sort_run(lst, 0, len(lst)-1)

def quick_sort_run(lst, start, end):
    if start < end:
        split = partition(lst, start, end)
        quick_sort_run(lst, start, split-1)
        quick_sort_run(lst, split+1, end)

def partition(lst, start, end):
    pivot = lst[start]
    left = start + 1
    right = end

    done = False
    while(not done):
        while (left <= right) and (lst[left] <= pivot):
            left = left + 1
        while (lst[right] >= pivot) and (right >= left):
            right = right - 1
        if right < left:
            done = True
        else:
            temp = lst[left]
            lst[left] = lst[right]
            lst[right] = temp
    temp = lst[start]
    lst[start] = lst[right]
    lst[right] = temp
    return right

def merge_sort(lst):
    if len(lst) <= 1:
        return lst

    middle = len(lst) // 2
    left = lst[:middle]
    right = lst[:middle]
    left = merge_sort(left)
    right = merge_sort(right)
    return list(merge_back(left, right))

def merge_back(left, right):
    result = []
    l_index = 0
    r_index = 0
    while (l_index < len(left)) and (r_index < len(right)):
        if left[l_index] <= right[r_index]:
            result.append(left[l_index])
            l_index += 1
        else:
            result.append(right[r_index])
            r_index += 1
    if left:
        result.extend(left[l_index:])
    if right:
        result.extend(right[r_index:])
    return result

def bubble_sort(lst):
    for index in range(len(lst)-1, 0, -1):
        for index2 in range(index):
            if lst[index2] > lst[index]:
                lst[index2], lst[index] = lst[index], lst[index2]
    return lst

def tim_sort(lst):
    return lst.sort()

def is_sorted(lst):
    if (len(lst)==1) or (len(lst)==0):
        return True
    if len(lst)==2:
        if lst[0] > lst[1]:
            return False
        return True
    return is_sorted(lst[:2]) and is_sorted(lst[1:len(lst)])


########################################
############# UNIT TESTS ###############
########################################


class BasicTests(unittest.TestCase):
    def test_is_sorted_unsorted(self):
        test = []
        for i in range(10, 1, -1):
            test.append(i)
        self.assertFalse(is_sorted(test))

    def test_is_sorted_sorted(self):
        test = []
        for i in range(1, 10):
            test.append(i)
        self.assertTrue(is_sorted(test))

    def test_is_sorted_edge_unsorted(self):
        test = []
        for i in range(1, 10):
            test.append(i)
        test.append(-1)
        self.assertFalse(is_sorted(test))

    def test_shell_sort(self):
        test = []
        for i in range(10, 1, -1):
            test.append(i)
        self.assertFalse(is_sorted(test))
        test = shell_sort(test)
        self.assertTrue(is_sorted(test))

    def test_shell_sort_large(self):
        test = []
        for i in range(800, 1, -1):
            test.append(i)
        self.assertFalse(is_sorted(test))
        test = shell_sort(test)
        self.assertTrue(is_sorted(test))
      
    def test_shell_sort_book(self):
        test = []
        for i in range(10, 1, -1):
            test.append(i)
        self.assertFalse(is_sorted(test))
        test = shell_sort(test)
        self.assertTrue(is_sorted(test))

    def test_shell_sort_book_large(self):
        test = []
        for i in range(800, 1, -1):
            test.append(i)
        self.assertFalse(is_sorted(test))
        test = shell_sort_book(test)
        self.assertTrue(is_sorted(test))

    def test_quick_sort(self):
        test = []
        for i in range(10, 1, -1):
            test.append(i)
        self.assertFalse(is_sorted(test))
        quick_sort(test)
        self.assertTrue(is_sorted(test))

    def test_quick_sort_large(self):
        test = []
        for i in range(800, 1, -1):
            test.append(i)
        self.assertFalse(is_sorted(test))
        quick_sort(test)
        self.assertTrue(is_sorted(test))

    def test_merge_sort(self):
        test = []
        for i in range(10, 1, -1):
            test.append(i)
        self.assertFalse(is_sorted(test))
        test = merge_sort(test)
        self.assertTrue(is_sorted(test))

    def test_merge_sort_large(self):
        test = []
        for i in range(800, 1, -1):
            test.append(i)
        self.assertFalse(is_sorted(test))
        test = merge_sort(test)
        self.assertTrue(is_sorted(test))

    def test_bubble_sort(self):
        test = []
        for i in range(10, 1, -1):
            test.append(i)
        self.assertFalse(is_sorted(test))
        test = bubble_sort(test)
        self.assertTrue(is_sorted(test))

    def test_bubble_sort_large(self):
        test = []
        for i in range(800, 1, -1):
            test.append(i)
        self.assertFalse(is_sorted(test))
        test = bubble_sort(test)
        self.assertTrue(is_sorted(test))


if __name__ == "__main__":
    random_list = random.sample(range(list_range), list_length)
    random_list1 = deepcopy(random_list)
    random_list2 = deepcopy(random_list)
    random_list3 = deepcopy(random_list)
    random_list4 = deepcopy(random_list)
    random_list5 = deepcopy(random_list)
    sort_dict = {}
    sort_dict["Shell Sort (halved)"] = timeit.timeit(wrapper(shell_sort, deepcopy(random_list)), number=10)
    sort_dict["Shell Sort (3-based-gap)"] = timeit.timeit(wrapper(shell_sort_book, deepcopy(random_list)), number=10)
    sort_dict["Insertion Sort"] = timeit.timeit(wrapper(insertion_sort, deepcopy(random_list)), number=10)
    sort_dict["Merge Sort"] = timeit.timeit(wrapper(merge_sort, deepcopy(random_list)), number=10)
    sort_dict["Tim Sort"] = timeit.timeit(wrapper(tim_sort, deepcopy(random_list)), number=10)
    sort_dict["Tim Sort"] = timeit.timeit(wrapper(bubble_sort, deepcopy(random_list)), number=10)
    sorted_keys = sorted(sort_dict, key=sort_dict.__getitem__)

    with open("output.txt", "w+") as output:
        string = "Fastest to Slowest Sorts with Randomized List of 25000 elements:\n" \
                 "-----------------------------------------------\n"
        for key in sorted_keys:
            string += str(key) + " : " + str(sort_dict[key]) + " seconds\n" \
                      "------------------------\n"
        print(string)
        output.write(string)
