"""Contains packets related to the chat."""

from __future__ import annotations

import uuid

from pymine_net.types.packet import ClientBoundPacket, ServerBoundPacket
from pymine_net.types.buffer import Buffer
from pymine_net.types.chat import Chat

__all__ = (
    "PlayChatMessageClientBound",
    "PlayChatMessageServerBound",
    #"PlayTabCompleteClientBound",
    "PlayTabCompleteServerBound",
    #"PlayTitle",
)


class PlayChatMessageClientBound(ClientBoundPacket):
    """A chat message from the server to the client (Server -> Client)

    :param Chat data: The actual chat data.
    :param int position: Where on the GUI the message is to be displayed.
    :param uuid.UUID sender: Unknown, see here: https://wiki.vg/Protocol#Chat_Message_.28clientbound.29.
    :ivar int id: Unique packet ID.
    :ivar data:
    :ivar position:
    :ivar sender:
    """

    id = 0x0F

    def __init__(self, data: Chat, position: int, sender: uuid.UUID):
        super().__init__()

        self.data = data
        self.position = position
        self.sender = sender

    def pack(self) -> Buffer:
        return Buffer().write_chat(self.data).write("b", self.position).write_uuid(self.sender)


class PlayChatMessageServerBound(ServerBoundPacket):
    """A chat message from a client to the server. Can be a command. (Client -> Server)

    :param str message: The raw text sent by the client.
    :ivar int id: Unique packet ID.
    :ivar message:
    """

    id = 0x03

    def __init__(self, message: str):
        super().__init__()

        self.message = message

    @classmethod
    def unpack(cls, buf: Buffer) -> PlayChatMessageServerBound:
        return cls(buf.read_string())


class PlayTabCompleteServerBound(ServerBoundPacket):
    """Used when a client wants to tab complete a chat message. (Client -> Server)

    :param int transaction_id: Number generated by the client.
    :param str text: All text behind/to the left of the cursor.
    :ivar int id: Unique packet ID.
    :ivar transaction_id:
    :ivar text:
    """

    id = 0x06

    def __init__(self, transaction_id: int, text: str) -> None:
        super().__init__()

        self.transaction_id = transaction_id
        self.text = text

    @classmethod
    def unpack(cls, buf: Buffer) -> PlayTabCompleteServerBound:
        return cls(buf.read_varint(), buf.read_string())
