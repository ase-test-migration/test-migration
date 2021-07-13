class State:
    def __init__(self, screenshot):
        self.screenshot = screenshot
        self.nodes = []
        self.actions = {}
        self.name_actions = {}
        self.activity = ""
        self.transitions = {}

    def add_node(self, node):
        self.nodes.append(node)

    def get_node(self, node_id):
        return self.nodes[node_id]

    def get_actions(self):
        return self.actions

    def get_name_actions(self):
        return self.name_actions

    def add_action(self, node_id, tag, action_type):
        self.actions[node_id]=action_type
        self.name_actions[tag]=action_type

    def set_activity(self, activity_name):
        self.activity = activity_name

    def add_transition(self, action, state):
        self.transitions[action] = state

    def print_state(self):
        print(self.name_actions)
        print("-------------------")
        for node in self.nodes:
            #if node.interactable:
                print(node.get_exec_identifiers())
        print("-------------------")

        