from main import Match
from agent.basic_agent import *
from agent.alpha_beta import *
from agent.rl_agent import *
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


if __name__ == '__main__':
    # agent_self = MinimaxAgent('BLACK',4)
    # agent_self = ApproxQAgent('BLACK', RlEnv())
    # agent_self.load('ApproxQAgent.npy')
    agent_self = AlphaBetaAgent('BLACK', 4)
    # agent_self = GreedyAgent('BLACK')
    

    # agent_oppo = RandomAgent('WHITE')
    agent_oppo = GreedyAgent('WHITE')
    # agent_oppo = AlphaBetaAgent('WHITE',2)
    # agent_oppo = AlphaBetaAgent('BLACK', 4)
    # agent_oppo = ApproxQAgent('WHITE', RlEnv())
    # agent_oppo.load('ApproxQAgent.npy')

    benchmark = Benchmark(agent_self=agent_self, agent_oppo=agent_oppo)
    win_mean, num_moves_mean, time_elapsed_mean = benchmark.run_benchmark(100, gui=0)
    print('Win rate: %f; Avg # moves: %f; Avg time: %f' % (win_mean, num_moves_mean, time_elapsed_mean))
