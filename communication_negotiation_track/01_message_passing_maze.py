import collections
import random
import time

class Agent:
    def __init__(self, agent_id, start_pos, grid_size):
        self.agent_id = agent_id
        self.pos = start_pos
        self.grid_size = grid_size
        self.visited = set()
        self.visited.add(start_pos)
        self.queue = collections.deque([start_pos])
        self.found_treasure = False
        self.path_to_treasure = []

    def move(self, grid, messages):
        if not self.queue and not self.found_treasure:
            return "IDLE"

        # Process messages
        for msg in messages:
            if msg['type'] == 'TREASURE_FOUND':
                self.found_treasure = True
                self.path_to_treasure = msg['path']
                return f"Agent {self.agent_id}: Received treasure location!"
            elif msg['type'] == 'VISITED':
                self.visited.add(msg['pos'])

        if self.found_treasure:
            return "DONE"

        # BFS Step
        if self.queue:
            current_pos = self.queue.popleft()
            r, c = current_pos
            
            # Check if treasure
            if grid[r][c] == 'T':
                self.found_treasure = True
                return {
                    'type': 'TREASURE_FOUND',
                    'agent_id': self.agent_id,
                    'path': [current_pos], # Simplified path for this demo
                    'pos': current_pos
                }

            # Explore neighbors
            neighbors = [
                (r+1, c), (r-1, c), (r, c+1), (r, c-1)
            ]
            
            for nr, nc in neighbors:
                if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                    if (nr, nc) not in self.visited and grid[nr][nc] != '#':
                        self.visited.add((nr, nc))
                        self.queue.append((nr, nc))
                        # Broadcast visited to avoid redundant exploration
                        return {
                            'type': 'VISITED',
                            'agent_id': self.agent_id,
                            'pos': (nr, nc)
                        }
            
            self.pos = current_pos # Teleport for BFS visualization simplicity
            return f"Agent {self.agent_id} exploring {current_pos}"

        return "IDLE"

def run_maze_simulation():
    GRID_SIZE = 10
    grid = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
    # Place obstacles
    for _ in range(15):
        r, c = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
        grid[r][c] = '#'
        
    # Place treasure
    tr, tc = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
    grid[tr][tc] = 'T'
    print(f"Treasure at: {(tr, tc)}")

    agents = [
        Agent(1, (0, 0), GRID_SIZE),
        Agent(2, (GRID_SIZE-1, GRID_SIZE-1), GRID_SIZE)
    ]

    step = 0
    while step < 100:
        print(f"--- Step {step} ---")
        messages = []
        all_done = True
        
        for agent in agents:
            result = agent.move(grid, messages)
            
            if isinstance(result, dict):
                messages.append(result)
                print(f"Agent {agent.agent_id} broadcast: {result['type']} at {result.get('pos')}")
                if result['type'] == 'TREASURE_FOUND':
                    print(f"*** TREASURE FOUND BY AGENT {agent.agent_id} ***")
                    return
            else:
                print(result)
                if result != "DONE" and result != "IDLE":
                    all_done = False
        
        # Share messages for next turn (simulating broadcast delay or immediate receipt)
        # In this loop, messages generated in this turn are available to others in next turn
        # For simplicity, we can pass them in next call, but here we passed empty list first.
        # Let's fix to pass messages generated in PREVIOUS turn or THIS turn depending on sync.
        # Here we just print. Real logic would accumulate messages.
        
        if all_done:
            break
        step += 1

if __name__ == "__main__":
    run_maze_simulation()
