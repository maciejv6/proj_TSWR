from statemachine import StateMachine, State, Transition
from generator import Generator
from config_path import Paths
import yaml


# read .yaml
with open('config.yaml', 'r') as file:
    config_states = yaml.load(file)
  
# ** -> unpack dict to args
master_states = [State(**opt) for opt in config_states['master']]
slave_states = [State(**opt) for opt in config_states['slave']]


master_form_to, master_paths = Paths.graph_master()
slave_form_to, slave_paths = Paths.graph_slave()


def main():
    master_transitions = Generator.create_transitons(master_form_to, master_states)
    slave_transitions = Generator.create_transitons(slave_form_to, slave_states)

    supervisor = Generator.create_master(master_states, master_transitions)
    Paths.path(master_paths, supervisor, master_transitions)
    supervisor = Generator.create_master(slave_states, slave_transitions)
    Paths.path(slave_paths, supervisor, slave_transitions)
            

# execute paths
if __name__ == '__main__':
    main()


