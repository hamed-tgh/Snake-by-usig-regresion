# -*- coding: utf-8 -*-
"""
Created on Sun May  1 15:14:48 2022

@author: Hamed
"""



import numpy as np
import random
import cv2
from scipy.spatial.distance import cdist
from scipy.spatial import distance
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt

# use a 2D convolution to move a movement.
def apply_filter(head_mask , kernel1 , body_mask):
    head_mask = cv2.filter2D(src=head_mask, ddepth=-1, kernel=kernel1)
    body_non_ones = np.where(body_mask != 0)
    body_mask[body_non_ones] -= 1    
    body_mask[np.where(head_mask == 1)] = np.max(body_mask)+1
    return head_mask , body_mask
    

# create up,down,left,right filter. 
def Return_movment_filters():
    right = np.zeros([3,3])
    right[1,0] = 1
    
    left = np.zeros([3,3])
    left[1,2] = 1
    
    up = np.zeros([3,3])
    up[2,1] = 1
    
    down = np.zeros([3,3])
    down[0,1] = 1     
    return right,left,up,down

# create initial enviroment
def create_state():
    # creating obstacle tensor
    obstacle = np.zeros([20,20])
    obstacle[0 , : ] = 1
    obstacle[: , 0 ] = 1
    obstacle[: , -1 ] = 1
    obstacle[-1 , :] = 1
    for i in range(4):
        rnd = np.random.randint(3,17,2)
        obstacle[rnd[0]-1 : rnd[0]+1 , rnd[1]-1 : rnd[1]+1] = 2
    
    
    #creaate head tensor
    head = np.zeros([20,20])
    while(True):
        a = random.randint(4, 16)
        b = random.randint(4, 16)
        temp = obstacle[b , a] 
        if( 1 != temp ):
            head[ a , b ] = 1
            break
        
    #Create body tensor
    body = np.zeros([20,20])
    index_head = np.where(head == 1)
    body[index_head] = 3
    count = 2
    if 1 not in (obstacle[int(index_head[0] -2) :int(index_head[0]) , index_head[1] ]):
        for i in range(1,3):
            body[index_head[0] - i , index_head[1]] =  count
            count-=1
    elif 1 not in (obstacle[int(index_head[0]):int(index_head[0]+2) , index_head[1] ]):
        for i in range(1,3):
            body[index_head[0] + i , index_head[1]] =  count
            count-=1
            
    elif 1 not in (obstacle[index_head[0] , int(index_head[1]):int(index_head[1]+2) ]):
        for i in range(1,3):
            body[index_head[0]  , index_head[1] + i] =  count
            count-=1
    elif 1 not in (obstacle[int(index_head[0]) , int(index_head[1]-2):int(index_head[1]) ]):
        for i in range(1,3):
            body[index_head[0]  , index_head[1] - i] =  count
            count-=1
    
    #locate food
    temp_food = np.zeros([20,20])
    temp_food[np.where(body !=  0 )] = 1
    temp_food[np.where(obstacle !=  0 )] = 1
    index_not_obstacle = np.where(temp_food == 0 )
    for i in range(1):
        rnd = random.randint(0, len(index_not_obstacle[0]) -1)
        obstacle[index_not_obstacle[0][rnd] , index_not_obstacle[1][rnd] ] = 3 
        
     
    return obstacle, body ,  head





#check its terminate state    
def check_status(body , obstacle , head):
    if( len((np.where(head * obstacle >= 1))[0]) >= 1 ):
        return -1000        
    temp_body = np.zeros(body.shape)
    temp_body[np.where(body != 0)] = 1
    if (len((np.where(temp_body * obstacle >= 1))[0]) > 1):
        return -1000
    temp_body[np.where(body == np.max(body))] = 0
    if( len(np.where((head * temp_body) != 0)[0]) >= 1  ):
        return -1000
    return 0
    

#evaluate a state
def check_columns(head, body , obstacle , food_count , option):
    #length of snake
    value = []
    body_one = len(list(np.where(body != 0)[0]))
    value.append( body_one)

    #distance to bondry 
    row,column = np.where(head ==1)
    a,b = np.where(obstacle == 1) # get rows and columns where vlue is less than 42.5
    x = zip(a,b) # create a list with (row,column)
    b = np.array([a , b ])
    a = np.array([[row,column]])
    dist = 87976
    dist2 = - 500
    for i in range(b.shape[1]):
        temp = b[:,i]
        temp = np.reshape(temp , (2, 1))
        d = np.sqrt(np.sum(np.square(np.array([row,column])-temp)))
        if d < dist:
            dist = d
    value.append(dist)
    
    
    #distance to obstacles
    row,column = np.where(head ==1)
    a,b = np.where(obstacle == 2) 
    x = zip(a,b)
    b = np.array([a , b ])
    a = np.array([[row,column]])
    dist = 87976
    for i in range(b.shape[1]):
        temp = b[:,i]
        temp = np.reshape(temp , (2, 1))
        d = np.sqrt(np.sum(np.square(np.array([row,column])-temp)))
        if d < dist:
            dist = d
    
    value.append(dist)
    
    #distamce to food
    row,column = np.where(head ==1)
    a,b = np.where(obstacle == 3) 
    x = zip(a,b)
    b = np.array([a , b ])
    a = np.array([[row,column]])
    dist = 87976
    for i in range(b.shape[1]):
        temp = b[:,i]
        temp = np.reshape(temp , (2, 1))
        d = np.sqrt(np.sum(np.square(np.array([row,column])-temp)))
        if d < dist:
            dist = d

    value.append(dist)
    
    if(value[1] == 0):
        value.append(10)
    else:
        value.append(0)
    
    if(value[2] == 0):
        value.append(10)
    else:
        value.append(0)
    
    
    return value
    
    
    
    
    
