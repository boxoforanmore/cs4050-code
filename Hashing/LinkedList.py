from __future__ import print_function
import unittest


class LinkedList(object):
    class Node(object):
        def __init__(self, value, next_node):
            self.value = value
            self.next_node = next_node

    def __init__(self, initial=None):
        self.front = self.back = self.current = None
        self.length = 0
        if initial != None:
            for element in tuple(initial):
                self.push_front(element)

    def __len__(self):
        return self.length

    def empty(self):
        return self.front == self.back == None

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
        return 'LinkedList((' + str(self) + '))'


    def push_front(self, value):
        new = self.Node(value, None)
        if self.empty():
            self.front = self.back = new
        else:
            new.next_node = self.front
            self.front = new
        self.length += 1


    def pop_front(self):
        tmp = self.front
        if self.empty():
            raise RuntimeError("LinkedList is empty")
        if self.front == self.back:
            value = self.front.value
            self.front = self.back = None
            self.length -= 1
            return value
        else:
            tmp = self.front.next_node
            value = self.front.value
            self.front.next_node = None
            self.front = tmp
            self.length -= 1
            return value


    def push_back(self, value):
        new = self.Node(value, None)
        if self.empty():
            self.front = self.back = new
            self.length += 1
            return
        self.back.next_node = new
        self.back = new
        self.length += 1


    def pop_back(self):
        if self.empty():
            raise RuntimeError("LinkedList is empty")
        if self.front is self.back:
            value = self.front.value
            self.front = self.back = None
            self.length -= 1
            return value
        else:
            current = self.front
            while current.next_node is not self.back:
                current = current.next_node
            value = current.next_node.value
            current.next_node = None
            self.back = current
            self.length -= 1
            return value

    
    def delete(self, value=None):
        if value == None:
            raise RuntimeError("LinkedList's delete method must be called with a value")
        if self.empty():
            raise RuntimeError("LinkedList is empty")
        if self.front.value == value:
            self.pop_front()
            return
        if self.back.value == value:
            self.pop_back()
            return
        else:
            prev = self.front
            current = self.front.next_node
            nxt = self.front.next_node.next_node
            if current.value is value:
                prev.next_node = nxt 
                current.next_node = None
                current = None
                self.length -= 1
                return
            while current is not self.back:
                if current.value is value:
                    prev.next_node = nxt
                    current.next_node = None
                    current = None
                    self.length -= 1
                    return
                else:
                    prev = current
                    current = nxt
                    nxt = nxt.next_node
            return
        raise RuntimeError("Delete method is not working correctly")

    # Inserts in reverse order
    def insert(self, value=None):
        if value == None:
            raise RuntimeError("LinkedList's insert method must be called with a value")
        if self.empty():
            self.push_front(value)
            return
        if self.front.value > value:
            self.push_front(value)
            return
        if self.back.value < value:
            self.push_back(value)
            return 
        prev = self.front
        while prev.next_node != None:
            if prev.next_node.value > value:
                temp = prev.next_node
                current = self.Node(value, temp)
                prev.next_node = current
                self.length += 1
                return
            prev = prev.next_node

    def find(self, value=None):
        if value == None:
            raise RuntimeError("LinkedList's find method must be called with a value")
        if self.empty():
            return False
        for node in self:
            if node == value:
                return True
        return False

    def middle(self):
        if self.empty():
            raise RuntimeError("LinkedList is empty")
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


