# -*- coding: utf-8 -*-
"""
Created on Wed Mar 28 14:48:36 2018
"""

import numpy as np 
import random
import math


class Agent(object):

    def __init__(self):
        
        """ Tunable Parameters """ 
        self.discount = 1.0 
        self.reward = {0: 1, 1: -1000} # Reward function, 0 = alive, 1 = dead
        self.initial_lr = 0.8 #learning rate
        self.epsilon = 0.0
        self.decay_type = 0 #Acceptable values: 'step', 'exp', 0. 0 means no decay.
        
        """ Everything else """ 
        self.episode = 0 # Game count of current run, incremented after every death
        self.q_mat()
        self.current_lr = self.initial_lr
        self.last_state = "420_240_0" #start point, center of screen
        self.last_action = 0
        self.moves = [] 
        
    def random_gen(self):
        #Used for exploring, made as a seperate function as a hotfix for bug
        return random.random()
    
    def LR_decay(self):
        
        if self.decay_type == 0:
            self.current_lr = self.initial_lr
            return self.current_lr
        
        elif self.decay_type == 'step': 
            """Tunable hyperparameters"""
            drop = 0.5 #lr decay rate (0.5 = halves every N epoch drops) #tunable
            ep_drop = 1000 #half every 1000 episodes (1 epoch = 20 episodes)
            min_acceptable_lr = 0.09
            self.current_lr = self.initial_lr * math.pow(drop,  
                                               math.floor((1+self.episode)/ep_drop))
        
            if self.current_lr < min_acceptable_lr:
                self.current_lr = min_acceptable_lr #creates a floor
                return self.current_lr
            
            return self.current_lr
        
        elif self.decay_type == 'exp':
            """Tunable hyperparameter"""
            k = 0.0001 #tunable hyperparameter, determines how steep the decay is
            self.current_lr = self.current_lr * math.exp(-k*self.episode)
            
            return self.current_lr
            
            if self.current_lr < min_acceptable_lr:
                self.current_lr = min_acceptable_lr #creates a floor
                return self.current_lr
    
    def q_mat(self):
        
        qval = {}
        self.bucket = 10 #tunable, so long as its divisible by 5.
        for x in list(range(-40,421,self.bucket)): #x-axis distance from center of pipe
            for y in list(range(-300,421,self.bucket)): #y-axis distance from top of pipe
                for v in range(-10,11):  #vertical velocity
                    qval[str(x)+'_'+str(y)+'_'+str(v)] = [0,0]       #keys
        
        self.qvalues = qval
        
        return self.qvalues
    
    
    def map_state(self, xdif, ydif, vel):
        #maps state to buckets
        
        xdif = min(list(range(-40,421,self.bucket)), key=lambda x:abs(x-xdif))
        ydif = min(list(range(-300,421,self.bucket)), key=lambda x:abs(x-ydif))
    
        return str(int(xdif))+'_'+str(int(ydif))+'_'+str(vel)

        

    def act(self, xdif, ydif, vel):
        '''
        Chooses the best action wrt the current state - do nothing if tie
        '''
        state = self.map_state(xdif, ydif, vel)
        self.moves.append( [self.last_state, self.last_action, state] ) # Add the experience to the history
        self.last_state = state # Update the last_state with the current state
        rr = self.random_gen() 
        
        if self.epsilon >= rr: 
            print 'Random action taken.'
            random_action = np.random.choice([0,1])
            self.last_action = random_action
            return random_action
    
        elif self.qvalues[state][0] >= self.qvalues[state][1]:
            self.last_action = 0
            return 0
        else:
            self.last_action = 1
            return 1

    def get_last_state(self):
        return self.last_state

    def update_scores(self):
        '''
        Update qvalues by iterating over experiences
        '''
        history = list(reversed(self.moves))

        #Flag if the bird died in the top pipe
        high_death_flag = True if int(history[0][2].split('_')[1]) > 120 else False

        #Q-learning score updates
        t = 1
        for exp in history:
            state = exp[0]
            act = exp[1]
            res_state = exp[2]
            if t == 1 or t == 2:  #Q update
                self.qvalues[state][act] = (self.qvalues[state][act]) + (self.LR_decay()) * (( self.reward[1] + (self.discount)*max(self.qvalues[res_state]) - (self.qvalues[state][act])))
            
            elif high_death_flag and act:
                self.qvalues[state][act] = (self.qvalues[state][act]) + (self.LR_decay()) * (( self.reward[1] + (self.discount)*max(self.qvalues[res_state]) - (self.qvalues[state][act])))
                high_death_flag = False
            
            else:
                self.qvalues[state][act] = (self.qvalues[state][act]) + (self.LR_decay()) * (( self.reward[0] + (self.discount)*max(self.qvalues[res_state]) - (self.qvalues[state][act])))
            t += 1

        self.episode += 1 #increase episode count
        self.moves = []  #clear history after updating strategies



   
