from main import Match
from agent.basic_agent import *
from agent.alpha_beta import *
#from agent.rl_agent import *
from statistics import mean


class Benchmark:
    def __init__(self, agent_self, agent_oppo):
        """
        :param agent_self: the agent to evaluate
        :param agent_oppo: the opponent agent, such as RandomAgent, GreedyAgent
        """
        if (agent_self.color == 'BLACK' and agent_oppo.color == 'WHITE') \
                or (agent_self.color == 'WHITE' and agent_oppo.color == 'BLACK'):
            self.agent_self = agent_self
            self.agent_oppo = agent_oppo
        else:
            raise ValueError('Must have one BLACK agent and one WHITE agent!')

    def create_match(self, gui=False):
        if self.agent_self.color == 'BLACK':
            return Match(black_agent=self.agent_self, white_agent=self.agent_oppo, gui=gui)
        else:
            return Match(white_agent=self.agent_self, black_agent=self.agent_oppo, gui=gui)

    def run_benchmark(self, num_tests, gui=False):
        list_win = []
        list_num_moves = []
        list_time_elapsed = []

        for i in range(1,num_tests+1):
            print('Running game %d: ' % i, end='')
            match = self.create_match(gui=gui)
            match.start()

            list_win.append(match.winner == self.agent_self.color)
            list_num_moves.append(match.counter_move)
            list_time_elapsed.append(match.time_elapsed)
            print('\tWinner: ' + match.winner)

        win_mean = mean(list_win)
        num_moves_mean = mean(list_num_moves)
        time_elapsed_mean = mean(list_time_elapsed)
        return win_mean, num_moves_mean, time_elapsed_mean

def get_agent(agent, color, depth):
    if agent == 0:
        return None, 'HUMAN'
    elif agent == 1:
        return RandomAgent(color), 'Random Agent'
    elif agent == 2:
        return GreedyAgent(color), 'Greedy Agent'
    elif agent == 3:
        return MinimaxAgent(color, depth=depth), 'Minimax Agent'
    elif agent == 4:
        return AlphaBetaAgent(color, depth=depth), 'AlphaBeta Agent'
    # elif agent == 5:
    #     agent = ApproxQAgent(color, RlEnv())
    #     agent.load('ApproxQAgent.npy')
    #     return agent, 'RL Agent'
    else:
        raise ValueError('Invalid agent for ' + color)

if __name__ == '__main__':
    
    depth1 = depth2 = agent_self = agent_oppo = -1
    
    while agent_self not in [0,1,2,3,4,5]:
        agent_self = int(input("Choose your agent for self(black) - 1 (random); 2 (greedy); 3 (minimax); 4 (alpha-beta prunning) : "))
        if agent_self in [3,4]:
            while depth1 <= 0:
                depth1 = int(input("Choose depth for black agent (depth > 0): "))
    agent_self = get_agent(agent_self,'BLACK',depth1)
        
    while agent_oppo not in [0,1,2,3,4,5]:
        agent_oppo = int(input("Choose your agent for opponent(white) - 1 (random); 2 (greedy); 3 (minimax); 4 (alpha-beta prunning) : "))
        if agent_oppo in [3,4]:
            while depth2 <= 0:
                depth2 = int(input("Choose depth for white agent (depth > 0): "))
    agent_oppo = get_agent(agent_oppo,'WHITE',depth2)
    
    gg = 2
    while gg not in [0, 1]: 
        gg = int(input("play game with (1) or without (0) gui: "))

    benchmark = Benchmark(agent_self[0], agent_oppo[0])
    win_mean, num_moves_mean, time_elapsed_mean = benchmark.run_benchmark(100, gui=gg)
    print("Self agent: ", agent_self[1])
    print("Opponent agent: ", agent_oppo[1])
    print('Win rate: %f; Avg # moves: %f; Avg time: %f' % (win_mean, num_moves_mean, time_elapsed_mean))
