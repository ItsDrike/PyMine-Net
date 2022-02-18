"""Contains packets relating to client logins."""

from __future__ import annotations

from uuid import UUID
import secrets

from pymine_net.types.packet import ServerBoundPacket, ClientBoundPacket
from pymine_net.types.buffer import Buffer

__all__ = (
    "LoginStart",
    "LoginEncryptionRequest",
    "LoginEncryptionResponse",
    "LoginSuccess",
    "LoginDisconnect",
)


class LoginStart(ServerBoundPacket):
    """Packet from client asking to start login process. (Client -> Server)

    :param str username: Username of the client who sent the request.
    :ivar int id: Unique packet ID.
    :ivar username:
    """

    id = 0x00

    def __init__(self, username: str) -> None:
        super().__init__()

        self.username = username

    @classmethod
    def decode(cls, buf: Buffer) -> LoginStart:
        return cls(buf.read_string())


class LoginEncryptionRequest(ClientBoundPacket):
    """Used by the server to ask the client to encrypt the login process. (Server -> Client)

    :param bytes public_key: Public key.
    :ivar type verify_token: Verify token, randomly generated.
    :ivar int id: Unique packet ID.
    :ivar public_key:
    """

    id = 0x01

    def __init__(self, public_key: bytes) -> None:  # https://wiki.vg/Protocol#Encryption_Request
        super().__init__()

        self.public_key = public_key
        self.verify_token = secrets.token_bytes(16)

    def encode(self) -> bytes:
        return (
            Buffer.pack_string(" " * 20)
            + Buffer.pack_varint(len(self.public_key))
            + self.public_key
            + Buffer.pack_varint(len(self.verify_token))
            + self.verify_token
        )


class LoginEncryptionResponse(ServerBoundPacket):
    """Response from the client to a LoginEncryptionRequest. (Client -> Server)

    :param bytes shared_key: The shared key used in the login process.
    :param bytes verify_token: The verify token used in the login process.
    :ivar int id: Unique packet ID.
    :ivar shared_key:
    :ivar verify_token:
    """

    id = 0x01

    def __init__(self, shared_key: bytes, verify_token: bytes) -> None:
        super().__init__()

        self.shared_key = shared_key
        self.verify_token = verify_token

    @classmethod
    def decode(cls, buf: Buffer) -> LoginEncryptionResponse:
        return cls(buf.read(buf.unpack_varint()), buf.read(buf.unpack_varint()))


class LoginSuccess(ClientBoundPacket):
    """Sent by the server to denote a successfull login. (Server -> Client)

    :param UUID uuid: The UUID of the connecting player/client.
    :param str username: The username of the connecting player/client.
    :ivar int id: Unique packet ID.
    :ivar uuid:
    :ivar username:
    """

    id = 0x02

    def __init__(self, uuid: UUID, username: str) -> None:
        super().__init__()

        self.uuid = uuid
        self.username = username

    def encode(self) -> bytes:
        return Buffer().write_uuid(self.uuid).write_string(self.username)


class LoginDisconnect(ClientBoundPacket):
    """Sent by the server to kick a player while in the login state. (Server -> Client)

    :param str reason: The reason for the disconnect.
    :ivar int id: Unique packet ID.
    :ivar username:
    """

    id = 0x00

    def __init__(self, reason: str) -> None:
        super().__init__()

        self.reason = reason

    def encode(self) -> bytes:
        return Buffer.pack_chat(Chat(self.reason))
