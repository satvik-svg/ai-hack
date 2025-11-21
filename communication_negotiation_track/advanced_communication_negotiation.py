import random
import time
import heapq
import collections
import math
import sys
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Any, Optional

# Configure Logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger()

# ==========================================
# Shared Utilities
# ==========================================

class Agent(ABC):
    def __init__(self, agent_id: int):
        self.agent_id = agent_id

    def __repr__(self):
        return f"Agent({self.agent_id})"

# ==========================================
# Task 1: Advanced Message Passing Maze (A*)
# ==========================================

class MazeAgent(Agent):
    def __init__(self, agent_id: int, start_pos: Tuple[int, int], grid_size: int):
        super().__init__(agent_id)
        self.pos = start_pos
        self.grid_size = grid_size
        self.known_grid = {}  # (r, c) -> cell_type
        self.visited = set()
        self.path_to_target = []
        self.target_pos = None

    def update_knowledge(self, new_info: Dict[Tuple[int, int], str]):
        self.known_grid.update(new_info)

    def plan_path(self, target: Tuple[int, int], obstacles: set):
        # A* Algorithm
        start = self.pos
        frontier = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}

        while frontier:
            _, current = heapq.heappop(frontier)

            if current == target:
                break

            r, c = current
            neighbors = [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]
            
            for next_pos in neighbors:
                nr, nc = next_pos
                if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                    if next_pos in obstacles:
                        continue
                    
                    new_cost = cost_so_far[current] + 1
                    if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                        cost_so_far[next_pos] = new_cost
                        priority = new_cost + abs(nr - target[0]) + abs(nc - target[1])
                        heapq.heappush(frontier, (priority, next_pos))
                        came_from[next_pos] = current
        
        # Reconstruct path
        if target not in came_from:
            return []
            
        path = []
        curr = target
        while curr != start:
            path.append(curr)
            curr = came_from[curr]
        path.reverse()
        return path

def run_advanced_maze():
    print("\n--- Task 1: Advanced Message Passing Maze (A*) ---")
    GRID_SIZE = 10
    grid = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
    # Obstacles
    obstacles = set()
    for _ in range(20):
        r, c = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        if (r, c) not in [(0,0), (GRID_SIZE-1, GRID_SIZE-1)]:
            grid[r][c] = '#'
            obstacles.add((r, c))
            
    # Treasure
    while True:
        tr, tc = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        if (tr, tc) not in obstacles and (tr, tc) not in [(0,0), (GRID_SIZE-1, GRID_SIZE-1)]:
            grid[tr][tc] = 'T'
            treasure_pos = (tr, tc)
            break
            
    print(f"Treasure located at {treasure_pos}")
    
    agents = [
        MazeAgent(1, (0, 0), GRID_SIZE),
        MazeAgent(2, (GRID_SIZE-1, GRID_SIZE-1), GRID_SIZE)
    ]
    
    found = False
    for step in range(20):
        print(f"Step {step}:")
        
        # 1. Sense
        for agent in agents:
            # Simulate sensing local area
            r, c = agent.pos
            local_obs = {}
            # Sense 3x3 area
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                        local_obs[(nr, nc)] = grid[nr][nc]
                        if grid[nr][nc] == 'T':
                            agent.target_pos = (nr, nc)
                            print(f"  Agent {agent.agent_id} FOUND TREASURE at {(nr, nc)}!")
                            found = True
            agent.update_knowledge(local_obs)

        # 2. Communicate (Share Knowledge)
        # In advanced version, they merge maps
        merged_knowledge = {}
        for agent in agents:
            merged_knowledge.update(agent.known_grid)
        
        shared_target = None
        for agent in agents:
            if agent.target_pos:
                shared_target = agent.target_pos
                break
        
        for agent in agents:
            agent.update_knowledge(merged_knowledge)
            if shared_target:
                agent.target_pos = shared_target

        if found:
            print("  Treasure location shared. Planning paths...")
            for agent in agents:
                known_obstacles = {p for p, t in agent.known_grid.items() if t == '#'}
                path = agent.plan_path(agent.target_pos, known_obstacles)
                if path:
                    print(f"  Agent {agent.agent_id} path to treasure: {path}")
                else:
                    print(f"  Agent {agent.agent_id} cannot reach treasure (blocked).")
            return

        # 3. Move (Random exploration if no target)
        for agent in agents:
            possible_moves = []
            r, c = agent.pos
            for nr, nc in [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]:
                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                    if agent.known_grid.get((nr, nc)) != '#':
                        possible_moves.append((nr, nc))
            
            if possible_moves:
                # Prefer unvisited
                unvisited = [m for m in possible_moves if m not in agent.visited]
                if unvisited:
                    move = random.choice(unvisited)
                else:
                    move = random.choice(possible_moves)
                agent.pos = move
                agent.visited.add(move)
                print(f"  Agent {agent.agent_id} moved to {move}")

