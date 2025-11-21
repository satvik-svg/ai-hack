import random

class Agent:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        # Vocabulary: State -> Symbol (for Sender), Symbol -> Action (for Receiver)
        self.sender_strategy = {} 
        self.receiver_strategy = {}
        
    def speak(self, state):
        if state not in self.sender_strategy:
            self.sender_strategy[state] = random.choice(['A', 'B', 'C'])
        return self.sender_strategy[state]
        
    def listen(self, symbol):
        if symbol not in self.receiver_strategy:
            self.receiver_strategy[symbol] = random.choice(['Act1', 'Act2', 'Act3'])
        return self.receiver_strategy[symbol]
        
    def update(self, role, input_val, output_val, success):
        # Simple Reinforcement Learning
        if success:
            # Keep strategy
            pass
        else:
            # Change strategy
            if role == 'sender':
                self.sender_strategy[input_val] = random.choice(['A', 'B', 'C'])
            else:
                self.receiver_strategy[input_val] = random.choice(['Act1', 'Act2', 'Act3'])

def run_language_evolution():
    # Lewis Signaling Game
    # States: S1, S2, S3
    # Actions: Act1, Act2, Act3
    # Goal: S1->Act1, S2->Act2, S3->Act3
    
    states = ['S1', 'S2', 'S3']
    correct_mapping = {'S1': 'Act1', 'S2': 'Act2', 'S3': 'Act3'}
    
    a1 = Agent(1)
    a2 = Agent(2)
    
    print("--- Language Evolution Start ---")
    
    for round_num in range(100):
        state = random.choice(states)
        
        # A1 speaks, A2 listens
        symbol = a1.speak(state)
        action = a2.listen(symbol)
        
        success = (action == correct_mapping[state])
        
        a1.update('sender', state, symbol, success)
        a2.update('receiver', symbol, action, success)
        
        if round_num % 20 == 0:
            print(f"Round {round_num}: State {state} -> Sym {symbol} -> Act {action} ({'Success' if success else 'Fail'})")

    print("\n--- Final Protocol ---")
    print("Sender (A1) Map:", a1.sender_strategy)
    print("Receiver (A2) Map:", a2.receiver_strategy)
    
    # Verify
    score = 0
    for s in states:
        sym = a1.sender_strategy[s]
        act = a2.receiver_strategy[sym]
        if act == correct_mapping[s]:
            score += 1
    print(f"Agreement Score: {score}/{len(states)}")

if __name__ == "__main__":
    run_language_evolution()
