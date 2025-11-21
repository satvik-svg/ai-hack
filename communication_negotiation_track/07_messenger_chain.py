import collections

class NetworkAgent:
    def __init__(self, agent_id, neighbors):
        self.agent_id = agent_id
        self.neighbors = neighbors
        self.received_message = False
        self.message_content = None
        self.hop_count = float('inf')
        self.parent = None

    def receive_message(self, message, sender_id):
        content = message['content']
        hops = message['hops']
        
        if not self.received_message or hops < self.hop_count:
            self.received_message = True
            self.message_content = content
            self.hop_count = hops
            self.parent = sender_id
            return True # Propagate further
        return False

def run_messenger_chain():
    # Define Graph Structure (Adjacency List)
    # 0 -> 1, 2
    # 1 -> 3
    # 2 -> 3, 4
    # 3 -> 5
    # 4 -> 5
    adj_list = {
        0: [1, 2],
        1: [3],
        2: [3, 4],
        3: [5],
        4: [5],
        5: []
    }
    
    agents = {i: NetworkAgent(i, adj_list[i]) for i in range(6)}
    
    source_id = 0
    target_id = 5
    
    print(f"--- Messenger Chain: {source_id} -> {target_id} ---")
    
    # BFS Queue for message propagation: (agent_id, message_packet, sender_id)
    queue = collections.deque([(source_id, {'content': 'SECRET', 'hops': 0}, -1)])
    
    while queue:
        current_id, msg, sender_id = queue.popleft()
        agent = agents[current_id]
        
        print(f"Agent {current_id} received msg from {sender_id} (Hops: {msg['hops']})")
        
        should_propagate = agent.receive_message(msg, sender_id)
        
        if current_id == target_id:
            print(f"TARGET REACHED! Hops: {msg['hops']}")
            # We don't stop immediately in flooding to find all paths, but for shortest path BFS we can stop if unweighted
            # Here we continue to show full propagation logic or break if we just want first arrival
            break 
            
        if should_propagate:
            new_msg = {'content': msg['content'], 'hops': msg['hops'] + 1}
            for neighbor_id in agent.neighbors:
                queue.append((neighbor_id, new_msg, current_id))

    # Reconstruct Path
    path = []
    curr = target_id
    while curr != -1:
        path.append(curr)
        curr = agents[curr].parent
        if curr == -1: break
        
    print(f"Shortest Path: {path[::-1]}")

if __name__ == "__main__":
    run_messenger_chain()
