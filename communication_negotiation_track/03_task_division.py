import random

class WorkerAgent:
    def __init__(self, agent_id, capabilities):
        self.agent_id = agent_id
        self.capabilities = capabilities # Dict of task_type -> cost multiplier
        self.tasks = []

    def bid_for_task(self, task):
        # Bid is based on cost. Lower is better.
        base_cost = task['difficulty']
        multiplier = self.capabilities.get(task['type'], 2.0) # Default high cost if unskilled
        bid_price = base_cost * multiplier
        return bid_price

    def assign_task(self, task):
        self.tasks.append(task)
        print(f"Agent {self.agent_id} assigned task {task['id']} ({task['type']})")

def run_task_division():
    task_types = ['coding', 'design', 'testing']
    
    # Create tasks
    tasks = []
    for i in range(10):
        t_type = random.choice(task_types)
        tasks.append({
            'id': i,
            'type': t_type,
            'difficulty': random.randint(1, 10)
        })
        
    # Create agents with different specializations
    agents = [
        WorkerAgent(1, {'coding': 0.5, 'design': 1.5, 'testing': 1.0}), # Coder
        WorkerAgent(2, {'coding': 2.0, 'design': 0.5, 'testing': 1.2}), # Designer
        WorkerAgent(3, {'coding': 1.2, 'design': 1.2, 'testing': 0.6})  # Tester
    ]
    
    print("--- Task Auction Start ---")
    total_cost = 0
    
    for task in tasks:
        print(f"\nAuctioning Task {task['id']}: {task['type']} (Diff: {task['difficulty']})")
        bids = []
        for agent in agents:
            bid = agent.bid_for_task(task)
            bids.append((bid, agent))
            print(f"  Agent {agent.agent_id} bids: {bid:.2f}")
            
        # Winner is lowest bidder
        winning_bid, winner = min(bids, key=lambda x: x[0])
        print(f"  -> Winner: Agent {winner.agent_id} with bid {winning_bid:.2f}")
        
        winner.assign_task(task)
        total_cost += winning_bid
        
    print(f"\nTotal Efficiency Cost: {total_cost:.2f}")
    for agent in agents:
        print(f"Agent {agent.agent_id} task count: {len(agent.tasks)}")

if __name__ == "__main__":
    run_task_division()
