from exlog import ExLog
from collections import defaultdict

class CentralHub:
    def __init__(self, logger=None):
        self.swarms = {}
        self.logger = logger or ExLog(log_level=1) # You can change this within the instantiation for your own scripts to be silent just set logger=ExLog(log_level=0)

    def register_swarm(self, swarm):
        """Register a swarm."""
        self.swarms[swarm.name] = swarm
        self.logger.dprint(f"Swarm '{swarm.name}' registered.", level="info")

    def send_message(self, message, sender_swarm_name, recipient_swarm_name, recipient_name=None, group_name=None):
        """Synchronously send a message."""
        if sender_swarm_name == recipient_swarm_name:
            self.logger.dprint("Warning: Cannot send to the same swarm. Ignoring.", level="warning")
            return

        if recipient_swarm_name in self.swarms:
            recipient_swarm = self.swarms[recipient_swarm_name]
            recipient_swarm.receive_message_from_swarm(message, sender_swarm_name, recipient_name, group_name)
        else:
            self.logger.dprint(f"Error: Swarm '{recipient_swarm_name}' not registered.", level="error")

    async def async_send_message(self, message, sender_swarm_name, recipient_swarm_name, recipient_name=None, group_name=None):
        """Asynchronously send a message."""
        if sender_swarm_name == recipient_swarm_name:
            self.logger.dprint("Warning: Cannot send to the same swarm. Ignoring.", level="warning")
            return

        if recipient_swarm_name in self.swarms:
            recipient_swarm = self.swarms[recipient_swarm_name]
            await recipient_swarm.async_receive_message_from_swarm(message, sender_swarm_name, recipient_name, group_name)
        else:
            self.logger.dprint(f"Error: Swarm '{recipient_swarm_name}' not registered.", level="error")