#return correct movement
def correct_movment(body):
    movemnt = []
    movemnt_name = []
    right,left,up,down  = Return_movment_filters()
    index_head = np.where(body == np.max(body))
    if (body[int(index_head[0] -1) , index_head[1] ] == 0 ):
        movemnt.append(up)
        movemnt_name.append('up')
    if (body[int(index_head[0] +1) , index_head[1] ] == 0 ):
        movemnt.append(down)
        movemnt_name.append('down')
    if (body[index_head[0] , int(index_head[1]-1)] == 0 ):
        movemnt.append(left)
        movemnt_name.append('left')

    if (body[index_head[0] , int(index_head[1] +1)] == 0 ):
        movemnt.append(right)
        movemnt_name.append('right')

    return movemnt , movemnt_name
    
    
    

        
    
    

import copy

if __name__ == "__main__" :
    

    dim = 20
    food_count = 0 
    obstacle, body ,  head = create_state()
    w = np.load('Weight.npy')
    option = 0
    for i in range(1 , 200):
        # option = 0
            
        operation , movemnt_name = correct_movment(body)
        max_value = -800
        max_index = 0
        for j in range(len(operation)):     
            # dir = directions[i]
                
            head_temp , body_temp = apply_filter(copy.copy(head) , operation[j]
                                                 , copy.copy(body))
            value = check_columns(head_temp, body_temp , obstacle , food_count,
                                  option)         
            if (np.dot(w,value) > max_value):
                max_value = np.dot(w,value)
                max_index = j
                movment = movemnt_name[j]
            
        head , body = apply_filter(copy.copy(head) , operation[max_index]
                                             , copy.copy(body))
        # print(movment)
        food = np.zeros([20,20])
        food[np.where(obstacle == 3)] = 1
        if (len(np.where((head * food) != 0 )[0]) > 0):
            # body[np.where(body!=0)] -= 1
            # body[np.where(obstacle == 3)] = np.max(body)+2
            food_loc = np.where(obstacle == 3 )
            if body[int(food_loc[0]) ,int(food_loc[1]-1) ] == 0:
                body[int(food_loc[0]) ,int(food_loc[1]-1) ] = np.max(body)+1
                head = np.zeros([20,20])
                head[int(food_loc[0]) ,int(food_loc[1]-1) ] = 1
            else:
                body[int(food_loc[0]) ,int(food_loc[1]+1) ] = np.max(body)+1
                head = np.zeros([20,20])
                head[int(food_loc[0]) ,int(food_loc[1]+1) ] = 1
            
            # head[np.where(obstacle == 3)] = 1 
            obstacle[np.where(obstacle == 3)] = 0 
            #reposition food
            temp_food = np.zeros([20,20])
            # temp_food[np.where(body ==  0 )] = 1
            temp_food[np.where(obstacle ==  0 )] = 1
            temp_food[np.where(body !=  0 )] = 0
            index_not_obstacle = np.where(temp_food == 1 )
            rnd = random.randint(0, len(index_not_obstacle[0])-1)
            obstacle[index_not_obstacle[0][rnd] , index_not_obstacle[1][rnd] ] = 3
            food_count +=1
            print('length of snake: ' , value[0]+1)
        



        # 
        game_value = check_status(body, obstacle, head)
        board_value = check_columns(head, body, obstacle , food_count , option)
        # w = w - alpha * ( np.dot(w , board_value) - game_value) * board_value
        if option == 40:
            obstacle, body ,  head = create_state()
        if game_value == -1000:
            obstacle, body ,  head = create_state()
            # w = w - (alpha * (np.dot(w , board_value) - game_value)) * board_value
            print("LOST")
            # print(board_value)
            option = 0
        else:
            option+=1
            
                    
        
        Total_boards =np.zeros([20,20])
        Total_boards[np.where(obstacle == 1)] = 1
        Total_boards[np.where(obstacle == 2)] = 1
        Total_boards[np.where(obstacle == 3)] = 2
        
        Total_boards[np.where(body !=  0)] =  3
        plt.pcolor(np.arange(-0.5, dim), np.arange(-0.5, dim), Total_boards, cmap=ListedColormap(['crimson', 'turquoise' , 'orange']))
        plt.show()
        if (i % 200 == 0 ):
            True
            # alpha *= 0.1
        # plt.close()
       
    # np.save("Weight.npy" , w)
        
            
        
               
        
        
        
        
        
        
        
        