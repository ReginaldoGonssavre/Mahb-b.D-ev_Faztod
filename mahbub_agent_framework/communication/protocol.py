"""
Communication protocol for multi-agent interaction.
"""

class CommunicationProtocol:
    def send_message(self, sender, receiver, message):
        # Placeholder for sending a message
        return f"Message from {sender} to {receiver}: {message}"

    def broadcast_message(self, sender, message):
        # Placeholder for broadcasting a message
        return f"Broadcast from {sender}: {message}"
