class JohnsonTrotter(object):
    class __nums(object):
        class __num(object):
            def __init__(self, number, direction='>'):
                self.number = number
                self.direction = direction

            def flip(self):
                if self.direction == '<':
                    self.direction == '>' 
                elif self.direction == '>':
                    self.direction = '<' 

            def __str__(self):
                return str(self.number)

            def __eq__(self, other):
                if other.number == self.number:
                    return True
                return False

        def __init__(self, string):
            self.perm = []
            for index, item in enumerate(string):
                if index == (len(string)-1):
                    self.perm.append(self.__num(str(item), '<'))
                    break
                self.perm.append(self.__num(str(item)))
                #self.perm(self.__num(str(item)))
            self.mover = self.perm[len(self.perm)-1]

        def __str__(self):
            ret_str = ""
            for item in self.perm:
                ret_str += str(item)
            return ret_str
            

        def move(self):
            pos = self.pos()
            end = len(self.perm) - 1
            if self.mover.direction == '<':
                if pos > 0:
                    self.__move_left(pos)
                else:
                    self.perm[end], self.perm[end-1] = self.perm[end-1], self.perm[end]
                    self.perm[end].flip()
                    self.perm[end-1].flip()
                    self.mover.flip()
                    self.mover.direction = '>'
            else:
                if pos != end:
                    self.__move_right(pos)
                else:
                    self.perm[0], self.perm[1] = self.perm[1], self.perm[0]
                    self.perm[0].flip()
                    self.perm[1].flip()
                    self.mover.direction = '<'

        def __move_left(self, pos):
            self.perm[pos], self.perm[pos-1] = self.perm[pos-1], self.perm[pos]
            self.mover = self.perm[pos-1]

        def __move_right(self, pos):
            self.perm[pos], self.perm[pos+1] = self.perm[pos+1], self.perm[pos]
            self.mover = self.perm[pos+1]

        def pos(self):
            return self.perm.index(self.mover)

        def __line_flip(self):
            pass

    def __init__(self, n):
        self.n = n
        self.n_combos = self.facto(n)
        self.set_of_all = set()
        self.start_string = ""
        for i in range(1, self.n + 1):
            self.start_string += str(i)
        ##for index, item in enumerate(self.start_string):
        ##    if index == (len(self.start_string)-1):
        self.set_of_all.add(self.start_string)
        self.nums = self.__nums(self.start_string)

    def __str__(self):
        return str(self.nums)        

    def facto(self,n_iter):
        if n_iter == 1:
            return 1
        return n_iter * self.facto(n_iter-1)

    def nextPermutation(self):
        self.nums.move()
        return str(self.nums)

test = JohnsonTrotter(9)
print(test)
for i in range(10):
    print(test.nextPermutation())
