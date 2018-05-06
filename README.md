# Flappybird-Qlearning
Extension of Sarvagya Vaish (2014), Cihan Ceyhan’s (2017) and Tony Poerio’s (2016) Flappy Bird Q learning implementations. 

Ceyhan, C., Flappybird-qlearning-bot, (2017), GitHub repository, https://github.com/chncyhn/flappybird-qlearning-bot<br />
Poerio, T., Flappy-AI, (2016), GitHub repository, https://github.com/adpoe/Flappy-AI<br />
Sarvagya V., FlapPyBird, (2014), GitHub repository, https://github.com/SarvagyaVaish/FlappyBirdRL

<br />
<br />


### Abstract
This project attempts to apply a standard Q-Learning algorithm to a Flappy Bird playing agent. 
The agent was demonstrated to successfully learn to play the game at a superhuman level following a pure-greedy. 
Modular adjustments were made to the learning rate to investigate whether a decay scheduler would improve performance.


# METHODOLOGY
Libraries and Contributors
The infrastructure for this project consisted of using the PyGame library, as well as pre-built Flappy Bird environment to which the agent would send commands (Sourabh, 2014). This project was inspired by Sarvagya Vaish’s (2014) outline of a Flappy Bird playing agent, with parts of the code used from Cihan Ceyhan’s (2017) and Tony Poerio’s (2016) Flappy Bird implementation. 

## Domain
The agent’s goal is to navigate through narrow gaps between side-scrolling (constant-rate) obstacles. At any state, one of two actions can be performed: jump or do nothing. During gameplay, each frame is evaluated to determine whether the agent is alive or dead, where it rewards or punishes the agent respectively. The maximum runnable frames-per-second speed is 580 FPS, equating to approximately 5 hours of gameplay to reach 7000 episodes. This speed constraint was the bottleneck during experimentation and parameter tuning.
One of the main technical obstacles with a game like Flappy Bird is the mapping of continuous states to a discretized Q-matrix. There are three continuous variables that the agent measures: horizontal difference between the sprite and end of the upcoming pipe (0 to 480), vertical difference between the sprite and lower pipe (0 to 720), and vertical velocity (-10 to 10). To combat this, a reasonable strategy is to bin these continuous distances. Without binning, the Q-matrix would consist of 6,912,000 states. Unless stated otherwise, the vertical and horizontal distances of this agent were binned by 10 (i.e., {0, 10, … 720}, {0, 10, … 480}). No binning was applied

## Policy and Epislon

Given the nature of this task, there is a very narrow window of rewarding actions the agent can take. When comparing epsilon-greedy and pure greedy policies, it was found that pure greedy policy (epsilon=0) would outperform in all cases (other parameters: alpha=0.8, discount=0.9).
Beyond the initial learning phase, where the largest distance exists between the agent and the upcoming pipe, an exploring element is not advantageous. Instead, in later iterations it is likely a hindrance to convergence as most deaths occur due to inappropriate jumping or straying from the narrow, acceptable path between the two pipe gaps. However, a rapidly decaying epsilon (time-based) may prove beneficial during the early learning stages, before the agent encounters the first pipe. Unfortunately, due to the rapid state evaluation that occurs every 60ms, even a small epsilon value (e.g., 0.001) would prompt the agent to engage in random behaviour more than intended, consequently “overinflating” the epsilon value during the episodes. This difficulty was also observed in past implementations (Quinn & Reis, 2017).
A comparable solution to increase learning during early, pre-pipe stages would be to implement a learning rate scheduler where the learning rate would be very high up until the first pipe was cleared, and then decrease at some predetermined rate or step. This is later implemented, comparing different decay scheduler performances versus maintaining a constant learning rate.

## Reward Function
During every gametick, the agent would take record of its current state, as well as whether it is alive or dead. A reward function of +1 or -1000 was applied for each respective outcome. It is important to maintain a high negative reward for death as that indicates a “game over”, and there is no other reward beyond this point. For example, if the negative reward yielded -10pts; given the proper exploratory parameters, the agent may explore the possibility that incurring this small penalty may yield to a far greater, consistent stream of points later on. This is obviously not the case as the game conditions and states of Flappy Bird are deterministic.
Furthermore, due to the pipe obstacles being generated randomly, planning for future events is impossible beyond a short horizon. For this reason, a discount rate of 0.9 was selected for most instances.

## State transition function
In total, there exists 72051 possible states. Horizontal movement is constant as the screen scrolls from right to left as the game progresses, hence the agent has no choice regarding horizontal movement. At the moment an agent chooses to jump, the vertical velocity reaches 10, meaning the next state the agent will enter will be 10px higher than the previous (-10px to 0px). Had the agent done nothing, the next state will be a maximum of 10px below the previous state. The default downward acceleration rate (gravity) is 5, meaning that every gametick (60ms), the agents vertical velocity will decrease by 5.

## Q-Matrix
Due to the large number of states (72051), it is impractical to enumerate the full Q-matrix here. As mentioned earlier, to reduce the number of states binning was applied in buckets of 10 for horizontal and vertical distances. The Q-matrix was stored in a dictionary variable where each key corresponds to one possible combination of velocity and horizontal and vertical distances. Below is an illustration of how a typical learning cycle follows and how states are conceptualized:
Figure 1: A typical learning cycle and an illustration of the Q-matrix states.
While the state space is vast, the constant decrease in horizontal distance (xdiff) due to the side-scrolling nature of the game makes it easier to conceptualize state transition options. Every gametick, the agent progresses forward 10 pixels towards the upcoming pipe, during which the state is observed to determine whether the agent is alive or dead. The agent then has the two options (jump or do nothing) that will increase ydiff by 10 (maximum upward velocity) or decrease it according to the current negative velocity. A list of actions (history) is recorded as well as the corresponding states. It is only after the agent has died that the Q-matrix is updated using this list. The update equation is the standard Q-learning algorithm:


![Standard Q-Learning Equation](https://imgur.com/fgt2Pgr.jpg)


## Learning-rate Decay Scheduler
It is intuitive to have the agent take larger leaps during the early learning process, whereas in later episodes to make smaller changes to learned behaviours. In an attempt to facilitate this, a decay scheduler was implemented that would decrease the learning rate at some rate as episode count increases. Two main decay schedules were examined: fixed and step-wise. Fixed decay would result in a decrease of 0.15 in learning rate every 1000 episodes, whereas step-wise would halve the learning rate every 1000 episodes (similar to exponential, albeit less continuously updated).
