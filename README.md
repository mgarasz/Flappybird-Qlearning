# Flappybird Q-Learning with variable LR and tunable epsilon
Extension of Sarvagya Vaish (2014), Cihan Ceyhan’s (2017) and Tony Poerio’s (2016) Flappy Bird Q learning implementations. 

Ceyhan, C., Flappybird-qlearning-bot, (2017), GitHub repository, https://github.com/chncyhn/flappybird-qlearning-bot<br />
Poerio, T., Flappy-AI, (2016), GitHub repository, https://github.com/adpoe/Flappy-AI<br />
Sarvagya V., FlapPyBird, (2014), GitHub repository, https://github.com/SarvagyaVaish/FlappyBirdRL

<br />
<br />


### Abstract
This project attempts to apply a standard Q-Learning algorithm to a Flappy Bird playing agent. 
The agent was demonstrated to successfully learn to play the game at a superhuman level following a pure-greedy (e=0) policy. 
Modular adjustments were made to the learning rate to investigate whether a decay scheduler would improve performance.


# METHODOLOGY
## Libraries and Contributors
The infrastructure for this project consisted of using the PyGame library, as well as pre-built Flappy Bird environment to which the agent would send commands (Sourabh, 2014). This project was inspired by Sarvagya Vaish’s (2014) outline of a Flappy Bird playing agent, with parts of the code used from Cihan Ceyhan’s (2017) and Tony Poerio’s (2016) Flappy Bird implementation. 

## Domain
The agent’s goal is to navigate through narrow gaps between side-scrolling (constant-rate) obstacles. At any state, one of two actions can be performed: jump or do nothing. During gameplay, each frame is evaluated to determine whether the agent is alive or dead, where it rewards or punishes the agent respectively. The maximum runnable frames-per-second speed is 580 FPS, equating to approximately 5 hours of gameplay to reach 7000 episodes. This speed constraint was the bottleneck during experimentation and parameter tuning.
One of the main technical obstacles with a game like Flappy Bird is the mapping of continuous states to a discretized Q-matrix. There are three continuous variables that the agent measures: horizontal difference between the sprite and end of the upcoming pipe (0 to 480), vertical difference between the sprite and lower pipe (0 to 720), and vertical velocity (-10 to 10). To combat this, a reasonable strategy is to bin these continuous distances. Without binning, the Q-matrix would consist of 6,912,000 states. Unless stated otherwise, the vertical and horizontal distances of this agent were binned by 10 (i.e., {0, 10, … 720}, {0, 10, … 480}). No binning was applied to velocity as there exists only 20 values. This results in a total of 72051 states that the agent can be in.

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

