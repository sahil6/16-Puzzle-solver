#!/bin/env python3
# solver16.py : Circular 16 Puzzle solver
# Based on skeleton code by D. Crandall, September 2018

import sys
import itertools

try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q



# shift a specified row left (-1) or right (1)
def shift_row(state, row, dir):
    change_row = state[(row * 4):(row * 4 + 4)]
    return (state[:(row * 4)] + change_row[-dir:] + change_row[:-dir] + state[(row * 4 + 4):],
            ("L" if dir == -1 else "R") + str(row + 1))


# shift a specified col up (1) or down (-1)
def shift_col(state, col, dir):
    change_col = state[col::4]
    s = list(state)
    s[col::4] = change_col[-dir:] + change_col[:-dir]
    return (tuple(s), ("U" if dir == -1 else "D") + str(col + 1))


# pretty-print board state
def print_board(row):
    for j in range(0, 16, 4):
        print('%3d %3d %3d %3d' % (row[j:(j + 4)]))


# return a list of possible successor states
def successors(state):
    return [shift_row(state, i, d) for i in range(0, 4) for d in (1, -1)] + [shift_col(state, i, d) for i in range(0, 4)
                                                                             for d in (1, -1)]


# check if we've reached the goal
def is_goal(state):
    return sorted(state) == list(state)


# This heuristic is based on the number of misplaced tiles
# Heuristic function, h = misplaced tiles/4 because one move can correct 4 positions. Therefore for the heuristic to be
# admissible(it can never overestimate) we divide it by 4 here
def misplaced(current_successor):
    heuristic = [b for a, b in
                 itertools.zip_longest(current_successor, sorted(current_successor), fillvalue=object()) if
                 a != b]
    return len(heuristic)/4


# positions of blocks in the final goal state
actual_positions = {1:(0, 0), 2:(0, 1), 3:(0, 2), 4:(0, 3), 5:(1, 0), 6:(1, 1), 7:(1, 2), 8:(1, 3),
                    9:(2, 0), 10:(2, 1), 11:(2, 2),12:(2,3), 13:(3,0), 14:(3,1), 15:(3,2), 16:(3,3)}


# This heuristic is based on the manhattan distance of tiles from their final position
# This is divided by 6 because each move from the final position offsets the manhattan distance by 6.
# Therefore manhattan distance needs to be divided by 6 to make it admissible

def manhattan(s):
    global dist
    final_dist = 0
    for index in range(0, 16):
        val = s[index]
        temp=actual_positions[val]
        k=temp[0]
        l=temp[1]
        i = int(index/4)
        j = int(index%4)
        dist = abs(k-i)+abs(l-j)
        final_dist += dist
    return float(final_dist/6)


# The solver!
# I've used 3 different heuristics. 1 is based on the h function is 0(uniform cost search)
# The user can uncomment and compare the efficiency of each heuristic on the final result

def solve(initial_board):
    fringe = Q.PriorityQueue()
    fringe.put((0, [initial_board, ""]))

    while not fringe.empty():
        result = fringe.get()
        # print('res:',result[0], result[1])
        (state, route_so_far) = result[1]
        for (succ, move) in successors(state):
            # print('succ',succ)
            if is_goal(succ):
                return route_so_far + " " + move
            # fringe.put((misplaced(succ) + (len(route_so_far + " " + move)) / 3, [succ, route_so_far + " " + move]))
            fringe.put((manhattan(succ)+ (len(route_so_far + " " + move))/3, [succ, route_so_far + " " + move]))
            # fringe.put(((len(route_so_far + " " + move))/3, [succ, route_so_far + " " + move]))

    return False



# test cases
start_state = []
with open(sys.argv[1], 'r') as file:
    for line in file:
        start_state += [int(i) for i in line.split()]

if len(start_state) != 16:
    print("Error: couldn't parse start state file")

print("Start state: ")
print_board(tuple(start_state))

print("Solving...")
route = solve(tuple(start_state))

print("Solution found in " + str(len(route) / 3) + " moves:" + "\n" + route)
