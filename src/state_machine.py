from statemachine import StateMachine, State, Transition
from generator import Generator
import yaml


# read .yaml
with open('config.yaml', 'r') as file:
    config_states = yaml.load(file)
  
# ** -> unpack dict to args
master_states = [State(**opt) for opt in config_states['master']]
slave_states = [State(**opt) for opt in config_states['slave']]

# valid transitions for a master (indices of states from-to)
master_form_to = [
    [0, [1]],
    [1, [2, 3]],
    [2, [0]],
    [3, [4]],
    [4, [5, 6]],
    [5, [0]],
    [6, [5, 7]],
    [7, [0]]
]

slave_form_to = [
    [0, [1]],
    [1, [1, 2]]
]

# create paths from transitions (exemplary)
master_path_1 = ["m_0_1", "m_1_2", "m_2_0"]
master_path_2 = ["m_0_1", "m_1_3", "m_3_4", "m_4_5", "m_5_0"]
master_path_3 = ["m_0_1", "m_1_3", "m_3_4", "m_4_6", "m_6_5", "m_5_0"]
master_path_4 = ["m_0_1", "m_1_3", "m_3_4", "m_4_6", "m_6_7", "m_7_0"]

slave_path_1 = ["m_0_1", "m_1_1", "m_1_2"]
master_paths = [master_path_1, master_path_2, master_path_3, master_path_4]
slave_paths = [slave_path_1]

def create_transitons():
    master_transitions = {}
    for indices in master_form_to:
        from_idx, to_idx_tuple = indices  # unpack list of two elements into separate from_idx and to_idx_tuple
        for to_idx in to_idx_tuple:  # iterate over destinations from a source state
            op_identifier = "m_{}_{}".format(from_idx, to_idx)  # parametrize identifier of a transition

            # create transition object and add it to the master_transitions dict
            transition = Transition(master_states[from_idx], master_states[to_idx], identifier=op_identifier)
            master_transitions[op_identifier] = transition

            # add transition to source state
            master_states[from_idx].transitions.append(transition)

    slave_transitions = {}
    for indices in slave_form_to:
        from_idx, to_idx_tuple = indices  # unpack list of two elements into separate from_idx and to_idx_tuple
        for to_idx in to_idx_tuple:  # iterate over destinations from a source state
            op_identifier = "m_{}_{}".format(from_idx, to_idx)  # parametrize identifier of a transition

            # create transition object and add it to the master_transitions dict
            transition = Transition(slave_states[from_idx], slave_states[to_idx], identifier=op_identifier)
            slave_transitions[op_identifier] = transition

            # add transition to source state
            slave_states[from_idx].transitions.append(transition)

    return master_transitions, slave_transitions

def main():
    master_transitions, slave_transitions = create_transitons()

    for path in master_paths:

        # create a supervisor
        supervisor = Generator.create_master(master_states, master_transitions)
        print('\n' + str(supervisor))

        # run supervisor for exemplary path
        print("Executing path: {}".format(path))
        print(supervisor.current_state)
        for event in path:

            # launch a transition in our supervisor
            master_transitions[event]._run(supervisor)
            print(supervisor.current_state)

    # execute paths
    for path in slave_paths:

        # create a supervisor
        supervisor = Generator.create_master(slave_states, slave_transitions)
        print('\n' + str(supervisor))

        # run supervisor for exemplary path
        print("Executing path: {}".format(path))
        print(supervisor.current_state)
        for event in path:

            # launch a transition in our supervisor
            slave_transitions[event]._run(supervisor)
            print(supervisor.current_state)
            

# execute paths
if __name__ == '__main__':
    main()


