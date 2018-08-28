from __future__ import print_function
import unittest

class PriorityQueue(object):
    class Node(object):
        def __init__(self, value, next_node):
            self.value = value
            self.next_node = next_node


    def __init__(self, initial=None):
        self.front = self.back = self.current = None
        self.__length = 0
        if initial != None:
            for element in tuple(initial):
                self.enqueue(element[0], element[1])


    def empty(self):
        return self.front == self.back == None


    def __len__(self):
        return self.__length


    def __iter__(self):
        self.current = self.front
        return self


    def __next__(self):
        if self.current:
            tmp = self.current.value
            self.current = self.current.next_node
            return tmp
        else:
            raise StopIteration()


    def __str__(self):
        if self.empty():
            return str(None)
        if self.front == self.back:
            return str(self.front.value)
        vals = ''
        for item in self:
            if item == self.back.value:
                vals += str(item)
                break
            vals += str(item) + ', '
        return vals


    def __repr__(self):
        return 'PriorityQueue((' + str(self) + '))'


    def __push_front(self, value):
        new = self.Node(value, None)
        if self.empty():
            self.front = self.back = new
            self.__length += 1
        else:
            new.next_node = self.front
            self.front = new
            self.__length += 1


    def __pop_front(self):
        tmp = self.front
        if self.empty():
            raise RuntimeError("PriorityQueue is empty")
        if self.front == self.back:
            value = self.front.value
            self.front = self.back = None
            self.__length -= 1
            return value
        else:
            tmp = self.front.next_node
            value = self.front.value
            self.front.next_node = None
            self.front = tmp
            self.__length -= 1
            return value


    def __push_back(self, value):
        new = self.Node(value, None)
        if self.empty():
            self.front = self.back = new
            self.__length += 1
            return
        self.back.next_node = new
        self.back = new
        self.__length += 1


    def __pop_back(self):
        if self.empty():
            raise RuntimeError("PriorityQueue is empty")
        if self.front is self.back:
            value = self.front.value
            self.front = self.back = None
            self.__length -= 1
            return value
        else:
            current = self.front
            while current.next_node is not self.back:
                current = current.next_node
            value = current.next_node.value
            current.next_node = None
            self.back = current
            self.__length -= 1
            return value

    
    def delete(self, value=None):
        if value == None:
            raise RuntimeError("PriorityQueue's delete method must be called with a value")
        if self.empty():
            raise RuntimeError("PriorityQueue is empty")
        if self.front.value["name"] == value:
            self.__pop_front()
            return
        if self.back.value["name"] == value:
            self.__pop_back()
            return
        else:
            prev = self.front
            current = self.front.next_node
            nxt = self.front.next_node.next_node
            if current.value["name"] == value:
                prev.next_node = nxt 
                current.next_node = None
                current = None
                return
            while current is not self.back:
                if current.value["name"] == value:
                    prev.next_node = nxt
                    current.next_node = None
                    current = None
                    return
                else:
                    prev = current
                    current = nxt
                    nxt = nxt.next_node
            return
        raise RuntimeError("Delete method is not working correctly")



    def middle_from_node(self, start=None):
        if self.empty():
            raise RuntimeError("PriorityQueue is empty")
        if self.front == self.back:
            return start
        if start == None:
            return start
        fast = start.next_node.next_node
        slow = start
        while fast is not None:
            fast = fast.next_node
            if fast is not None:
                fast = fast.next_node
            slow = slow.next_node
        return slow


    def names(self):
        name_list = list()
        for item in self:
            name_list.append(item["name"])
        return name_list


    def enqueue(self, priority, name, time=0):
        if priority > 5:
            priority = 5
        elif priority < 0:
            priority = 0.0
        item = {"priority": priority,
                "name": name,
                "time": time}
        needsSort = False
        if self.empty() or (item["priority"] <= self.back.value["priority"]):
            self.__push_back(item)
        elif self.front.value["priority"] < item["priority"]:
            self.__push_front(item)
            nxt = self.front.next_node
            while nxt != None:
                nxt.value["priority"] = round((nxt.value["priority"] + 0.4), 1)
                if nxt.value["priority"] > 5:
                    nxt.value["priority"] = 5
                nxt = nxt.next_node
            needsSort = True 
        else:
            inserted = False
            nxt = self.front
            while nxt != self.back.next_node:
                if (inserted == False) and (nxt.next_node.value["priority"] < item["priority"]):
                    temp = nxt.next_node
                    nxt.next_node = self.Node(item, temp)
                    inserted = True
                    nxt = nxt.next_node
                    self.__length += 1
                    continue
                if inserted == True and nxt.value != item:
                    nxt.value["priority"] = round((nxt.value["priority"] + 0.4), 1)
                    if nxt.value["priority"] > 5:
                         nxt.value["priority"] = int(5)
                nxt = nxt.next_node
            needsSort = True
        if needsSort == True:
            self.front = self.mergeSort(self.front)


    def mergeSort(self, noderino):
        if (noderino == None) or (noderino.next_node == None):
            return noderino
        mid = self.middle_from_node(noderino)
        mid_next = mid.next_node
        mid.next_node = None

        left_side = self.mergeSort(noderino)
        right_side = self.mergeSort(mid_next)
        return self.mergeBack(left_side, right_side)


    def mergeBack(self, left, right):
        sortedList = None
        if left == None:
            return right
        if right == None:
            return left
        if left.value["priority"] >= right.value["priority"]:
            sortedList = left
            sortedList.next_node = self.mergeBack(left.next_node, right)
        else:
            sortedList = right
            sortedList.next_node = self.mergeBack(left, right.next_node)
        return sortedList


    def dequeue(self):
        return self.__pop_front()




