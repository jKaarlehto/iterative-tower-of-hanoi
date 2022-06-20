#base case: sum(stack3) == (discs/2)*(1+discs)
#algorithm:
#start from rightmost stack.

#1. step to next stack with discs
#2. pick up a disc 
#3. step to next stack
#4. inspect if disc can be placed
#       if true -> place disc and go to step 1. 
#       else -> step to next stack
#6. inspect if disc can be placed
#       if true -> place disc and go to step 1.
#       else -> go to step 1.
#even number of discs: step = positive
#odd number of discs: step = negative
from collections import deque
import math
import os
import time
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class disc_tower:
    steps = int()
    required_steps = int()
    state = list()
    discs = int()
    direction = int() 
    inspect_index = int()
    moving_disk_value = int()

    def __init__(self,discs:int):
        self.state = [deque([i for i in (range(1,discs+1))]),deque([]),deque([])]
        self.discs = discs
        self.direction = -1 if discs%2 != 0 else 1  
        self.inspect_index = 0
        self.steps = 0
        self.required_steps = (2**discs)-1



    def step(self):
        self.inspect_index = (self.inspect_index + 1*self.direction)%3
    def step_non_empty(self):
        self.step()
        while not (self.state[self.inspect_index]):
            self.step()
    def pick_up_disk(self):
        self.moving_disk_value = self.state[self.inspect_index][0]
        self.state[self.inspect_index].popleft()

    def can_be_placed(self) -> bool:
        if not self.state[self.inspect_index]:
            return True
        else:
            return (self.moving_disk_value < self.state[self.inspect_index][0])

    def place_disk(self):
        self.steps = self.steps + 1 
        self.state[self.inspect_index].appendleft(self.moving_disk_value)
        self.print_state()

    def is_solved(self):
        return (sum(self.state[-1]) == (self.discs/2)*(1+self.discs))
    
    def print_state(self):
        cls() 
        symbol_width = 2 
                 
        stack_width = self.discs*symbol_width

        total_render_lines = self.discs 
        for current_render_line in range(total_render_lines):
            for stack in self.state:
                stack_render_index = len(stack) - (total_render_lines - current_render_line) 
                stack_visible = stack_render_index >= 0

                if (stack_visible):
                    disc_symbols = stack[stack_render_index]*symbol_width
                    disc_symbol = "X" 
                else:
                    disc_symbols = 0 
                    disc_symbol = ""

                space_symbols = math.floor((stack_width - disc_symbols)/2)
                print(space_symbols*symbol_width*" ",end="") 
                print(disc_symbols*symbol_width*disc_symbol,end="")
                print(space_symbols*symbol_width*" ",end="")

            current_render_line += 1
            print("\n")

    @staticmethod
    def solve(disc_tower, speed):
        while not disc_tower.is_solved():
            time.sleep(1/speed)
            disc_tower.step_non_empty()
            disc_tower.pick_up_disk()
            disc_tower.step()

            if disc_tower.can_be_placed():
                disc_tower.place_disk()
                continue
            else:
                disc_tower.step()
            if disc_tower.can_be_placed():
                disc_tower.place_disk()
                continue
            else:
                disc_tower.step() 
                disc_tower.place_disk()
                disc_tower.steps = disc_tower.steps -1
                continue 
        disc_tower.print_state()
        print(" COMPLETED")
        print("TOTAL STEPS: ", disc_tower.steps)

size = int(input("Enter tower height: "))
game = disc_tower(size)
speed = int(input("Enter solving speed: "))
disc_tower.solve(game,speed)
