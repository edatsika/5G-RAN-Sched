import numpy as np
import gym
import scheduler


def e_greedy(Q, s, epsilon=0.1):
    if np.random.uniform(0, 1) < epsilon:
        # Choose a random action
        #print(">>>>>>>>>>>>>>> Random action", np.random.randint(Q.shape[1]))
        return np.random.randint(Q.shape[1])
    else:
        return greedy(Q, s)


def greedy(Q, s):
    return np.argmax(Q[s])

def run_episodes(env, Q, episodes, print_results=False):
    '''
    Run some episodes to test the policy
    '''
    tot_rew = []
    state = env.reset()

    for _ in range(episodes):
        done = False
        game_rew = 0

        while not done:
            # select a greedy action
            next_state, rew, done, _ = env.step(greedy(Q, state))

            state = next_state
            game_rew += rew
            if done:
                state = env.reset()
                tot_rew.append(game_rew)

    if print_results:
        print('Mean score: %.3f of %i games!' % (np.mean(tot_rew), episodes))

    return np.mean(tot_rew)

def Q_learning(env, episodes, learn_rate, epsilon, gamma, reduce_eps):
    nA = env.RBs
    nS = env.observation_space.n
    print(env.action_space.sample())
    print("nS",nS)
    print("nA",nA)
    Q = np.zeros((nS, nA))
    curr_rews = []
    total_reward = []

    for n in range(episodes):
        state = env.reset()
        done = False
        tot_rew = 0

        if epsilon > 0.01:
            epsilon -= reduce_eps

        while not done:
            action = e_greedy(Q, state, epsilon)
            #print(">>>>>>>>>>>>>>> Action selected: ", action)
            next_state, rew, done, _ = env.step(action)
            Qrow = Q.max(axis=1)
            Q[state][action] = Q[state][action] + learn_rate * (rew + gamma * Qrow[next_state]- Q[state][action])

            state = next_state
            tot_rew += rew

            if done:
                total_reward.append(tot_rew)
    return Q


if __name__ == '__main__':
    env = gym.make("scheduler-v0")
    obs_space = env.observation_space
    action_space = env.action_space
    print("The observation space: {}".format(obs_space))
    print("The action space: {}".format(action_space))
    print("Environment created!")
    print("Select number of episodes (higher than 100)")
    episodes = int(input())
    learn_rate = 0.1
    epsilon = 0.01
    gamma = 0.9
    reduce_eps = 0.001
    Q_learning = Q_learning(env, episodes, learn_rate, epsilon, gamma, reduce_eps) #eps=0.05?
    print("Episodes: ", episodes)
    print("Final Ptx: ", env.Ptx)