# ==========================================
# Task 2: Advanced Resource Negotiators
# ==========================================

class NegotiatorAgent(Agent):
    def __init__(self, agent_id: int, resources: Dict[str, int], preferences: Dict[str, float]):
        super().__init__(agent_id)
        self.resources = resources
        self.preferences = preferences

    def utility(self, resources=None):
        if resources is None: resources = self.resources
        # Diminishing marginal utility: utility = weight * log(count + 1)
        u = 0
        for r, count in resources.items():
            weight = self.preferences.get(r, 1.0)
            u += weight * math.log(count + 1)
        return u

def run_advanced_negotiation():
    print("\n--- Task 2: Advanced Resource Negotiators (Multi-Round) ---")
    resources_list = ['Gold', 'Wood', 'Food']
    
    a1 = NegotiatorAgent(1, {'Gold': 10, 'Wood': 2, 'Food': 5}, {'Gold': 1.0, 'Wood': 5.0, 'Food': 2.0})
    a2 = NegotiatorAgent(2, {'Gold': 2, 'Wood': 10, 'Food': 5}, {'Gold': 5.0, 'Wood': 1.0, 'Food': 2.0})
    
    agents = [a1, a2]
    
    print("Initial Utilities:")
    for a in agents:
        print(f"  Agent {a.agent_id}: {a.utility():.2f}")

    # Multi-round bargaining
    for round_num in range(1, 6):
        print(f"\nRound {round_num}")
        proposer = random.choice(agents)
        responder = a2 if proposer == a1 else a1
        
        # Smart Proposal Generation
        # Identify what I have excess of (low marginal gain) and what I want (high marginal gain)
        best_offer = None
        max_gain = 0
        
        # Try all 1-for-1 trades
        for give_r in resources_list:
            if proposer.resources[give_r] > 0:
                for get_r in resources_list:
                    if give_r == get_r: continue
                    
                    # Simulate my new utility
                    my_new_res = proposer.resources.copy()
                    my_new_res[give_r] -= 1
                    my_new_res[get_r] += 1
                    my_gain = proposer.utility(my_new_res) - proposer.utility()
                    
                    if my_gain > max_gain:
                        max_gain = my_gain
                        best_offer = (give_r, get_r, 1)

        if best_offer:
            give, want, amt = best_offer
            print(f"  Agent {proposer.agent_id} proposes: Give {amt} {give} for {amt} {want}")
            
            # Responder Evaluation
            if responder.resources.get(want, 0) >= amt: # Can I afford to give what they want?
                # Note: Offer says "Proposer Gives X, Wants Y". So Responder Gets X, Gives Y.
                resp_new_res = responder.resources.copy()
                resp_new_res[give] += amt
                resp_new_res[want] -= amt
                
                resp_gain = responder.utility(resp_new_res) - responder.utility()
                
                if resp_gain > 0:
                    print(f"  Agent {responder.agent_id} ACCEPTS (Gain: {resp_gain:.2f})")
                    # Execute
                    proposer.resources[give] -= amt
                    proposer.resources[want] += amt
                    responder.resources[give] += amt
                    responder.resources[want] -= amt
                else:
                    print(f"  Agent {responder.agent_id} REJECTS (Loss: {resp_gain:.2f})")
            else:
                print(f"  Agent {responder.agent_id} REJECTS (Insufficient funds)")
        else:
            print(f"  Agent {proposer.agent_id} is satisfied, no trade proposed.")

    print("\nFinal Utilities:")
    for a in agents:
        print(f"  Agent {a.agent_id}: {a.utility():.2f} {a.resources}")

# ==========================================
# Task 3: Advanced Task Division (CNP)
# ==========================================

class CNPWorker(Agent):
    def __init__(self, agent_id: int, skills: Dict[str, float]):
        super().__init__(agent_id)
        self.skills = skills # Efficiency multiplier (lower is better)
        self.load = 0

    def evaluate_cfp(self, task_type: str, difficulty: int) -> float:
        # Bid = (Difficulty * Skill_Multiplier) + Current_Load_Penalty
        skill_mult = self.skills.get(task_type, 2.0)
        cost = (difficulty * skill_mult) + (self.load * 0.5)
        return cost

    def assign_task(self, cost: float):
        self.load += cost

