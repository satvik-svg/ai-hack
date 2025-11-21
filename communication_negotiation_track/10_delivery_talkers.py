import random

class DeliveryAgent:
    def __init__(self, agent_id, location):
        self.agent_id = agent_id
        self.location = location
        self.available = True

    def receive_request(self, task_location):
        if not self.available:
            return float('inf')
        # Cost is distance
        return abs(self.location - task_location)

    def assign(self, task_location):
        self.available = False
        print(f"Agent {self.agent_id} accepted task at {task_location}")
        self.location = task_location # Teleport for simplicity
        self.available = True

def run_delivery_talkers():
    # 1D World
    agents = [
        DeliveryAgent(1, 0),
        DeliveryAgent(2, 10),
        DeliveryAgent(3, 20)
    ]
    
    tasks = [2, 9, 18, 5, 12]
    
    print("--- Delivery Coordination ---")
    
    for t in tasks:
        print(f"\nNew Task at location {t}")
        
        # Broadcast to all agents
        bids = []
        for a in agents:
            cost = a.receive_request(t)
            bids.append((cost, a))
            print(f"  Agent {a.agent_id} bids cost {cost}")
            
        # Select best
        best_cost, best_agent = min(bids, key=lambda x: x[0])
        
        print(f"  -> Task assigned to Agent {best_agent.agent_id}")
        best_agent.assign(t)

if __name__ == "__main__":
    run_delivery_talkers()
