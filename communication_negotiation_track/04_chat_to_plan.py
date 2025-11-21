import random

class NavAgent:
    def __init__(self, agent_id, start_pos, goal_pos):
        self.agent_id = agent_id
        self.pos = start_pos
        self.goal = goal_pos

    def propose_next_move(self):
        # Simple logic: move towards goal
        r, c = self.pos
        gr, gc = self.goal
        
        moves = []
        if r < gr: moves.append((r+1, c))
        if r > gr: moves.append((r-1, c))
        if c < gc: moves.append((r, c+1))
        if c > gc: moves.append((r, c-1))
        
        if not moves:
            return self.pos # Stay put if at goal
            
        return random.choice(moves)

    def vote_on_proposal(self, proposal, other_agent_pos):
        # Check for collision
        if proposal == other_agent_pos:
            return False # Veto if it hits me
        return True

def run_chat_to_plan():
    # 5x5 Grid
    # Agent 1: (0,0) -> (4,4)
    # Agent 2: (4,0) -> (0,4)
    # They will cross paths!
    
    a1 = NavAgent(1, (0,0), (4,4))
    a2 = NavAgent(2, (4,0), (0,4))
    
    agents = [a1, a2]
    
    for step in range(10):
        print(f"\n--- Step {step} ---")
        print(f"Positions: A1{a1.pos}, A2{a2.pos}")
        
        if a1.pos == a1.goal and a2.pos == a2.goal:
            print("Both agents reached goals!")
            break
            
        # Phase 1: Propose
        proposals = {}
        for a in agents:
            if a.pos != a.goal:
                prop = a.propose_next_move()
                proposals[a.agent_id] = prop
                print(f"Agent {a.agent_id} proposes move to {prop}")
            else:
                proposals[a.agent_id] = a.pos
                
        # Phase 2: Negotiate/Vote
        # Check for conflicts (swapping positions or moving to same spot)
        move_map = {a.agent_id: proposals[a.agent_id] for a in agents}
        
        conflict = False
        # Check same cell collision
        if move_map[1] == move_map[2]:
            conflict = True
            print("Conflict: Agents trying to move to same cell!")
            
        # Check swap collision
        if move_map[1] == a2.pos and move_map[2] == a1.pos:
            conflict = True
            print("Conflict: Agents trying to swap cells directly!")
            
        if conflict:
            # Resolution: Priority to Agent 1 this time (could be random or alternating)
            print("Resolving conflict: Agent 1 moves, Agent 2 waits.")
            a1.pos = move_map[1]
            # Agent 2 stays
        else:
            print("No conflict. Moves approved.")
            a1.pos = move_map[1]
            a2.pos = move_map[2]

if __name__ == "__main__":
    run_chat_to_plan()
