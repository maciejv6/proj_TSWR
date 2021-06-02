import networkx as nx
import matplotlib.pyplot as plt




def draw_graphs(current_state_master, current_state_slave, current_process):
    master_edges = [("Oczekiwanie na element", "Sprawdzenie rodzju elementu"),
                    ("Sprawdzenie rodzju elementu", "Oczekiwanie az element opusci tasme"),
                    ("Oczekiwanie az element opusci tasme", "Oczekiwanie na element"),
                    ("Sprawdzenie rodzju elementu", "Zatrzymanie tasmy"),
                    ("Zatrzymanie tasmy", "Chwytanie elementu"),
                    ("Chwytanie elementu", "Umieszczenie elementu w pojemniku"),
                    ("Chwytanie elementu", "Ponowna proba chwycenia elementu"),
                    ("Umieszczenie elementu w pojemniku", "Oczekiwanie na element"),
                    ("Ponowna proba chwycenia elementu", "Umieszczenie elementu w pojemniku"),
                    ("Ponowna proba chwycenia elementu", "awaria"),
                    ("awaria", "Oczekiwanie na element")
                    ]
    poss_master = { "Oczekiwanie na element": ([0.0, -0.15]),  # 1
                    "Sprawdzenie rodzju elementu": ([-0.1, -0.08]),  # 2
                    "Oczekiwanie az element opusci tasme": ([0.01 , -0.0]),  # 3
                    "Zatrzymanie tasmy": ([-0.15, -0.2]),  # 4
                    "Chwytanie elementu": ([-0.14 , -0.35]),  # 5
                    "Umieszczenie elementu w pojemniku": ([-0.07, -0.23]),  # 6
                    "Ponowna proba chwycenia elementu": ([-0.005 , -0.45]),  # 7
                    "awaria": ([0.05 , -0.25])  # 8
                   }

    master_nodes = ["Oczekiwanie na element",  # 1
                    "Sprawdzenie rodzju elementu",  # 2
                    "Oczekiwanie az element opusci tasme",  # 3
                    "Zatrzymanie tasmy",  # 4
                    "Chwytanie elementu",  # 5
                    "Umieszczenie elementu w pojemniku",  # 6
                    "Ponowna proba chwycenia elementu",  # 7
                    "awaria"  # 8
                    ]

    master_edge_labels = {("Oczekiwanie na element", "Sprawdzenie rodzju elementu"): 'Wykryto element',
                          ("Sprawdzenie rodzju elementu", "Oczekiwanie az element opusci tasme"): 'Element duzy',
                          ("Oczekiwanie az element opusci tasme", "Oczekiwanie na element"): 'Uruchomienie tasmy',
                          ("Sprawdzenie rodzju elementu", "Zatrzymanie tasmy"): 'Element maly',
                          ("Zatrzymanie tasmy", "Chwytanie elementu"): 'Tasma zatrzymana',
                          ("Chwytanie elementu", "Umieszczenie elementu w pojemniku"): 'Element chwycony',
                          ("Chwytanie elementu", "Ponowna proba chwycenia elementu"): 'Element niechwycony',
                          ("Umieszczenie elementu w pojemniku", "Oczekiwanie na element"): 'Uruchomienie tasmy',
                          ("Ponowna proba chwycenia elementu", "Umieszczenie elementu w pojemniku"): 'Element chwycony',
                          ("Ponowna proba chwycenia elementu", "awaria"): 'Element niechwycony',
                          ("awaria", "Oczekiwanie na element"): 'Uruchomienie tasmy'}

    slave_edges = [("awaria", "Usuwanie usterki"),
                   ("Usuwanie usterki", "Usuwanie usterki"),
                   ("Usuwanie usterki", "Wylaczenie alarmu")
                   ]
    slave_nodes = ["awaria",  # 1
                   "Usuwanie usterki",  # 2
                   "Wylaczenie alarmu",  # 3
                   ]

    poss_slave = {"awaria": ([0.0 , 0.4]),  # 1
                   "Usuwanie usterki": ([0.0 , 0.2]),  # 2
                   "Wylaczenie alarmu": ([0.0 , 0.0]),  # 3
                   }

    slave_edge_labels = {("awaria", "Usuwanie usterki"): 'Wezwanie operatora',
                         #("Usuwanie usterki", "Usuwanie usterki"): 'Usterka nieusunieta',
                         ("Usuwanie usterki", "Wylaczenie alarmu"): 'Usterka usunieta'}

    master = nx.DiGraph()

    master.add_edges_from(master_edges)
    master.add_nodes_from(master_nodes)
    # pos_master = nx.circular_layout(master)
    pos_master = nx.kamada_kawai_layout(master)

    slave = nx.DiGraph()

    slave.add_edges_from(slave_edges)
    slave.add_nodes_from(slave_nodes)
    pos_slave = nx.kamada_kawai_layout(slave)

    color_map_master = []

    for node in master:

        if node == current_state_master and current_process == 'master_state':
            color_map_master.append('red')
        else:
            color_map_master.append('green')


    color_map_slave = []

    for node in slave:

        if node == current_state_slave and current_process == 'slave_state':
            color_map_slave.append('red')
        else:
            color_map_slave.append('green')

    plt.figure("Proces segregacji", figsize=(10, 5), dpi=100)

    plt.subplot(1, 6, (1, 5), title = "SEGREGACJA")
    #plt.ylim(-1, 1)
    #plt.xlim(-1, 1)
    nx.draw(master, poss_master, with_labels=True, edge_color='g', node_color=color_map_master, font_size=8,
            node_size=2000)
    nx.draw_networkx_edge_labels(master, poss_master, edge_labels=master_edge_labels, rotate=False, font_size=6)

    plt.subplot(1, 6, (6), title = "AWARIA")

    nx.draw(slave, poss_slave, with_labels=True, edge_color='g', node_color=color_map_slave, font_size=8, node_size=2000)
    nx.draw_networkx_edge_labels(slave, poss_slave, edge_labels=slave_edge_labels, rotate=False, font_size=6)


    plt.draw()
    plt.pause(0.01)
    plt.clf()







