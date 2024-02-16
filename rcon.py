import socket
import struct
import logging

from enum import Enum
from dataclasses import dataclass
from typing import Optional

log = logging.getLogger(__name__)


class RCONPacketType(Enum):
    SERVERDATA_AUTH = 3
    SERVERDATA_AUTH_RESPONSE = 2
    SERVERDATA_EXECCOMMAND = 2
    SERVERDATA_RESPONSE_VALUE = 0


@dataclass
class RconPacket:
    # https://developer.valvesoftware.com/wiki/Source_RCON_Protocol#Basic_Packet_Structure
    size: int = None
    id: int = None
    type: RCONPacketType = None
    body: str = None
    terminator: bytes = b"\x00"
    RCON_PACKET_HEADER_LENGTH: int = 12
    RCON_PACKET_TERMINATOR_LENGTH: int = 2

    def pack(self):
        body_encoded = (
            self.body.encode("ascii") + self.terminator
        )  # The packet body field is a null-terminated string encoded in ASCII
        self.size = (
            len(body_encoded) + 10
        )  # Only value that can change is the length of the body, so do len(body) + 10.
        return (
            struct.pack("<iii", self.size, self.id, self.type.value)
            + body_encoded
            + self.terminator
        )

    @staticmethod
    def unpack(packet: bytes):
        if len(packet) < RconPacket.RCON_PACKET_HEADER_LENGTH:
            return RconPacket(size=None, id=None, type=None, body="Invalid packet")

        size, request_id, type = struct.unpack(
            "<iii", packet[: RconPacket.RCON_PACKET_HEADER_LENGTH]
        )
        body = packet[
            RconPacket.RCON_PACKET_HEADER_LENGTH : -RconPacket.RCON_PACKET_TERMINATOR_LENGTH
        ].decode("utf-8", errors="replace")
        return RconPacket(size=size, id=request_id, type=type, body=body)


class SourceRcon:
    def __init__(self, server_ip: str, rcon_port: int, rcon_password: str, timeout: Optional[int] = 10) -> None:
        self.SERVER_IP = server_ip
        self.RCON_PORT = rcon_port
        self.RCON_PASSWORD = rcon_password
        self.timeout = timeout

        self.AUTH_FAILED_RESPONSE = -1

    def create_packet(
        self,
        command: str,
        request_id: int = 1,
        type: RCONPacketType = RCONPacketType.SERVERDATA_EXECCOMMAND,
    ) -> RconPacket:
        packet = RconPacket(id=request_id, type=type, body=command)
        final_packet = packet.pack()

        log.debug(f"Final packet: {final_packet}")
        return final_packet

    def receive_all(self, sock: socket.socket, bytes_in: int = 4096) -> bytes:
        response = b""
        while True:
            try:
                part = sock.recv(bytes_in)
                if not part:
                    break
                response += part
                if len(part) < bytes_in:
                    break
            except socket.error as e:
                log.error(f"Error receiving data: {e}")
                break
        return response

    def check_auth_response(self, auth_response_packet: bytes) -> bool:
        unpacked_packet = RconPacket.unpack(auth_response_packet)

        if (
            unpacked_packet.size is None
            or unpacked_packet.type != RCONPacketType.SERVERDATA_AUTH_RESPONSE.value
        ):
            log.error("Invalid response or wrong packet type.")
            return False

        return unpacked_packet.id != self.AUTH_FAILED_RESPONSE

    def auth_to_rcon(self, socket: socket.socket) -> bool:
        # Create and send rcon authentication packet
        log.debug("Authenticating to server rcon before sending command.")
        auth_packet = self.create_packet(
            self.RCON_PASSWORD, type=RCONPacketType.SERVERDATA_AUTH
        )
        socket.sendall(auth_packet)

        # Get and parse rcon authentication response
        auth_response = self.receive_all(socket)
        if self.check_auth_response(auth_response):
            log.debug("rcon authentication successful.")
            return True
        else:
            log.error("rcon authentication failed.")
            return False

    def establish_connection(self, socket: socket.socket) -> bool:
        try:
            socket.connect((self.SERVER_IP, self.RCON_PORT))
            log.debug("Socket connection successful.")
            return True
        except Exception as e:
            log.error(f"Error while establishing a connection: {e}")
            return False

    def execute_command(self, socket: socket.socket, command: str) -> str:
        command_packet = self.create_packet(command)
        socket.sendall(command_packet)

        response = self.receive_all(socket)
        unpacked_packet = RconPacket.unpack(response)
        log.debug(f"Command response: {unpacked_packet.body}")
        return unpacked_packet.body

    def send_command(self, command: str, args: list = []) -> str:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Set socket connection timeout.
            s.settimeout(self.timeout)
            if not self.establish_connection(s):
                return "Failed to establish connection."

            if not self.auth_to_rcon(s):
                return "Authentication failed. not running command."

            if command.lower() == "broadcast":
                broadcast_msg = args[0]
                # Replace spaces with fake spaces since palworld doesnt parse them correctly.
                fixed_broadcast_msg = broadcast_msg.replace(" ", "\x1F")
                command = f"{command} {fixed_broadcast_msg}"
            else:
                args = " ".join(args)
                command = f"{command} {args}"

            log.debug(f"Sending command: {command}")
            return self.execute_command(s, command)
