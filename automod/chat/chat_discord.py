from . import ChatBase


class ChatDiscord(ChatBase):
    def on_message_received(self, user_id, message):
        pass  # TODO

    def broadcast_message(self, message) -> None:
        pass  # TODO

    def send_message_to(self, user_id, message) -> None:
        pass  # TODO

    def send_ban_req(self, user_id, reason=None) -> bool:
        pass  # TODO

    def send_mute_req(self, user_id: str, reason=None) -> bool:
        pass  # TODO