''''''''''''''''''''
''''''''''''''''''''
'''''Unit Tests'''''
''''''''''''''''''''
''''''''''''''''''''
# Run unittests with:
##  OSX:      'python3 -m unittest PriorityQueue.py'
##  Windows:  'python  -m unittest PriorityQueue.py'

class BasicTests(unittest.TestCase):
    def test_empty(self):
        self.assertTrue(PriorityQueue().empty())

    def test_enqueue_simple(self):
        priority_queue = PriorityQueue()
        priority = 5
        name = "test"
        priority_queue.enqueue(priority, name)
        self.assertFalse(priority_queue.empty())

    def test_length(self):
        priority_queue = PriorityQueue()
        priority = 5
        top = 11
        for task_id in range(1, top):
            priority_queue.enqueue(priority, task_id)
            priority -= .5
        self.assertEqual(len(priority_queue), top-1)

    def test_enqueue_same_priority_simple(self):
        priority_queue = PriorityQueue()
        priority = 5
        top = 5
        for task_id in range(1, top):
            priority_queue.enqueue(priority, task_id)
        self.assertEqual(len(priority_queue), top-1)
        self.assertEqual(priority_queue.names(), [1, 2, 3, 4])

    def test_enqueue_increasing_priority(self):
        priority_queue = PriorityQueue()
        priority = 1
        top = 11
        for task_id in range(1, top):
            priority_queue.enqueue(priority, task_id)
            priority += .5
        self.assertEqual(len(priority_queue), top-1)
        self.assertEqual(priority_queue.names(), [9, 10, 8, 7, 6, 5, 4, 3, 2, 1])

    def test_init(self):
        students = [[4, "John"], [5,  "Bill"], [2, "Joe"], [3, "Janet"]]
        priority_queue = PriorityQueue(students)
        self.assertEqual(len(priority_queue), len(students))

    def test_deqeue_empty(self):
        self.assertRaises(RuntimeError, lambda: PriorityQueue().dequeue())

    def test_dequeue(self):
        students = [[4, "John"], [5,  "Bill"], [2, "Joe"], [3, "Janet"]]
        priority_queue = PriorityQueue(students)
        self.assertEqual(priority_queue.dequeue()["name"], "Bill")
        self.assertEqual(priority_queue.dequeue()["name"], "John")
        self.assertEqual(priority_queue.dequeue()["name"], "Janet")
        self.assertEqual(priority_queue.dequeue()["name"], "Joe")
        self.assertTrue(priority_queue.empty())

    def test_str(self):
        students = [[4, "John"], [5,  "Bill"], [2, "Joe"]]
        priority_queue = PriorityQueue(students)
        self.assertEqual(priority_queue.__str__(), "{'priority': 5, 'name': 'Bill', 'time': 0}, " \
                                                   "{'priority': 4.4, 'name': 'John', 'time': 0}, {'priority': 2, 'name': 'Joe', 'time': 0}")

    def test_repr(self):
        students = [[4, "John"], [5,  "Bill"], [2, "Joe"]]
        priority_queue = PriorityQueue(students)
        self.assertEqual(priority_queue.__repr__(), "PriorityQueue(({'priority': 5, 'name': 'Bill', 'time': 0}, " \
                                                    "{'priority': 4.4, 'name': 'John', 'time': 0}, {'priority': 2, 'name': 'Joe', 'time': 0}))")



