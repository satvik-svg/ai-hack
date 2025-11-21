import random
import math

class ReliefAgent:
    def __init__(self, agent_id, pos, capacity):
        self.agent_id = agent_id
        self.pos = pos
        self.capacity = capacity
        self.carrying = capacity

    def move_towards(self, target):
        # Simple grid movement
        r, c = self.pos
        tr, tc = target
        
        if r < tr: r += 1
        elif r > tr: r -= 1
        
        if c < tc: c += 1
        elif c > tc: c -= 1
        
        self.pos = (r, c)
        return self.pos

class DisasterZone:
    def __init__(self, zone_id, pos, severity):
        self.zone_id = zone_id
        self.pos = pos
        self.severity = severity # Resources needed

def run_disaster_relief():
    GRID_SIZE = 10
    zones = [
        DisasterZone(1, (2, 2), 5),
        DisasterZone(2, (7, 8), 8)
    ]
    
    agents = [
        ReliefAgent(1, (0, 0), 5),
        ReliefAgent(2, (9, 9), 5)
    ]
    
    print("--- Disaster Relief Coordination ---")
    print(f"Zones: {[f'Z{z.zone_id} at {z.pos} (Need {z.severity})' for z in zones]}")
    
    # Simple coordination: Assign closest agent to each zone
    assignments = {}
    
    # Calculate distances and assign
    # This is a centralized coordination simulation via communication
    unassigned_zones = list(zones)
    
    for agent in agents:
        if not unassigned_zones:
            break
            
        # Find closest zone
        best_zone = min(unassigned_zones, 
                       key=lambda z: abs(agent.pos[0]-z.pos[0]) + abs(agent.pos[1]-z.pos[1]))
        
        assignments[agent.agent_id] = best_zone
        unassigned_zones.remove(best_zone)
        print(f"Agent {agent.agent_id} assigned to Zone {best_zone.zone_id}")

    # Simulation Loop
    for step in range(15):
        print(f"\nStep {step}")
        all_cleared = True
        
        for agent in agents:
            if agent.agent_id in assignments:
                target_zone = assignments[agent.agent_id]
                
                if target_zone.severity <= 0:
                    print(f"Agent {agent.agent_id}: Zone {target_zone.zone_id} is clear.")
                    continue
                    
                all_cleared = False
                
                if agent.pos != target_zone.pos:
                    agent.move_towards(target_zone.pos)
                    print(f"Agent {agent.agent_id} moving to {agent.pos}")
                else:
                    # Deliver aid
                    amount = min(agent.carrying, target_zone.severity)
                    target_zone.severity -= amount
                    agent.carrying -= amount
                    print(f"Agent {agent.agent_id} delivered {amount} to Zone {target_zone.zone_id}. Remaining need: {target_zone.severity}")
                    
                    if agent.carrying == 0 and target_zone.severity > 0:
                        print(f"Agent {agent.agent_id} out of resources! Needs resupply (not implemented).")
        
        if all_cleared:
            print("All disaster zones relieved!")
            break

if __name__ == "__main__":
    run_disaster_relief()
