#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May  3 01:36:01 2018

@author: Iswariya Manivannan
"""

import sys
import os
import time


def maze_map_to_tree(maze_map):
    """Function to create a tree from the map file. The idea is
    to check for the possible movements from each position on the
    map and encode it in a data structure like list.

    Parameters
    ----------
    maze_map : Sequence[str]
        A list of lines read from the map file

    Returns
    -------
    Sequence[int]
        tree with every possible movements from each position
    """
    #intializing tree
    tree = list()
    #obstacles in the map
    obstacle = ['|','=']

    for x in range(1,len(maze_map)-1):
        for y in range(1,len(maze_map[0])-1):
            #current node
            node = [x,y]
            #nodes in left, right, up & down of current node
            all_nodes = [[x-1, y], [x+1, y], [x, y-1], [x, y+1]]
            valid_nodes = list()
            for n in all_nodes:
                #getting content in the cell
                cell_value = maze_map[n[0]][n[1]]
                #ignoring cell with obstacle
                if cell_value not in obstacle:
                    #possible movements from current position
                    valid_nodes.append(n)
            #branch of tree with current position and possible movement 
            tree.append([node,valid_nodes])
    #returing resultant tree
    return tree

def assign_character_for_nodes(search_map, current_node, queue):
    """Function to assign character for the visited nodes. Please assign
    meaningful characters based on the direction of tree traversal.

    Parameters
    ----------
    search_map : Sequence[str]
        A list of lines from search map
    current_node : [int,int]
        current node position for which character has to be assigned
    queue :  Sequence[int]
        queue which contains (parent,child) nodes

    Returns
    -------
    Sequence[str]
        map with character assigned for current node
    """
    x0,y0 = current_node   #current

    for entry in queue:
        if entry[1] == current_node:
            #parent node of current node
            prev_node1 = entry[0] 
    
    if prev_node1 != "":
        x1,y1 = prev_node1  #previous

        for entry in queue:
            if entry[1] == prev_node1:
                #parent node of prev_node1
                prev_node2 = entry[0]

        if prev_node2 != "":
            x2,y2 = prev_node2   #previous to previous
            
            #right to left or left to right
            if   (x2 - x1 ==  0) and (x1 - x0 ==  0):
                character = "\u2574"

            #up to down or down to up
            elif (y2 - y1 ==  0) and (y1 - y0 ==  0):
                character = "\u2575"

            #left to down or down to left
            elif ((y2 - y1 == -1) and (x1 - x0 == -1)) or ((x2 - x1 ==  1) and (y1 - y0 ==  1)):
                character = "\u2510"

            #right to up or up to right
            elif ((x2 - x1 == -1) and (y1 - y0 == -1)) or ((y2 - y1 ==  1) and (x1 - x0 ==  1)):
                character = "\u2514"
        
            #right to down or down to right 
            elif ((y2 - y1 ==  1) and (x1 - x0 == -1)) or ((x2 - x1 ==  1) and (y1 - y0 == -1)):
                character = "\u250C"

            #left to up or up to left
            elif ((x2 - x1 == -1) and (y1 - y0 ==  1)) or ((y2 - y1 == -1) and (x1 - x0 ==  1)):
                character = "\u2518"
        
            assign_character(search_map,(x1,y1),character)

        #short horizontal
        if   (x1 - x0 ==  0) :      
            character = "\u2574"  
        #short vertical  
        elif (y1 - y0 ==  0) :
            character = "\u2575"
    
        assign_character(search_map,(x0,y0),character)

    if True :
        for line in search_map:
            print (line)

        time.sleep(0.03)

    #returing resultant map
    return search_map

def write_to_file(file_name, path):
    """Function to write output to console and the optimal path
    from start to each goal to txt file.
    Please ensure that it should ALSO be possible to visualize each and every
    step of the tree traversal algorithm in the map in the console.
    This enables understanding towards the working of your
    tree traversal algorithm as to how it reaches the goals.

    Parameters
    ----------
    filen_name : string
        This parameter defines the name of the txt file.
    path : Sequence[str]
        path map from start position to one of the goal position

    """
    working_directory = os.getcwd()
    
    #results directory
    map_directory = 'results/'

    #joining file path
    file_path = os.path.join(working_directory, map_directory + file_name +".txt")

    f = open(file_path, "a") #append mode

    #checking that path is not empty
    if path != None:
        #writing path to file
        for line in path:
            f.write(line)
    f.close()

def get_cell_pos(maze_map,cell_val):
    """Function to get position of cell in the map which 
    contains given value. used to find start position
    and goal positions

    Parameters
    ----------
    maze_map : Sequence[str]
        A list of lines read from map file
    cell_val : char
        character/value for which position needs to be found

    Returns
    -------
    Sequence[int]
        index or list of indices (position) of cells
    """
    cell_pos = list()
    for row,x in zip(maze_map,range(len(maze_map))) :
        for cell,y in zip(row,range(len(row))):
            if cell == cell_val:
                cell_pos.append([x,y])
    #cell_pos = [[maze_map.index(row),row.index(cell)] for row in maze_map for cell in row if cell == cell_val]  
    return cell_pos

def assign_character(map,position,character):
    """Function to assign a character in the given 
    position of the given map 

    Parameters
    ----------
    maze_map : Sequence[str]
        A list of lines from map
    position : [int,int]
        position in which character has to be assigned
    character: char
        character which has to written inside the map

    Returns
    -------
    Sequence[str]
        map with character assigned
    """
    #unpacking
    x,y = position[0],position[1]

    #replacing character in a string
    map[x] = map[x][:y] + character + map[x][y+1:]

    #returing resultant map
    return map

def create_pathmap(maze_map, path):
    """Function to create path map from start to goal.

    Parameters
    ----------
    maze_map : Sequence[str]
        A list of lines from search map
    path : Sequence[int]
        A list of positions which forms the path from start to goal

    Returns
    -------
    Sequence[str]
       path map from start position to one of the goal position
    """
    path_map = maze_map[:]
    for i in range(1, len(path)-1):
       
        cx,cy = path[i]     #current
        px,py = path[i-1]   #previous
        nx,ny = path[i+1]   #next

        #right to left or left to right
        if   (px - cx ==  0) and (cx - nx ==  0):
            character = "\u2500"

        #up to down or down to up
        elif (py - cy ==  0) and (cy - ny ==  0):
            character = "\u2502"

        #left to down or down to left
        elif ((py - cy == -1) and (cx - nx == -1)) or ((px - cx ==  1) and (cy - ny ==  1)):
            character = "\u2510"

        #right to up or up to right
        elif ((px - cx == -1) and (cy - ny == -1)) or ((py - cy ==  1) and (cx - nx ==  1)):
            character = "\u2514"
        
        #right to down or down to right 
        elif ((py - cy ==  1) and (cx - nx == -1)) or ((px - cx ==  1) and (cy - ny == -1)):
            character = "\u250C"

        #left to up or up to left
        elif ((px - cx == -1) and (cy - ny ==  1)) or ((py - cy == -1) and (cx - nx ==  1)):
            character = "\u2518"

        else:
            character = "@" #unknown
        
        #write character in the map
        assign_character(path_map,(cx,cy),character)
    #Goal position
    x,y = path[-1]
    assign_character(path_map,(x,y),"X")
    assign_character(maze_map,(x,y),"X")
    #returning resultant map
    return path_map