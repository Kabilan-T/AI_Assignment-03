#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 21:15:04 2018

@author: Iswariya Manivannan
"""
import sys
import os
from collections import deque
from helper import maze_map_to_tree, write_to_file, assign_character_for_nodes, assign_character, create_pathmap, get_cell_pos


def breadth_first_search(maze_map, start_pos, goal_pos):
    """Function to implement the BFS algorithm.
    Please use the functions in helper.py to complete the algorithm.
    Please do not clutter the code this file by adding extra functions.
    Additional functions if required should be added in helper.py

    Parameters
    ----------
    maze_map : Sequence[str]
        A list of lines read from the map file
    start_pos : [int,int]
        position of cell which contains start value (s)
    goal_pos :  [int,int]
        position of cell which contains gaol value (*)

    Returns
    -------
    Sequence[str]
       path map from start position to one of the goal position
    """
    start = start_pos[0]
    goal = goal_pos
    queue = deque([("", start)])

    # Fill in your BFS algorithm here

    #tree with possible movements
    tree = maze_map_to_tree(maze_map)

    #search map for visualising
    search_map = maze_map[:]

    new_nodes = deque()
    visited_nodes  = list()

    #add start to new_nodes
    new_nodes.append(start)

    while len(new_nodes) != 0 :
        #FIFO method
        current_node = new_nodes.popleft()

        #goal reached condition
        if current_node == goal:
            path = list()
            while True:
                #appending path from goal to start
                path.append(current_node)
                if current_node == start:
                    break
                for entry in queue:
                    if entry[1] == current_node:
                        current_node = entry[0]
                        break
            #reversing goal to start path to get start to goal path       
            path = path[::-1]

            #create path map from path.
            path_map = create_pathmap(maze_map,path)

            #returning path map
            return path_map

        #possible_nodes
        for branch in tree:
            if branch[0] == current_node:
                possible_nodes = branch[1]
                break

        for node in possible_nodes:
            if node in visited_nodes:
                continue
            elif node not in new_nodes:

                #adding new nodes
                new_nodes.append(node)

                #queing parent and child node
                queue.append((current_node, node))

        #marking current node as visited
        visited_nodes.append(current_node)

        #visualizing search map
        for entry in queue:
            if entry[1] == current_node:
                #parent node of current node
                prev_node = entry[0] 
        if current_node != start:
            assign_character_for_nodes(search_map,current_node,prev_node)
        

    #if no path is available from start to goal    
    return None
    

if __name__ == '__main__':

    working_directory = os.getcwd()

    if len(sys.argv) > 1:
        map_directory = sys.argv[1]
    else:
        map_directory = 'maps'

    file_path_map1 = os.path.join(working_directory, map_directory + '/map1.txt')
    file_path_map2 = os.path.join(working_directory, map_directory + '/map2.txt')
    file_path_map3 = os.path.join(working_directory, map_directory + '/map3.txt')

    maze_map_map1 = []
    with open(file_path_map1) as f1:
        maze_map_map1 = f1.readlines()

    maze_map_map2 = []
    with open(file_path_map2) as f2:
        maze_map_map2 = f2.readlines()

    maze_map_map3 = []
    with open(file_path_map3) as f3:
        maze_map_map3 = f3.readlines()

    start_pos_map1 = get_cell_pos(maze_map_map1,'s')
    start_pos_map2 = get_cell_pos(maze_map_map2,'s')
    start_pos_map3 = get_cell_pos(maze_map_map3,'s')
    goals_pos_map1 = get_cell_pos(maze_map_map1,'*')
    goals_pos_map2 = get_cell_pos(maze_map_map2,'*')
    goals_pos_map3 = get_cell_pos(maze_map_map3,'*')
   
    # CALL THESE FUNCTIONS after filling in the necessary implementations
    
    for goal_pos_map1 in goals_pos_map1:
        path_map1 = breadth_first_search(maze_map_map1, start_pos_map1, goal_pos_map1)
        write_to_file("bfs_map1", path_map1)

    for goal_pos_map2 in goals_pos_map2:
        path_map2 = breadth_first_search(maze_map_map2, start_pos_map2, goal_pos_map2)
        write_to_file("bfs_map2", path_map2)

    for goal_pos_map3 in goals_pos_map3:
        path_map3 = breadth_first_search(maze_map_map3, start_pos_map3, goal_pos_map3)
        write_to_file("bfs_map3", path_map3)
