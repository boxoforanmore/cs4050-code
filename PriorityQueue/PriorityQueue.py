from __future__ import print_function
import unittest

class PriorityQueue(object):
    class Node(object):
        # pylint: disable=too-few-public-methods
        ''' no need for get or set, we only access the values inside the
            PriorityQueue class. and really: never have setters. '''

        def __init__(self, value, next_node):
            self.value = value
            self.next_node = next_node

    def __init__(self, initial=None):
        self.front = self.back = self.current = None
        self.__length = 0
        if initial != None:
            for element in tuple(initial):
                self.__push_front(element)

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
        output = ''
        tmp = self.back
        tmp2 = None
        while tmp is not self.front:
            tmp2 = self.front
            output += str(tmp.value) + ', '
            while tmp2.next_node is not tmp:
                tmp2 = tmp2.next_node
            tmp = tmp2
        return (output + str(tmp.value))


    def __repr__(self):
        return 'PriorityQueue((' + str(self) + '))'


    def __push_front(self, value):
        new = self.Node(value, self.front)
        if self.empty():
            self.front = self.back = new
            self.__length += 1
        else:
            new.next_node = self.front
            self.front = new
            self.__length += 1

    ''' you need to(at least) implement the following three methods'''

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
        if self.front.value == value:
            self.__pop_front()
            return
        if self.back.value == value:
            self.__pop_back()
            return
        else:
            prev = self.front
            current = self.front.next_node
            nxt = self.front.next_node.next_node
            if current.value is value:
                prev.next_node = nxt 
                current.next_node = None
                current = None
                return
            while current is not self.back:
                if current.value is value:
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

    def middle_value(self):
        if self.empty():
            raise RuntimeError("PriorityQueue is empty")
        if self.front == self.back:
            return self.front.value
        if self.front.next_node == self.back:
            return self.back.value
        fast = self.front.next_node.next_node
        slow = self.front.next_node
        while fast is not self.back:
            if fast.next_node.next_node is None:
                fast = fast.next_node
            else:
                fast = fast.next_node.next_node
            slow = slow.next_node
        return slow.value

    def middle(self):
        if self.empty():
            raise RuntimeError("PriorityQueue is empty")
        if self.front == self.back:
            return self.front
        if self.front.next_node == self.back:
            return self.back
        fast = self.front.next_node.next_node
        slow = self.front.next_node
        while fast is not self.back:
            if fast.next_node.next_node is None:
                fast = fast.next_node
            else:
                fast.next_node.next_node
            slow = slow.next_node
        return slow

    def search(self, value=None):
        if self.empty():
            raise RuntimeError("PriorityQueue is empty")
        pos = 1
        for item in self:
            if value < item["priority"]:
                return pos
            pos += 1
        return pos


    def enqueue(self, priority, name, time=0):
        if priority > 5:
             priority = 5.0
        temp = {"priority": priority,
                "name": name,
                "time": time}
        if self.empty():
            self.__push_back(temp)
        else:
            position = self.search(temp["priority"])
            if position > len(self):
                self.__push_back(temp)
            else:
                # have insert return if it needs to be from earlier than the pointer
                sortAll = self.insert(temp, position)
                self = self.mergeSort(self.middle())


    def insert(self, item, position):
        track = 0
        inserted = False
        # Case for only 1?
        sortAll = True
        noderino = self.front.next_node
        if len(self) == 1:
            if position == 0:
                self.__push_front(item)
                inserted = True
            elif position == 1:
                self.__push_back(item)
                return False
        else:
            for element in self:
                if track == position:
                    noderino = element.next_node
                    sortAll = (element.value["priority"] < (noderino.value["priority"] + 0.4))
                    new = self.Node(item, noderino)
                    element.next_node = new
                    inserted = True
                    self.__length += 1
                    break
                track += 1
        while noderino != None:
            noderino.value["priority"] += 0.4
            if noderino.value["priority"] > 5:
                noderino.value["priority"] = 5
            noderino = noderino.next_node
        return sortAll

    # Bubble sort at position or all
    def mergeSort(self, noderino):
        if (noderino == None) or (noderino.next_node == None):
            return noderino

        mid = self.middle()
        mid_next = mid.next_node
        mid.next_node = None

        left_side = mergeSort(noderino)
        right_side = mergeSort(mid_next)

        return mergeBack(left, right)

    def mergeBack(self, left, right):
        sortedList = None
        if left == None:
            return right
        if right == None:
            return left
        if left.value["priority"] >= right.value["priority"]:
            sortedList = left
            sortedList.next_node = mergeBack(left.next_node, right)
        else:
            sortedList = right
            sortedList.next_node = mergeBack(left, right.next_node)
        return result


    def dequeue(self):
        if self.empty():
            raise RuntimeError("PriorityQueue is empty")
        if self.front == self.back:
            temp = self.front.value
            self.front = self.back = None
            return temp
        else:
            return self.__pop_front()



