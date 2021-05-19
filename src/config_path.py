

class Paths():
    @classmethod
    def graph_master(self):

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
        # create paths from transitions (exemplary)
        master_path_1 = ["m_0_1", "m_1_2", "m_2_0"]
        master_path_2 = ["m_0_1", "m_1_3", "m_3_4", "m_4_5", "m_5_0"]
        master_path_3 = ["m_0_1", "m_1_3", "m_3_4", "m_4_6", "m_6_5", "m_5_0"]
        master_path_4 = ["m_0_1", "m_1_3", "m_3_4", "m_4_6", "m_6_7", "m_7_0"]
        master_paths = [master_path_1, master_path_2, master_path_3, master_path_4]
        return master_form_to, master_paths

    def graph_master_end():
        #state end
        return 7

    def graph_slave():
        slave_form_to = [
            [0, [1]],
            [1, [1, 2]]
        ]
        # create paths from transitions (exemplary)
        slave_path_1 = ["m_0_1", "m_1_1", "m_1_2"]
        slave_paths = [slave_path_1]
        return slave_form_to, slave_paths

    def graph_slave_end():
        #state end
        return 2


    def path(master_paths, supervisor, master_transitions):


        for path in master_paths:

            # create a supervisor
            print('\n' + str(supervisor))

            # run supervisor for exemplary path
            print("Executing path: {}".format(path))
            print(supervisor.current_state)
            for event in path:
                # launch a transition in our supervisor
                master_transitions[event]._run(supervisor)
                print(supervisor.current_state)

        return 0


