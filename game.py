import random

class Player():
    def __init__(self, hh: int, ht: int, th: int, tt: int):
        self.hh = hh        # (r1,c1) payoff
        self.ht = ht        # (r1,c2) payoff
        self.th = th        # (r2,c1) payoff
        self.tt = tt        # (r2,c2) payoff
        self.other_head = random.random() + random.randint(0,10)       # set opponent previous action with random number
        self.other_tail = 10 - self.other_head
        #print(f"h={self._other_head} t={self._other_tail}")


    def strategy(self) -> int:
        select_h = self.other_head * self.hh + self.other_tail * self.ht
        select_t = self.other_head * self.th + self.other_tail * self.tt
        if select_h >= select_t:
            return 0            # choose strategy 1
        else:
            return 1            # choose strategy 2

    def set_belief(self, other: int):   # update opponent action
        if other == 0:
            self.other_head += 1
        else:
            self.other_tail += 1

'''
class Player():
    def __init__(self, hh: int, ht: int, th: int, tt: int):
        self.hh = hh        # (r1,c1) payoff
        self.ht = ht        # (r1,c2) payoff
        self.th = th        # (r2,c1) payoff
        self.tt = tt        # (r2,c2) payoff
        self._other_head = random.random() + random.randint(0,10)       # set opponent previous action with random number
        self._other_tail = random.random() + random.randint(0,10)
        #print(f"h={self._other_head} t={self._other_tail}")


    def strategy(self) -> int:
        select_h = self._other_head * self.hh + self._other_tail * self.ht
        select_t = self._other_head * self.th + self._other_tail * self.tt
        if select_h >= select_t:
            return 0            # choose strategy 1
        else:
            return 1            # choose strategy 2

    def set_belief(self, other: int):   # update opponent action
        if other == 0:
            self._other_head += 1
        else:
            self._other_tail += 1
'''

def repear_1000_times(func):
    def warp(*args):
        result_dict = {("r1", "c1"): 0,
                       ("r1", "c2"): 0,
                       ("r2", "c1"): 0,
                       ("r2", "c2"): 0}
        for i in range(1000):
            res = func(*args)
            result_dict[res] += 1
        print(f"(r1,c1): {result_dict[('r1', 'c1')]/1000} (r1,c2): {result_dict[('r1', 'c2')]/1000} "
              f"(r2,c1): {result_dict[('r2', 'c1')]/1000} (r2,c2): {result_dict[('r2', 'c2')]/1000}")
    return warp


def repeat_1000(func):
    def warp(*args):
        result_dict = {0: 0,
                       1: 0,
                       2: 0,
                       3: 0}
        for i in range(1000):
            res = func(*args)
            for i in range(4):
                result_dict[i] += res[i]
        print(f"p_r1: {round(result_dict[0] / 1000, 3)} p_r2: {round(result_dict[1] / 1000, 3)} "
              f"p_c1: {round(result_dict[2] / 1000, 3)} p_c2: {round(result_dict[3] / 1000, 3)}")
    return warp

def repeat_1000s(func):
    def warp(*args):
        result_dict = {0: 0,            # represent pure strategy (r1,c1)
                       1: 0,            # represent pure strategy (r1,c2)
                       2: 0,            # represent pure strategy (r2,c1)
                       3: 0,            # represent pure strategy (r2,c2)
                       4: 0}            # represent mix strategy
        mix_strategy = tuple()
        for i in range(1000):
            res = func(*args)
            if res[0] > 0.99 and res[2] > 0.99:
                result_dict[0] += 1
            elif res[0] > 0.99 and res[3] > 0.99:
                result_dict[1] += 1
            elif res[1] > 0.99 and res[2] > 0.99:
                result_dict[2] += 1
            elif res[1] > 0.99 and res[3] > 0.99:
                result_dict[3] += 1
            else:
                result_dict[4] += 1
                mix_strategy = res

        print(f"NE(r1,c1):{round(result_dict[0] / 1000, 3)} NE(r1,c2):{round(result_dict[1] / 1000, 3)} "
              f"NE(r2,c1):{round(result_dict[2] / 1000, 3)} NE(r2,c2):{round(result_dict[3] / 1000, 3)} "
              f"Mixed-strategy NE:{round(result_dict[4] / 1000, 3)} , probability:{mix_strategy} ")
    return warp


# Q1
def check(strategy_history: list) -> bool:
    strategy = max(set(strategy_history), key = strategy_history.count)
    if float(strategy) / float(len(strategy_history)) >= 0.99:
        return True
    return False

