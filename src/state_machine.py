from statemachine import StateMachine, State, Transition

# define states for a master (way of passing args to class)
master_options = [
    {"name": "Oczekiwanie na element", "initial": True, "value": "Oczekiwanie na element"}, #0

    {"name": "Sprawdzenie rodzju elementu", "initial": False, "value": "Sprawdzenie rodzju elementu"}, #1

    {"name": "Oczekiwanie aż element opuści taśmę", "initial": False, "value": "Oczekiwanie aż element opuści taśmę"}, #2

    {"name": "Zatrzymanie taśmy", "initial": False, "value": "Zatrzymanie taśmy"}, #3

    {"name": "Chwytanie elementu", "initial": False, "value": "Chwycenie elementu"}, #4

    {"name": "Umieszczenie elementu w pojemniku", "initial": False, "value": "Umieszczenie elementu w pojemniku"}, #5

    {"name": "Ponowna próba chwycenia elementu", "initial": False, "value": "Ponowna próba chwycenia elementu"}, #6

    {"name": "awaria", "initial": False, "value": "awaria"}]  # 7

slave_options = [
    {"name": "awaria", "initial": True, "value": "awaria"}, #0

    {"name": "Usuwanie usterki", "initial": False, "value": "Usuwanie usterki"}, #1

    {"name": "Wyłączenie alarmu", "initial": False, "value": "Wyłączenie alarmu"}] #2

# create State objects for a master
# ** -> unpack dict to args
master_states = [State(**opt) for opt in master_options]
slave_states = [State(**opt) for opt in slave_options]

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

# create transitions for a master (as a dict)
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


# create a generator class
class Generator(StateMachine):
    states = []
    transitions = []
    states_map = {}
    current_state = None

    def __init__(self, states, transitions):

        # creating each new object needs clearing its variables (otherwise they're duplicated)
        self.states = []
        self.transitions = []
        self.states_map = {}
        self.current_state = states[0]

        # create fields of states and transitions using setattr()
        # create lists of states and transitions
        # create states map - needed by StateMachine to map states and its values
        for s in states:
            setattr(self, str(s.name).lower(), s)
            self.states.append(s)
            self.states_map[s.value] = str(s.name)

        for key in transitions:
            setattr(self, str(transitions[key].identifier).lower(), transitions[key])
            self.transitions.append(transitions[key])

        # super() - allows us to use methods of StateMachine in our Generator object
        super(Generator, self).__init__()

    # define a printable introduction of a class
    def __repr__(self):
        return "{}(model={!r}, state_field={!r}, current_state={!r})".format(
            type(self).__name__, self.model, self.state_field,
            self.current_state.identifier,
        )

    # method of creating objects in a flexible way (we can define multiple functions
    # which will create objects in different ways)
    @classmethod
    def create_master(cls, states, transitions) -> 'Generator':
        return cls(states, transitions)


# create paths from transitions (exemplary)
master_path_1 = ["m_0_1", "m_1_2", "m_2_0"]
master_path_2 = ["m_0_1", "m_1_3", "m_3_4", "m_4_5", "m_5_0"]
master_path_3 = ["m_0_1", "m_1_3", "m_3_4", "m_4_6", "m_6_5", "m_5_0"]
master_path_4 = ["m_0_1", "m_1_3", "m_3_4", "m_4_6", "m_6_7", "m_7_0"]

slave_path_1 = ["m_0_1", "m_1_1", "m_1_2"]


master_paths = [master_path_1, master_path_2, master_path_3, master_path_4]
slave_paths = [slave_path_1]


# execute paths
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
        

