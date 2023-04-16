# Snake-by-usig-regresion
solving Snake by using regresion concept


History:

Snake’s story begins long before it found a mass audience with Nokia. It was first created as a concept in 1976 under the name of Blockage, and was a monochromatic two-player arcade game developed by video games company, Gremlin Interactive.


Environment Representation

The key idea is to represent the full state of the environment as a single tensor. In fact, multiple environments are represented as multiple 3d tensor as follow:

![image](https://user-images.githubusercontent.com/47190471/232274614-be299b69-3b9b-40b2-8d51-3b50fe4167cd.png)


After representing game environment, we have to implement the gameplay. The first trick is that we can move the position of all snake head and body by using 2D convolution with a hand-crafted filter as bellow.

![image](https://user-images.githubusercontent.com/47190471/232274631-1d18d745-2cdc-41e4-b58e-8aa526e775d3.png)


Learning Game

	We have chosen a linear representation for snake as V:V(x)= W^T x
	 [distance to obstacle, distance to boarders, length of snake, distance to food, is it final move which leads to hit to obstacle, is it final move which leads to hit to boarder] have been chosen as features to represent our environment.
	A function that shows current state is terminate or non-terminate state has been developed which return -1000 in case it is terminate state otherwise it returns 0.
	After any movement weights are being updated based on gradient descent roll.

w_i= w_i-alpha*( V_train (s_t )  -  V(s_t )  ).x_i

	Go to state 3



![image](https://user-images.githubusercontent.com/47190471/232274660-9b054aca-96c1-4598-a18d-a21936149870.png)


## note that

This game is depended on the features which we used to learn.
