import random

class Agent:
    def __init__(self, agent_id, resources, preferences):
        self.agent_id = agent_id
        self.resources = resources
        self.preferences = preferences # Weights for each resource type

    def calculate_utility(self, resources=None):
        if resources is None:
            resources = self.resources
        utility = 0
        for r_type, count in resources.items():
            utility += count * self.preferences.get(r_type, 0)
        return utility

    def propose_trade(self, other_agent):
        # Simple strategy: offer a resource I have plenty of (and low value) for one I need (high value)
        # Find resource with lowest marginal utility for me that I have > 0
        # Find resource with highest marginal utility for me that I want
        
        give_resource = min((r for r in self.resources if self.resources[r] > 0), 
                            key=lambda r: self.preferences[r], default=None)
        
        want_resource = max(self.preferences, key=lambda r: self.preferences[r])
        
        if give_resource and want_resource and give_resource != want_resource:
            return {'give': give_resource, 'want': want_resource, 'amount': 1}
        return None

    def evaluate_offer(self, offer):
        # Offer format from proposer: {'give': 'A', 'want': 'B', 'amount': 1}
        # Means proposer gives A, wants B.
        # So I (receiver) get A, give B.
        
        get_res = offer['give']
        give_res = offer['want']
        amount = offer['amount']
        
        if self.resources.get(give_res, 0) < amount:
            return False # Cannot afford
            
        current_util = self.calculate_utility()
        
        # Simulate trade
        temp_resources = self.resources.copy()
        temp_resources[get_res] = temp_resources.get(get_res, 0) + amount
        temp_resources[give_res] -= amount
        
        new_util = self.calculate_utility(temp_resources)
        
        return new_util > current_util

    def execute_trade(self, offer, role):
        if role == 'proposer':
            self.resources[offer['give']] -= offer['amount']
            self.resources[offer['want']] = self.resources.get(offer['want'], 0) + offer['amount']
        else: # receiver
            self.resources[offer['give']] = self.resources.get(offer['give'], 0) + offer['amount']
            self.resources[offer['want']] -= offer['amount']

def run_negotiation():
    # Setup
    resources = ['Apple', 'Banana', 'Water']
    
    a1 = Agent(1, {'Apple': 10, 'Banana': 0, 'Water': 5}, {'Apple': 1, 'Banana': 5, 'Water': 2})
    a2 = Agent(2, {'Apple': 0, 'Banana': 10, 'Water': 5}, {'Apple': 5, 'Banana': 1, 'Water': 2})
    
    agents = [a1, a2]
    
    print("Initial State:")
    for a in agents:
        print(f"Agent {a.agent_id}: {a.resources} (Util: {a.calculate_utility()})")
        
    for round_num in range(5):
        print(f"\n--- Round {round_num + 1} ---")
        # Randomly pick proposer
        proposer = random.choice(agents)
        receiver = a2 if proposer == a1 else a1
        
        offer = proposer.propose_trade(receiver)
        if offer:
            print(f"Agent {proposer.agent_id} proposes: Give {offer['give']}, Want {offer['want']}")
            accepted = receiver.evaluate_offer(offer)
            
            if accepted:
                print(f"Agent {receiver.agent_id} ACCEPTS.")
                proposer.execute_trade(offer, 'proposer')
                receiver.execute_trade(offer, 'receiver')
            else:
                print(f"Agent {receiver.agent_id} REJECTS.")
        else:
            print(f"Agent {proposer.agent_id} has no trade to propose.")

    print("\nFinal State:")
    for a in agents:
        print(f"Agent {a.agent_id}: {a.resources} (Util: {a.calculate_utility()})")

if __name__ == "__main__":
    run_negotiation()
