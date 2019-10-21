from . import ChatBase


class ChatDiscord(ChatBase):
    def on_message_received(self, user_id: str, message: str) -> None:
        ...

    def broadcast_message(self, message: str) -> None:
        ...

    def send_message_to(self, user_id: str, message: str) -> None:
        ...

    def send_ban_req(self, user_id: str, reason: str = None) -> bool:
        ...

    def send_mute_req(self, user_id: str, reason: str = None) -> bool:
        ...