class PriorityQueue2(list):
    def enqueue(self, value):
        list.insert(self, 0, value)

    def dequeue(self):
        pass
        #temp =
    # use a dictionary for adding to the queue 

    def __sort__(self):
        pass 


'''Unit Tests'''

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
        priority = 1
        top = 11
        for task_id in range(1, top):
             priority_queue.enqueue(priority, task_id)
             priority += .5
        self.assertEqual(len(priority_queue), top-1)

    def test_enqueue_sort_simple(self):
        priority_queue = PriorityQueue()
        priority = 5
        top = 11
        for task_id in range(1, top):
             priority_queue.enqueue(priority, task_id)
             priority -= .5
        self.assertEqual(len(priority_queue), top-1)
        print(priority_queue)
        pass

    def test_init(self):
        priority_queue = PriorityQueue(("one", 2, 3.141592))
        self.assertEqual(priority_queue.dequeue(), 3.141592)
        self.assertEqual(priority_queue.dequeue(), 2)
        self.assertEqual(priority_queue.dequeue(), "one")

    def test_str(self):
        priority_queue = PriorityQueue((1, 2, 3))
        self.assertEqual(priority_queue.__str__(), '1, 2, 3')

    def test_repr(self):
        priority_queue = PriorityQueue((1, 2, 3))
        self.assertEqual(priority_queue.__repr__(), 'PriorityQueue((1, 2, 3))')


class TestDelete(unittest.TestCase):
    def test_delete_empty(self):
        self.assertRaises(RuntimeError, lambda: PriorityQueue().delete(3))

    def test_delete_bad_call(self):
        self.assertRaises(RuntimeError, lambda: PriorityQueue().delete())

    def test_delete_first_item(self):
        priority_queue = PriorityQueue((1, 2, 3, 4, 5, 6)) 
        priority_queue.delete(1)
        self.assertEqual(priority_queue.__str__(), '2, 3, 4, 5, 6')

    def test_delete_last_item(self):
        priority_queue = PriorityQueue((1, 2, 3, 4, 5, 6)) 
        priority_queue.delete(6)
        self.assertEqual(priority_queue.__str__(), '1, 2, 3, 4, 5')

    def test_delete_middle_value_item(self):
        priority_queue = PriorityQueue((1, 2, 3, 4, 5, 6, 7)) 
        priority_queue.delete(4)
        self.assertEqual(priority_queue.__str__(), '1, 2, 3, 5, 6, 7')

    def test_first_edge(self):
        priority_queue = PriorityQueue((1, 2, 3, 4, 5, 6))
        priority_queue.delete(2)
        self.assertEqual(priority_queue.__str__(), '1, 3, 4, 5, 6')

    def test_last_edge(self):
        priority_queue = PriorityQueue((1, 2, 3, 4, 5, 6))
        priority_queue.delete(5)
        self.assertEqual(priority_queue.__str__(), '1, 2, 3, 4, 6')

    def test_delete_all(self):
        values = (1, 2, 3, 4, 5, 6)
        priority_queue = PriorityQueue(values)
        self.assertFalse(priority_queue.empty())
        for value in values:
            priority_queue.delete(value)
        self.assertTrue(priority_queue.empty())

class TestMiddle(unittest.TestCase):
    def test_empty(self):
        self.assertRaises(RuntimeError, lambda: PriorityQueue().middle_value())

    def test_find_middle_value_single(self):
        priority_queue = PriorityQueue((3,))
        self.assertEqual(priority_queue.middle_value(), 3)

    def test_find_middle_value_of_two(self):
        priority_queue = PriorityQueue((1, 2))
        self.assertEqual(priority_queue.middle_value(), 1)

    def test_find_middle_value_of_three(self):
        priority_queue = PriorityQueue((1, 2, 3))
        self.assertEqual(priority_queue.middle_value(), 2)

    def test_find_middle_value_of_four(self):
        priority_queue = PriorityQueue((1, 2, 3, 4))
        self.assertEqual(priority_queue.middle_value(), 2)

    def test_find_middle_value_of_five(self):
        priority_queue = PriorityQueue((1, 2, 3, 4, 5))
        self.assertEqual(priority_queue.middle_value(), 3)

    def test_find_middle_value_of_20(self):
        priority_queue = PriorityQueue(tuple(range(1, 21))) 
        self.assertEqual(priority_queue.middle_value(), 10)

    def test_find_middle_value_of_103(self):
        priority_queue = PriorityQueue(tuple(range(1, 104)))
        self.assertEqual(priority_queue.middle_value(), 52)


if '__main__' == __name__:
    unittest.main()