class TestDelete(unittest.TestCase):
    def test_delete_empty(self):
        self.assertRaises(RuntimeError, lambda: PriorityQueue().delete(3))

    def test_delete_bad_call(self):
        self.assertRaises(RuntimeError, lambda: PriorityQueue().delete())

    def test_delete_first_item(self):
        students = [[4, "John"], [5,  "Bill"], [2, "Joe"]]
        priority_queue = PriorityQueue(students)
        priority_queue.delete("Bill")
        self.assertEqual(priority_queue.__str__(), "{'priority': 4.4, 'name': 'John', 'time': 0}, " \
                                                   "{'priority': 2, 'name': 'Joe', 'time': 0}")

    def test_delete_last_item(self):
        students = [[4, "John"], [5,  "Bill"], [2, "Joe"]]
        priority_queue = PriorityQueue(students)
        priority_queue.delete("Joe")
        self.assertEqual(priority_queue.__str__(), "{'priority': 5, 'name': 'Bill', 'time': 0}, " \
                                                   "{'priority': 4.4, 'name': 'John', 'time': 0}")

    def test_delete_middle_item(self):
        students = [[4, "John"], [5,  "Bill"], [2, "Joe"]]
        priority_queue = PriorityQueue(students)
        priority_queue.delete("John")
        self.assertEqual(priority_queue.__str__(), "{'priority': 5, 'name': 'Bill', 'time': 0}, " \
                                                   "{'priority': 2, 'name': 'Joe', 'time': 0}")

    def test_first_edge(self):
        students = [[4, "John"], [5,  "Bill"], [2, "Joe"], [3, "Janet"]]
        priority_queue = PriorityQueue(students)
        priority_queue.delete("John")
        self.assertEqual(priority_queue.__str__(), "{'priority': 5, 'name': 'Bill', 'time': 0}, "  \
                                                   "{'priority': 3, 'name': 'Janet', 'time': 0}, {'priority': 2.4, 'name': 'Joe', 'time': 0}")

    def test_last_edge(self):
        students = [[4, "John"], [5,  "Bill"], [2, "Joe"], [3, "Janet"]]
        priority_queue = PriorityQueue(students)
        priority_queue.delete("Janet")
        self.assertEqual(priority_queue.__str__(), "{'priority': 5, 'name': 'Bill', 'time': 0}, " \
                                                   "{'priority': 4.4, 'name': 'John', 'time': 0}, {'priority': 2.4, 'name': 'Joe', 'time': 0}")

    def test_delete_all(self):
        students = [[4, "John"], [5,  "Bill"], [2, "Joe"], [3, "Janet"]]
        priority_queue = PriorityQueue(students)
        for student in students:
            priority_queue.delete(student[1])
        self.assertTrue(priority_queue.empty())


class TestMiddleFromNode(unittest.TestCase):
    def test_empty(self):
        self.assertRaises(RuntimeError, lambda: PriorityQueue().middle_from_node())

    def test_find_middle_single(self):
        students = [[4, "John"]]
        priority_queue = PriorityQueue(students)
        self.assertEqual(priority_queue.middle_from_node(priority_queue.front).value["name"], "John")

    def test_find_middle_value_of_two(self):
        students = [[4, "John"], [5,  "Bill"]]
        priority_queue = PriorityQueue(students)
        self.assertEqual(priority_queue.middle_from_node(priority_queue.front).value["name"], "Bill")

    def test_find_middle_value_of_three(self):
        students = [[4, "John"], [5,  "Bill"], [2, "Joe"]]
        priority_queue = PriorityQueue(students)
        self.assertEqual(priority_queue.middle_from_node(priority_queue.front).value["name"], "John")

    def test_find_middle_value_of_four(self):
        students = [[4, "John"], [5,  "Bill"], [2, "Joe"], [3, "Janet"]]
        priority_queue = PriorityQueue(students)
        self.assertEqual(priority_queue.middle_from_node(priority_queue.front).value["name"], "John")

    def test_find_middle_value_of_five(self):
        students = [[4, "John"], [5,  "Bill"], [2, "Joe"], [3, "Janet"], [2, "Jimothy"]]
        priority_queue = PriorityQueue(students)
        self.assertEqual(priority_queue.middle_from_node(priority_queue.front).value["name"], "Janet")




'''''''''''''''''''''''''''
''''Main Runtime Script''''
'''''''''''''''''''''''''''


if '__main__' == __name__:
    def print_queue(priority_queue):
        num = 1
        for item in priority_queue:
            print(f"{num} : {item}")
            num += 1

    def file_read(file_name):
        priority_queue = PriorityQueue()
        with open(file_name) as inputFile:
            for line in inputFile:
                temp = line.split(" ")
                priority_queue.enqueue(int(temp[0]), temp[1].rstrip())
        if inputFile.closed == False:
            raise RuntimeError("Input file did not close correctly")
        print_queue(priority_queue)

    input_type = input("Input from a file or from user input? ('file' or 'user')")

    while input_type.lower() not in ('user', 'file'):
        print(f"'{input_type}' is not a valid option")
        input_type = input("Input from a file or from user input? ('file' or 'user')")
    if input_type.lower() == 'file':
        print("Test Cases with Detailed Event Logs")
        print("\n\n---------------------------------------------\n\n", "test_data1.dat")
        file_read("test_data1.dat")
        print("\n\n---------------------------------------------\n\n", "test_data2.dat")
        file_read("test_data2.dat")
        print("\n\n---------------------------------------------\n\n", "test_data3.dat")
        file_read("test_data3.dat")
    else:
        done = False
        priority_queue = PriorityQueue()
        while(done != True):
            name = input("Student name?")
            priority = input("Task priority?")
            priority_queue.enqueue(int(priority), name)
            exit = input("Another student? (yes or no)")
            if exit.lower() == 'no':
                done = True
        print_queue(priority_queue)
