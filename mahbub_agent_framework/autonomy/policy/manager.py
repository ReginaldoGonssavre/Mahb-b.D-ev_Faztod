"""
Policy management for autonomous agents.
"""

class PolicyManager:
    def __init__(self):
        self.policies = {}

    def update_policy(self, policy_name, policy_data):
        self.policies[policy_name] = policy_data

    def get_policy(self, policy_name):
        return self.policies.get(policy_name)
