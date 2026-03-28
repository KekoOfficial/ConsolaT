# 💀 MP SYSTEM CLEAN CONFIG (FIXED + STABLE)

# 🌐 SERVER
HOST = "0.0.0.0"
PORT = 5000
DEBUG = True

# 🔐 AUTH
ADMIN_USER = "admin"
ADMIN_PASS = "1234"

# 🔑 API TOKEN
API_TOKEN = "8367475601:AAExk4xLECpm1wqTlJUeAyfzKhxMq7msHio"

# 📡 SOCKET
SOCKET_CORS = "*"

# 👤 USERS
USERS = {
    "1": {"name": "Usuario A"},
    "2": {"name": "Usuario B"},
    "3": {"name": "Usuario C"}
}

# 💬 GROUPS
GROUPS = {
    "1": {
        "name": "Familia",
        "members": ["1", "2"],
        "messages": []
    },
    "2": {
        "name": "Clan Devs",
        "members": ["2", "3"],
        "messages": []
    }
}

# ⚡ PERFORMANCE
MAX_LOGS = 200
MAX_MESSAGES = 1000

# 🔥 SECURITY
REQUIRE_TOKEN = True
ALLOW_GUESTS = False