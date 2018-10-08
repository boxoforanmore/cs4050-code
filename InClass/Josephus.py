class PlayJosephus(object):
    class __soldiers(object):
        def __init__(self, number):
            self.soulja_boyz = []
            self.final = None
            self.alive = number

        def add(self, soldier):
            self.soulja_boys.add(soldier)

        def __len__(self):
            return len(self.soulja_boyz)

        def run_round(self):
            if self.alive == 1:
                print(self.final)
            else:
                for index, soulja in enumerate(self.soulja_boyz):
                    if (self.soulja_boyz[soulja.next_index].state == "alive"):
                        self.soulja_boyz[soulja.next_index].kill()
                        self.alive -= 1
                        print(f"{index + 1} kills {soulja.next_index + 1}")
                        found = False
                        for i in range(soulja.next_index, len(self)):
                            if self.soulja_boyz[i].state == "alive":
                                found = True
                                soulja.next_index = i
                                break
                        if not found:
                            for i in range(0, soulja.index):
                                if self.soulja_boyz[i].state == "alive":
                                    found = True
                                    soulja.next_index = i
                            
                         

    class __soldier(object):
        def __init__(self, index, next_index):
            self.index = index
            self.next_index = next_index
            self.state = "alive"

        def kill(self):
            self.state = "dead"

        def __str__(self):
            return "Soldier: " + str(self.index) + " " + str(self.state.upper())

    def __init__(self, number=None, position=None):
        self.number = number
        self.position = position
        answer = "y"
        replay = "y"
        while answer == "y":
            if (self.number == None) or (replay == "y"):
                self.number = int(input("What is the number of soldiers? "))
            if (self.position == None) or (replay == "y"):
                self.position = int(input("What position do you choose? "))
            result = self.Josephus()
            if result != self.position:
                print("You have killed Josephus!")
                print(f"You chose: {self.position}")
                print(f"Soldier {result} survived")
                answer = input("Try again? (y/n) ")
            else:
                print("Josephus has survived!") 
                answer = input("Play again? (y/n)")
         #self.__see_path()

    def __see_path(self):
       soldiers = soldier 

    def __run_path(self):
        soldiers = {}
        for i in range(1, self.number + 1):
            soldiers[i] = "alive"
        for i in range(1, self.number + 1):
            if soldiers[i] == "alive":
                killed = False
                j = int(i + 1)
                while killed == False:
                    if soldiers[j] == "alive":
                        soldiers[k] == "dead"

    def Josephus(self):
        if self.number == 1:
            return 1
        power = self.__two_pow(self.number)
        return (2*(self.number - (2**power))) + 1

 
    def __two_pow(self, num):
        power = 0
        while ((2**(power+1)) <= num):
            power += 1
        return power


PlayJosephus()
