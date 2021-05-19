from statemachine import StateMachine, State, Transition
from generator import Generator
from config_path import Paths
import yaml

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

    while True:

        if current_process == 'master_state':
            available_states = Generator.print_current_state(current_state, master_states, master_form_to)
            current_state = Generator.choose_user(available_states)
            if current_state == Paths.graph_master_end():
                current_state = 0
                current_process = 'slave_state'
                print('\n--------PROCES PODRZEDNY--------')
                print('-------------AWARIA-------------')

        elif current_process == 'slave_state':
            available_states = Generator.print_current_state(current_state, slave_states, slave_form_to)
            current_state = Generator.choose_user(available_states)
            if current_state == Paths.graph_slave_end():
                current_state = 0
                current_process = 'master_state'
                print('\n--------PROCES NADRZEDNY--------')
                print('-----------SEGREGACJA-----------')

# execute paths
if __name__ == '__main__':
    main()