@repear_1000_times
def pure_strategy_NE(r1c1 : tuple, r1c2: tuple, r2c1: tuple, r2c2: tuple) -> tuple:
    player1 = Player(hh= r1c1[0], ht= r1c2[0], th= r2c1[0], tt= r2c2[0])
    player2 = Player(hh= r1c1[1], ht= r2c1[1], th= r1c2[1], tt= r2c2[1])
    player1_strategy_history = []
    player2_strategy_history = []
    while(True):
        s1 = player1.strategy()
        s2 = player2.strategy()
        player1_strategy_history.append(s1)
        player2_strategy_history.append(s2)
        player2.set_belief(s1)
        player1.set_belief(s2)
        if check(player1_strategy_history) and check(player2_strategy_history):
            break

    p1_strategy = player1.strategy()
    p2_strategy = player2.strategy()
    strategySet = {"00":("r1","c1"),
                   "01":("r1","c2"),
                   "10":("r2","c1"),
                   "11":("r2","c2")}
    return strategySet[str(p1_strategy)+str(p2_strategy)]




#Q2Q3
@repear_1000_times
def more_pure_strategy_NE(r1c1 : tuple, r1c2: tuple, r2c1: tuple, r2c2: tuple, e = 0.99) -> tuple:
    player1 = Player(hh=r1c1[0], ht=r1c2[0], th=r2c1[0], tt=r2c2[0])
    player2 = Player(hh=r1c1[1], ht=r2c1[1], th=r1c2[1], tt=r2c2[1])
    player1_strategy_history = []
    player2_strategy_history = []
    for i in range(10000):
        s1 = player1.strategy()
        s2 = player2.strategy()
        player1_strategy_history.append(s1)
        player2_strategy_history.append(s2)
        player2.set_belief(s1)
        player1.set_belief(s2)
    strategy1 = max(set(player1_strategy_history), key=player1_strategy_history.count)
    strategy2 = max(set(player2_strategy_history), key=player2_strategy_history.count)
    strategySet = {(0,0): ("r1", "c1"),
                    (0,1): ("r1", "c2"),
                    (1,0): ("r2", "c1"),
                    (1,1): ("r2", "c2")}

    return strategySet[(strategy1,strategy2)]


# Q4
@repeat_1000
def mixed_strategy_NE(r1c1 : tuple, r1c2: tuple, r2c1: tuple, r2c2: tuple, e = 0.99) -> tuple:
    player1 = Player(hh=r1c1[0], ht=r1c2[0], th=r2c1[0], tt=r2c2[0])
    player2 = Player(hh=r1c1[1], ht=r2c1[1], th=r1c2[1], tt=r2c2[1])
    player1_strategy_history = []
    player2_strategy_history = []
    for i in range(10000):
        s1 = player1.strategy()
        s2 = player2.strategy()
        player1_strategy_history.append(s1)
        player2_strategy_history.append(s2)
        player2.set_belief(s1)
        player1.set_belief(s2)
    p_r1 = player1_strategy_history.count(0) / float(len(player1_strategy_history))
    p_r2 = player1_strategy_history.count(1) / float(len(player1_strategy_history))
    p_c1 = player2_strategy_history.count(0) / float(len(player2_strategy_history))
    p_c2 = player2_strategy_history.count(1) / float(len(player2_strategy_history))

    return (p_r1, p_r2, p_c1, p_c2)



# Q5
@repeat_1000
def best_reply_path(r1c1 : tuple, r1c2: tuple, r2c1: tuple, r2c2: tuple, e = 0.99) -> tuple:
    player1 = Player(hh=r1c1[0], ht=r1c2[0], th=r2c1[0], tt=r2c2[0])
    player2 = Player(hh=r1c1[1], ht=r2c1[1], th=r1c2[1], tt=r2c2[1])
    player1_strategy_history = []
    player2_strategy_history = []
    for i in range(10000):
        s1 = player1.strategy()
        s2 = player2.strategy()
        player1_strategy_history.append(s1)
        player2_strategy_history.append(s2)
        player2.set_belief(s1)
        player1.set_belief(s2)
    p_r1 = player1_strategy_history.count(0) / float(len(player1_strategy_history))
    p_r2 = player1_strategy_history.count(1) / float(len(player1_strategy_history))
    p_c1 = player2_strategy_history.count(0) / float(len(player2_strategy_history))
    p_c2 = player2_strategy_history.count(1) / float(len(player2_strategy_history))
    return (p_r1, p_r2, p_c1, p_c2)


# Q6  depend on initial belief if initial is p1(9,9) p2(3,3) than is mix; other's is pure strategy
@repeat_1000s
def pure_coordination(r1c1 : tuple, r1c2: tuple, r2c1: tuple, r2c2: tuple, e = 0.99) -> tuple:
    player1 = Player(hh=r1c1[0], ht=r1c2[0], th=r2c1[0], tt=r2c2[0])
    player2 = Player(hh=r1c1[1], ht=r2c1[1], th=r1c2[1], tt=r2c2[1])
    player1_strategy_history = []
    player2_strategy_history = []
    for i in range(10000):
        s1 = player1.strategy()
        s2 = player2.strategy()
        player1_strategy_history.append(s1)
        player2_strategy_history.append(s2)
        player2.set_belief(s1)
        player1.set_belief(s2)
    p_r1 = player1_strategy_history.count(0) / float(len(player1_strategy_history))
    p_r2 = player1_strategy_history.count(1) / float(len(player1_strategy_history))
    p_c1 = player2_strategy_history.count(0) / float(len(player2_strategy_history))
    p_c2 = player2_strategy_history.count(1) / float(len(player2_strategy_history))
    return (p_r1, p_r2, p_c1, p_c2)


