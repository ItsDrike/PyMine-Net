# A flexible and fast Minecraft server software written completely in Python.
# Copyright (C) 2021 PyMine

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Contains packets related to beacons."""

from __future__ import annotations

from pymine.types.packet import ServerBoundPacket
from pymine.types.buffer import Buffer

__all__ = ("PlaySetBeaconEffect",)


class PlaySetBeaconEffect(ServerBoundPacket):
    """Changes the effect of the current beacon. (Client -> Server)

    :param int primary_effect: Description of parameter `primary_effect`.
    :param int secondary_effect: Description of parameter `secondary_effect`.
    :ivar int id: Unique packet ID.
    :ivar primary_effect:
    :ivar secondary_effect:
    """

    id = 0x24

    def __init__(self, primary_effect: int, secondary_effect: int) -> None:
        super().__init__()

        self.primary_effect = primary_effect
        self.secondary_effect = secondary_effect

    @classmethod
    def unpack(cls, buf: Buffer) -> PlaySetBeaconEffect:
        return cls(buf.read_varint(), buf.read_varint())