def run_advanced_task_division():
    print("\n--- Task 3: Advanced Task Division (Contract Net Protocol) ---")
    
    workers = [
        CNPWorker(1, {'coding': 0.5, 'testing': 1.5}),
        CNPWorker(2, {'coding': 1.5, 'testing': 0.5}),
        CNPWorker(3, {'coding': 1.0, 'testing': 1.0})
    ]
    
    tasks = [
        ('coding', 10), ('testing', 8), ('coding', 20), ('testing', 5), ('design', 10)
    ]
    
    for i, (t_type, diff) in enumerate(tasks):
        print(f"\nManager announces Task {i}: {t_type} (Diff: {diff})")
        
        # 1. Announcement (CFP)
        bids = []
        for w in workers:
            bid_price = w.evaluate_cfp(t_type, diff)
            bids.append((bid_price, w))
            print(f"  Worker {w.agent_id} bids: {bid_price:.2f}")
            
        # 2. Award
        best_bid, winner = min(bids, key=lambda x: x[0])
        print(f"  -> Awarded to Worker {winner.agent_id} at cost {best_bid:.2f}")
        winner.assign_task(best_bid)

# ==========================================
# Task 4: Advanced Chat to Plan (Prioritized)
# ==========================================

def run_advanced_chat_to_plan():
    print("\n--- Task 4: Advanced Chat to Plan (Prioritized Planning) ---")
    # Scenario: 2 agents in a narrow corridor swapping places
    # 0 1 2 3 4
    # A . . . B
    # Goal: A->4, B->0
    
    grid_len = 5
    agents = [
        {'id': 'A', 'start': 0, 'goal': 4, 'prio': 1},
        {'id': 'B', 'start': 4, 'goal': 0, 'prio': 2}
    ]
    
    # Prioritized Planning: Higher priority plans first, lower priority plans around them
    agents.sort(key=lambda x: x['prio'])
    
    reservations = set() # (time, location)
    
    full_plans = {}
    
    for agent in agents:
        print(f"Planning for Agent {agent['id']}...")
        # A* with time dimension
        start_node = (0, agent['start']) # (time, pos)
        goal_pos = agent['goal']
        
        frontier = [(0, start_node)]
        came_from = {start_node: None}
        cost_so_far = {start_node: 0}
        
        found_path = None
        
        while frontier:
            _, current = heapq.heappop(frontier)
            curr_time, curr_pos = current
            
            if curr_pos == goal_pos and curr_time > 8: # Wait a bit to ensure stability
                 found_path = current
                 break
            
            if curr_time > 15: # Timeout
                break
                
            # Moves: Left, Right, Wait
            next_moves = []
            if curr_pos > 0: next_moves.append(curr_pos - 1)
            if curr_pos < grid_len - 1: next_moves.append(curr_pos + 1)
            next_moves.append(curr_pos) # Wait
            
            for next_pos in next_moves:
                next_time = curr_time + 1
                if (next_time, next_pos) in reservations:
                    continue # Collision with higher priority agent
                
                # Vertex collision check is not enough, need edge collision (swapping) check?
                # For 1D, swapping means: I go i->j, other went j->i at same time.
                # Since we reserve (t, pos), if higher prio is at pos at time t, I can't be there.
                # This handles vertex collisions.
                
                new_cost = cost_so_far[current] + 1
                if (next_time, next_pos) not in cost_so_far or new_cost < cost_so_far[(next_time, next_pos)]:
                    cost_so_far[(next_time, next_pos)] = new_cost
                    prio = new_cost + abs(next_pos - goal_pos)
                    heapq.heappush(frontier, (prio, (next_time, next_pos)))
                    came_from[(next_time, next_pos)] = current

        # Reconstruct
        if found_path:
            path = []
            curr = found_path
            while curr:
                path.append(curr)
                reservations.add(curr) # Reserve space-time
                curr = came_from[curr]
            path.reverse()
            full_plans[agent['id']] = path
            print(f"  Path found: {[(t, p) for t, p in path]}")
        else:
            print("  No path found!")

# ==========================================
# Task 5: Advanced Multi-Agent Auction
# ==========================================

class AuctionAgent(Agent):
    def __init__(self, agent_id: int, valuation: int):
        super().__init__(agent_id)
        self.valuation = valuation
        self.active = True

