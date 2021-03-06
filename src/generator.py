from statemachine import StateMachine, State, Transition

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

    def create_transitons(form_to, states):
        transitions = {}
        for indices in form_to:
            from_idx, to_idx_tuple = indices  # unpack list of two elements into separate from_idx and to_idx_tuple
            for to_idx in to_idx_tuple:  # iterate over destinations from a source state
                op_identifier = "m_{}_{}".format(from_idx, to_idx)  # parametrize identifier of a transition

                # create transition object and add it to the master_transitions dict
                transition = Transition(states[from_idx], states[to_idx], identifier=op_identifier)
                transitions[op_identifier] = transition

                # add transition to source state
                states[from_idx].transitions.append(transition)
        return transitions




    def choose_user(available_states):
        while True:
            try:
                next_state = int(input('\nWybierz nast??pny stan:'))
                for state in available_states:
                    if state == next_state:
                        return next_state
                    if next_state == 9:
                        return next_state
                raise ValueError('B????d')
                break
            except:
                print('Zdarzenie nie istnieje')


    def print_current_state(current_state, states, form_to):
        print('\nObecny stan:')
        print(f'[{current_state}] {states[current_state].name}')
        print('\nMo??liwe zdarzenia:')
        available_states = form_to[current_state][1]
        for i in available_states:
            print(f'[{i}] {states[i].value}')
        print('[9] Zako??cz program')

        return available_states


    # method of creating objects in a flexible way (we can define multiple functions
    # which will create objects in different ways)
    @classmethod
    def create_master(cls, states, transitions) -> 'Generator':
        return cls(states, transitions)

