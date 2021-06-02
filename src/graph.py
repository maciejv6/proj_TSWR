from statemachine import StateMachine, State, Transition
from generator import Generator
from config_path import Paths
import yaml
import network

import matplotlib
matplotlib.use('TkAgg')



# read .yaml
with open('config.yaml', 'r') as file:
    config_states = yaml.load(file, Loader=yaml.FullLoader)

# ** -> unpack dict to args
master_states = [State(**opt) for opt in config_states['master']]
slave_states = [State(**opt) for opt in config_states['slave']]

master_form_to, master_paths = Paths.graph_master()
slave_form_to, slave_paths = Paths.graph_slave()


def main():

    current_state = 0
    current_process = 'master_state'



    network.draw_graphs(master_states[current_state].name, slave_states[current_state].name, current_process)
    while True:



        if current_process == 'master_state':
            available_states = Generator.print_current_state(current_state, master_states, master_form_to)
            network.draw_graphs(master_states[current_state].name, slave_states[0].name, current_process)
            current_state = Generator.choose_user(available_states)
            if current_state == 9:
                return False

            if current_state == Paths.graph_master_end():
                network.draw_graphs(master_states[current_state].name, slave_states[0].name, current_process)
                current_state = 0
                current_process = 'slave_state'
                print('\n--------PROCES PODRZEDNY--------')
                print('-------------AWARIA-------------')



        elif current_process == 'slave_state':
            available_states = Generator.print_current_state(current_state, slave_states, slave_form_to)
            network.draw_graphs(master_states[7].name, slave_states[current_state].name, current_process)
            current_state = Generator.choose_user(available_states)
            if current_state == 9:
                return False

            if current_state == Paths.graph_slave_end():
                network.draw_graphs(master_states[7].name, slave_states[current_state].name, current_process)
                current_state = 0
                current_process = 'master_state'
                print('\n--------PROCES NADRZEDNY--------')
                print('-----------SEGREGACJA-----------')



# execute paths
if __name__ == '__main__':
    main()


