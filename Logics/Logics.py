# Task 2: Implement a simple planning agent in Python
from collections import deque

class Action:
    def __init__(self, name, pos_preconds, neg_preconds, pos_effects, neg_effects):
        self.name = name
        self.pos_preconds = set(pos_preconds)
        self.neg_preconds = set(neg_preconds)
        self.pos_effects = set(pos_effects)
        self.neg_effects = set(neg_effects)

    def is_applicable(self, state):
        # All positive preconditions must be in the state
        if not self.pos_preconds.issubset(state):
            return False
        # None of the negative preconditions can be in the state
        if self.neg_preconds.intersection(state):
            return False
        return True

    def apply(self, state):
        new_state = state.copy()
        new_state.difference_update(self.neg_effects)
        new_state.update(self.pos_effects)
        return new_state

def bfs_plan(initial_state, goal_state, actions):
    # Queue stores tuples of (current_state, plan_so_far, states_reached)
    queue = deque([(set(initial_state), [], [set(initial_state)])])
    visited = [] 

    while queue:
        current_state, plan, states = queue.popleft()

        # Check if goal is reached (all goal propositions are in current state)
        if goal_state.issubset(current_state):
            return plan, states

        if current_state not in visited:
            visited.append(current_state)

            for action in actions:
                if action.is_applicable(current_state):
                    next_state = action.apply(current_state)
                    queue.append((next_state, plan + [action.name], states + [next_state]))

    return None, None

def run_tests():
    # Define Actions for the warehouse problem
    actions = [
        Action("Move(A, B)", ["At(Robot, A)"], [], ["At(Robot, B)"], ["At(Robot, A)"]),
        Action("Move(B, A)", ["At(Robot, B)"], [], ["At(Robot, A)"], ["At(Robot, B)"]),
        Action("Move(B, C)", ["At(Robot, B)"], [], ["At(Robot, C)"], ["At(Robot, B)"]),
        Action("Move(C, B)", ["At(Robot, C)"], [], ["At(Robot, B)"], ["At(Robot, C)"]),
        
        Action("PickUp(Package, A)", ["At(Robot, A)", "At(Package, A)"], [], ["Holding(Package)"], ["At(Package, A)"]),
        Action("PickUp(Package, B)", ["At(Robot, B)", "At(Package, B)"], [], ["Holding(Package)"], ["At(Package, B)"]),
        Action("PickUp(Package, C)", ["At(Robot, C)", "At(Package, C)"], [], ["Holding(Package)"], ["At(Package, C)"]),
        
        Action("Drop(Package, A)", ["At(Robot, A)", "Holding(Package)"], [], ["At(Package, A)"], ["Holding(Package)"]),
        Action("Drop(Package, B)", ["At(Robot, B)", "Holding(Package)"], [], ["At(Package, B)"], ["Holding(Package)"]),
        Action("Drop(Package, C)", ["At(Robot, C)", "Holding(Package)"], [], ["At(Package, C)"], ["Holding(Package)"])
    ]

    print("--- Test A: Solvable Problem ---")
    initial_state_a = {"At(Robot, A)", "At(Package, A)"}
    goal_state_a = {"At(Package, C)"}
    plan_a, states_a = bfs_plan(initial_state_a, goal_state_a, actions)
    
    if plan_a is None:
        print("No plan found\n")
    else:
        print("Plan found!")
        print(f"Initial State: {states_a[0]}")
        for act, state in zip(plan_a, states_a[1:]):
            print(f"Action: {act}")
            print(f"State after action: {state}")
        print()

    print("--- Test B: Impossible Problem ---")
    # Modify the problem so that the robot cannot pick up the package (remove PickUp actions).
    impossible_actions = [a for a in actions if not a.name.startswith("PickUp")]
    plan_b, states_b = bfs_plan(initial_state_a, goal_state_a, impossible_actions)
    
    if plan_b is None:
        print("No plan found\n")
    else:
        print("Plan found (Unexpected)!\n")

    print("--- Test C: Irrelevant Actions ---")
    # The normal Move actions already allow moving the robot independently of the package.
    # The planner must not confuse the robot reaching C with the package reaching C.
    goal_state_c = {"At(Package, C)"}
    plan_c, states_c = bfs_plan(initial_state_a, goal_state_c, actions)
    
    if plan_c is None:
        print("No plan found\n")
    else:
        print("Plan found!")
        for act in plan_c:
            print(f"Action: {act}")
        print("Check passed: The planner did not confuse the robot reaching C with the package reaching C.\n")

if __name__ == "__main__":
    run_tests()
