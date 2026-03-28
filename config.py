from dataclasses import dataclass, field
from typing import Dict, List


# 🌐 SERVER
@dataclass
class ServerConfig:
    host: str = "0.0.0.0"
    port: int = 5000
    debug: bool = True


# 🔐 AUTH
@dataclass
class AuthConfig:
    admin_user: str = "admin"
    admin_pass: str = "1234"
    api_token: str = "8367475601:AAExk4xLECpm1wqTlJUeAyfzKhxMq7msHio"


# 📡 SOCKET
@dataclass
class SocketConfig:
    cors: str = "*"


# 👤 USERS
@dataclass
class UserConfig:
    users: Dict[str, dict] = field(default_factory=lambda: {
        "1": {"name": "Usuario A"},
        "2": {"name": "Usuario B"},
        "3": {"name": "Usuario C"}
    })


# 💬 GROUPS
@dataclass
class GroupConfig:
    groups: Dict[str, dict] = field(default_factory=lambda: {
        "1": {"name": "Familia", "members": ["1", "2"], "messages": []},
        "2": {"name": "Clan Devs", "members": ["2", "3"], "messages": []}
    })


# 💀 MASTER CONFIG
@dataclass
class Config:
    server: ServerConfig = field(default_factory=ServerConfig)
    auth: AuthConfig = field(default_factory=AuthConfig)
    socket: SocketConfig = field(default_factory=SocketConfig)
    users: UserConfig = field(default_factory=UserConfig)
    groups: GroupConfig = field(default_factory=GroupConfig)


config = Config()