class BasicTests(unittest.TestCase):
    def test_empty(self):
        self.assertTrue(LinkedList().empty())

    def test_push_front_pop_back(self):
        linked_list = LinkedList()
        linked_list.push_front(1)
        linked_list.push_front(2)
        linked_list.push_front(3)
        self.assertFalse(linked_list.empty())
        self.assertEqual(linked_list.pop_back(), 1)
        self.assertEqual(linked_list.pop_back(), 2)
        self.assertEqual(linked_list.pop_back(), 3)
        self.assertTrue(linked_list.empty())

    def test_push_front_pop_front(self):
        linked_list = LinkedList()
        linked_list.push_front(1)
        linked_list.push_front(2)
        linked_list.push_front(3)
        self.assertEqual(linked_list.pop_front(), 3)
        self.assertEqual(linked_list.pop_front(), 2)
        self.assertEqual(linked_list.pop_front(), 1)
        self.assertTrue(linked_list.empty())

    def test_push_back_pop_front(self):
        linked_list = LinkedList()
        linked_list.push_back(1)
        linked_list.push_back(2)
        linked_list.push_back(3)
        self.assertFalse(linked_list.empty())
        self.assertEqual(linked_list.pop_front(), 1)
        self.assertEqual(linked_list.pop_front(), 2)
        self.assertEqual(linked_list.pop_front(), 3)
        self.assertTrue(linked_list.empty())

    def test_push_back_pop_back(self):
        linked_list = LinkedList()
        linked_list.push_back(1)
        linked_list.push_back("foo")
        linked_list.push_back([3, 2, 1])
        self.assertFalse(linked_list.empty())
        self.assertEqual(linked_list.pop_back(), [3, 2, 1])
        self.assertEqual(linked_list.pop_back(), "foo")
        self.assertEqual(linked_list.pop_back(), 1)
        self.assertTrue(linked_list.empty())

    def test_init(self):
        linked_list = LinkedList(("one", 2, 3.141592))
        self.assertEqual(linked_list.pop_back(), "one")
        self.assertEqual(linked_list.pop_back(), 2)
        self.assertEqual(linked_list.pop_back(), 3.141592)

    def test_str(self):
        linked_list = LinkedList((1, 2, 3))
        self.assertEqual(linked_list.__str__(), '1, 2, 3')

    def test_iter(self):
        nums = [2, 1, 8]
        linked_list = LinkedList(nums)
        nums = [8, 1, 2]
        for num, item in enumerate(linked_list):
            self.assertEqual(item, nums[num])

    def test_repr(self):
        linked_list = LinkedList((1, 2, 3))
        self.assertEqual(linked_list.__repr__(), 'LinkedList((1, 2, 3))')

    def test_pop_front_empty(self):
        self.assertRaises(RuntimeError, lambda: LinkedList().pop_front())

    def test_pop_back_empty(self):
        self.assertRaises(RuntimeError, lambda: LinkedList().pop_back())

    def test_delete_empty(self):
        self.assertRaises(RuntimeError, lambda: LinkedList().delete(3))

    def test_delete_bad_call(self):
        self.assertRaises(RuntimeError, lambda: LinkedList().delete())

    def test_delete_first_item(self):
        linked_list = LinkedList((1, 2, 3, 4, 5, 6)) 
        linked_list.delete(1)
        self.assertEqual(linked_list.__str__(), '2, 3, 4, 5, 6')

    def test_delete_last_item(self):
        linked_list = LinkedList((1, 2, 3, 4, 5, 6)) 
        linked_list.delete(6)
        self.assertEqual(linked_list.__str__(), '1, 2, 3, 4, 5')

    def test_delete_middle_item(self):
        linked_list = LinkedList((1, 2, 3, 4, 5, 6, 7)) 
        linked_list.delete(4)
        self.assertEqual(linked_list.__str__(), '1, 2, 3, 5, 6, 7')

    def test_first_edge(self):
        linked_list = LinkedList((1, 2, 3, 4, 5, 6))
        linked_list.delete(2)
        self.assertEqual(linked_list.__str__(), '1, 3, 4, 5, 6')

    def test_last_edge(self):
        linked_list = LinkedList((1, 2, 3, 4, 5, 6))
        linked_list.delete(5)
        self.assertEqual(linked_list.__str__(), '1, 2, 3, 4, 6')

    def test_delete_all(self):
        values = (1, 2, 3, 4, 5, 6)
        linked_list = LinkedList(values)
        self.assertFalse(linked_list.empty())
        for value in values:
            linked_list.delete(value)
        self.assertTrue(linked_list.empty())

    def test_empty(self):
        self.assertRaises(RuntimeError, lambda: LinkedList().middle())

    def test_find_middle_single(self):
        linked_list = LinkedList((3,))
        self.assertEqual(linked_list.middle(), 3)

    def test_find_middle_of_two(self):
        linked_list = LinkedList((1, 2))
        self.assertEqual(linked_list.middle(), 1)

    def test_find_middle_of_three(self):
        linked_list = LinkedList((1, 2, 3))
        self.assertEqual(linked_list.middle(), 2)

    def test_find_middle_of_four(self):
        linked_list = LinkedList((1, 2, 3, 4))
        self.assertEqual(linked_list.middle(), 2)

    def test_find_middle_of_five(self):
        linked_list = LinkedList((1, 2, 3, 4, 5))
        self.assertEqual(linked_list.middle(), 3)

    def test_find_middle_of_20(self):
        linked_list = LinkedList(tuple(range(1, 21))) 
        self.assertEqual(linked_list.middle(), 10)

    def test_find_middle_of_103(self):
        linked_list = LinkedList(tuple(range(1, 104)))
        self.assertEqual(linked_list.middle(), 52)

    def test_insert_none(self):
        self.assertRaises(RuntimeError, lambda: LinkedList().insert())

    def test_insert_empty(self):
        linked_list = LinkedList()
        linked_list.insert(1)
        self.assertEqual(str(linked_list), '1')

    def test_insert_range(self):
        linked_list = LinkedList()
        nums = [45, 6, 523, 234, 43, 143, 2, 97]
        length = len(nums)
        for num in nums:
            linked_list.insert(num)
        test = ''
        for num, item in enumerate(reversed(sorted(nums))):
            if num == length-1:
                test += str(item)
                break
            test += str(item) + ', '
        self.assertEqual(str(linked_list), test)

    def test_find_none(self):
        self.assertRaises(RuntimeError, lambda: LinkedList().find())

    def test_find_empty(self):
        self.assertFalse(LinkedList().find('1'))

    def test_find_true(self):
        linked_list = LinkedList((2, 4, 6))
        self.assertTrue(linked_list.find(2))

    def test_find_false(self):
        linked_list = LinkedList((2, 4, 6))
        self.assertFalse(linked_list.find(3))

    def test_length_empty(self):
        self.assertEqual(len(LinkedList()), 0)

    def test_length_push_front_pop_front(self):
        linked_list = LinkedList()
        linked_list.push_front(4)
        self.assertEqual(len(linked_list), 1)
        linked_list.pop_front()
        self.assertEqual(len(linked_list), 0)

    def test_length_push_back_pop_back(self):
        linked_list = LinkedList()
        linked_list.push_back(4)
        self.assertEqual(len(linked_list), 1)
        linked_list.pop_back()
        self.assertEqual(len(linked_list), 0)

    def test_length_insert_pop_back(self):
        linked_list = LinkedList()
        linked_list.insert(5)
        self.assertEqual(len(linked_list), 1)
        linked_list.pop_back()
        self.assertEqual(len(linked_list), 0)

    def test_length_all(self):
        linked_list = LinkedList()
        items1 = tuple(range(1, 10))
        items2 = tuple(range(11, 30))
        items3 = tuple(range(31, 50))
        count = 0
        for item in items1:
            linked_list.push_front(item)
            count += 1
        for item in items2:
            linked_list.push_back(item)
            count += 1
        for item in items3:
            linked_list.insert(item)
            count += 1
        self.assertEqual(len(linked_list), count)
        for i in range(1, 10):
            linked_list.pop_back()
            linked_list.pop_front()
            count -= 2
        self.assertEqual(len(linked_list), count)
        for i in range(13, 25):
            linked_list.delete(i)
            count -= 1
        self.assertEqual(len(linked_list), count)



if '__main__' == __name__:
    unittest.main()
