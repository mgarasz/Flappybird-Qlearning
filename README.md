# Flappybird-Qlearning
Extension of Sarvagya Vaish (2014), Cihan Ceyhan’s (2017) and Tony Poerio’s (2016) Flappy Bird Q learning implementations. 

Ceyhan, C., Flappybird-qlearning-bot, (2017), GitHub repository, https://github.com/chncyhn/flappybird-qlearning-bot<br />
Poerio, T., Flappy-AI, (2016), GitHub repository, https://github.com/adpoe/Flappy-AI<br />
Sarvagya V., FlapPyBird, (2014), GitHub repository, https://github.com/SarvagyaVaish/FlappyBirdRL

<br />
<br />


# Abstract
This project attempts to apply a standard Q-Learning algorithm to a Flappy Bird playing agent. 
The agent was demonstrated to successfully learn to play the game at a superhuman level following a pure-greedy. 
Modular adjustments were made to the learning rate to investigate whether a decay scheduler would improve performance.

## Policy and Epislon

Given the nature of this task, there is a very narrow window of rewarding actions the agent can take. When comparing epsilon-greedy and pure greedy policies, it was found that pure greedy policy (epsilon=0) would outperform in all cases (other parameters: alpha=0.8, discount=0.9).
Beyond the initial learning phase, where the largest distance exists between the agent and the upcoming pipe, an exploring element is not advantageous. Instead, in later iterations it is likely a hindrance to convergence as most deaths occur due to inappropriate jumping or straying from the narrow, acceptable path between the two pipe gaps. However, a rapidly decaying epsilon (time-based) may prove beneficial during the early learning stages, before the agent encounters the first pipe. Unfortunately, due to the rapid state evaluation that occurs every 60ms, even a small epsilon value (e.g., 0.001) would prompt the agent to engage in random behaviour more than intended, consequently “overinflating” the epsilon value during the episodes. This difficulty was also observed in past implementations (Quinn & Reis, 2017).
A comparable solution to increase learning during early, pre-pipe stages would be to implement a learning rate scheduler where the learning rate would be very high up until the first pipe was cleared, and then decrease at some predetermined rate or step. This is later implemented, comparing different decay scheduler performances versus maintaining a constant learning rate.

## Learning-rate Decay Scheduler
It is intuitive to have the agent take larger leaps during the early learning process, whereas in later episodes to make smaller changes to learned behaviours. In an attempt to facilitate this, a decay scheduler was implemented that would decrease the learning rate at some rate as episode count increases. Two main decay schedules were examined: fixed and step-wise. Fixed decay would result in a decrease of 0.15 in learning rate every 1000 episodes, whereas step-wise would halve the learning rate every 1000 episodes (similar to exponential, albeit less continuously updated).