def run_advanced_auction():
    print("\n--- Task 5: Advanced Multi-Agent Auction ---")
    print("Select Auction Type: 1. English (Ascending)  2. Vickrey (Sealed 2nd Price)")
    # For demo, we'll run English
    print("Running English Auction...")
    
    agents = [AuctionAgent(i, random.randint(50, 150)) for i in range(5)]
    for a in agents: print(f"  Agent {a.agent_id} Val: {a.valuation}")
    
    current_price = 0
    min_increment = 10
    winner = None
    
    while True:
        active_bidders = [a for a in agents if a.active]
        if len(active_bidders) == 0:
            print("No bidders left. Item unsold.")
            break
        if len(active_bidders) == 1:
            winner = active_bidders[0]
            print(f"Auction ended! Winner: Agent {winner.agent_id} at Price: {current_price}")
            if winner.valuation >= current_price:
                print(f"  Agent Profit: {winner.valuation - current_price}")
            else:
                print("  Winner overpaid (Winner's curse)!")
            break
            
        # Bidding round
        current_price += min_increment
        print(f"Price raised to {current_price}")
        
        for a in active_bidders:
            if a.valuation < current_price:
                a.active = False
                print(f"  Agent {a.agent_id} drops out.")
            else:
                print(f"  Agent {a.agent_id} stays in.")

# ==========================================
# Task 6: Advanced Disaster Relief
# ==========================================

def run_advanced_disaster_relief():
    print("\n--- Task 6: Advanced Disaster Relief (Dynamic) ---")
    # Agents have fuel. Zones appear dynamically.
    
    zones = []
    agents = [{'id': 1, 'pos': 0, 'fuel': 20}, {'id': 2, 'pos': 10, 'fuel': 20}]
    
    for time_step in range(10):
        # Random zone appearance
        if random.random() < 0.4:
            z_pos = random.randint(0, 10)
            zones.append({'pos': z_pos, 'severity': random.randint(3, 8)})
            print(f"Time {time_step}: New Disaster at {z_pos}!")
            
        # Assignment (Greedy with Fuel Check)
        for z in zones[:]:
            best_agent = None
            min_dist = float('inf')
            
            for a in agents:
                dist = abs(a['pos'] - z['pos'])
                if dist <= a['fuel'] and dist < min_dist:
                    min_dist = dist
                    best_agent = a
            
            if best_agent:
                print(f"  Agent {best_agent['id']} responding to {z['pos']} (Dist: {min_dist})")
                best_agent['fuel'] -= min_dist
                best_agent['pos'] = z['pos']
                zones.remove(z) # Solved
            else:
                print(f"  Zone at {z['pos']} unserved (No fuel/agents)!")

# ==========================================
# Task 7: Advanced Messenger Chain
# ==========================================

def run_advanced_messenger():
    print("\n--- Task 7: Advanced Messenger Chain (Reliability) ---")
    # Simulating packet loss and retries
    
    path = [0, 1, 2, 3] # Linear chain
    message = "SECRET_CODE"
    
    current_node = 0
    target_node = 3
    
    while current_node != target_node:
        next_node = path[path.index(current_node) + 1]
        
        success = False
        attempts = 0
        while not success and attempts < 3:
            attempts += 1
            print(f"Node {current_node} sending to {next_node} (Attempt {attempts})...")
            
            if random.random() > 0.3: # 70% success rate
                print("  ACK received.")
                success = True
                current_node = next_node
            else:
                print("  Packet Lost/Timeout.")
        
        if not success:
            print("Link failure! Transmission aborted.")
            return

    print(f"Message '{message}' delivered to Node {target_node}!")

# ==========================================
# Task 8: Advanced Negotiating Cleaners
# ==========================================

def run_advanced_cleaners():
    print("\n--- Task 8: Advanced Negotiating Cleaners (Market) ---")
    # Agents bid for zones. If one agent wins too many, they can subcontract.
    
    zones = ['Z1', 'Z2', 'Z3', 'Z4']
    agents = [{'id': 1, 'cap': 2}, {'id': 2, 'cap': 2}] # Capacity limit
    
    assignments = {1: [], 2: []}
    
    for z in zones:
        # Random bids
        bids = [(random.randint(1, 10), a) for a in agents]
        cost, winner = min(bids, key=lambda x: x[0])
        
        if len(assignments[winner['id']]) < winner['cap']:
            assignments[winner['id']].append(z)
            print(f"Zone {z} won by Agent {winner['id']} for {cost}")
        else:
            print(f"Agent {winner['id']} won {z} but is at capacity! Subcontracting...")
            other = agents[1] if winner['id'] == 1 else agents[0]
            assignments[other['id']].append(z)
            print(f"  -> Transferred to Agent {other['id']}")

