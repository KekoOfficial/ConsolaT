# 💀 MP SYSTEM CONFIG v3 (ARCHITECTURE LEVEL)

from dataclasses import dataclass, field
from typing import Dict, List

# =========================
# 🌐 SERVER CONFIG
# =========================
@dataclass
class ServerConfig:
    host: str = "0.0.0.0"
    port: int = 5000
    debug: bool = True
    workers: int = 1
    thread_pool: int = 100


# =========================
# 🔐 AUTH SYSTEM
# =========================
@dataclass
class AuthConfig:
    admin_user: str = "admin"
    admin_pass: str = "1234"

    tokens: Dict[str, str] = field(default_factory=lambda: {
        "master": "MP-MASTER-ULTRA-KEY-V3",
        "api": "MP-API-KEY-V3",
        "socket": "MP-SOCKET-KEY-V3"
    })

    token_required: bool = True
    allow_multi_session: bool = True
    token_expire_minutes: int = 60


# =========================
# 📡 SOCKET CONFIG
# =========================
@dataclass
class SocketConfig:
    cors: str = "*"
    ping_timeout: int = 8
    ping_interval: int = 3
    max_connections: int = 2000
    compression: bool = True
    async_mode: str = "threading"


# =========================
# ⚡ PERFORMANCE ENGINE
# =========================
@dataclass
class PerformanceConfig:
    max_logs: int = 300
    max_private_messages: int = 1000
    max_group_messages: int = 2000
    cache_enabled: bool = True
    ultra_fast_emit: bool = True
    memory_mode: str = "ram"  # ram | hybrid | db-ready


# =========================
# 👤 USER SYSTEM
# =========================
@dataclass
class UserConfig:
    users: Dict[str, dict] = field(default_factory=lambda: {
        "1": {"name": "Usuario A", "role": "user", "online": False},
        "2": {"name": "Usuario B", "role": "mod", "online": False},
        "3": {"name": "Usuario C", "role": "admin", "online": False}
    })


# =========================
# 💬 CHAT SYSTEM
# =========================
@dataclass
class ChatConfig:
    private_enabled: bool = True
    group_enabled: bool = True
    message_limit: int = 1000
    edit_enabled: bool = False
    delete_enabled: bool = True
    realtime: bool = True


# =========================
# 💬 GROUP SYSTEM
# =========================
@dataclass
class GroupConfig:
    groups: Dict[str, dict] = field(default_factory=lambda: {
        "1": {
            "name": "Familia",
            "members": ["1", "2"],
            "messages": [],
            "locked": False,
            "slow_mode": 0
        },
        "2": {
            "name": "Clan Devs",
            "members": ["2", "3"],
            "messages": [],
            "locked": False,
            "slow_mode": 2
        }
    })


# =========================
# 📜 LOG SYSTEM
# =========================
@dataclass
class LogConfig:
    enabled: bool = True
    level: str = "DEBUG"
    max_size: int = 300
    memory_only: bool = True
    show_socket_events: bool = True


# =========================
# ⚡ RATE LIMIT SYSTEM
# =========================
@dataclass
class RateLimitConfig:
    messages_per_minute: int = 30
    block_seconds: int = 60
    warning_threshold: int = 20


# =========================
# 🔥 SECURITY ENGINE
# =========================
@dataclass
class SecurityConfig:
    require_token: bool = True
    block_unauthorized: bool = True
    anti_flood: bool = True
    allow_guests: bool = False
    ip_blacklist: List[str] = field(default_factory=list)


# =========================
# 🧩 FEATURE FLAGS
# =========================
@dataclass
class FeatureFlags:
    private_chat: bool = True
    group_chat: bool = True
    file_upload: bool = False
    voice_messages: bool = False
    ai_bot: bool = False
    admin_panel: bool = False


# =========================
# 🧠 AI ENGINE (FUTURE)
# =========================
@dataclass
class AIConfig:
    enabled: bool = False
    auto_reply: bool = False
    moderation: bool = False


# =========================
# 💀 MASTER CONFIG WRAPPER
# =========================
@dataclass
class Config:
    server: ServerConfig = ServerConfig()
    auth: AuthConfig = AuthConfig()
    socket: SocketConfig = SocketConfig()
    performance: PerformanceConfig = PerformanceConfig()
    users: UserConfig = UserConfig()
    chat: ChatConfig = ChatConfig()
    groups: GroupConfig = GroupConfig()
    logs: LogConfig = LogConfig()
    rate_limit: RateLimitConfig = RateLimitConfig()
    security: SecurityConfig = SecurityConfig()
    features: FeatureFlags = FeatureFlags()
    ai: AIConfig = AIConfig()


# 🚀 SINGLE INSTANCE (IMPORT ESTO EN server.py)
config = Config()