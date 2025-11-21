import random

class BidderAgent:
    def __init__(self, agent_id, valuation):
        self.agent_id = agent_id
        self.valuation = valuation # Private value for the item

    def generate_bid(self):
        # In Vickrey auction, dominant strategy is to bid your true valuation
        return self.valuation

def run_auction():
    print("--- Multi-Agent Vickrey Auction ---")
    
    # Setup agents with random valuations
    agents = []
    for i in range(5):
        val = random.randint(10, 100)
        agents.append(BidderAgent(i+1, val))
        print(f"Agent {i+1} created (Private Valuation: {val})") # Hidden in real scenario
        
    # Bidding Phase
    bids = []
    print("\nBidding Phase:")
    for agent in agents:
        bid = agent.generate_bid()
        bids.append((bid, agent))
        print(f"Agent {agent.agent_id} submits sealed bid.")
        
    # Winner Determination
    # Sort bids descending
    bids.sort(key=lambda x: x[0], reverse=True)
    
    winner_bid, winner_agent = bids[0]
    second_highest_bid = bids[1][0]
    
    print("\n--- Results ---")
    print(f"Winner: Agent {winner_agent.agent_id}")
    print(f"Winning Bid (Truthful): {winner_bid}")
    print(f"Price Paid (Second Price): {second_highest_bid}")
    print(f"Agent Profit (Value - Price): {winner_agent.valuation - second_highest_bid}")

if __name__ == "__main__":
    run_auction()