![Learning cycle and states](https://imgur.com/EFFKJlH.jpg)

#### Figure 1: A typical learning cycle and an illustration of the Q-matrix states. <br />



While the state space is vast, the constant decrease in horizontal distance (xdiff) due to the side-scrolling nature of the game makes it easier to conceptualize state transition options. Every gametick, the agent progresses forward 10 pixels towards the upcoming pipe, during which the state is observed to determine whether the agent is alive or dead. The agent then has the two options (jump or do nothing) that will increase ydiff by 10 (maximum upward velocity) or decrease it according to the current negative velocity. A list of actions (history) is recorded as well as the corresponding states. It is only after the agent has died that the Q-matrix is updated using this list. The update equation is the standard Q-learning algorithm:


![Standard Q-Learning Equation](https://imgur.com/fgt2Pgr.jpg)




# RESULTS AND ANALYSIS
## Quantitative Analysis
To evaluate performance, the agent completed thousands of episodes (up until convergence or significant point of interest) with different parameter values, one at a time whilst keeping the remaining parameters constant. Firstly, learning rate had a significant impact on overall performance, namely average score where convergence occurred. As expected, a lower learning rate would result in delayed convergence. Surprisingly, in addition to faster convergence, a high learning rate (0.8) led to a significantly higher average score. The top score was 1210 points (alpha=0.8).

Examining the effects of introducing an exploring element (epsilon) into the early learning process, it was found that epsilon of any value higher than 0 would hinder the agent even after it was reduced to zero (episode 500). It is speculated that this may be a consequence of the agent investing too heavily in a sub-optimal state-reward association learned during this early phase.

![Comparing LRs](https://imgur.com/dIf3glm.jpg)


Finally, examining the impact of changing discount factors, two agents were compared different gamma values, while holding the remaining parameters constant. The results are consistent with the notion that due to the random spawning of pipes, the agent cannot advantageously plan beyond a short time horizon.

## Qualitative Analysis
Across most parameter variations, each agent underwent a period where it would exhibit a high number of deaths due to overshooting (jumping too high), and diverge from a previously higher average performance. After approximately 2000 more episodes, performance sharply increased with no prior indication of gradual improvement. This phenomena was not observed in agents with a very low learning rate, leading to the speculation that whatever state/action relationship was learned to cause such a dramatic increase in performance was one that required extremely fine changes in behaviour. Low learning rate agents also did not suffer from overshooting the optimum because of gradual changes and improvements to the Q-matrix, rather than large leaps.

![Overshoot Period](https://imgur.com/iiB1P8K.jpg)

## Learning-rate Decay Scheduler
It is intuitive to have the agent take larger leaps during the early learning process, whereas in later episodes to make smaller changes to learned behaviours. In an attempt to facilitate this, a decay scheduler was implemented that would decrease the learning rate at some rate as episode count increases. Two main decay schedules were examined: fixed and step-wise. Fixed decay would result in a decrease of 0.15 in learning rate every 1000 episodes, whereas step-wise would halve the learning rate every 1000 episodes (similar to exponential, albeit less continuously updated).

![Decay scheduler](https://imgur.com/uwZIbD9.jpg)

The results were surprising in that a step-wise decay scheduler had led to an earlier increase in performance, albeit with a lower average score upon convergence. It is speculated that the sufficiently small learning rate (0.4) starting at episode 1000 helped the agent avoid the overshoot learning period. However, it is arguable that the monotonic decay rate with regards to step-wise scheduler may be too aggressive, as it converged to an unsatisfactory score. Perhaps in future iterations of such an agent, an adaptive learning rate scheduler (increase or decrease depending on on-the-fly performance metrics) should be considered.

## References
Ceyhan, C., Flappybird-qlearning-bot, (2017), GitHub repository, https://github.com/chncyhn/flappybird-qlearning-bot <br />
Corriea, A. (2014). Flappy Bird collects $50K per day in ad revenue. [online] Polygon. Available at: https://www.polygon.com/2014/2/6/5385880/flappy-bird-collects-50k-per-day-in-ad-revenue <br />
Dredge, S. (2014). Flappy Bird at risk of extinction as developer 'cannot take this anymore'. [online] the Guardian. Available at: https://www.theguardian.com/technology/2014/feb/08/flappy-bird-dong-nguyen-deleting <br />
Gibbs, S. (2014). 'Flappy Bird phones' on sale on eBay from $300 to $90,000. [online] the Guardian. Available at: https://www.theguardian.com/technology/2014/feb/10/phones-flappy-bird-ebay-app-store <br />
Lau, S. (2017). Learning Rate Schedules and Adaptive Learning Rate Methods for Deep Learning. [online] Towards Data Science. Available at: https://towardsdatascience.com/learning-rate-schedules-and-adaptive-learning-rate-methods-for-deep-learning-2c8f433990d1 [Accessed 7 Apr. 2018].<br />
Poerio, T., Flappy-AI, (2016), GitHub repository, https://github.com/adpoe/Flappy-AI <br />
Quinn, M. and Reis, G. Automatic Flappy Bird Player, (2017), Standford, https://web.stanford.edu/class/cs221/2017/restricted/p-final/greis/final.pdf <br />
Sourabh, V., FlapPyBird, (2014), GitHub repository, https://github.com/sourabhv/FlapPyBird<br />
Vaish S., FlappyBirdRL, (2014), GitHub repository, https://github.com/SarvagyaVaish/FlappyBirdRL <br />