# ==========================================
# Task 9: Advanced Language Evolution
# ==========================================

def run_advanced_language():
    print("\n--- Task 9: Advanced Language Evolution (RL) ---")
    # Q-Learning for Naming Game
    
    objects = ['Apple', 'Banana']
    vocab = ['Word1', 'Word2']
    
    # Q-Table: Agent -> Object -> Word -> Value
    q_table = {
        1: {o: {w: 0.0 for w in vocab} for o in objects},
        2: {o: {w: 0.0 for w in vocab} for o in objects} # Receiver interprets Word -> Object
    }
    
    # Simplified: A1 is always Speaker, A2 Listener
    # Speaker learns Object -> Word
    # Listener learns Word -> Object
    
    speaker_q = {o: {w: 0.0 for w in vocab} for o in objects}
    listener_q = {w: {o: 0.0 for o in objects} for w in vocab}
    
    epsilon = 0.5
    alpha = 0.1
    
    for i in range(20):
        target_obj = random.choice(objects)
        
        # Speaker chooses word
        if random.random() < epsilon:
            word = random.choice(vocab)
        else:
            word = max(speaker_q[target_obj], key=speaker_q[target_obj].get)
            
        # Listener guesses object
        if random.random() < epsilon:
            guess = random.choice(objects)
        else:
            guess = max(listener_q[word], key=listener_q[word].get)
            
        reward = 1 if guess == target_obj else -1
        
        # Update
        speaker_q[target_obj][word] += alpha * (reward - speaker_q[target_obj][word])
        listener_q[word][guess] += alpha * (reward - listener_q[word][guess])
        
        if i % 5 == 0:
            print(f"Iter {i}: Obj {target_obj} -> Word {word} -> Guess {guess} (R: {reward})")
            
    print("Final Speaker Q:", speaker_q)

# ==========================================
# Task 10: Advanced Delivery Talkers
# ==========================================

def run_advanced_delivery():
    print("\n--- Task 10: Advanced Delivery Talkers (VRP Heuristic) ---")
    # Nearest Neighbor Heuristic
    
    depot = (0,0)
    truck_pos = depot
    deliveries = [(2,3), (5,1), (1,4), (6,6)]
    
    print(f"Start at {depot}. Deliveries: {deliveries}")
    
    route = []
    current = truck_pos
    
    while deliveries:
        # Find nearest
        nearest = min(deliveries, key=lambda p: abs(p[0]-current[0]) + abs(p[1]-current[1]))
        route.append(nearest)
        print(f"  -> Going to {nearest}")
        current = nearest
        deliveries.remove(nearest)
        
    print("Route Complete.")

# ==========================================
# Main Menu
# ==========================================

def main():
    tasks = {
        '1': run_advanced_maze,
        '2': run_advanced_negotiation,
        '3': run_advanced_task_division,
        '4': run_advanced_chat_to_plan,
        '5': run_advanced_auction,
        '6': run_advanced_disaster_relief,
        '7': run_advanced_messenger,
        '8': run_advanced_cleaners,
        '9': run_advanced_language,
        '10': run_advanced_delivery
    }
    
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        print("Running Automated Tests...")
        for k, func in tasks.items():
            try:
                func()
                print(f"Task {k} PASSED")
            except Exception as e:
                print(f"Task {k} FAILED: {e}")
        return

    while True:
        print("\n==========================================")
        print("   Advanced Multi-Agent Simulation Hub    ")
        print("==========================================")
        print("1. Message Passing Maze (A*)")
        print("2. Resource Negotiators (Multi-Round)")
        print("3. Task Division (Contract Net)")
        print("4. Chat to Plan (Prioritized)")
        print("5. Multi-Agent Auction (English)")
        print("6. Disaster Relief (Dynamic)")
        print("7. Messenger Chain (Reliable)")
        print("8. Negotiating Cleaners (Market)")
        print("9. Language Evolution (RL)")
        print("10. Delivery Talkers (VRP)")
        print("q. Quit")
        
        choice = input("\nSelect a task (1-10): ").strip().lower()
        
        if choice == 'q':
            print("Exiting...")
            break
            
        if choice in tasks:
            try:
                tasks[choice]()
                input("\nPress Enter to continue...")
            except Exception as e:
                print(f"Error running task: {e}")
        else:
            print("Invalid selection.")

if __name__ == "__main__":
    main()
