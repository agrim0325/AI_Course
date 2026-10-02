# Search and A* - Laboratory Report

## Task 0: Understand the Search Problem
| Component | Your specification |
|---|---|
| State S | The set of all unblocked grid coordinates (x, y). |
| Actions A | {Up, Down, Left, Right} |
| Transition T | T((x, y), Action) \to (x', y') where (x', y') is the adjacent coordinate in the chosen direction. |
| Initial state s_0 | The grid coordinate containing S. |
| Goal G | The grid coordinate containing G. |
| Cost c | c(s, a, s') = 1 for all valid transitions. |

**(a) What information is necessary to specify a state?**
Only the robot's current (x, y) coordinate in the warehouse grid.
**(b) What makes an action invalid?**
Moving out of the grid boundaries or moving into a cell containing an obstacle #.
**(c) Is this a deterministic search problem?**
Yes, every action reliably leads to exactly one intended next state without randomness.
**(d) What would constitute a solution?**
A sequence of valid actions (e.g., [Right, Right, Down, ...]) that transitions the robot from s_0 (S) to G (G).

---

## Task 1: Plan the Agent
1. **State representation:** A tuple of integers (r, c) representing row and column.
2. **Warehouse representation:** A 2D list (or array of strings) parsed from the ASCII text.
3. **Valid actions:** Checking all 4 neighbors (r±1, c±1) and verifying they are within array bounds and do not contain #.
4. **Recognising goal:** current_state == goal_state.
5. **Frontier storage:**
   - For BFS: A collections.deque queue storing states.
   - For A*: A priority queue (min-heap via heapq) storing (f_score, state) tuples.
6. **Path reconstruction:** A came_from dictionary mapping each state to the state that generated it, allowing us to trace back from the goal to the start.

---

## Task 4: Inspect the A* Algorithm
| Concept | Where does it appear in the code? |
|---|---|
| State | (r, c) tuples handled as current and 
eighbor. |
| Action | Implicitly defined in the get_neighbors function which checks the 4 directions. |
| Transition | Handled by get_neighbors returning the new valid (r, c) coordinates. |
| Goal test | if current == goal: block inside the while loop. |
| g(n) | g_score[neighbor] = tentative_g_score dictionary. |
| h(n) | heuristic_func(neighbor, goal) call. |
| (n) | _score = tentative_g_score + heuristic_func(neighbor, goal) pushed to the heap. |
| Frontier | rontier = [] managed using heapq.heappush and heappop. |
| Visited states | expanded set which tracks popped states. |
| Path reconstruction | came_from dictionary mapped backwards in econstruct_path. |

**(a) What data structure is used for the A* frontier?** Min-heap (Priority Queue).
**(b) How does the program select the next state to expand?** Pops the element with the lowest _score from the heap.
**(c) Where is the heuristic calculated?** Right before pushing a neighbor to the frontier.
**(d) Does the program explicitly calculate (n) = g(n) + h(n)?** Yes.
**(e) How does the program prevent unnecessary repeated exploration?** By skipping states that are already in the expanded set upon being popped from the frontier.

---

## Task 5: Compare A* with Blind Search
| Measure | BFS | A* |
|---|---|---|
| Solution found | Yes | Yes |
| Path length | 40 | 40 |
| States expanded | 64 | 64 |

**(a) Did both algorithms find a solution?** Yes.
**(b) Did they find paths of the same length?** Yes.
**(c) Which algorithm expanded fewer states?** In the *Original Map*, they expanded the exact same number of states (64).
**(d) Why might A* expand fewer states?** The original map is essentially a winding corridor with no real alternative paths to explore, so both algorithms are forced to explore the entire accessible area. In a wide open grid with obstacles, A* would expand far fewer states because it uses the heuristic to pull the search directly toward the goal, whereas BFS searches outwards in a blind radius in all directions.

---

## Task 6: Investigate the Heuristic
**Why is Manhattan distance appropriate?**
Because the robot can only move horizontally and vertically (no diagonals). The Manhattan distance perfectly estimates the minimum possible steps to the goal ignoring obstacles.

**Experimental Investigation (Original Map):**
- **h(n) = 0 (Uniform Cost Search):** Path Length: 40 | Expanded: 64
- **h(n) = Euclidean:** Path Length: 40 | Expanded: 64
- **h(n) = 2 * Manhattan:** Path Length: 40 | Expanded: 64

*Note: Since the original map forces exploration of all reachable cells to find the single winding path to the goal, heuristic variation didn't reduce expansions. If we tested on an open map, 2 * Manhattan (which makes the heuristic inadmissible) would act like a greedy search, minimizing expansions but risking sub-optimal paths.*

---

## 6 Final Reflection
1. **Why is it important to formulate the search problem before writing the search algorithm?** It creates a clear separation between the *problem domain* (states, transitions) and the *solver* (BFS, A*). This allows us to plug the exact same problem definition into different search algorithms seamlessly.
2. **In what sense is A* an “informed” search algorithm?** It doesn't just blindly explore outward (like BFS/DFS); it is "informed" by a heuristic function h(n) that provides domain-specific knowledge about the estimated distance to the goal.
3. **Why does the choice of heuristic matter?** A good heuristic radically reduces the number of states expanded (speeding up search). If the heuristic is *admissible* (never overestimates), A* is guaranteed to find the shortest path. If it overestimates, it loses that guarantee.
4. **What did the LLM contribute to the engineering process?** The LLM generated the boilerplate syntax, data structures (heap queues, dictionaries), and algorithmic loops, translating my conceptual design into a functional Python program.
5. **What could go wrong if an engineer simply accepted LLM-generated code without testing it?** The code might contain subtle logical bugs (like expanding states incorrectly or using an invalid heuristic) that produce *plausible but sub-optimal paths*, masking the fact that the algorithm isn't actually working as designed. Testing proves the behavior matches the specification.
