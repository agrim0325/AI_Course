# Logical Reasoning for Planning - Lab Report

## Task 0: Understand the Planning Problem
**(a) What is the initial state I?**
`I = {At(Robot, A), At(Package, A)}`

**(b) What is the goal G?**
`G = {At(Package, C)}`

**(c) List the actions available to the robot.**
- `Move(A, B)`, `Move(B, A)`, `Move(B, C)`, `Move(C, B)`
- `PickUp(Package, A)`, `PickUp(Package, B)`, `PickUp(Package, C)`
- `Drop(Package, A)`, `Drop(Package, B)`, `Drop(Package, C)`

**(d) For each action, identify its preconditions and effects.**
- **Move(X, Y)**: Preconditions: `At(Robot, X)`. Effects: `At(Robot, Y)`, `¬At(Robot, X)`.
- **PickUp(Package, X)**: Preconditions: `At(Robot, X)`, `At(Package, X)`. Effects: `Holding(Package)`, `¬At(Package, X)`.
- **Drop(Package, X)**: Preconditions: `At(Robot, X)`, `Holding(Package)`. Effects: `At(Package, X)`, `¬Holding(Package)`.

**Question: Starting from I, is `PickUp(Package, A)` applicable? What about `Drop(Package, C)`?**
- `PickUp(Package, A)` is applicable because both of its preconditions (`At(Robot, A)` and `At(Package, A)`) are present in the initial state `I`.
- `Drop(Package, C)` is not applicable because neither of its preconditions (`At(Robot, C)` and `Holding(Package)`) are present in the initial state `I`.

---

## Task 1: Construct a Plan by Hand
**State Sequence:**
- `S0`: `At(Robot, A)`, `At(Package, A)`
- **Action 1**: `PickUp(Package, A)`
- `S1`: `At(Robot, A)`, `Holding(Package)`
- **Action 2**: `Move(A, B)`
- `S2`: `At(Robot, B)`, `Holding(Package)`
- **Action 3**: `Move(B, C)`
- `S3`: `At(Robot, C)`, `Holding(Package)`
- **Action 4**: `Drop(Package, C)`
- `S4`: `At(Robot, C)`, `At(Package, C)`

---

## Task 2 & 3: Ask an LLM to Implement the Planner & Test the Generated Planner
(See `Logics.py` for the implementation and the test output)

### Test Results
- **Test A (Solvable Problem):** A valid plan was found (`PickUp(Package, A)` -> `Move(A, B)` -> `Move(B, C)` -> `Drop(Package, C)`).
- **Test B (Impossible Problem):** The program correctly reported "No plan found" when the `PickUp` actions were removed.
- **Test C (Irrelevant Actions):** The planner correctly identified that just because the robot reaches `C`, the goal is not met unless the package is also dropped at `C`.

---

## Task 4: Logic and Search
**Where is each used?**
- **Logical reasoning** is used to determine whether an action is applicable in a given state (by checking if the state entails the action's preconditions) and how it logically updates the state (applying effects).
- **Search** is used to explore different possible sequences of actions (using Breadth-First Search) until a state is reached that satisfies the goal condition.

**Question:** Complete the following description:
Current state
↓
Check action preconditions
↓
**Applicable actions** 
↓
Generate successor state
↓
Search over alternatives
↓
Goal?

---

## Task 5: Optional – Can the LLM Verify Its Own Plan?
**Question: Which should you trust more?**
(b) the independently executed state transitions.

**Explain why:**
An LLM generates text based on probabilistic patterns, and its "explanations" are just plausible-sounding justifications generated after the fact. It might confidently hallucinate that a precondition was met when it wasn't. An independent Python program executes hard-coded logical rules deterministically, providing a verifiable and rigorous check of the state transitions.

---

## Reflection Questions

1. **Why is it useful to specify action preconditions and effects before asking an LLM to write the planner?**
   It grounds the LLM in a formal, logical structure. Without explicit constraints, the LLM might write arbitrary code or hallucinate impossible actions instead of implementing a strict state-transition model.
2. **Give an example of an error that could occur if the planner failed to check an action's preconditions.**
   The robot could execute `Drop(Package, C)` while it was still at location `A` and not holding anything, magically teleporting the package to `C`.
3. **Why is a plan that “looks reasonable” not necessarily a valid plan?**
   It might violate a subtle logical constraint (e.g., trying to pick up a package when already holding one, or moving to a non-connected node) that a human might miss but a logical verifier would catch.
4. **What did the LLM contribute to the implementation?**
   The LLM (in this case, me) provided the translation of the abstract logical definitions into executable Python code, structuring the breadth-first search and the set operations for state management.
5. **What did you have to verify independently?**
   I had to verify that the LLM's generated plan actually solved the problem through deterministic code execution, running tests on edge cases (impossible problems, irrelevant actions) to ensure logical soundness.
6. **In this laboratory, where is logical reasoning being used?**
   Logical reasoning is used in the `is_applicable` method (checking if preconditions are a subset of the current state) and the `apply` method (adding/removing propositions).
7. **How is planning related to the search algorithms studied in the previous module?**
   Planning is a specific application of search algorithms. The states are logical propositions, and the edges (transitions) are logically applicable actions. We use BFS to find the shortest path from the initial state to a state that satisfies the goal.

---

## 7.2 Prolog Reflection Questions (Optional)
1. **What is the difference between a Prolog fact and a Prolog rule?**
   A fact is an unconditional assertion (e.g., `connected(a, b)`). A rule is a conditional assertion that depends on other facts or rules (e.g., `can_move(X,Y) :- connected(X,Y)`).
2. **How does a Prolog query correspond to asking whether something follows from a knowledge base?**
   A query asks the Prolog engine to use logical inference (unification and backtracking) to prove whether the queried statement can be derived from the provided facts and rules.
3. **Why might it be useful to use a Prolog program to verify a plan generated by a Python program?**
   Prolog is specifically designed for formal logical inference. Using a different paradigm (logic programming vs. imperative programming) reduces the chance that a bug in the Python planner is also present in the verification step.
4. **What advantage does an independent verifier provide when the original plan was generated with the help of an LLM?**
   An independent verifier provides a strict, deterministic, rule-based check that is immune to the LLM's tendency to hallucinate or generate plausible but logically flawed outputs.
