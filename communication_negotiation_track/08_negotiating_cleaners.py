import random

class CleanerAgent:
    def __init__(self, agent_id, start_pos):
        self.agent_id = agent_id
        self.pos = start_pos
        self.assigned_zone = None

    def bid_for_zones(self, zones):
        # Bid based on distance to zone center
        bids = {}
        for z_id, z_pos in zones.items():
            dist = abs(self.pos[0] - z_pos[0]) + abs(self.pos[1] - z_pos[1])
            bids[z_id] = dist
        return bids

def run_negotiating_cleaners():
    # 10x10 Grid split into 4 zones
    zones = {
        'TopLeft': (2, 2),
        'TopRight': (2, 7),
        'BottomLeft': (7, 2),
        'BottomRight': (7, 7)
    }
    
    agents = [
        CleanerAgent(1, (0, 0)),
        CleanerAgent(2, (9, 9)),
        CleanerAgent(3, (0, 9)),
        CleanerAgent(4, (9, 0))
    ]
    
    print("--- Zone Negotiation ---")
    
    # Collect all bids
    all_bids = [] # (cost, agent_id, zone_id)
    
    for agent in agents:
        bids = agent.bid_for_zones(zones)
        for z_id, cost in bids.items():
            all_bids.append((cost, agent.agent_id, z_id))
            
    # Sort by cost (lowest distance first)
    all_bids.sort(key=lambda x: x[0])
    
    assigned_zones = set()
    assigned_agents = set()
    
    print("Allocating Zones based on proximity bids:")
    
    for cost, ag_id, z_id in all_bids:
        if ag_id not in assigned_agents and z_id not in assigned_zones:
            print(f"Agent {ag_id} assigned to {z_id} (Distance: {cost})")
            assigned_zones.add(z_id)
            assigned_agents.add(ag_id)
            
    # Check for unassigned
    if len(assigned_agents) < len(agents):
        print("Warning: Some agents unassigned (should not happen in this symmetric setup)")

if __name__ == "__main__":
    run_negotiating_cleaners()