#Q7 the same as Q6
@repeat_1000s
def anti_coordination(r1c1 : tuple, r1c2: tuple, r2c1: tuple, r2c2: tuple, e = 0.99) -> tuple:
    player1 = Player(hh=r1c1[0], ht=r1c2[0], th=r2c1[0], tt=r2c2[0])
    player2 = Player(hh=r1c1[1], ht=r2c1[1], th=r1c2[1], tt=r2c2[1])
    player1_strategy_history = []
    player2_strategy_history = []
    for i in range(10000):
        s1 = player1.strategy()
        s2 = player2.strategy()
        player1_strategy_history.append(s1)
        player2_strategy_history.append(s2)
        player2.set_belief(s1)
        player1.set_belief(s2)
    p_r1 = player1_strategy_history.count(0) / float(len(player1_strategy_history))
    p_r2 = player1_strategy_history.count(1) / float(len(player1_strategy_history))
    p_c1 = player2_strategy_history.count(0) / float(len(player2_strategy_history))
    p_c2 = player2_strategy_history.count(1) / float(len(player2_strategy_history))

    return (p_r1, p_r2, p_c1, p_c2)


#Q8 one mix when h1= 9.8 t1= 6.6; h2= 5.2 t2= 8.8 result p1(0.6,0.4) p2(0.4,0.6)
@repeat_1000s
def battle_of_the_sexes(r1c1 : tuple, r1c2: tuple, r2c1: tuple, r2c2: tuple, e = 0.99) -> tuple:
    player1 = Player(hh=r1c1[0], ht=r1c2[0], th=r2c1[0], tt=r2c2[0])
    player2 = Player(hh=r1c1[1], ht=r2c1[1], th=r1c2[1], tt=r2c2[1])
    player1_strategy_history = []
    player2_strategy_history = []
    for i in range(10000):
        s1 = player1.strategy()
        s2 = player2.strategy()
        player1_strategy_history.append(s1)
        player2_strategy_history.append(s2)
        player2.set_belief(s1)
        player1.set_belief(s2)
    p_r1 = player1_strategy_history.count(0) / float(len(player1_strategy_history))
    p_r2 = player1_strategy_history.count(1) / float(len(player1_strategy_history))
    p_c1 = player2_strategy_history.count(0) / float(len(player2_strategy_history))
    p_c2 = player2_strategy_history.count(1) / float(len(player2_strategy_history))

    return (p_r1, p_r2, p_c1, p_c2)

#Q9
@repeat_1000s
def stag_hunt_game(r1c1 : tuple, r1c2: tuple, r2c1: tuple, r2c2: tuple, e = 0.99) -> tuple:
    player1 = Player(hh=r1c1[0], ht=r1c2[0], th=r2c1[0], tt=r2c2[0])
    player2 = Player(hh=r1c1[1], ht=r2c1[1], th=r1c2[1], tt=r2c2[1])
    player1_strategy_history = []
    player2_strategy_history = []
    for i in range(10000):
        s1 = player1.strategy()
        s2 = player2.strategy()
        player1_strategy_history.append(s1)
        player2_strategy_history.append(s2)
        player2.set_belief(s1)
        player1.set_belief(s2)
    p_r1 = player1_strategy_history.count(0) / float(len(player1_strategy_history))
    p_r2 = player1_strategy_history.count(1) / float(len(player1_strategy_history))
    p_c1 = player2_strategy_history.count(0) / float(len(player2_strategy_history))
    p_c2 = player2_strategy_history.count(1) / float(len(player2_strategy_history))

    return (p_r1, p_r2, p_c1, p_c2)












print(f"Q1 result:")
res1 = pure_strategy_NE((-1,-1), (1,0), (0,1), (3,3))
print(f"Q2 result:")
res2 = more_pure_strategy_NE((2,2), (1,0), (0,1), (3,3))
print(f"Q3 result:")
res3 = more_pure_strategy_NE((1,1), (0,0), (0,0), (0,0))
print(f"Q4 result:")
res4 = mixed_strategy_NE((0,1), (2,0), (2,0), (0,4))
print(f"Q5 result:")
res5 = best_reply_path((0,1), (1,0), (1,0), (0,1))
print(f"Q6 result:")
res6 = pure_coordination((10,10), (0,0), (0,0), (10,10))
print(f"Q7 result:")
res7 = anti_coordination((0,0), (1,1), (1,1), (0,0))
print(f"Q8 result:")
res8 = battle_of_the_sexes((3,2), (0,0), (0,0), (2,3))
print(f"Q9 result:")
res9 = stag_hunt_game((3,3), (0,2), (2,0), (1,1))




