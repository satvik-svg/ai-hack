import random

def calculate_utility(agent, resources=None):
    if resources is None:
        resources = agent["resources"]
    utility = 0
    for r_type, count in resources.items():
        utility += count * agent["preferences"].get(r_type, 0)
    return utility


def propose_trade(proposer, receiver):
    resources = proposer["resources"]
    prefs = proposer["preferences"]

    # Pick resource with lowest preference that proposer has > 0
    give_resource = min(
        (r for r in resources if resources[r] > 0),
        key=lambda r: prefs[r],
        default=None
    )

    # Pick highest-value resource proposer wants
    want_resource = max(prefs, key=lambda r: prefs[r])

    if give_resource and want_resource and give_resource != want_resource:
        return {"give": give_resource, "want": want_resource, "amount": 1}
    return None


def evaluate_offer(agent, offer):
    get_res = offer["give"]
    give_res = offer["want"]
    amount = offer["amount"]

    if agent["resources"].get(give_res, 0) < amount:
        return False

    current_util = calculate_utility(agent)

    temp_resources = agent["resources"].copy()
    temp_resources[get_res] = temp_resources.get(get_res, 0) + amount
    temp_resources[give_res] -= amount

    new_util = calculate_utility(agent, temp_resources)

    return new_util > current_util


def execute_trade(agent, offer, role):
    if role == "proposer":
        agent["resources"][offer["give"]] -= offer["amount"]
        agent["resources"][offer["want"]] = agent["resources"].get(offer["want"], 0) + offer["amount"]
    else:
        agent["resources"][offer["give"]] = agent["resources"].get(offer["give"], 0) + offer["amount"]
        agent["resources"][offer["want"]] -= offer["amount"]


def run_negotiation():
    a1 = {
        "id": 1,
        "resources": {"Apple": 10, "Banana": 0, "Water": 5},
        "preferences": {"Apple": 1, "Banana": 5, "Water": 2},
    }

    a2 = {
        "id": 2,
        "resources": {"Apple": 0, "Banana": 10, "Water": 5},
        "preferences": {"Apple": 5, "Banana": 1, "Water": 2},
    }

    agents = [a1, a2]

    print("Initial State:")
    for ag in agents:
        print(f"Agent {ag['id']}: {ag['resources']} (Util: {calculate_utility(ag)})")

    for round_num in range(5):
        print(f"\n--- Round {round_num + 1} ---")

        proposer = random.choice(agents)
        receiver = a2 if proposer is a1 else a1

        offer = propose_trade(proposer, receiver)

        if offer:
            print(f"Agent {proposer['id']} proposes: Give {offer['give']}, Want {offer['want']}")
            accepted = evaluate_offer(receiver, offer)

            if accepted:
                print(f"Agent {receiver['id']} ACCEPTS.")
                execute_trade(proposer, offer, "proposer")
                execute_trade(receiver, offer, "receiver")
            else:
                print(f"Agent {receiver['id']} REJECTS.")
        else:
            print(f"Agent {proposer['id']} has no trade to propose.")

    print("\nFinal State:")
    for ag in agents:
        print(f"Agent {ag['id']}: {ag['resources']} (Util: {calculate_utility(ag)})")

if __name__ == "__main__":
    run_negotiation()
