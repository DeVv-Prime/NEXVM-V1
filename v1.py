#!/usr/bin/env python3
# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║                                                                                               ║
# ║     ███████╗██╗   ██╗███╗   ███╗███████╗    ██████╗  ██████╗ ████████╗                      ║
# ║     ██╔════╝██║   ██║████╗ ████║██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝                      ║
# ║     ███████╗██║   ██║██╔████╔██║█████╗      ██████╔╝██║   ██║   ██║                         ║
# ║     ╚════██║╚██╗ ██╔╝██║╚██╔╝██║██╔══╝      ██╔══██╗██║   ██║   ██║                         ║
# ║     ███████║ ╚████╔╝ ██║ ╚═╝ ██║███████╗    ██████╔╝╚██████╔╝   ██║                         ║
# ║     ╚══════╝  ╚═══╝  ╚═╝     ╚═╝╚══════╝    ╚═════╝  ╚═════╝    ╚═╝                         ║
# ║                                                                                               ║
# ║                    🚀 COMPLETE VPS MANAGEMENT BOT - ULTIMATE EDITION 🚀                      ║
# ║                                                                                               ║
# ║                         ████████╗ ██████╗  ██████╗ ██╗     ███████╗                          ║
# ║                         ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔════╝                          ║
# ║                            ██║   ██║   ██║██║   ██║██║     █████╗                            ║
# ║                            ██║   ██║   ██║██║   ██║██║     ██╔══╝                            ║
# ║                            ██║   ╚██████╔╝╚██████╔╝███████╗███████╗                          ║
# ║                            ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚══════╝                          ║
# ║                                                                                               ║
# ║                         Made by Ankit-Dev with ❤️ - Version 5.0.0                            ║
# ║                    ALL ISSUES FIXED • DATABASE FIXED • ALL COMMANDS WORKING                  ║
# ║                                                                                               ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

import discord
from discord.ext import commands, tasks
from discord.ui import Modal, InputText, View, Button, Select
import asyncio
import json
import os
import random
import string
import subprocess
import sys
import re
import sqlite3
import logging
import shlex
import shutil
import time
import aiohttp
import psutil
import netifaces
import socket
import requests
import hashlib
import base64
import uuid
import qrcode
import io
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple
from contextlib import closing
from functools import wraps

# Make sure you have a variable or list for your Admin IDs
ADMIN_IDS = [1405866008127864852]  # <-- Replace with your actual Telegram User ID

def admin_only():
    def decorator(func):
        @wraps(func)
        async def wrapper(update, context, *args, **kwargs):
            user_id = update.effective_user.id
            if user_id not in ADMIN_IDS:
                await update.message.reply_text("❌ This command is restricted to admins.")
                return
            return await func(update, context, *args, **kwargs)
        return wrapper
    return decorator
    
# ==================================================================================================
#  📝  LOGGING SETUP - FIXED (Moved before database to avoid import issues)
# ==================================================================================================

# Create logs directory
os.makedirs('/opt/svm5-bot/logs', exist_ok=True)
os.makedirs('/opt/svm5-bot/data', exist_ok=True)
os.makedirs('/opt/svm5-bot/backups', exist_ok=True)
os.makedirs('/opt/svm5-bot/qr_codes', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('/opt/svm5-bot/logs/svm5.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SVM5-BOT")

# ==================================================================================================
#  ⚙️  CONFIGURATION SECTION
# ==================================================================================================

# 🔑 Discord Bot Configuration
BOT_TOKEN = ""           # Get from Discord Developer Portal
BOT_PREFIX = "."                                      # Command prefix
BOT_NAME = "SVM5-BOT"                                 # Bot display name
BOT_AUTHOR = "Ankit-Dev"                              # Your name
MAIN_ADMIN_IDS = [1405866008127864852]                # Your Discord User ID

# 🖥️ Server Configuration
DEFAULT_STORAGE_POOL = "default"                      # LXC storage pool
SERVER_HOSTNAME = socket.gethostname()                # Auto-detected hostname

# 🌐 Auto-detect Server Public IP
try:
    SERVER_IP = requests.get('https://api.ipify.org', timeout=5).text.strip()
    logger.info(f"✅ Auto-detected public IP: {SERVER_IP}")
except:
    try:
        SERVER_IP = subprocess.getoutput("curl -s ifconfig.me")
        logger.info(f"✅ Auto-detected public IP: {SERVER_IP}")
    except:
        SERVER_IP = "13.208.181.149"
        logger.warning(f"⚠️ Could not auto-detect IP, using fallback: {SERVER_IP}")

# 🔌 Get MAC Address
def get_mac_address():
    try:
        interfaces = netifaces.interfaces()
        for iface in interfaces:
            if iface != 'lo':
                addr = netifaces.ifaddresses(iface)
                if netifaces.AF_LINK in addr:
                    return addr[netifaces.AF_LINK][0]['addr']
    except:
        pass
    return "00:00:00:00:00:00"

MAC_ADDRESS = get_mac_address()

# 💰 UPI Payment Configuration
UPI_ID = "9892642904@ybl"                            # Your UPI ID
UPI_NAME = "Ankit-Dev"                                # Your name for UPI
IPV4_PRICE_INR = 50                                   # Price per IPv4 in INR

# 🤖 AI Configuration - UPDATED WORKING MODEL
AI_API_KEY = "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"
AI_MODEL = "llama-3.3-70b-versatile"                  # ✅ WORKING MODEL

# 🖼️ Thumbnail URL for embeds
THUMBNAIL_URL = "https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg"

# 🔐 License Keys
VALID_LICENSE_KEYS = [
    "AnkitDev99$@", 
    "SVM5-PRO-2025", 
    "SVM5-ENTERPRISE", 
    "DEVELOPER-ANKIT",
    "PREMIUM-2025",
    "ULTIMATE-2025"
]

# 💎 Free VPS Plans
FREE_VPS_PLANS = {
    'invites': [
        {'name': '🥉 Bronze Plan', 'invites': 5, 'ram': 2, 'cpu': 1, 'disk': 20, 'emoji': '🥉'},
        {'name': '🥈 Silver Plan', 'invites': 10, 'ram': 4, 'cpu': 2, 'disk': 40, 'emoji': '🥈'},
        {'name': '🥇 Gold Plan', 'invites': 15, 'ram': 8, 'cpu': 4, 'disk': 80, 'emoji': '🥇'},
        {'name': '🏆 Platinum Plan', 'invites': 20, 'ram': 16, 'cpu': 8, 'disk': 160, 'emoji': '🏆'},
        {'name': '💎 Diamond Plan', 'invites': 25, 'ram': 32, 'cpu': 16, 'disk': 320, 'emoji': '💎'},
        {'name': '👑 Royal Plan', 'invites': 30, 'ram': 64, 'cpu': 32, 'disk': 640, 'emoji': '👑'},
        {'name': '⚡ Legendary Plan', 'invites': 40, 'ram': 128, 'cpu': 64, 'disk': 1280, 'emoji': '⚡'},
    ]
}

# 🐧 OS Options
OS_OPTIONS = [
    {"label": "🐧 Ubuntu 20.04 LTS", "value": "ubuntu:20.04", "desc": "Focal Fossa - Stable LTS", "emoji": "🐧"},
    {"label": "🐧 Ubuntu 22.04 LTS", "value": "ubuntu:22.04", "desc": "Jammy Jellyfish - Current LTS", "emoji": "🐧"},
    {"label": "🐧 Ubuntu 24.04 LTS", "value": "ubuntu:24.04", "desc": "Noble Numbat - Latest LTS", "emoji": "🐧"},
    {"label": "🌀 Debian 11", "value": "images:debian/11", "desc": "Bullseye - Old Stable", "emoji": "🌀"},
    {"label": "🌀 Debian 12", "value": "images:debian/12", "desc": "Bookworm - Current Stable", "emoji": "🌀"},
    {"label": "🌀 Debian 13", "value": "images:debian/13", "desc": "Trixie - Testing", "emoji": "🌀"},
    {"label": "🎩 Fedora 39", "value": "images:fedora/39", "desc": "Fedora 39", "emoji": "🎩"},
    {"label": "🎩 Fedora 40", "value": "images:fedora/40", "desc": "Fedora 40 - Latest", "emoji": "🎩"},
    {"label": "🎩 Fedora 41", "value": "images:fedora/41", "desc": "Fedora 41 - Development", "emoji": "🎩"},
    {"label": "🦊 Rocky Linux 8", "value": "images:rockylinux/8", "desc": "Rocky 8 - Enterprise", "emoji": "🦊"},
    {"label": "🦊 Rocky Linux 9", "value": "images:rockylinux/9", "desc": "Rocky 9 - Latest", "emoji": "🦊"},
    {"label": "🦊 AlmaLinux 8", "value": "images:almalinux/8", "desc": "Alma 8 - RHEL Compatible", "emoji": "🦊"},
    {"label": "🦊 AlmaLinux 9", "value": "images:almalinux/9", "desc": "Alma 9 - Latest", "emoji": "🦊"},
    {"label": "📦 CentOS 7", "value": "images:centos/7", "desc": "CentOS 7 - Legacy", "emoji": "📦"},
    {"label": "📦 CentOS 8", "value": "images:centos/8", "desc": "CentOS 8 - Stream", "emoji": "📦"},
    {"label": "📦 CentOS 9", "value": "images:centos/9", "desc": "CentOS 9 - Stream", "emoji": "📦"},
    {"label": "🔴 Red Hat 8", "value": "images:rhel/8", "desc": "RHEL 8 - Enterprise", "emoji": "🔴"},
    {"label": "🔴 Red Hat 9", "value": "images:rhel/9", "desc": "RHEL 9 - Latest", "emoji": "🔴"},
    {"label": "🐧 Alpine 3.18", "value": "images:alpine/3.18", "desc": "Alpine - Lightweight", "emoji": "🐧"},
    {"label": "🐧 Alpine 3.19", "value": "images:alpine/3.19", "desc": "Alpine - Latest", "emoji": "🐧"},
    {"label": "🐧 Alpine 3.20", "value": "images:alpine/3.20", "desc": "Alpine - Edge", "emoji": "🐧"},
    {"label": "📀 Arch Linux", "value": "images:archlinux", "desc": "Arch - Rolling Release", "emoji": "📀"},
    {"label": "💻 Gentoo", "value": "images:gentoo", "desc": "Gentoo - Source based", "emoji": "💻"},
    {"label": "🔵 FreeBSD 13", "value": "images:freebsd/13", "desc": "FreeBSD 13 - Unix", "emoji": "🔵"},
    {"label": "🔵 FreeBSD 14", "value": "images:freebsd/14", "desc": "FreeBSD 14 - Latest", "emoji": "🔵"},
    {"label": "🟢 OpenSUSE 15.5", "value": "images:opensuse/15.5", "desc": "OpenSUSE Leap", "emoji": "🟢"},
    {"label": "🟢 OpenSUSE Tumbleweed", "value": "images:opensuse/tumbleweed", "desc": "OpenSUSE Rolling", "emoji": "🟢"},
    {"label": "🟣 Kali Linux", "value": "images:kali", "desc": "Kali - Security", "emoji": "🟣"},
    {"label": "⚪ Void Linux", "value": "images:voidlinux", "desc": "Void - Independent", "emoji": "⚪"},
]

# ==================================================================================================
#  🗄️  DATABASE SETUP - FIXED (Connection handling)
# ==================================================================================================

DATABASE_PATH = '/opt/svm5-bot/data/svm5.db'

def get_db():
    """Get database connection with proper error handling"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logger.error(f"Database connection error: {e}")
        return None

def init_db():
    """Initialize database with all tables - FIXED connection handling"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            logger.error("Failed to connect to database")
            return False
        
        cur = conn.cursor()
        
        # 👑 Admins table
        cur.execute('''CREATE TABLE IF NOT EXISTS admins (
            user_id TEXT PRIMARY KEY,
            added_by TEXT,
            added_at TEXT,
            permissions TEXT DEFAULT 'all'
        )''')
        
        # Add main admin
        for admin_id in MAIN_ADMIN_IDS:
            cur.execute('INSERT OR IGNORE INTO admins (user_id, added_at) VALUES (?, ?)', 
                       (str(admin_id), datetime.now().isoformat()))
        
        # 🖥️ VPS table
        cur.execute('''CREATE TABLE IF NOT EXISTS vps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            container_name TEXT UNIQUE NOT NULL,
            plan_name TEXT DEFAULT 'Custom',
            ram INTEGER NOT NULL,
            cpu INTEGER NOT NULL,
            disk INTEGER NOT NULL,
            os_version TEXT DEFAULT 'ubuntu:22.04',
            status TEXT DEFAULT 'stopped',
            suspended INTEGER DEFAULT 0,
            suspended_reason TEXT DEFAULT '',
            purge_protected INTEGER DEFAULT 0,
            node_name TEXT DEFAULT 'local',
            created_at TEXT NOT NULL,
            last_started TEXT,
            last_stopped TEXT,
            ip_address TEXT,
            mac_address TEXT,
            backup_enabled INTEGER DEFAULT 0,
            backup_frequency TEXT DEFAULT 'daily',
            last_backup TEXT,
            notes TEXT
        )''')
        
        # 🌐 Nodes table
        cur.execute('''CREATE TABLE IF NOT EXISTS nodes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            host TEXT NOT NULL,
            port INTEGER DEFAULT 22,
            username TEXT NOT NULL,
            password TEXT,
            ssh_key TEXT,
            status TEXT DEFAULT 'offline',
            total_ram INTEGER DEFAULT 0,
            used_ram INTEGER DEFAULT 0,
            total_cpu INTEGER DEFAULT 0,
            used_cpu REAL DEFAULT 0,
            total_disk INTEGER DEFAULT 0,
            used_disk INTEGER DEFAULT 0,
            lxc_count INTEGER DEFAULT 0,
            api_key TEXT UNIQUE,
            api_url TEXT,
            region TEXT DEFAULT 'us',
            last_checked TEXT,
            added_by TEXT,
            added_at TEXT NOT NULL,
            description TEXT
        )''')
        
        # 📊 User stats table
        cur.execute('''CREATE TABLE IF NOT EXISTS user_stats (
            user_id TEXT PRIMARY KEY,
            invites INTEGER DEFAULT 0,
            boosts INTEGER DEFAULT 0,
            claimed_vps_count INTEGER DEFAULT 0,
            total_spent INTEGER DEFAULT 0,
            api_key TEXT UNIQUE,
            last_updated TEXT
        )''')
        
        # ⚙️ Settings table
        cur.execute('''CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            description TEXT,
            updated_at TEXT
        )''')
        
        # 💳 Transactions table
        cur.execute('''CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            txn_ref TEXT UNIQUE NOT NULL,
            txn_id TEXT,
            amount INTEGER,
            currency TEXT DEFAULT 'INR',
            payment_method TEXT DEFAULT 'UPI',
            status TEXT DEFAULT 'pending',
            purpose TEXT DEFAULT 'ipv4',
            created_at TEXT NOT NULL,
            verified_at TEXT,
            verified_by TEXT,
            notes TEXT
        )''')
        
        # 🌍 IPv4 allocations
        cur.execute('''CREATE TABLE IF NOT EXISTS ipv4 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            container_name TEXT NOT NULL,
            public_ip TEXT,
            private_ip TEXT,
            mac_address TEXT,
            gateway TEXT,
            netmask TEXT,
            interface TEXT,
            node_name TEXT DEFAULT 'local',
            tunnel_url TEXT,
            tunnel_id TEXT,
            assigned_at TEXT NOT NULL,
            expires_at TEXT,
            auto_renew INTEGER DEFAULT 1,
            UNIQUE(user_id, container_name)
        )''')
        
        # 🔌 Port forwards
        cur.execute('''CREATE TABLE IF NOT EXISTS port_forwards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            container_name TEXT NOT NULL,
            container_port INTEGER NOT NULL,
            host_port INTEGER UNIQUE NOT NULL,
            protocol TEXT DEFAULT 'tcp+udp',
            node_name TEXT DEFAULT 'local',
            created_at TEXT NOT NULL,
            description TEXT
        )''')
        
        # 📦 Port allocations
        cur.execute('''CREATE TABLE IF NOT EXISTS port_allocations (
            user_id TEXT PRIMARY KEY,
            allocated_ports INTEGER DEFAULT 0,
            used_ports INTEGER DEFAULT 0,
            last_updated TEXT
        )''')
        
        # ⛔ Suspension logs
        cur.execute('''CREATE TABLE IF NOT EXISTS suspension_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            container_name TEXT NOT NULL,
            user_id TEXT NOT NULL,
            action TEXT NOT NULL,
            reason TEXT,
            admin_id TEXT,
            created_at TEXT NOT NULL
        )''')
        
        # 💾 Snapshots
        cur.execute('''CREATE TABLE IF NOT EXISTS snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            container_name TEXT NOT NULL,
            snapshot_name TEXT NOT NULL,
            size_mb INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            UNIQUE(container_name, snapshot_name)
        )''')
        
        # 🤖 AI chat history
        cur.execute('''CREATE TABLE IF NOT EXISTS ai_history (
            user_id TEXT PRIMARY KEY,
            messages TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )''')
        
        # 🔐 License table
        cur.execute('''CREATE TABLE IF NOT EXISTS license (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            license_key TEXT NOT NULL,
            activated_at TEXT NOT NULL,
            activated_by TEXT,
            mac_address TEXT,
            hostname TEXT,
            ip_address TEXT,
            expires_at TEXT
        )''')
        
        # 📦 Panel installations
        cur.execute('''CREATE TABLE IF NOT EXISTS panels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            panel_type TEXT NOT NULL,
            panel_url TEXT,
            admin_user TEXT,
            admin_pass TEXT,
            admin_email TEXT,
            node_name TEXT DEFAULT 'local',
            container_name TEXT,
            tunnel_url TEXT,
            installed_at TEXT NOT NULL,
            last_accessed TEXT
        )''')
        
        # 📋 Invite tracking
        cur.execute('''CREATE TABLE IF NOT EXISTS invites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inviter_id TEXT NOT NULL,
            invited_id TEXT NOT NULL,
            joined_at TEXT NOT NULL,
            rewarded INTEGER DEFAULT 0,
            UNIQUE(invited_id)
        )''')
        
        # 💰 UPI Configuration
        cur.execute('''CREATE TABLE IF NOT EXISTS upi_config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            upi_id TEXT NOT NULL,
            upi_name TEXT,
            qr_code_path TEXT,
            payment_link TEXT,
            is_active INTEGER DEFAULT 1,
            updated_by TEXT,
            updated_at TEXT
        )''')
        
        # 🚀 Initialize default settings
        settings_init = [
            ('cpu_threshold', '90', 'CPU usage threshold for alerts'),
            ('ram_threshold', '90', 'RAM usage threshold for alerts'),
            ('disk_threshold', '90', 'Disk usage threshold for alerts'),
            ('maintenance_mode', 'false', 'Maintenance mode status'),
            ('bot_version', '5.0.0', 'Bot version'),
            ('bot_status', 'online', 'Bot status'),
            ('bot_activity', 'watching', 'Bot activity type'),
            ('bot_activity_name', f'{BOT_NAME} VPS Manager', 'Bot activity text'),
            ('license_verified', 'false', 'License verification status'),
            ('server_ip', SERVER_IP, 'Server public IP'),
            ('mac_address', MAC_ADDRESS, 'Server MAC address'),
            ('hostname', BOT_NAME, 'Server hostname'),
            ('total_vps_created', '0', 'Total VPS created'),
            ('total_panels_installed', '0', 'Total panels installed'),
            ('total_nodes', '0', 'Total nodes added'),
            ('total_transactions', '0', 'Total transactions'),
            ('default_port_quota', '5', 'Default port quota for new users'),
            ('allow_free_vps', 'true', 'Allow free VPS claiming'),
            ('require_invites', 'true', 'Require invites for free VPS'),
            ('maintenance_message', 'Bot is under maintenance', 'Maintenance mode message'),
            ('welcome_message', 'Welcome to SVM5-BOT!', 'Welcome message'),
            ('default_node', 'local', 'Default node name'),
            ('upi_id', UPI_ID, 'Default UPI ID'),
            ('upi_name', UPI_NAME, 'UPI account name'),
        ]
        
        for key, value, desc in settings_init:
            cur.execute('INSERT OR IGNORE INTO settings (key, value, description) VALUES (?, ?, ?)', 
                       (key, value, desc))
        
        # Insert default UPI config
        cur.execute('''INSERT OR IGNORE INTO upi_config (upi_id, upi_name, is_active, updated_at) 
                       VALUES (?, ?, 1, ?)''', (UPI_ID, UPI_NAME, datetime.now().isoformat()))
        
        conn.commit()
        logger.info("✅ Database initialized successfully with all tables")
        return True
        
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")
        return False
    finally:
        if conn:
            conn.close()

# Initialize database with error handling
if not init_db():
    logger.error("Failed to initialize database. Exiting.")
    sys.exit(1)

# ==================================================================================================
#  📊  DATABASE HELPER FUNCTIONS
# ==================================================================================================

def get_setting(key: str, default: Any = None) -> Any:
    """Get a setting value"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return default
        cur = conn.cursor()
        cur.execute('SELECT value FROM settings WHERE key = ?', (key,))
        row = cur.fetchone()
        return row[0] if row else default
    except sqlite3.Error as e:
        logger.error(f"Error getting setting {key}: {e}")
        return default
    finally:
        if conn:
            conn.close()

def set_setting(key: str, value: str):
    """Set a setting value"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute('INSERT OR REPLACE INTO settings (key, value, updated_at) VALUES (?, ?, ?)',
                    (key, value, datetime.now().isoformat()))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error setting {key}: {e}")
    finally:
        if conn:
            conn.close()

def increment_setting(key: str):
    """Increment a numeric setting"""
    current = int(get_setting(key, '0'))
    set_setting(key, str(current + 1))

def get_user_vps(user_id: str) -> List[Dict]:
    """Get all VPS for a user"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute('SELECT * FROM vps WHERE user_id = ? ORDER BY id', (user_id,))
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Error getting user VPS: {e}")
        return []
    finally:
        if conn:
            conn.close()

def get_all_vps() -> List[Dict]:
    """Get all VPS from all users"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute('SELECT * FROM vps ORDER BY user_id, id')
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Error getting all VPS: {e}")
        return []
    finally:
        if conn:
            conn.close()

def add_vps(user_id: str, container_name: str, ram: int, cpu: int, disk: int, 
            os_version: str, plan_name: str = "Custom") -> Optional[Dict]:
    """Add a new VPS to database"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return None
        cur = conn.cursor()
        now = datetime.now().isoformat()
        
        cur.execute('''INSERT INTO vps 
                       (user_id, container_name, plan_name, ram, cpu, disk, os_version, status, created_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (user_id, container_name, plan_name, ram, cpu, disk, os_version, 'running', now))
        vps_id = cur.lastrowid
        conn.commit()
        
        increment_setting('total_vps_created')
        
        cur.execute('SELECT * FROM vps WHERE id = ?', (vps_id,))
        vps = dict(cur.fetchone())
        return vps
    except sqlite3.Error as e:
        logger.error(f"Error adding VPS: {e}")
        return None
    finally:
        if conn:
            conn.close()

def update_vps_status(container_name: str, status: str):
    """Update VPS status"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return
        cur = conn.cursor()
        now = datetime.now().isoformat()
        if status == 'running':
            cur.execute('UPDATE vps SET status = ?, last_started = ? WHERE container_name = ?', 
                       (status, now, container_name))
        elif status == 'stopped':
            cur.execute('UPDATE vps SET status = ?, last_stopped = ? WHERE container_name = ?', 
                       (status, now, container_name))
        else:
            cur.execute('UPDATE vps SET status = ? WHERE container_name = ?', (status, container_name))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error updating VPS status: {e}")
    finally:
        if conn:
            conn.close()

def delete_vps(container_name: str) -> bool:
    """Delete VPS from database"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return False
        cur = conn.cursor()
        cur.execute('DELETE FROM vps WHERE container_name = ?', (container_name,))
        cur.execute('DELETE FROM ipv4 WHERE container_name = ?', (container_name,))
        cur.execute('DELETE FROM port_forwards WHERE container_name = ?', (container_name,))
        cur.execute('DELETE FROM snapshots WHERE container_name = ?', (container_name,))
        conn.commit()
        return cur.rowcount > 0
    except sqlite3.Error as e:
        logger.error(f"Error deleting VPS: {e}")
        return False
    finally:
        if conn:
            conn.close()

def get_admins() -> List[str]:
    """Get all admin IDs"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute('SELECT user_id FROM admins')
        rows = cur.fetchall()
        return [row['user_id'] for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Error getting admins: {e}")
        return []
    finally:
        if conn:
            conn.close()

def is_admin(user_id: str) -> bool:
    """Check if user is admin"""
    return user_id in get_admins() or user_id in [str(a) for a in MAIN_ADMIN_IDS]

def add_admin(user_id: str, added_by: str = "system"):
    """Add a new admin"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute('INSERT OR IGNORE INTO admins (user_id, added_by, added_at) VALUES (?, ?, ?)',
                   (user_id, added_by, datetime.now().isoformat()))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error adding admin: {e}")
    finally:
        if conn:
            conn.close()

def remove_admin(user_id: str):
    """Remove an admin"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute('DELETE FROM admins WHERE user_id = ?', (user_id,))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error removing admin: {e}")
    finally:
        if conn:
            conn.close()

def get_user_stats(user_id: str) -> Dict:
    """Get user statistics"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return {'user_id': user_id, 'invites': 0, 'boosts': 0, 'claimed_vps_count': 0, 'api_key': None}
        cur = conn.cursor()
        cur.execute('SELECT * FROM user_stats WHERE user_id = ?', (user_id,))
        row = cur.fetchone()
        if row:
            return dict(row)
        return {'user_id': user_id, 'invites': 0, 'boosts': 0, 'claimed_vps_count': 0, 'api_key': None}
    except sqlite3.Error as e:
        logger.error(f"Error getting user stats: {e}")
        return {'user_id': user_id, 'invites': 0, 'boosts': 0, 'claimed_vps_count': 0, 'api_key': None}
    finally:
        if conn:
            conn.close()

def update_user_stats(user_id: str, invites: int = 0, boosts: int = 0, claimed_vps_count: int = 0):
    """Update user statistics"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return
        cur = conn.cursor()
        # Generate API key if not exists
        cur.execute('SELECT api_key FROM user_stats WHERE user_id = ?', (user_id,))
        row = cur.fetchone()
        api_key = row['api_key'] if row and row['api_key'] else hashlib.sha256(f"{user_id}{time.time()}".encode()).hexdigest()[:16]
        
        cur.execute('''INSERT OR REPLACE INTO user_stats 
                       (user_id, invites, boosts, claimed_vps_count, api_key, last_updated) 
                       VALUES (?, 
                               COALESCE((SELECT invites FROM user_stats WHERE user_id = ?), 0) + ?, 
                               COALESCE((SELECT boosts FROM user_stats WHERE user_id = ?), 0) + ?,
                               COALESCE((SELECT claimed_vps_count FROM user_stats WHERE user_id = ?), 0) + ?,
                               ?,
                               ?)''',
                    (user_id, user_id, invites, user_id, boosts, user_id, claimed_vps_count, 
                     api_key, datetime.now().isoformat()))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error updating user stats: {e}")
    finally:
        if conn:
            conn.close()

def get_user_api_key(user_id: str) -> str:
    """Get or generate user API key"""
    stats = get_user_stats(user_id)
    if stats.get('api_key'):
        return stats['api_key']
    
    # Generate new API key
    api_key = hashlib.sha256(f"{user_id}{time.time()}{random.randint(1000,9999)}".encode()).hexdigest()[:16]
    conn = None
    try:
        conn = get_db()
        if not conn:
            return api_key
        cur = conn.cursor()
        cur.execute('UPDATE user_stats SET api_key = ?, last_updated = ? WHERE user_id = ?',
                   (api_key, datetime.now().isoformat(), user_id))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error updating API key: {e}")
    finally:
        if conn:
            conn.close()
    return api_key

def add_transaction(user_id: str, txn_ref: str, amount: int) -> Optional[int]:
    """Add a new transaction"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return None
        cur = conn.cursor()
        now = datetime.now().isoformat()
        cur.execute('''INSERT INTO transactions (user_id, txn_ref, amount, created_at)
                       VALUES (?, ?, ?, ?)''', (user_id, txn_ref, amount, now))
        txn_id = cur.lastrowid
        conn.commit()
        increment_setting('total_transactions')
        return txn_id
    except sqlite3.Error as e:
        logger.error(f"Error adding transaction: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_pending_transactions() -> List[Dict]:
    """Get all pending transactions"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute('SELECT * FROM transactions WHERE status = "pending" ORDER BY created_at')
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Error getting pending transactions: {e}")
        return []
    finally:
        if conn:
            conn.close()

def verify_transaction(txn_ref: str, txn_id: str, verified_by: str = "") -> bool:
    """Verify a transaction"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return False
        cur = conn.cursor()
        now = datetime.now().isoformat()
        cur.execute('''UPDATE transactions SET status = 'verified', txn_id = ?, verified_at = ?, verified_by = ?
                       WHERE txn_ref = ? AND status = 'pending' ''', (txn_id, now, verified_by, txn_ref))
        verified = cur.rowcount > 0
        conn.commit()
        return verified
    except sqlite3.Error as e:
        logger.error(f"Error verifying transaction: {e}")
        return False
    finally:
        if conn:
            conn.close()

def add_ipv4(user_id: str, container_name: str, public_ip: str, private_ip: str, 
             mac_address: str = "", gateway: str = "", netmask: str = "", 
             interface: str = "eth0", node_name: str = "local", tunnel_url: str = ""):
    """Add IPv4 allocation"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return
        cur = conn.cursor()
        now = datetime.now().isoformat()
        tunnel_id = str(uuid.uuid4())[:8] if tunnel_url else None
        cur.execute('''INSERT OR REPLACE INTO ipv4 
                       (user_id, container_name, public_ip, private_ip, mac_address, gateway, netmask, interface, node_name, tunnel_url, tunnel_id, assigned_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                    (user_id, container_name, public_ip, private_ip, mac_address, gateway, netmask, interface, node_name, tunnel_url, tunnel_id, now))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error adding IPv4: {e}")
    finally:
        if conn:
            conn.close()

def get_user_ipv4(user_id: str) -> List[Dict]:
    """Get all IPv4 for a user"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute('SELECT * FROM ipv4 WHERE user_id = ?', (user_id,))
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Error getting user IPv4: {e}")
        return []
    finally:
        if conn:
            conn.close()

def remove_ipv4(user_id: str, container_name: str = None):
    """Remove IPv4 allocation"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return
        cur = conn.cursor()
        if container_name:
            cur.execute('DELETE FROM ipv4 WHERE user_id = ? AND container_name = ?', (user_id, container_name))
        else:
            cur.execute('DELETE FROM ipv4 WHERE user_id = ?', (user_id,))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error removing IPv4: {e}")
    finally:
        if conn:
            conn.close()

def get_port_allocation(user_id: str) -> int:
    """Get user's port quota"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return 0
        cur = conn.cursor()
        cur.execute('SELECT allocated_ports FROM port_allocations WHERE user_id = ?', (user_id,))
        row = cur.fetchone()
        return row[0] if row else int(get_setting('default_port_quota', '5'))
    except sqlite3.Error as e:
        logger.error(f"Error getting port allocation: {e}")
        return int(get_setting('default_port_quota', '5'))
    finally:
        if conn:
            conn.close()

def set_port_allocation(user_id: str, amount: int):
    """Set user's port quota"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute('INSERT OR REPLACE INTO port_allocations (user_id, allocated_ports, last_updated) VALUES (?, ?, ?)',
                    (user_id, amount, datetime.now().isoformat()))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error setting port allocation: {e}")
    finally:
        if conn:
            conn.close()

def add_port_allocation(user_id: str, amount: int):
    """Add to user's port quota"""
    current = get_port_allocation(user_id)
    set_port_allocation(user_id, current + amount)

def get_user_port_forwards(user_id: str) -> List[Dict]:
    """Get all port forwards for a user"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute('SELECT * FROM port_forwards WHERE user_id = ? ORDER BY created_at', (user_id,))
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Error getting port forwards: {e}")
        return []
    finally:
        if conn:
            conn.close()

def add_port_forward(user_id: str, container_name: str, container_port: int, host_port: int, protocol: str = "tcp+udp") -> Optional[int]:
    """Add a port forward"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return None
        cur = conn.cursor()
        now = datetime.now().isoformat()
        cur.execute('''INSERT INTO port_forwards (user_id, container_name, container_port, host_port, protocol, created_at)
                       VALUES (?, ?, ?, ?, ?, ?)''', (user_id, container_name, container_port, host_port, protocol, now))
        pf_id = cur.lastrowid
        conn.commit()
        return pf_id
    except sqlite3.Error as e:
        logger.error(f"Error adding port forward: {e}")
        return None
    finally:
        if conn:
            conn.close()

def remove_port_forward(pf_id: int) -> Tuple[bool, str, int]:
    """Remove a port forward"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return False, "", 0
        cur = conn.cursor()
        cur.execute('SELECT user_id, container_name, host_port FROM port_forwards WHERE id = ?', (pf_id,))
        row = cur.fetchone()
        if not row:
            return False, "", 0
        user_id, container_name, host_port = row['user_id'], row['container_name'], row['host_port']
        cur.execute('DELETE FROM port_forwards WHERE id = ?', (pf_id,))
        conn.commit()
        return True, container_name, host_port
    except sqlite3.Error as e:
        logger.error(f"Error removing port forward: {e}")
        return False, "", 0
    finally:
        if conn:
            conn.close()

def log_suspension(container_name: str, user_id: str, action: str, reason: str = "", admin_id: str = ""):
    """Log a suspension action"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return
        cur = conn.cursor()
        now = datetime.now().isoformat()
        cur.execute('''INSERT INTO suspension_logs (container_name, user_id, action, reason, admin_id, created_at)
                       VALUES (?, ?, ?, ?, ?, ?)''', (container_name, user_id, action, reason, admin_id, now))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error logging suspension: {e}")
    finally:
        if conn:
            conn.close()

def add_snapshot(user_id: str, container_name: str, snapshot_name: str):
    """Add a snapshot record"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return
        cur = conn.cursor()
        now = datetime.now().isoformat()
        cur.execute('''INSERT OR REPLACE INTO snapshots (user_id, container_name, snapshot_name, created_at)
                       VALUES (?, ?, ?, ?)''', (user_id, container_name, snapshot_name, now))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error adding snapshot: {e}")
    finally:
        if conn:
            conn.close()

def get_snapshots(container_name: str = None) -> List[Dict]:
    """Get snapshots"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return []
        cur = conn.cursor()
        if container_name:
            cur.execute('SELECT * FROM snapshots WHERE container_name = ? ORDER BY created_at DESC', (container_name,))
        else:
            cur.execute('SELECT * FROM snapshots ORDER BY created_at DESC LIMIT 50')
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Error getting snapshots: {e}")
        return []
    finally:
        if conn:
            conn.close()

def save_ai_history(user_id: str, messages: List[Dict]):
    """Save AI chat history"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return
        cur = conn.cursor()
        now = datetime.now().isoformat()
        cur.execute('''INSERT OR REPLACE INTO ai_history (user_id, messages, updated_at)
                       VALUES (?, ?, ?)''', (user_id, json.dumps(messages), now))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error saving AI history: {e}")
    finally:
        if conn:
            conn.close()

def load_ai_history(user_id: str) -> List[Dict]:
    """Load AI chat history"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute('SELECT messages FROM ai_history WHERE user_id = ?', (user_id,))
        row = cur.fetchone()
        if row:
            return json.loads(row['messages'])
        return []
    except sqlite3.Error as e:
        logger.error(f"Error loading AI history: {e}")
        return []
    finally:
        if conn:
            conn.close()

def clear_ai_history(user_id: str):
    """Clear AI chat history"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return
        cur = conn.cursor()
        cur.execute('DELETE FROM ai_history WHERE user_id = ?', (user_id,))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error clearing AI history: {e}")
    finally:
        if conn:
            conn.close()

def add_panel(user_id: str, panel_type: str, panel_url: str, admin_user: str, admin_pass: str, admin_email: str, container_name: str = "", tunnel_url: str = ""):
    """Add panel installation record"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return
        cur = conn.cursor()
        now = datetime.now().isoformat()
        cur.execute('''INSERT INTO panels (user_id, panel_type, panel_url, admin_user, admin_pass, admin_email, container_name, tunnel_url, installed_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                    (user_id, panel_type, panel_url, admin_user, admin_pass, admin_email, container_name, tunnel_url, now))
        conn.commit()
        increment_setting('total_panels_installed')
    except sqlite3.Error as e:
        logger.error(f"Error adding panel: {e}")
    finally:
        if conn:
            conn.close()

def get_user_panels(user_id: str) -> List[Dict]:
    """Get panels for a user"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute('SELECT * FROM panels WHERE user_id = ? ORDER BY installed_at DESC', (user_id,))
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Error getting user panels: {e}")
        return []
    finally:
        if conn:
            conn.close()

# 🌐 Node Management Functions
def add_node(name: str, host: str, username: str, password: str = None, ssh_key: str = None, 
             port: int = 22, region: str = "us", description: str = "", added_by: str = "") -> Optional[Dict]:
    """Add a new node to the cluster"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return None
        cur = conn.cursor()
        now = datetime.now().isoformat()
        
        # Generate API key for node
        api_key = hashlib.sha256(f"{name}{host}{time.time()}{random.randint(1000,9999)}".encode()).hexdigest()[:32]
        
        cur.execute('''INSERT INTO nodes 
                       (name, host, port, username, password, ssh_key, api_key, region, description, added_by, added_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (name, host, port, username, password, ssh_key, api_key, region, description, added_by, now))
        node_id = cur.lastrowid
        conn.commit()
        
        increment_setting('total_nodes')
        
        cur.execute('SELECT * FROM nodes WHERE id = ?', (node_id,))
        node = dict(cur.fetchone())
        return node
    except sqlite3.Error as e:
        logger.error(f"Error adding node: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_node(name: str) -> Optional[Dict]:
    """Get node by name"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return None
        cur = conn.cursor()
        cur.execute('SELECT * FROM nodes WHERE name = ?', (name,))
        row = cur.fetchone()
        return dict(row) if row else None
    except sqlite3.Error as e:
        logger.error(f"Error getting node: {e}")
        return None
    finally:
        if conn:
            conn.close()

def get_all_nodes() -> List[Dict]:
    """Get all nodes"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return []
        cur = conn.cursor()
        cur.execute('SELECT * FROM nodes ORDER BY name')
        rows = cur.fetchall()
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Error getting all nodes: {e}")
        return []
    finally:
        if conn:
            conn.close()

def update_node_status(name: str, status: str, stats: Dict = None):
    """Update node status and stats"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return
        cur = conn.cursor()
        now = datetime.now().isoformat()
        
        if stats:
            cur.execute('''UPDATE nodes SET 
                           status = ?, total_ram = ?, used_ram = ?, total_cpu = ?, 
                           used_cpu = ?, total_disk = ?, used_disk = ?, lxc_count = ?,
                           last_checked = ?
                           WHERE name = ?''',
                        (status, stats.get('total_ram', 0), stats.get('used_ram', 0),
                         stats.get('total_cpu', 0), stats.get('used_cpu', 0),
                         stats.get('total_disk', 0), stats.get('used_disk', 0),
                         stats.get('lxc_count', 0), now, name))
        else:
            cur.execute('UPDATE nodes SET status = ?, last_checked = ? WHERE name = ?',
                        (status, now, name))
        
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Error updating node status: {e}")
    finally:
        if conn:
            conn.close()

def delete_node(name: str) -> bool:
    """Delete a node"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return False
        cur = conn.cursor()
        cur.execute('DELETE FROM nodes WHERE name = ?', (name,))
        deleted = cur.rowcount > 0
        conn.commit()
        return deleted
    except sqlite3.Error as e:
        logger.error(f"Error deleting node: {e}")
        return False
    finally:
        if conn:
            conn.close()

# 💰 UPI Configuration Functions
def get_upi_config() -> Dict:
    """Get active UPI configuration"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return {'upi_id': UPI_ID, 'upi_name': UPI_NAME}
        cur = conn.cursor()
        cur.execute('SELECT * FROM upi_config WHERE is_active = 1 ORDER BY id DESC LIMIT 1')
        row = cur.fetchone()
        if row:
            return dict(row)
        return {'upi_id': UPI_ID, 'upi_name': UPI_NAME}
    except sqlite3.Error as e:
        logger.error(f"Error getting UPI config: {e}")
        return {'upi_id': UPI_ID, 'upi_name': UPI_NAME}
    finally:
        if conn:
            conn.close()

def update_upi_config(upi_id: str, upi_name: str = None, qr_path: str = None, payment_link: str = None, updated_by: str = ""):
    """Update UPI configuration"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return
        cur = conn.cursor()
        now = datetime.now().isoformat()
        
        # Deactivate old config
        cur.execute('UPDATE upi_config SET is_active = 0 WHERE is_active = 1')
        
        # Insert new config
        cur.execute('''INSERT INTO upi_config (upi_id, upi_name, qr_code_path, payment_link, is_active, updated_by, updated_at)
                       VALUES (?, ?, ?, ?, 1, ?, ?)''',
                    (upi_id, upi_name or upi_id.split('@')[0], qr_path, payment_link, updated_by, now))
        conn.commit()
        
        # Update settings
        set_setting('upi_id', upi_id)
        if upi_name:
            set_setting('upi_name', upi_name)
    except sqlite3.Error as e:
        logger.error(f"Error updating UPI config: {e}")
    finally:
        if conn:
            conn.close()

def generate_upi_qr(upi_id: str, amount: int = None, note: str = None) -> Optional[str]:
    """Generate UPI QR code"""
    try:
        # Create UPI payment URL
        if amount and note:
            upi_url = f"upi://pay?pa={upi_id}&pn={UPI_NAME}&am={amount}&tn={note}"
        else:
            upi_url = f"upi://pay?pa={upi_id}&pn={UPI_NAME}"
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(upi_url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        return img_bytes
    except Exception as e:
        logger.error(f"Error generating QR code: {e}")
        return None

# ==================================================================================================
#  🛠️  LXC HELPER FUNCTIONS
# ==================================================================================================

def run_lxc_sync(command: str, timeout: int = 60) -> Tuple[str, str, int]:
    """Run LXC command synchronously"""
    try:
        cmd = shlex.split(command)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", f"Command timed out after {timeout} seconds", -1
    except Exception as e:
        return "", str(e), -1

async def run_lxc(command: str, timeout: int = 60) -> Tuple[str, str, int]:
    """Run an LXC command asynchronously"""
    return await asyncio.get_event_loop().run_in_executor(None, run_lxc_sync, command, timeout)

async def exec_in_container(container_name: str, command: str, timeout: int = 30) -> Tuple[str, str, int]:
    """Execute a command inside a container"""
    return await run_lxc(f"lxc exec {container_name} -- bash -c {shlex.quote(command)}", timeout)

def get_container_status_sync(container_name: str) -> str:
    """Get container status synchronously"""
    try:
        result = subprocess.run(['lxc', 'info', container_name], 
                                capture_output=True, text=True, timeout=10)
        for line in result.stdout.splitlines():
            if line.startswith("Status: "):
                return line.split(": ", 1)[1].strip().lower()
        return "unknown"
    except:
        return "unknown"

async def get_container_status(container_name: str) -> str:
    """Get container status asynchronously"""
    return await asyncio.get_event_loop().run_in_executor(None, get_container_status_sync, container_name)

async def get_container_real_time_stats(container_name: str) -> Dict:
    """Get real-time container stats with live updates"""
    stats = {
        'status': 'unknown',
        'cpu': '0.0%',
        'cpu_usage': 0.0,
        'memory': '0/0 MB (0%)',
        'memory_used': 0,
        'memory_total': 0,
        'memory_percent': 0,
        'disk': '0/0 GB (0%)',
        'disk_used': 0,
        'disk_total': 0,
        'disk_percent': 0,
        'uptime': '0 min',
        'uptime_seconds': 0,
        'ipv4': [],
        'ipv6': [],
        'mac': 'N/A',
        'processes': 0,
        'process_list': [],
        'load': '0.00 0.00 0.00',
        'load_1': 0.0,
        'load_5': 0.0,
        'load_15': 0.0,
        'network_rx': '0 B',
        'network_tx': '0 B',
        'network_rx_bytes': 0,
        'network_tx_bytes': 0,
        'hostname': container_name,
        'kernel': 'N/A',
        'os': 'N/A',
        'node': 'local',
        'users': 0,
        'temperature': 'N/A'
    }
    
    # Get status
    stats['status'] = await get_container_status(container_name)
    
    if stats['status'] == 'running':
        # Get CPU usage
        out, _, _ = await exec_in_container(container_name, "top -bn1 | grep 'Cpu(s)' | awk '{print $2}'")
        stats['cpu'] = f"{out}%" if out else "0.0%"
        stats['cpu_usage'] = float(out) if out else 0.0
        
        # Get memory usage
        out, _, _ = await exec_in_container(container_name, "free -m | awk '/^Mem:/{print $2,$3}'")
        if out:
            parts = out.split()
            if len(parts) >= 2:
                stats['memory_total'] = int(parts[0])
                stats['memory_used'] = int(parts[1])
                stats['memory_percent'] = (stats['memory_used'] / stats['memory_total'] * 100) if stats['memory_total'] > 0 else 0
                stats['memory'] = f"{stats['memory_used']}/{stats['memory_total']} MB ({stats['memory_percent']:.1f}%)"
        
        # Get disk usage
        out, _, _ = await exec_in_container(container_name, "df -BG / | awk 'NR==2{print $2,$3,$5}' | sed 's/G//g'")
        if out:
            parts = out.split()
            if len(parts) >= 3:
                stats['disk_total'] = int(parts[0])
                stats['disk_used'] = int(parts[1])
                stats['disk_percent'] = float(parts[2].replace('%', ''))
                stats['disk'] = f"{stats['disk_used']}/{stats['disk_total']} GB ({stats['disk_percent']}%)"
        
        # Get uptime
        out, _, _ = await exec_in_container(container_name, "cat /proc/uptime | awk '{print $1}'")
        if out:
            stats['uptime_seconds'] = float(out.split()[0])
            days = int(stats['uptime_seconds'] // 86400)
            hours = int((stats['uptime_seconds'] % 86400) // 3600)
            minutes = int((stats['uptime_seconds'] % 3600) // 60)
            stats['uptime'] = f"{days}d {hours}h {minutes}m"
        
        # Get IPv4 addresses
        out, _, _ = await exec_in_container(container_name, "ip -4 addr show | grep -oP '(?<=inet\\s)\\d+\\.\\d+\\.\\d+\\.\\d+' | grep -v '127.0.0.1'")
        if out:
            stats['ipv4'] = out.splitlines()
        
        # Get IPv6 addresses
        out, _, _ = await exec_in_container(container_name, "ip -6 addr show | grep -oP '(?<=inet6\\s)[a-f0-9:]+' | grep -v '::1'")
        if out:
            stats['ipv6'] = out.splitlines()
        
        # Get MAC address
        out, _, _ = await exec_in_container(container_name, "ip link show eth0 | grep -oP '(?<=link/ether\\s)\\S+'")
        stats['mac'] = out.strip() if out else "N/A"
        
        # Get process list
        out, _, _ = await exec_in_container(container_name, "ps aux --no-headers | wc -l")
        stats['processes'] = int(out) if out and out.isdigit() else 0
        
        out, _, _ = await exec_in_container(container_name, "ps aux --no-headers --sort=-%cpu | head -10 | awk '{print $1, $2, $3, $11}'")
        if out:
            stats['process_list'] = out.splitlines()
        
        # Get load average
        out, _, _ = await exec_in_container(container_name, "cat /proc/loadavg | awk '{print $1, $2, $3}'")
        if out:
            parts = out.split()
            if len(parts) >= 3:
                stats['load_1'] = float(parts[0])
                stats['load_5'] = float(parts[1])
                stats['load_15'] = float(parts[2])
                stats['load'] = f"{stats['load_1']:.2f} {stats['load_5']:.2f} {stats['load_15']:.2f}"
        
        # Get network stats
        out, _, _ = await exec_in_container(container_name, "cat /sys/class/net/eth0/statistics/rx_bytes")
        if out and out.isdigit():
            stats['network_rx_bytes'] = int(out)
            stats['network_rx'] = f"{stats['network_rx_bytes']/1024/1024:.2f} MB"
        
        out, _, _ = await exec_in_container(container_name, "cat /sys/class/net/eth0/statistics/tx_bytes")
        if out and out.isdigit():
            stats['network_tx_bytes'] = int(out)
            stats['network_tx'] = f"{stats['network_tx_bytes']/1024/1024:.2f} MB"
        
        # Get hostname
        out, _, _ = await exec_in_container(container_name, "hostname")
        stats['hostname'] = out.strip() if out else container_name
        
        # Get kernel version
        out, _, _ = await exec_in_container(container_name, "uname -r")
        stats['kernel'] = out.strip() if out else "N/A"
        
        # Get OS info
        out, _, _ = await exec_in_container(container_name, "cat /etc/os-release | grep PRETTY_NAME | cut -d= -f2 | tr -d '\"'")
        stats['os'] = out.strip() if out else "N/A"
        
        # Get user count
        out, _, _ = await exec_in_container(container_name, "users | wc -w")
        stats['users'] = int(out) if out and out.isdigit() else 0
        
        # Get temperature (if available)
        out, _, _ = await exec_in_container(container_name, "cat /sys/class/thermal/thermal_zone0/temp 2>/dev/null")
        if out and out.isdigit():
            stats['temperature'] = f"{int(out)/1000:.1f}°C"
    
    return stats

async def get_container_stats(container_name: str) -> Dict:
    """Alias for get_container_real_time_stats"""
    return await get_container_real_time_stats(container_name)

async def apply_lxc_config(container_name: str):
    """Apply LXC configuration for better compatibility"""
    try:
        # Enable nesting and privileged mode
        await run_lxc(f"lxc config set {container_name} security.nesting true")
        await run_lxc(f"lxc config set {container_name} security.privileged true")
        
        # Add kernel modules
        await run_lxc(f"lxc config set {container_name} linux.kernel_modules overlay,br_netfilter,nf_nat,ip_tables,ip6_tables,netlink_diag,xt_conntrack,nf_conntrack")
        
        # Raw LXC config
        raw_config = """
lxc.apparmor.profile = unconfined
lxc.cgroup.devices.allow = a
lxc.cap.drop =
lxc.mount.auto = proc:rw sys:rw cgroup:rw
"""
        await run_lxc(f"lxc config set {container_name} raw.lxc '{raw_config}'")
        
        logger.info(f"✅ Applied LXC config to {container_name}")
    except Exception as e:
        logger.error(f"Failed to apply LXC config to {container_name}: {e}")

async def apply_internal_permissions(container_name: str):
    """Apply internal permissions for Docker compatibility"""
    await asyncio.sleep(3)
    commands = [
        "mkdir -p /etc/sysctl.d/",
        "echo 'net.ipv4.ip_unprivileged_port_start=0' > /etc/sysctl.d/99-custom.conf",
        "echo 'net.ipv4.ping_group_range=0 2147483647' >> /etc/sysctl.d/99-custom.conf",
        "echo 'fs.inotify.max_user_watches=524288' >> /etc/sysctl.d/99-custom.conf",
        "sysctl -p /etc/sysctl.d/99-custom.conf || true",
        "apt-get update -qq",
        "apt-get install -y -qq curl wget sudo vim nano htop net-tools iproute2 iputils-ping dnsutils traceroute mtr tcpdump telnet ncdu tmux screen",
    ]
    for cmd in commands:
        await exec_in_container(container_name, cmd)

async def get_available_host_port() -> Optional[int]:
    """Get an available host port for forwarding"""
    conn = None
    try:
        conn = get_db()
        if not conn:
            return None
        cur = conn.cursor()
        cur.execute('SELECT host_port FROM port_forwards')
        used_ports = {row[0] for row in cur.fetchall()}
        
        # Also check system for used ports
        try:
            result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if ':' in line:
                    parts = line.split()
                    for part in parts:
                        if ':' in part and part.split(':')[-1].isdigit():
                            used_ports.add(int(part.split(':')[-1]))
        except:
            pass
        
        for _ in range(100):
            port = random.randint(20000, 50000)
            if port not in used_ports:
                return port
        return None
    except Exception as e:
        logger.error(f"Error getting available port: {e}")
        return None
    finally:
        if conn:
            conn.close()

async def create_port_forward(user_id: str, container_name: str, container_port: int, protocol: str = "tcp+udp") -> Optional[int]:
    """Create a port forward"""
    host_port = await get_available_host_port()
    if not host_port:
        return None
    
    try:
        if protocol == "tcp" or protocol == "tcp+udp":
            await run_lxc(f"lxc config device add {container_name} proxy-tcp-{host_port} proxy listen=tcp:0.0.0.0:{host_port} connect=tcp:127.0.0.1:{container_port}")
        
        if protocol == "udp" or protocol == "tcp+udp":
            await run_lxc(f"lxc config device add {container_name} proxy-udp-{host_port} proxy listen=udp:0.0.0.0:{host_port} connect=udp:127.0.0.1:{container_port}")
        
        pf_id = add_port_forward(user_id, container_name, container_port, host_port, protocol)
        return host_port if pf_id else None
    except Exception as e:
        logger.error(f"Failed to create port forward: {e}")
        return None

async def remove_port_forward_device(container_name: str, host_port: int):
    """Remove port forward devices"""
    try:
        await run_lxc(f"lxc config device remove {container_name} proxy-tcp-{host_port}")
    except:
        pass
    try:
        await run_lxc(f"lxc config device remove {container_name} proxy-udp-{host_port}")
    except:
        pass

async def get_container_console(container_name: str, lines: int = 20, follow: bool = False) -> str:
    """Get console output from container with real-time option"""
    try:
        if follow:
            # Get live output
            out, _, _ = await exec_in_container(container_name, f"tail -f /var/log/syslog 2>/dev/null | head -{lines} || journalctl -f -n {lines} --no-pager 2>/dev/null")
        else:
            # Get last N lines
            out, _, _ = await exec_in_container(container_name, f"dmesg | tail -{lines} 2>/dev/null || journalctl -n {lines} --no-pager 2>/dev/null")
        
        if out:
            return out
        
        # Fallback to process list
        out, _, _ = await exec_in_container(container_name, f"ps aux --forest | head -{lines*2}")
        return out or "No console output available"
    except Exception as e:
        return f"Error getting console: {str(e)}"

async def check_node_health(node: Dict) -> Dict:
    """Check node health via SSH"""
    import paramiko
    
    stats = {
        'status': 'offline',
        'total_ram': 0,
        'used_ram': 0,
        'total_cpu': 0,
        'used_cpu': 0.0,
        'total_disk': 0,
        'used_disk': 0,
        'lxc_count': 0
    }
    
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        if node.get('password'):
            client.connect(node['host'], port=node['port'], 
                          username=node['username'], password=node['password'], timeout=10)
        elif node.get('ssh_key'):
            key = paramiko.RSAKey.from_private_key_file(node['ssh_key'])
            client.connect(node['host'], port=node['port'], 
                          username=node['username'], pkey=key, timeout=10)
        else:
            return stats
        
        # Get system stats
        stdin, stdout, stderr = client.exec_command('nproc')
        total_cpu = stdout.read().decode().strip()
        stats['total_cpu'] = int(total_cpu) if total_cpu.isdigit() else 0
        
        stdin, stdout, stderr = client.exec_command("top -bn1 | grep 'Cpu(s)' | awk '{print $2}'")
        used_cpu = stdout.read().decode().strip()
        stats['used_cpu'] = float(used_cpu) if used_cpu else 0.0
        
        stdin, stdout, stderr = client.exec_command("free -m | awk '/^Mem:/{print $2}'")
        total_ram = stdout.read().decode().strip()
        stats['total_ram'] = int(total_ram) if total_ram.isdigit() else 0
        
        stdin, stdout, stderr = client.exec_command("free -m | awk '/^Mem:/{print $3}'")
        used_ram = stdout.read().decode().strip()
        stats['used_ram'] = int(used_ram) if used_ram.isdigit() else 0
        
        stdin, stdout, stderr = client.exec_command("df -BG / | awk 'NR==2{print $2}' | sed 's/G//'")
        total_disk = stdout.read().decode().strip()
        stats['total_disk'] = int(total_disk) if total_disk.isdigit() else 0
        
        stdin, stdout, stderr = client.exec_command("df -BG / | awk 'NR==2{print $3}' | sed 's/G//'")
        used_disk = stdout.read().decode().strip()
        stats['used_disk'] = int(used_disk) if used_disk.isdigit() else 0
        
        stdin, stdout, stderr = client.exec_command("lxc list --format csv 2>/dev/null | wc -l")
        lxc_count = stdout.read().decode().strip()
        stats['lxc_count'] = int(lxc_count) if lxc_count.isdigit() else 0
        
        stats['status'] = 'online'
        client.close()
        
    except Exception as e:
        logger.error(f"Node {node['name']} health check failed: {e}")
        stats['status'] = 'offline'
    
    return stats

# ==================================================================================================
#  🚀  CLOUDFLARED TUNNEL FUNCTIONS
# ==================================================================================================

CLOUDFLARED_AVAILABLE = shutil.which("cloudflared") is not None

async def create_cloudflared_tunnel(container_name: str, port: int = 80) -> Optional[str]:
    """Create a cloudflared tunnel for a container"""
    if not CLOUDFLARED_AVAILABLE:
        return None
    
    try:
        # Install cloudflared in container if not present
        await exec_in_container(container_name, "which cloudflared || (wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O /usr/local/bin/cloudflared && chmod +x /usr/local/bin/cloudflared)")
        
        # Generate unique tunnel ID
        tunnel_id = str(uuid.uuid4())[:8]
        
        # Start tunnel
        cmd = f"nohup cloudflared tunnel --url http://localhost:{port} --no-autoupdate > /tmp/cloudflared_{tunnel_id}.log 2>&1 & echo $!"
        pid, _, _ = await exec_in_container(container_name, cmd)
        
        # Wait for tunnel to establish
        await asyncio.sleep(5)
        
        # Get tunnel URL
        out, _, _ = await exec_in_container(container_name, f"cat /tmp/cloudflared_{tunnel_id}.log | grep -oP 'https://[a-z0-9-]+\\.trycloudflare\\.com' | head -1")
        url = out.strip()
        
        if url:
            return url
    except Exception as e:
        logger.error(f"Failed to create cloudflared tunnel: {e}")
    
    return None

# ==================================================================================================
#  🎨  EMBED HELPER FUNCTIONS - ENHANCED WITH GLOW EFFECTS
# ==================================================================================================

def create_embed(title: str, description: str = "", color: int = 0x5865F2) -> discord.Embed:
    """Create a styled embed with glow effects"""
    embed = discord.Embed(
        title=f"```glow\n✦ {BOT_NAME} - {title} ✦\n```",
        description=description,
        color=color
    )
    
    if THUMBNAIL_URL:
        embed.set_thumbnail(url=THUMBNAIL_URL)
    
    embed.set_footer(
        text=f"⚡ {BOT_NAME} • {BOT_AUTHOR} • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ⚡",
        icon_url=THUMBNAIL_URL
    )
    
    return embed

def success_embed(title: str, description: str = "") -> discord.Embed:
    """Create a success embed with glow"""
    return create_embed(f"✅ {title}", description, 0x57F287)

def error_embed(title: str, description: str = "") -> discord.Embed:
    """Create an error embed with glow"""
    return create_embed(f"❌ {title}", description, 0xED4245)

def info_embed(title: str, description: str = "") -> discord.Embed:
    """Create an info embed with glow"""
    return create_embed(f"ℹ️ {title}", description, 0x5865F2)

def warning_embed(title: str, description: str = "") -> discord.Embed:
    """Create a warning embed with glow"""
    return create_embed(f"⚠️ {title}", description, 0xFEE75C)

def node_embed(title: str, description: str = "") -> discord.Embed:
    """Create a node-specific embed with glow"""
    return create_embed(f"🌐 {title}", description, 0x9B59B6)

def terminal_embed(title: str, content: str, color: int = 0x2C2F33) -> discord.Embed:
    """Create a terminal-style embed for console output"""
    terminal_title = f"```fix\n[ {title} ]\n```"
    embed = discord.Embed(
        title=terminal_title,
        description=f"```bash\n{content[:1900]}\n```",
        color=color
    )
    embed.set_footer(text=f"⚡ {BOT_NAME} • Terminal Output • {datetime.now().strftime('%H:%M:%S')} ⚡")
    return embed

def realtime_embed(title: str, content: str, color: int = 0x00ff00) -> discord.Embed:
    """Create a real-time embed with live updates"""
    terminal_title = f"```fix\n[ LIVE ] {title}\n```"
    embed = discord.Embed(
        title=terminal_title,
        description=f"```bash\n{content[:1900]}\n```",
        color=color
    )
    embed.set_footer(text=f"⚡ {BOT_NAME} • Live Updates • {datetime.now().strftime('%H:%M:%S')} ⚡")
    return embed

def no_vps_embed() -> discord.Embed:
    """Create a no VPS embed"""
    return info_embed(
        "No VPS Found",
        f"```diff\n- You don't have any VPS yet.\n```\n\n"
        f"**To get a free VPS:**\n"
        f"• Use `{BOT_PREFIX}plans` to see available plans\n"
        f"• Use `{BOT_PREFIX}claim-free` to claim based on invites\n"
        f"• Contact an admin for custom VPS"
    )

# ==================================================================================================
#  🤖  BOT SETUP
# ==================================================================================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents, help_command=None)
bot.start_time = datetime.utcnow()

# Global variables
MAINTENANCE_MODE = get_setting('maintenance_mode', 'false').lower() == 'true'
CPU_THRESHOLD = int(get_setting('cpu_threshold', 90))
RAM_THRESHOLD = int(get_setting('ram_threshold', 90))
DISK_THRESHOLD = int(get_setting('disk_threshold', 90))
LICENSE_VERIFIED = get_setting('license_verified', 'false') == 'true'

# Active help menus
active_help_menus = {}

# Admin notification on startup
async def notify_admins():
    """Notify admins when bot starts"""
    for admin_id in MAIN_ADMIN_IDS:
        try:
            admin = await bot.fetch_user(admin_id)
            if admin:
                embed = success_embed(
                    "🚀 Bot Started Successfully",
                    f"```fix\nBot Name: {BOT_NAME}\nVersion: 5.0.0\nServer IP: {SERVER_IP}\nMAC: {MAC_ADDRESS}\nUptime: Just Started\n```\n"
                    f"All systems are operational. Use `.help` to see commands."
                )
                await admin.send(embed=embed)
        except:
            pass

# Node monitoring task
@tasks.loop(minutes=5)
async def monitor_nodes():
    """Monitor all nodes every 5 minutes"""
    nodes = get_all_nodes()
    for node in nodes:
        if node['status'] == 'online':
            stats = await check_node_health(node)
            update_node_status(node['name'], stats['status'], stats)
            logger.info(f"Node {node['name']} status: {stats['status']}")

@tasks.loop(hours=1)
async def cleanup_old_logs():
    """Clean up old logs every hour"""
    # Implement log cleanup
    pass

# ==================================================================================================
#  ✅  MAINTENANCE CHECK DECORATOR
# ==================================================================================================

async def maintenance_check(ctx) -> bool:
    """Check if bot is in maintenance mode"""
    global MAINTENANCE_MODE
    
    if MAINTENANCE_MODE and not is_admin(str(ctx.author.id)):
        embed = warning_embed(
            "Maintenance Mode Active",
            f"```fix\n{get_setting('maintenance_message', 'Bot is under maintenance')}\n```\n"
            "Only administrators can use commands at this time."
        )
        await ctx.send(embed=embed)
        return False
    return True

# ==================================================================================================
#  ✅  LICENSE CHECK DECORATOR
# ==================================================================================================

async def license_check(ctx) -> bool:
    """Check if license is verified"""
    global LICENSE_VERIFIED
    
    if not LICENSE_VERIFIED and not is_admin(str(ctx.author.id)):
        embed = error_embed(
            "License Required",
            "```diff\n- This bot requires a valid license key to operate.\n```\n\n"
            "**Purchase Information:**\n"
            f"• UPI: `9892642904@ybl`\n"
            f"• Amount: `₹499` (One-time)\n"
            f"• Contact: @Ankit-Dev on Discord\n\n"
            "After payment, you will receive a valid license key."
        )
        await ctx.send(embed=embed)
        return False
    return True

# ==================================================================================================
#  ✅  ON READY - FIXED WITH ADMIN NOTIFICATION
# ==================================================================================================

@bot.event
async def on_ready():
    """Bot ready event - FIXED with admin notification"""
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{BOT_PREFIX}help | {BOT_NAME}"
        )
    )
    logger.info(f"✅ Bot is ready: {bot.user} (ID: {bot.user.id})")
    
    # Check license
    global LICENSE_VERIFIED
    LICENSE_VERIFIED = get_setting('license_verified', 'false') == 'true'
    
    # Start monitoring tasks
    monitor_nodes.start()
    cleanup_old_logs.start()
    
    # Get server stats
    all_vps = get_all_vps()
    total_vps = len(all_vps)
    running_vps = sum(1 for v in all_vps if v['status'] == 'running' and not v['suspended'])
    nodes = len(get_all_nodes())
    
    # Create VPS user role if needed
    for guild in bot.guilds:
        role = discord.utils.get(guild.roles, name=f"{BOT_NAME} User")
        if not role:
            try:
                await guild.create_role(
                    name=f"{BOT_NAME} User",
                    color=discord.Color.purple(),
                    reason=f"{BOT_NAME} user role"
                )
                logger.info(f"✅ Created role in {guild.name}")
            except:
                pass
    
    # Notify admins
    await notify_admins()
    
    # Beautiful startup banner
    print(f"""
╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                               ║
║                      ███████╗██╗   ██╗███╗   ███╗███████╗    ██████╗  ██████╗ ████████╗      ║
║                      ██╔════╝██║   ██║████╗ ████║██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝      ║
║                      ███████╗██║   ██║██╔████╔██║█████╗      ██████╔╝██║   ██║   ██║         ║
║                      ╚════██║╚██╗ ██╔╝██║╚██╔╝██║██╔══╝      ██╔══██╗██║   ██║   ██║         ║
║                      ███████║ ╚████╔╝ ██║ ╚═╝ ██║███████╗    ██████╔╝╚██████╔╝   ██║         ║
║                      ╚══════╝  ╚═══╝  ╚═╝     ╚═╝╚══════╝    ╚═════╝  ╚═════╝    ╚═╝         ║
║                                                                                               ║
║                          ██████╗  ██████╗ ████████╗    ██╗   ██╗███████╗                     ║
║                          ██╔══██╗██╔═══██╗╚══██╔══╝    ██║   ██║██╔════╝                     ║
║                          ██████╔╝██║   ██║   ██║       ██║   ██║███████╗                     ║
║                          ██╔══██╗██║   ██║   ██║       ╚██╗ ██╔╝╚════██║                     ║
║                          ██████╔╝╚██████╔╝   ██║        ╚████╔╝ ███████║                     ║
║                          ╚═════╝  ╚═════╝    ╚═╝         ╚═══╝  ╚══════╝                     ║
║                                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                               ║
║  📍 Bot Status:    🟢 ONLINE                                                                 ║
║  🤖 Bot Name:      {bot.user:<58} ║
║  🆔 Bot ID:        {bot.user.id:<64} ║
║  🔧 Prefix:        {BOT_PREFIX:<65} ║
║                                                                                               ║
║  🔐 License:       {'✅ VERIFIED' if LICENSE_VERIFIED else '❌ NOT VERIFIED':<58} ║
║  🌐 Server IP:     {SERVER_IP:<61} ║
║  🔌 MAC Address:   {MAC_ADDRESS:<57} ║
║  💻 Hostname:      {HOSTNAME:<61} ║
║                                                                                               ║
║  🖥️ Total VPS:     {total_vps:<6} (Running: {running_vps:<4})                                  ║
║  🌍 Total Nodes:   {nodes:<6}                                                                  ║
║  📊 Commands:      75+                                                                         ║
║  🤖 AI Model:      {AI_MODEL:<60} ║
║                                                                                               ║
║  👑 Main Admin:    <@1405866008127864852>                                                     ║
║                                                                                               ║
║                         Made by Ankit-Dev with ❤️ - ALL ISSUES FIXED                         ║
║              ✅ Database Fixed • ✅ Help Fixed • ✅ AI Fixed • ✅ SSH Fixed                    ║
║           ✅ Real-time Console • ✅ UPI QR • ✅ Node Management • ✅ Cloudflare                ║
║                                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════╝
    """)

# ==================================================================================================
#  ❌  ERROR HANDLER - COMPLETELY FIXED
# ==================================================================================================

@bot.event
async def on_command_error(ctx, error):
    """Global error handler - FIXED"""
    
    # Log the error
    logger.error(f"Error in command '{ctx.command}': {error}")
    
    if isinstance(error, commands.CommandNotFound):
        return
    
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = error_embed(
            "Missing Argument",
            f"```fix\nUsage: {BOT_PREFIX}{ctx.command.name} {ctx.command.signature}\n```\n"
            f"Use `{BOT_PREFIX}help` for more information."
        )
        await ctx.send(embed=embed)
    
    elif isinstance(error, commands.BadArgument):
        embed = error_embed(
            "Invalid Argument",
            "```diff\n- Please check your input and try again.\n```"
        )
        await ctx.send(embed=embed)
    
    elif isinstance(error, commands.CheckFailure):
        embed = error_embed(
            "Access Denied",
            "```diff\n- You don't have permission to use this command.\n```"
        )
        await ctx.send(embed=embed)
    
    elif isinstance(error, commands.CommandOnCooldown):
        embed = warning_embed(
            "Command on Cooldown",
            f"```fix\nPlease wait {error.retry_after:.1f} seconds before using this command again.\n```"
        )
        await ctx.send(embed=embed)
    
    elif isinstance(error, discord.errors.InteractionResponded):
        try:
            await ctx.send(embed=warning_embed(
                "Slow Down",
                "```fix\nPlease wait a moment before using this again.\n```"
            ), ephemeral=True)
        except:
            pass
    
    elif isinstance(error, discord.errors.Forbidden):
        embed = error_embed(
            "Permission Error",
            "```diff\n- I don't have permission to do that. Please check my permissions.\n```"
        )
        await ctx.send(embed=embed)
    
    elif isinstance(error, asyncio.TimeoutError):
        embed = error_embed(
            "Timeout Error",
            "```diff\n- The operation timed out. Please try again.\n```"
        )
        await ctx.send(embed=embed)
    
    elif isinstance(error, commands.CommandInvokeError) and "Interaction" in str(error):
        try:
            await ctx.send(embed=warning_embed(
                "Interaction Error",
                "```fix\nThere was an issue with the interaction. Please try again.\n```"
            ))
        except:
            pass
    
    elif isinstance(error, sqlite3.Error):
        embed = error_embed(
            "Database Error",
            "```diff\n- A database error occurred. Please try again later.\n```"
        )
        await ctx.send(embed=embed)
    
    else:
        embed = error_embed(
            "Unexpected Error",
            f"```diff\n- {str(error)[:1900]}\n```\n"
            f"Please report this to an admin."
        )
        try:
            await ctx.send(embed=embed)
        except:
            pass

# ==================================================================================================
#  📖  HELP COMMAND - ULTIMATE INTERACTIVE VERSION
# ==================================================================================================

class HelpView(View):
    """Interactive help menu with all commands - ULTIMATE"""
    def __init__(self, ctx):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.current_page = 0
        self.pages = [
            {
                "title": "📚 WELCOME TO SVM5-BOT HELP",
                "description": f"```glow\nPrefix: {BOT_PREFIX} | Version: 5.0.0 | Author: {BOT_AUTHOR}\nServer IP: {SERVER_IP} | MAC: {MAC_ADDRESS}\n```\n**Select a category below to see commands:**",
                "fields": [
                    ("👤 USER COMMANDS", "`Basic commands for all users`", True),
                    ("🖥️ VPS MANAGEMENT", "`Control your VPS containers`", True),
                    ("📟 CONSOLE & SSH", "`Real-time terminal access`", True),
                    ("🔌 PORT FORWARDING", "`Manage port forwards`", True),
                    ("🌐 NODE MANAGEMENT", "`Manage cluster nodes`", True),
                    ("📦 PANEL INSTALL", "`Install game panels`", True),
                    ("🌍 IPv4 MANAGEMENT", "`Buy and manage IPv4`", True),
                    ("💰 INVITE SYSTEM", "`Earn free VPS`", True),
                    ("🤖 AI CHAT", "`Chat with AI assistant`", True),
                    ("💳 UPI PAYMENTS", "`Manage UPI payments`", True),
                    ("🛡️ ADMIN COMMANDS", "`Administrator commands`", True),
                    ("👑 MAIN ADMIN", "`Main admin commands`", True),
                ]
            },
            {
                "title": "👤 USER COMMANDS",
                "description": "```fix\nBasic commands available to all users\n```",
                "fields": [
                    (f"{BOT_PREFIX}help", "Show this interactive help menu", False),
                    (f"{BOT_PREFIX}ping", "Check bot latency with graph", False),
                    (f"{BOT_PREFIX}uptime", "Show bot uptime", False),
                    (f"{BOT_PREFIX}bot-info", "Detailed bot information", False),
                    (f"{BOT_PREFIX}server-info", "Show server hardware info", False),
                    (f"{BOT_PREFIX}plans", "View free VPS plans", False),
                    (f"{BOT_PREFIX}stats", "View your stats and API key", False),
                    (f"{BOT_PREFIX}inv", "Check your invites", False),
                    (f"{BOT_PREFIX}claim-free", "Claim free VPS with invites", False),
                    (f"{BOT_PREFIX}my-acc", "View your generated account", False),
                    (f"{BOT_PREFIX}gen-acc", "Generate random account with API key", False),
                    (f"{BOT_PREFIX}api-key", "View or regenerate your API key", False),
                ]
            },
            {
                "title": "🖥️ VPS MANAGEMENT",
                "description": "```fix\nControl and manage your VPS containers\n```",
                "fields": [
                    (f"{BOT_PREFIX}myvps", "List your VPS with status", False),
                    (f"{BOT_PREFIX}list", "Detailed VPS list with IPs", False),
                    (f"{BOT_PREFIX}manage", "Interactive VPS manager with buttons", False),
                    (f"{BOT_PREFIX}stats [container]", "View real-time VPS statistics", False),
                    (f"{BOT_PREFIX}logs [container] [lines]", "View VPS logs", False),
                    (f"{BOT_PREFIX}reboot <container>", "Reboot VPS", False),
                    (f"{BOT_PREFIX}shutdown <container>", "Shutdown VPS", False),
                    (f"{BOT_PREFIX}rename <container> <new-name>", "Rename VPS container", False),
                ]
            },
            {
                "title": "📟 CONSOLE & SSH COMMANDS",
                "description": "```fix\nReal-time terminal access and console commands\n```",
                "fields": [
                    (f"{BOT_PREFIX}ss [container]", "Show real-time VPS console (live)", False),
                    (f"{BOT_PREFIX}console <container>", "Interactive console with command input", False),
                    (f"{BOT_PREFIX}execute <container> <cmd>", "Execute command in VPS", False),
                    (f"{BOT_PREFIX}ssh-gen <container>", "Generate temporary SSH access", False),
                    (f"{BOT_PREFIX}top <container>", "Show live process monitor", False),
                    (f"{BOT_PREFIX}df <container>", "Show disk usage with graph", False),
                    (f"{BOT_PREFIX}free <container>", "Show memory usage with graph", False),
                    (f"{BOT_PREFIX}netstat <container>", "Show network connections", False),
                    (f"{BOT_PREFIX}ps <container>", "Show process list", False),
                    (f"{BOT_PREFIX}who <container>", "Show logged-in users", False),
                    (f"{BOT_PREFIX}uptime <container>", "Show container uptime", False),
                ]
            },
            {
                "title": "🔌 PORT FORWARDING",
                "description": "```fix\nManage port forwarding for your VPS\n```",
                "fields": [
                    (f"{BOT_PREFIX}ports", "Port forwarding help", False),
                    (f"{BOT_PREFIX}ports add <num> <port> [tcp/udp]", "Add port forward", False),
                    (f"{BOT_PREFIX}ports list", "List your forwards with IDs", False),
                    (f"{BOT_PREFIX}ports remove <id>", "Remove port forward", False),
                    (f"{BOT_PREFIX}ports quota", "Check your port quota", False),
                    (f"{BOT_PREFIX}ports check <port>", "Check if port is available", False),
                ]
            },
            {
                "title": "🌐 NODE MANAGEMENT",
                "description": "```fix\nManage cluster nodes (Admin only)\n```",
                "fields": [
                    (f"{BOT_PREFIX}node", "List all nodes with live stats", False),
                    (f"{BOT_PREFIX}node-info <name>", "Detailed node information", False),
                    (f"{BOT_PREFIX}node-add <name> <host> <user> <pass>", "Add new node", False),
                    (f"{BOT_PREFIX}node-remove <name>", "Remove a node", False),
                    (f"{BOT_PREFIX}node-check <name>", "Check node health", False),
                    (f"{BOT_PREFIX}node-stats", "Show cluster statistics", False),
                    (f"{BOT_PREFIX}node-sync <name>", "Sync containers from node", False),
                ]
            },
            {
                "title": "📦 PANEL INSTALLATION",
                "description": "```fix\nInstall game server panels on your VPS\n```",
                "fields": [
                    (f"{BOT_PREFIX}install-panel", "Install Pterodactyl/Pufferpanel", False),
                    (f"{BOT_PREFIX}panel-info", "Show your installed panel info", False),
                    (f"{BOT_PREFIX}panel-tunnel <container> [port]", "Create cloudflared tunnel", False),
                    (f"{BOT_PREFIX}panel-reset <container>", "Reset panel admin password", False),
                ]
            },
            {
                "title": "🌍 IPv4 MANAGEMENT",
                "description": "```fix\nBuy and manage IPv4 addresses\n```",
                "fields": [
                    (f"{BOT_PREFIX}ipv4", "View your IPv4 list with details", False),
                    (f"{BOT_PREFIX}buy-ipv4", "Purchase IPv4 via UPI with QR", False),
                    (f"{BOT_PREFIX}ipv4-details <container>", "Show detailed IPv4 info", False),
                    (f"{BOT_PREFIX}ipv4-renew <container>", "Renew IPv4 lease", False),
                ]
            },
            {
                "title": "💰 INVITE SYSTEM",
                "description": "```fix\nEarn free VPS by inviting users\n```",
                "fields": [
                    (f"{BOT_PREFIX}plans", "View plan requirements", False),
                    (f"{BOT_PREFIX}inv", "Check your invites", False),
                    (f"{BOT_PREFIX}stats", "View your stats", False),
                    (f"{BOT_PREFIX}claim-free", "Claim your VPS", False),
                    (f"{BOT_PREFIX}invites-top", "Show top inviters", False),
                ]
            },
            {
                "title": "🤖 AI CHAT",
                "description": f"```fix\nChat with AI assistant (Model: {AI_MODEL})\n```",
                "fields": [
                    (f"{BOT_PREFIX}ai <message>", "Chat with AI", False),
                    (f"{BOT_PREFIX}ai-reset", "Reset chat history", False),
                    (f"{BOT_PREFIX}ai-help <topic>", "Get AI help on topic", False),
                ]
            },
            {
                "title": "💳 UPI PAYMENTS",
                "description": "```fix\nManage UPI payments and QR codes\n```",
                "fields": [
                    (f"{BOT_PREFIX}upi", "Show current UPI configuration", False),
                    (f"{BOT_PREFIX}upi-qr [amount]", "Generate UPI QR code", False),
                    (f"{BOT_PREFIX}pay <amount> [note]", "Generate payment link", False),
                ]
            },
        ]
        
        if is_admin(str(ctx.author.id)):
            self.pages.append({
                "title": "🛡️ ADMIN COMMANDS",
                "description": "```fix\nCommands for administrators\n```",
                "fields": [
                    (f"{BOT_PREFIX}create <ram> <cpu> <disk> @user", "Create VPS for user", False),
                    (f"{BOT_PREFIX}delete @user <num> [reason]", "Delete user's VPS", False),
                    (f"{BOT_PREFIX}suspend <container> [reason]", "Suspend VPS", False),
                    (f"{BOT_PREFIX}unsuspend <container>", "Unsuspend VPS", False),
                    (f"{BOT_PREFIX}add-resources <container> [ram] [cpu] [disk]", "Add resources", False),
                    (f"{BOT_PREFIX}userinfo @user", "User information with API key", False),
                    (f"{BOT_PREFIX}list-all", "List all VPS in system", False),
                    (f"{BOT_PREFIX}add-inv @user <amount>", "Add invites", False),
                    (f"{BOT_PREFIX}remove-inv @user <amount>", "Remove invites", False),
                    (f"{BOT_PREFIX}ports-add @user <amount>", "Add port slots", False),
                    (f"{BOT_PREFIX}serverstats", "Server statistics", False),
                    (f"{BOT_PREFIX}admin-add-ipv4 @user <container>", "Assign IPv4", False),
                    (f"{BOT_PREFIX}admin-rm-ipv4 @user [container]", "Remove IPv4", False),
                    (f"{BOT_PREFIX}admin-pending-ipv4", "View pending IPv4 purchases", False),
                    (f"{BOT_PREFIX}admin-panels", "List all installed panels", False),
                    (f"{BOT_PREFIX}node-add", "Add new node", False),
                    (f"{BOT_PREFIX}node-remove", "Remove node", False),
                    (f"{BOT_PREFIX}admin-add-upi <upi-id> [name]", "Set UPI ID", False),
                    (f"{BOT_PREFIX}admin-upi-qr", "Generate and set UPI QR", False),
                ]
            })
        
        if str(ctx.author.id) in [str(a) for a in MAIN_ADMIN_IDS]:
            self.pages.append({
                "title": "👑 MAIN ADMIN COMMANDS",
                "description": "```fix\nCommands for main administrator only\n```",
                "fields": [
                    (f"{BOT_PREFIX}admin-add @user", "Add new admin", False),
                    (f"{BOT_PREFIX}admin-remove @user", "Remove admin", False),
                    (f"{BOT_PREFIX}admin-list", "List all admins", False),
                    (f"{BOT_PREFIX}maintenance <on/off>", "Toggle maintenance mode", False),
                    (f"{BOT_PREFIX}set-threshold <cpu> <ram> <disk>", "Set resource thresholds", False),
                    (f"{BOT_PREFIX}purge-all", "Purge all unprotected VPS", False),
                    (f"{BOT_PREFIX}protect @user [num]", "Protect VPS from purge", False),
                    (f"{BOT_PREFIX}unprotect @user [num]", "Remove purge protection", False),
                    (f"{BOT_PREFIX}admin-users", "List all users", False),
                    (f"{BOT_PREFIX}system-info", "Detailed system information", False),
                    (f"{BOT_PREFIX}backup-db", "Backup database", False),
                    (f"{BOT_PREFIX}restore-db <file>", "Restore database", False),
                    (f"{BOT_PREFIX}reset-license", "Reset license verification", False),
                ]
            })
        
        self.update_embed()
    
    def update_embed(self):
        """Update the embed for current page"""
        page = self.pages[self.current_page]
        
        embed = discord.Embed(
            title=f"```glow\n{page['title']}\n```",
            description=page['description'],
            color=0x9B59B6 if "ADMIN" in page['title'] else 0x5865F2
        )
        
        if THUMBNAIL_URL:
            embed.set_thumbnail(url=THUMBNAIL_URL)
        
        for name, value, inline in page["fields"]:
            embed.add_field(name=f"**{name}**", value=value, inline=inline)
        
        footer_text = f"⚡ Page {self.current_page + 1}/{len(self.pages)} • Use buttons to navigate • {BOT_NAME} ⚡"
        embed.set_footer(
            text=footer_text,
            icon_url=THUMBNAIL_URL
        )
        
        self.embed = embed
    
    @discord.ui.button(label="◀️", style=discord.ButtonStyle.secondary)
    async def prev_button(self, button: Button, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        self.current_page = (self.current_page - 1) % len(self.pages)
        self.update_embed()
        await interaction.response.edit_message(embed=self.embed, view=self)
    
    @discord.ui.button(label="▶️", style=discord.ButtonStyle.secondary)
    async def next_button(self, button: Button, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        self.current_page = (self.current_page + 1) % len(self.pages)
        self.update_embed()
        await interaction.response.edit_message(embed=self.embed, view=self)
    
    @discord.ui.button(label="🗑️", style=discord.ButtonStyle.danger)
    async def delete_button(self, button: Button, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        await interaction.message.delete()

@bot.command(name="help")
@commands.cooldown(1, 3, commands.BucketType.user)
async def help_command(ctx):
    """Show interactive help menu - FIXED"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = ctx.author.id
    if user_id in active_help_menus:
        try:
            await active_help_menus[user_id].delete()
        except:
            pass
    
    view = HelpView(ctx)
    msg = await ctx.send(embed=view.embed, view=view)
    active_help_menus[user_id] = msg

@bot.command(name="commands")
async def commands_alias(ctx):
    """Alias for help"""
    await help_command(ctx)

# ==================================================================================================
#  ℹ️  INFO COMMANDS
# ==================================================================================================

@bot.command(name="ping")
@commands.cooldown(1, 3, commands.BucketType.user)
async def ping_command(ctx):
    """Check bot latency with graph - FIXED"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    start = time.time()
    msg = await ctx.send(embed=info_embed("Pinging...", "```fix\nMeasuring latency...\n```"))
    end = time.time()
    
    api_latency = round(bot.latency * 1000)
    response_latency = round((end - start) * 1000)
    
    embed = create_embed("Pong! 🏓")
    
    # Create latency bar
    if api_latency < 100:
        bar = "🟩" * 10
        status = "Excellent"
    elif api_latency < 200:
        bar = "🟨" * 7 + "⬜" * 3
        status = "Good"
    else:
        bar = "🟥" * 5 + "⬜" * 5
        status = "Poor"
    
    embed.add_field(name="📡 API Latency", value=f"```fix\n{api_latency}ms\n```", inline=True)
    embed.add_field(name="⏱️ Response Time", value=f"```fix\n{response_latency}ms\n```", inline=True)
    embed.add_field(name="📊 Status", value=f"```fix\n{status}\n{bar}\n```", inline=False)
    
    await msg.edit(embed=embed)

@bot.command(name="uptime")
@commands.cooldown(1, 5, commands.BucketType.user)
async def uptime_command(ctx):
    """Show bot uptime"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    uptime = datetime.utcnow() - bot.start_time
    days = uptime.days
    hours, rem = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    
    embed = info_embed(
        "Bot Uptime",
        f"```fix\n{days}d {hours}h {minutes}m {seconds}s\n```"
    )
    await ctx.send(embed=embed)

@bot.command(name="server-info")
@commands.cooldown(1, 5, commands.BucketType.user)
async def server_info(ctx):
    """Show server hardware information"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    # Get system info
    cpu_count = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq()
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk = psutil.disk_usage('/')
    disk_io = psutil.disk_io_counters()
    network = psutil.net_io_counters()
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    users = psutil.users()
    
    embed = create_embed("Server Information")
    
    # System Info
    sys_info = f"```fix\n"
    sys_info += f"Hostname : {HOSTNAME}\n"
    sys_info += f"Server IP: {SERVER_IP}\n"
    sys_info += f"MAC Addr : {MAC_ADDRESS}\n"
    sys_info += f"Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    sys_info += f"Users    : {len(users)}\n"
    sys_info += f"```"
    embed.add_field(name="💻 System", value=sys_info, inline=False)
    
    # CPU Info
    cpu_info = f"```fix\n"
    cpu_info += f"Cores    : {psutil.cpu_count()} ({psutil.cpu_count(logical=False)} physical)\n"
    cpu_info += f"Usage    : {cpu_percent:.1f}% (avg)\n"
    cpu_info += f"Frequency: {cpu_freq.current:.0f} MHz\n" if cpu_freq else ""
    cpu_info += f"```"
    embed.add_field(name="⚙️ CPU", value=cpu_info, inline=True)
    
    # Memory Info
    mem_info = f"```fix\n"
    mem_info += f"RAM      : {memory.used//1024//1024}MB/{memory.total//1024//1024}MB ({memory.percent}%)\n"
    mem_info += f"Swap     : {swap.used//1024//1024}MB/{swap.total//1024//1024}MB ({swap.percent}%)\n"
    mem_info += f"```"
    embed.add_field(name="💾 Memory", value=mem_info, inline=True)
    
    # Disk Info
    disk_info = f"```fix\n"
    disk_info += f"Disk     : {disk.used//1024//1024//1024}GB/{disk.total//1024//1024//1024}GB ({disk.percent}%)\n"
    disk_info += f"Read     : {disk_io.read_bytes//1024//1024} MB\n" if disk_io else ""
    disk_info += f"Write    : {disk_io.write_bytes//1024//1024} MB\n" if disk_io else ""
    disk_info += f"```"
    embed.add_field(name="📀 Disk", value=disk_info, inline=True)
    
    # Network Info
    net_info = f"```fix\n"
    net_info += f"Sent     : {network.bytes_sent/1024/1024:.2f} MB\n"
    net_info += f"Received : {network.bytes_recv/1024/1024:.2f} MB\n"
    net_info += f"Packets Sent: {network.packets_sent}\n"
    net_info += f"Packets Recv: {network.packets_recv}\n"
    net_info += f"```"
    embed.add_field(name="🌐 Network", value=net_info, inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name="bot-info")
@commands.cooldown(1, 5, commands.BucketType.user)
async def bot_info(ctx):
    """Show detailed bot information"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    uptime = datetime.utcnow() - bot.start_time
    days = uptime.days
    hours, rem = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(rem, 60)
    
    all_vps = get_all_vps()
    total_vps = len(all_vps)
    running_vps = sum(1 for v in all_vps if v['status'] == 'running' and not v['suspended'])
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT COUNT(DISTINCT user_id) FROM vps')
    total_users = cur.fetchone()[0] or 0
    
    cur.execute('SELECT COUNT(*) FROM panels')
    total_panels = cur.fetchone()[0] or 0
    
    cur.execute('SELECT COUNT(*) FROM nodes')
    total_nodes = cur.fetchone()[0] or 0
    
    cur.execute('SELECT COUNT(*) FROM transactions WHERE status = "pending"')
    pending_txns = cur.fetchone()[0] or 0
    conn.close()
    
    embed = create_embed("Bot Information")
    embed.add_field(name="📦 Version", value="```fix\n5.0.0\n```", inline=True)
    embed.add_field(name="👑 Author", value=f"```fix\n{BOT_AUTHOR}\n```", inline=True)
    embed.add_field(name="📚 Library", value=f"```fix\ndiscord.py {discord.__version__}\n```", inline=True)
    embed.add_field(name="⏱️ Uptime", value=f"```fix\n{days}d {hours}h {minutes}m\n```", inline=True)
    embed.add_field(name="🌐 Servers", value=f"```fix\n{len(bot.guilds)}\n```", inline=True)
    embed.add_field(name="👥 Users", value=f"```fix\n{total_users}\n```", inline=True)
    embed.add_field(name="🖥️ Total VPS", value=f"```fix\n{total_vps}\n```", inline=True)
    embed.add_field(name="🟢 Running VPS", value=f"```fix\n{running_vps}\n```", inline=True)
    embed.add_field(name="📦 Panels", value=f"```fix\n{total_panels}\n```", inline=True)
    embed.add_field(name="🌍 Nodes", value=f"```fix\n{total_nodes}\n```", inline=True)
    embed.add_field(name="💳 Pending Txns", value=f"```fix\n{pending_txns}\n```", inline=True)
    embed.add_field(name="🌐 Server IP", value=f"```fix\n{SERVER_IP}\n```", inline=True)
    embed.add_field(name="🔌 MAC", value=f"```fix\n{MAC_ADDRESS[:17]}\n```", inline=True)
    embed.add_field(name="🔐 License", value="```fix\n✅ VERIFIED\n```" if LICENSE_VERIFIED else "```fix\n❌ NOT VERIFIED\n```", inline=True)
    embed.add_field(name="🤖 AI Model", value=f"```fix\n{AI_MODEL}\n```", inline=True)
    
    await ctx.send(embed=embed)

# ==================================================================================================
#  👤  ACCOUNT GENERATOR WITH API KEY
# ==================================================================================================

def generate_username() -> str:
    """Generate a random username"""
    adjectives = ["cool", "fast", "dark", "epic", "blue", "swift", "neon", "alpha", "delta", "super", 
                  "mega", "ultra", "hyper", "cyber", "tech", "quantum", "nano", "pixel", "digital", "cloud",
                  "storm", "thunder", "lightning", "shadow", "phantom", "ghost", "crypto", "binary", "atomic"]
    nouns = ["wolf", "tiger", "storm", "byte", "nova", "blade", "fox", "raven", "hawk", "lion", 
             "dragon", "phoenix", "eagle", "shark", "viper", "phantom", "shadow", "ghost", "knight", "warrior",
             "phoenix", "dragon", "titan", "giant", "master", "legend", "hero", "ninja", "samurai"]
    num = random.randint(10, 9999)
    return f"{random.choice(adjectives)}{random.choice(nouns)}{num}"

def generate_email(username: str = None) -> str:
    """Generate a random email"""
    if not username:
        username = generate_username()
    domains = ["gmail.com", "yahoo.com", "outlook.com", "proton.me", "hotmail.com", "mail.com", 
               "icloud.com", "aol.com", "yandex.com", "gmx.com", "tutanota.com", "zoho.com"]
    return f"{username}@{random.choice(domains)}"

def generate_password(length: int = 16) -> str:
    """Generate a random password"""
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choices(chars, k=length))

@bot.command(name="gen-acc")
@commands.cooldown(1, 10, commands.BucketType.user)
async def gen_account(ctx):
    """Generate a random account with API key"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    username = generate_username()
    email = generate_email(username)
    password = generate_password()
    api_key = hashlib.sha256(f"{ctx.author.id}{time.time()}{random.randint(1000,9999)}".encode()).hexdigest()[:32]
    
    # Save to database
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute('''CREATE TABLE IF NOT EXISTS generated_accounts (
        user_id TEXT PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL,
        api_key TEXT NOT NULL,
        created_at TEXT NOT NULL
    )''')
    
    cur.execute('''INSERT OR REPLACE INTO generated_accounts (user_id, username, email, password, api_key, created_at)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                (str(ctx.author.id), username, email, password, api_key, datetime.now().isoformat()))
    conn.commit()
    conn.close()
    
    # Update user stats with API key
    update_user_stats(str(ctx.author.id))
    
    # Try to DM the full credentials
    try:
        dm_embed = success_embed("🔐 Your Generated Account")
        dm_embed.add_field(name="👤 Username", value=f"```fix\n{username}\n```", inline=False)
        dm_embed.add_field(name="📧 Email", value=f"```fix\n{email}\n```", inline=False)
        dm_embed.add_field(name="🔑 Password", value=f"```fix\n{password}\n```", inline=False)
        dm_embed.add_field(name="🗝️ API Key", value=f"```fix\n{api_key}\n```", inline=False)
        dm_embed.set_footer(text="⚡ Keep these safe! Delete this message after saving. ⚡")
        await ctx.author.send(embed=dm_embed)
        dm_status = "✅ Sent to your DMs"
    except:
        dm_status = "❌ Failed to send DM (enable DMs)"
    
    embed = success_embed("Account Generated!")
    embed.add_field(name="👤 Username", value=f"```fix\n{username}\n```", inline=True)
    embed.add_field(name="📧 Email", value=f"||`{email}`||", inline=True)
    embed.add_field(name="🔑 Password", value=f"||`{password}`||", inline=False)
    embed.add_field(name="🗝️ API Key", value=f"||`{api_key}`||", inline=False)
    embed.add_field(name="📩 DM Status", value=f"```fix\n{dm_status}\n```", inline=False)
    embed.set_footer(text="⚡ Full credentials sent to DM (check spam) ⚡")
    await ctx.send(embed=embed)

@bot.command(name="my-acc")
@commands.cooldown(1, 5, commands.BucketType.user)
async def my_account(ctx):
    """View your generated account"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM generated_accounts WHERE user_id = ?', (str(ctx.author.id),))
    account = cur.fetchone()
    conn.close()
    
    if account:
        embed = info_embed("Your Generated Account")
        embed.add_field(name="👤 Username", value=f"```fix\n{account['username']}\n```", inline=True)
        embed.add_field(name="📧 Email", value=f"||`{account['email']}`||", inline=True)
        embed.add_field(name="🔑 Password", value=f"||`{account['password']}`||", inline=False)
        embed.add_field(name="🗝️ API Key", value=f"||`{account['api_key']}`||", inline=False)
        embed.add_field(name="📅 Created", value=f"```fix\n{account['created_at'][:16]}\n```", inline=True)
    else:
        stats = get_user_stats(str(ctx.author.id))
        embed = info_embed("Your Account Info")
        embed.add_field(name="🆔 User ID", value=f"```fix\n{ctx.author.id}\n```", inline=True)
        embed.add_field(name="📨 Invites", value=f"```fix\n{stats.get('invites', 0)}\n```", inline=True)
        embed.add_field(name="🚀 Boosts", value=f"```fix\n{stats.get('boosts', 0)}\n```", inline=True)
        embed.add_field(name="🖥️ Claimed VPS", value=f"```fix\n{stats.get('claimed_vps_count', 0)}\n```", inline=True)
        embed.add_field(name="🗝️ API Key", value=f"```fix\n{stats.get('api_key', 'None')}\n```", inline=True)
        embed.add_field(name="📝 Note", value=f"Use `{BOT_PREFIX}gen-acc` to generate a new account", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name="api-key")
@commands.cooldown(1, 5, commands.BucketType.user)
async def api_key_command(ctx, action: str = "view"):
    """View or regenerate your API key"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    if action.lower() == "regenerate" or action.lower() == "new":
        # Generate new API key
        new_key = hashlib.sha256(f"{user_id}{time.time()}{random.randint(1000,9999)}".encode()).hexdigest()[:32]
        
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE user_stats SET api_key = ?, last_updated = ? WHERE user_id = ?',
                   (new_key, datetime.now().isoformat(), user_id))
        conn.commit()
        conn.close()
        
        embed = success_embed("API Key Regenerated", f"```fix\n{new_key}\n```\nKeep this key safe!")
        await ctx.send(embed=embed)
    else:
        # View current API key
        stats = get_user_stats(user_id)
        api_key = stats.get('api_key')
        
        if not api_key:
            api_key = get_user_api_key(user_id)
        
        embed = info_embed("Your API Key", f"```fix\n{api_key}\n```\nUse `{BOT_PREFIX}api-key regenerate` to generate a new one.")
        await ctx.send(embed=embed)

# ==================================================================================================
#  💰  FREE VPS PLANS & INVITE SYSTEM
# ==================================================================================================

@bot.command(name="plans")
@commands.cooldown(1, 5, commands.BucketType.user)
async def show_plans(ctx):
    """Show free VPS plans"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    embed = create_embed("Free VPS Plans", "```fix\nEarn VPS by inviting users to the server!\n```")
    
    plans_text = ""
    for plan in FREE_VPS_PLANS['invites']:
        plans_text += f"{plan['emoji']} **{plan['name']}**\n"
        plans_text += f"   • RAM: {plan['ram']}GB\n"
        plans_text += f"   • CPU: {plan['cpu']} Core(s)\n"
        plans_text += f"   • Disk: {plan['disk']}GB\n"
        plans_text += f"   • Requires: {plan['invites']} invites\n\n"
    
    embed.add_field(name="📋 Available Plans", value=plans_text, inline=False)
    embed.add_field(
        name="📌 How to Claim",
        value=f"• Use `{BOT_PREFIX}inv` to check your invites\n"
              f"• Use `{BOT_PREFIX}claim-free` to claim your VPS\n"
              f"• Invite more users to unlock better plans!",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name="freeplans")
async def freeplans_alias(ctx):
    """Alias for plans"""
    await show_plans(ctx)

@bot.command(name="inv")
@commands.cooldown(1, 3, commands.BucketType.user)
async def check_invites(ctx):
    """Check your invites"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    stats = get_user_stats(str(ctx.author.id))
    invites = stats.get('invites', 0)
    
    embed = info_embed("Your Invite Stats", f"```fix\nCurrent invites: {invites}\n```")
    
    # Show available plans
    available = []
    for plan in FREE_VPS_PLANS['invites']:
        if invites >= plan['invites']:
            available.append(f"✅ {plan['emoji']} {plan['name']}")
        else:
            available.append(f"❌ {plan['emoji']} {plan['name']} (need {plan['invites']})")
    
    embed.add_field(name="📋 Available Plans", value="\n".join(available), inline=False)
    embed.add_field(
        name="📌 Next Steps",
        value=f"• Use `{BOT_PREFIX}claim-free` to claim your VPS",
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name="invites-top")
@commands.cooldown(1, 5, commands.BucketType.user)
async def invites_top(ctx, limit: int = 10):
    """Show top inviters"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT user_id, invites FROM user_stats WHERE invites > 0 ORDER BY invites DESC LIMIT ?', (limit,))
    rows = cur.fetchall()
    conn.close()
    
    if not rows:
        await ctx.send(embed=info_embed("Top Inviters", "No invites yet."))
        return
    
    embed = info_embed(f"Top {min(limit, len(rows))} Inviters")
    
    for i, row in enumerate(rows, 1):
        try:
            user = await bot.fetch_user(int(row['user_id']))
            username = user.name
        except:
            username = f"Unknown ({row['user_id']})"
        
        embed.add_field(
            name=f"{i}. {username}",
            value=f"```fix\nInvites: {row['invites']}\n```",
            inline=False
        )
    
    await ctx.send(embed=embed)

class ClaimOSSelectView(View):
    """OS selection for VPS claim"""
    def __init__(self, ctx, plan):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.plan = plan
        
        options = []
        for os in OS_OPTIONS[:25]:
            options.append(discord.SelectOption(
                label=os["label"][:100],
                value=os["value"],
                description=os["desc"][:100] if os["desc"] else None,
                emoji=os.get("emoji", "🐧")
            ))
        
        self.select = Select(
            placeholder="📋 Select an operating system...",
            options=options,
            min_values=1,
            max_values=1
        )
        self.select.callback = self.select_callback
        self.add_item(self.select)
        
        cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary, row=1)
        cancel_btn.callback = self.cancel_callback
        self.add_item(cancel_btn)
    
    async def select_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        selected_os = self.select.values[0]
        
        # Create confirmation view
        view = View(timeout=60)
        confirm_btn = Button(label="✅ Confirm", style=discord.ButtonStyle.success)
        cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
        
        async def confirm_callback(confirm_interaction):
            await self.create_vps(confirm_interaction, selected_os)
        
        async def cancel_callback(cancel_interaction):
            await cancel_interaction.response.edit_message(
                embed=info_embed("Cancelled", "```fix\nVPS creation cancelled.\n```"),
                view=None
            )
        
        confirm_btn.callback = confirm_callback
        cancel_btn.callback = cancel_callback
        view.add_item(confirm_btn)
        view.add_item(cancel_btn)
        
        os_name = next((o["label"] for o in OS_OPTIONS if o["value"] == selected_os), selected_os)
        
        embed = warning_embed(
            "Confirm VPS Creation",
            f"```fix\nPlan: {self.plan['name']}\nOS: {os_name}\nRAM: {self.plan['ram']}GB\nCPU: {self.plan['cpu']} Core(s)\nDisk: {self.plan['disk']}GB\n```\n"
            f"This will use **{self.plan['invites']}** invites from your account."
        )
        
        await interaction.response.edit_message(embed=embed, view=view)
    
    async def cancel_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        await interaction.response.edit_message(
            embed=info_embed("Cancelled", "```fix\nVPS creation cancelled.\n```"),
            view=None
        )
    
    async def create_vps(self, interaction: discord.Interaction, os_version: str):
        await interaction.response.defer(ephemeral=True)
        
        user_id = str(self.ctx.author.id)
        stats = get_user_stats(user_id)
        
        # Check if user already has a VPS
        user_vps = get_user_vps(user_id)
        if user_vps:
            await interaction.followup.send(
                embed=error_embed("VPS Already Exists", "```diff\n- You already have a VPS. Contact an admin if you need another.\n```"),
                ephemeral=True
            )
            return
        
        # Generate container name
        container_name = f"svm5-{user_id[:6]}-{random.randint(1000, 9999)}"
        
        # Create the container
        progress = await interaction.followup.send(
            embed=info_embed("Creating VPS", "```fix\nStep 1/4: Initializing container...\n```"),
            ephemeral=True
        )
        
        try:
            # Initialize container
            ram_mb = self.plan['ram'] * 1024
            await run_lxc(f"lxc init {os_version} {container_name} -s {DEFAULT_STORAGE_POOL}")
            
            await progress.edit(embed=info_embed("Creating VPS", "```fix\nStep 2/4: Configuring resources...\n```"))
            
            # Set limits
            await run_lxc(f"lxc config set {container_name} limits.memory {ram_mb}MB")
            await run_lxc(f"lxc config set {container_name} limits.cpu {self.plan['cpu']}")
            await run_lxc(f"lxc config device set {container_name} root size={self.plan['disk']}GB")
            
            # Apply LXC config
            await apply_lxc_config(container_name)
            
            await progress.edit(embed=info_embed("Creating VPS", "```fix\nStep 3/4: Starting container...\n```"))
            
            # Start container
            await run_lxc(f"lxc start {container_name}")
            
            # Apply internal permissions
            await apply_internal_permissions(container_name)
            
            await progress.edit(embed=info_embed("Creating VPS", "```fix\nStep 4/4: Finalizing...\n```"))
            
            # Get container IP and MAC
            out, _, _ = await exec_in_container(container_name, "ip -4 addr show eth0 | grep -oP '(?<=inet\\s)\\d+\\.\\d+\\.\\d+\\.\\d+' | head -1")
            ip = out.strip() if out else "N/A"
            
            out, _, _ = await exec_in_container(container_name, "ip link show eth0 | grep -oP '(?<=link/ether\\s)\\S+'")
            mac = out.strip() if out else "N/A"
            
            # Save to database
            vps = add_vps(
                user_id=user_id,
                container_name=container_name,
                ram=self.plan['ram'],
                cpu=self.plan['cpu'],
                disk=self.plan['disk'],
                os_version=os_version,
                plan_name=self.plan['name']
            )
            
            # Update VPS with IP and MAC
            conn = get_db()
            cur = conn.cursor()
            cur.execute('UPDATE vps SET ip_address = ?, mac_address = ? WHERE container_name = ?',
                       (ip, mac, container_name))
            conn.commit()
            conn.close()
            
            # Deduct invites
            update_user_stats(user_id, invites=-self.plan['invites'], claimed_vps_count=1)
            
            # Assign role
            if self.ctx.guild:
                role = discord.utils.get(self.ctx.guild.roles, name=f"{BOT_NAME} User")
                if not role:
                    role = await self.ctx.guild.create_role(name=f"{BOT_NAME} User", color=discord.Color.purple())
                try:
                    await self.ctx.author.add_roles(role)
                except:
                    pass
            
            # Send DM
            try:
                dm_embed = success_embed("✅ VPS Created Successfully!")
                dm_embed.add_field(name="📦 Container", value=f"```fix\n{container_name}\n```", inline=True)
                dm_embed.add_field(name="📋 Plan", value=f"```fix\n{self.plan['name']}\n```", inline=True)
                dm_embed.add_field(name="🐧 OS", value=f"```fix\n{os_version}\n```", inline=True)
                dm_embed.add_field(name="⚙️ Resources", value=f"```fix\n{self.plan['ram']}GB RAM / {self.plan['cpu']} CPU / {self.plan['disk']}GB Disk\n```", inline=False)
                dm_embed.add_field(name="🌐 IP Address", value=f"```fix\n{ip}\n```", inline=True)
                dm_embed.add_field(name="🔌 MAC Address", value=f"```fix\n{mac}\n```", inline=True)
                dm_embed.add_field(name="🖥️ Management", value=f"Use `{BOT_PREFIX}manage` to control your VPS", inline=False)
                dm_embed.add_field(name="📟 Console", value=f"Use `{BOT_PREFIX}ss {container_name}` to view console", inline=False)
                await self.ctx.author.send(embed=dm_embed)
            except:
                pass
            
            # Success message
            embed = success_embed("✅ VPS Created Successfully!")
            embed.add_field(name="📦 Container", value=f"```fix\n{container_name}\n```", inline=True)
            embed.add_field(name="📋 Plan", value=f"```fix\n{self.plan['name']}\n```", inline=True)
            embed.add_field(name="🐧 OS", value=f"```fix\n{os_version}\n```", inline=True)
            embed.add_field(name="⚙️ Resources", value=f"```fix\n{self.plan['ram']}GB RAM / {self.plan['cpu']} CPU / {self.plan['disk']}GB Disk\n```", inline=False)
            embed.add_field(name="🌐 IP Address", value=f"```fix\n{ip}\n```", inline=True)
            embed.add_field(name="🔌 MAC Address", value=f"```fix\n{mac}\n```", inline=True)
            embed.add_field(name="🖥️ Management", value=f"Use `{BOT_PREFIX}manage` to control your VPS", inline=False)
            embed.add_field(name="📟 Console", value=f"Use `{BOT_PREFIX}ss {container_name}` to view console", inline=False)
            
            await progress.edit(embed=embed)
            
            # Log
            logger.info(f"User {self.ctx.author} created VPS {container_name} with plan {self.plan['name']}")
            
        except Exception as e:
            logger.error(f"VPS creation failed: {e}")
            await progress.edit(embed=error_embed("Creation Failed", f"```diff\n- Error: {str(e)}\n```"))
            
            # Clean up on failure
            try:
                await run_lxc(f"lxc delete {container_name} --force")
            except:
                pass

@bot.command(name="claim-free")
@commands.cooldown(1, 60, commands.BucketType.user)
async def claim_free(ctx):
    """Claim a free VPS based on your invites"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    stats = get_user_stats(user_id)
    invites = stats.get('invites', 0)
    
    # Check if user already has a VPS
    user_vps = get_user_vps(user_id)
    if user_vps:
        await ctx.send(embed=error_embed(
            "VPS Already Exists",
            "```diff\n- You already have a VPS. Each user can only claim one free VPS.\n```"
        ))
        return
    
    # Find highest eligible plan
    eligible_plan = None
    for plan in reversed(FREE_VPS_PLANS['invites']):
        if invites >= plan['invites']:
            eligible_plan = plan
            break
    
    if not eligible_plan:
        await ctx.send(embed=error_embed(
            "No Eligible Plans",
            f"```diff\n- You have {invites} invites.\n- You need at least 5 invites to claim a VPS.\n```\n\n"
            f"Invite more users to unlock plans!"
        ))
        return
    
    # Show plan details and ask for OS
    embed = info_embed(
        "You are eligible for:",
        f"**{eligible_plan['emoji']} {eligible_plan['name']}**\n"
        f"• RAM: {eligible_plan['ram']}GB\n"
        f"• CPU: {eligible_plan['cpu']} Core(s)\n"
        f"• Disk: {eligible_plan['disk']}GB\n"
        f"• Cost: {eligible_plan['invites']} invites\n\n"
        f"Please select an operating system:"
    )
    
    view = ClaimOSSelectView(ctx, eligible_plan)
    await ctx.send(embed=embed, view=view)

@bot.command(name="stats")
@commands.cooldown(1, 3, commands.BucketType.user)
async def user_stats_command(ctx):
    """View your statistics with API key"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    stats = get_user_stats(user_id)
    user_vps = get_user_vps(user_id)
    
    embed = info_embed(f"Statistics for {ctx.author.display_name}")
    embed.add_field(name="📨 Invites", value=f"```fix\n{stats.get('invites', 0)}\n```", inline=True)
    embed.add_field(name="🚀 Boosts", value=f"```fix\n{stats.get('boosts', 0)}\n```", inline=True)
    embed.add_field(name="🖥️ VPS Count", value=f"```fix\n{len(user_vps)}\n```", inline=True)
    embed.add_field(name="🎁 Claimed VPS", value=f"```fix\n{stats.get('claimed_vps_count', 0)}\n```", inline=True)
    embed.add_field(name="🗝️ API Key", value=f"```fix\n{stats.get('api_key', 'None')}\n```", inline=False)
    
    await ctx.send(embed=embed)

# ==================================================================================================
#  🌐 NODE MANAGEMENT COMMANDS
# ==================================================================================================

@bot.command(name="node")
@commands.cooldown(1, 3, commands.BucketType.user)
async def node_list(ctx):
    """List all nodes with stats"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    nodes = get_all_nodes()
    
    if not nodes:
        embed = info_embed(
            "No Nodes",
            "```fix\nNo nodes have been added yet.\n```\n\n"
            f"Use `{BOT_PREFIX}node-add` to add a node (admin only)."
        )
        await ctx.send(embed=embed)
        return
    
    embed = node_embed(f"Node Network ({len(nodes)} nodes)")
    
    online_count = sum(1 for n in nodes if n['status'] == 'online')
    offline_count = len(nodes) - online_count
    
    embed.add_field(name="📊 Summary", value=f"```fix\nOnline: {online_count} | Offline: {offline_count}\n```", inline=False)
    
    for node in nodes:
        status_emoji = "🟢" if node['status'] == 'online' else "🔴"
        
        ram_usage = (node['used_ram'] / node['total_ram'] * 100) if node['total_ram'] > 0 else 0
        cpu_usage = node['used_cpu']
        disk_usage = (node['used_disk'] / node['total_disk'] * 100) if node['total_disk'] > 0 else 0
        
        node_info = f"```fix\n"
        node_info += f"Host    : {node['host']}:{node['port']}\n"
        node_info += f"RAM     : {node['used_ram']}/{node['total_ram']} MB ({ram_usage:.1f}%)\n"
        node_info += f"CPU     : {cpu_usage:.1f}%\n"
        node_info += f"Disk    : {node['used_disk']}/{node['total_disk']} GB ({disk_usage:.1f}%)\n"
        node_info += f"LXC     : {node['lxc_count']} containers\n"
        node_info += f"Region  : {node.get('region', 'us')}\n"
        node_info += f"Last    : {node.get('last_checked', 'Never')[:16]}\n"
        node_info += f"```"
        
        embed.add_field(
            name=f"{status_emoji} {node['name']}",
            value=node_info,
            inline=False
        )
    
    embed.set_footer(text=f"⚡ Use {BOT_PREFIX}node-info <name> for details ⚡")
    await ctx.send(embed=embed)

@bot.command(name="node-info")
@commands.cooldown(1, 3, commands.BucketType.user)
async def node_info(ctx, name: str):
    """Get detailed node information"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    node = get_node(name)
    
    if not node:
        await ctx.send(embed=error_embed("Node Not Found", f"```diff\n- Node '{name}' not found.\n```"))
        return
    
    embed = node_embed(f"Node Details: {name}")
    
    status_emoji = "🟢" if node['status'] == 'online' else "🔴"
    
    # Basic info
    basic = f"```fix\n"
    basic += f"Status  : {node['status'].upper()}\n"
    basic += f"Host    : {node['host']}:{node['port']}\n"
    basic += f"Username: {node['username']}\n"
    basic += f"Region  : {node.get('region', 'us')}\n"
    basic += f"Added   : {node['added_at'][:16]}\n"
    basic += f"Added By: {node.get('added_by', 'System')}\n"
    basic += f"```"
    embed.add_field(name="📋 Basic Info", value=basic, inline=False)
    
    # Resource usage
    ram_usage = (node['used_ram'] / node['total_ram'] * 100) if node['total_ram'] > 0 else 0
    cpu_usage = node['used_cpu']
    disk_usage = (node['used_disk'] / node['total_disk'] * 100) if node['total_disk'] > 0 else 0
    
    resources = f"```fix\n"
    resources += f"RAM     : {node['used_ram']}/{node['total_ram']} MB ({ram_usage:.1f}%)\n"
    resources += f"CPU     : {cpu_usage:.1f}%\n"
    resources += f"Disk    : {node['used_disk']}/{node['total_disk']} GB ({disk_usage:.1f}%)\n"
    resources += f"LXC     : {node['lxc_count']} containers\n"
    resources += f"Last    : {node.get('last_checked', 'Never')}\n"
    resources += f"```"
    embed.add_field(name="📊 Resource Usage", value=resources, inline=False)
    
    # API Info
    api_info = f"```fix\n"
    api_info += f"API Key : {node['api_key'][:8]}...{node['api_key'][-8:]}\n"
    api_info += f"API URL : {node.get('api_url', 'N/A')}\n"
    api_info += f"```"
    embed.add_field(name="🔌 API Information", value=api_info, inline=False)
    
    # Description
    if node.get('description'):
        embed.add_field(name="📝 Description", value=f"```fix\n{node['description']}\n```", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name="node-add")
@admin_only()
@commands.cooldown(1, 10, commands.BucketType.user)
async def node_add(ctx, name: str, host: str, username: str, password: str = None, port: int = 22):
    """Add a new node to the cluster"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    # Check if node already exists
    existing = get_node(name)
    if existing:
        await ctx.send(embed=error_embed("Node Exists", f"```diff\n- Node '{name}' already exists.\n```"))
        return
    
    # Add node to database
    try:
        node = add_node(name, host, username, password, port=port, added_by=str(ctx.author.id))
        
        if not node:
            await ctx.send(embed=error_embed("Failed", "```diff\n- Could not add node to database.\n```"))
            return
        
        # Check node health
        stats = await check_node_health(node)
        update_node_status(name, stats['status'], stats)
        
        embed = success_embed("Node Added Successfully")
        status_emoji = "🟢" if stats['status'] == 'online' else "🔴"
        
        info = f"```fix\n"
        info += f"Name    : {name}\n"
        info += f"Host    : {host}:{port}\n"
        info += f"Status  : {stats['status'].upper()}\n"
        info += f"RAM     : {stats.get('total_ram', 0)} MB\n"
        info += f"CPU     : {stats.get('total_cpu', 0)} cores\n"
        info += f"Disk    : {stats.get('total_disk', 0)} GB\n"
        info += f"API Key : {node['api_key'][:8]}...{node['api_key'][-8:]}\n"
        info += f"```"
        
        embed.add_field(name="📋 Node Information", value=info, inline=False)
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(embed=error_embed("Failed to Add Node", f"```diff\n- Error: {str(e)}\n```"))

@bot.command(name="node-remove")
@admin_only()
@commands.cooldown(1, 10, commands.BucketType.user)
async def node_remove(ctx, name: str):
    """Remove a node from the cluster"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    # Check if node exists
    node = get_node(name)
    if not node:
        await ctx.send(embed=error_embed("Node Not Found", f"```diff\n- Node '{name}' not found.\n```"))
        return
    
    # Confirm deletion
    view = View(timeout=60)
    confirm_btn = Button(label="✅ Confirm", style=discord.ButtonStyle.danger)
    cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    
    async def confirm_callback(interaction):
        if delete_node(name):
            embed = success_embed("Node Removed", f"```fix\nNode '{name}' has been removed.\n```")
            await interaction.response.edit_message(embed=embed, view=None)
        else:
            await interaction.response.edit_message(embed=error_embed("Failed", "```diff\n- Could not remove node.\n```"), view=None)
    
    async def cancel_callback(interaction):
        await interaction.response.edit_message(embed=info_embed("Cancelled", "```fix\nNode removal cancelled.\n```"), view=None)
    
    confirm_btn.callback = confirm_callback
    cancel_btn.callback = cancel_callback
    view.add_item(confirm_btn)
    view.add_item(cancel_btn)
    
    embed = warning_embed(
        "Confirm Node Removal",
        f"```fix\nAre you sure you want to remove node '{name}'?\n```\n"
        f"Host: {node['host']}\n"
        f"Status: {node['status']}\n\n"
        f"This action cannot be undone!"
    )
    
    await ctx.send(embed=embed, view=view)

@bot.command(name="node-check")
@admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def node_check(ctx, name: str):
    """Check node health manually"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    node = get_node(name)
    if not node:
        await ctx.send(embed=error_embed("Node Not Found", f"```diff\n- Node '{name}' not found.\n```"))
        return
    
    msg = await ctx.send(embed=info_embed("Checking Node", f"```fix\nChecking health of node '{name}'...\n```"))
    
    stats = await check_node_health(node)
    update_node_status(name, stats['status'], stats)
    
    if stats['status'] == 'online':
        embed = success_embed("Node Health Check", f"```fix\nNode '{name}' is ONLINE\n```")
        
        info = f"```fix\n"
        info += f"RAM     : {stats['used_ram']}/{stats['total_ram']} MB\n"
        info += f"CPU     : {stats['used_cpu']:.1f}%\n"
        info += f"Disk    : {stats['used_disk']}/{stats['total_disk']} GB\n"
        info += f"LXC     : {stats['lxc_count']} containers\n"
        info += f"```"
        embed.add_field(name="📊 Resource Usage", value=info, inline=False)
        
    else:
        embed = error_embed("Node Health Check", f"```diff\n- Node '{name}' is OFFLINE\n```")
    
    await msg.edit(embed=embed)

@bot.command(name="node-stats")
@admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def node_stats(ctx):
    """Show cluster statistics"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    nodes = get_all_nodes()
    
    if not nodes:
        await ctx.send(embed=info_embed("No Nodes", "```fix\nNo nodes in the cluster.\n```"))
        return
    
    total_ram = sum(n['total_ram'] for n in nodes)
    used_ram = sum(n['used_ram'] for n in nodes)
    total_cpu = sum(n['total_cpu'] for n in nodes)
    total_disk = sum(n['total_disk'] for n in nodes)
    used_disk = sum(n['used_disk'] for n in nodes)
    total_lxc = sum(n['lxc_count'] for n in nodes)
    online_nodes = sum(1 for n in nodes if n['status'] == 'online')
    
    embed = node_embed("Cluster Statistics")
    
    summary = f"```fix\n"
    summary += f"Total Nodes  : {len(nodes)}\n"
    summary += f"Online Nodes : {online_nodes}\n"
    summary += f"Offline Nodes: {len(nodes) - online_nodes}\n"
    summary += f"Total LXC    : {total_lxc}\n"
    summary += f"```"
    embed.add_field(name="📊 Summary", value=summary, inline=False)
    
    resources = f"```fix\n"
    resources += f"RAM         : {used_ram}/{total_ram} MB ({(used_ram/total_ram*100) if total_ram>0 else 0:.1f}%)\n"
    resources += f"CPU Cores   : {total_cpu}\n"
    resources += f"Disk        : {used_disk}/{total_disk} GB ({(used_disk/total_disk*100) if total_disk>0 else 0:.1f}%)\n"
    resources += f"```"
    embed.add_field(name="💾 Total Resources", value=resources, inline=False)
    
    # Per-node breakdown
    for node in nodes:
        status_emoji = "🟢" if node['status'] == 'online' else "🔴"
        ram_pct = (node['used_ram'] / node['total_ram'] * 100) if node['total_ram'] > 0 else 0
        disk_pct = (node['used_disk'] / node['total_disk'] * 100) if node['total_disk'] > 0 else 0
        
        node_info = f"{status_emoji} **{node['name']}**\n"
        node_info += f"```fix\n"
        node_info += f"RAM: {node['used_ram']}/{node['total_ram']} MB ({ram_pct:.1f}%)\n"
        node_info += f"CPU: {node['used_cpu']:.1f}%\n"
        node_info += f"Disk: {node['used_disk']}/{node['total_disk']} GB ({disk_pct:.1f}%)\n"
        node_info += f"LXC: {node['lxc_count']}\n"
        node_info += f"```"
        embed.add_field(name=f"Node: {node['name']}", value=node_info, inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name="node-sync")
@admin_only()
@commands.cooldown(1, 30, commands.BucketType.user)
async def node_sync(ctx, name: str):
    """Sync containers from node"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    node = get_node(name)
    if not node:
        await ctx.send(embed=error_embed("Node Not Found", f"```diff\n- Node '{name}' not found.\n```"))
        return
    
    if node['status'] != 'online':
        await ctx.send(embed=error_embed("Node Offline", f"```diff\n- Node '{name}' is offline. Cannot sync.\n```"))
        return
    
    msg = await ctx.send(embed=info_embed("Syncing Node", f"```fix\nSyncing containers from node '{name}'...\n```"))
    
    try:
        import paramiko
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        if node.get('password'):
            client.connect(node['host'], port=node['port'], 
                          username=node['username'], password=node['password'], timeout=10)
        elif node.get('ssh_key'):
            key = paramiko.RSAKey.from_private_key_file(node['ssh_key'])
            client.connect(node['host'], port=node['port'], 
                          username=node['username'], pkey=key, timeout=10)
        else:
            await msg.edit(embed=error_embed("Sync Failed", "```diff\n- No authentication method available.\n```"))
            return
        
        # Get list of containers
        stdin, stdout, stderr = client.exec_command("lxc list --format csv -c n")
        containers = stdout.read().decode().strip().splitlines()
        
        synced = 0
        for container in containers:
            if container:
                # Check if container exists locally
                out, _, _ = await run_lxc(f"lxc list --format csv -c n | grep {container}")
                if not out:
                    # Copy container
                    await run_lxc(f"lxc copy {node['name']}:{container} {container}")
                    synced += 1
        
        client.close()
        
        embed = success_embed("Node Sync Complete", f"```fix\nSynced {synced} containers from node '{name}'.\n```")
        await msg.edit(embed=embed)
        
    except Exception as e:
        await msg.edit(embed=error_embed("Sync Failed", f"```diff\n- {str(e)}\n```"))

# ==================================================================================================
#  🖥️  VPS MANAGEMENT COMMANDS
# ==================================================================================================

@bot.command(name="myvps")
@commands.cooldown(1, 3, commands.BucketType.user)
async def my_vps(ctx):
    """List your VPS with detailed info"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not vps_list:
        await ctx.send(embed=no_vps_embed())
        return
    
    embed = info_embed(f"Your VPS ({len(vps_list)})")
    
    for i, vps in enumerate(vps_list, 1):
        status_emoji = "🟢" if vps['status'] == 'running' and not vps['suspended'] else "⛔" if vps['suspended'] else "🔴"
        status_text = vps['status'].upper()
        if vps['suspended']:
            status_text = "SUSPENDED"
        
        # Get live stats if running
        stats = {}
        if vps['status'] == 'running' and not vps['suspended']:
            stats = await get_container_stats(vps['container_name'])
        
        value = f"{status_emoji} **`{vps['container_name']}`**\n"
        value += f"Status: `{status_text}`\n"
        value += f"Plan: {vps['plan_name']}\n"
        value += f"Resources: {vps['ram']}GB RAM / {vps['cpu']} CPU / {vps['disk']}GB Disk\n"
        value += f"IP: `{vps.get('ip_address', 'N/A')}`\n"
        value += f"MAC: `{vps.get('mac_address', 'N/A')}`\n"
        
        if stats:
            value += f"CPU: {stats.get('cpu', 'N/A')} | RAM: {stats.get('memory', 'N/A')}\n"
        
        embed.add_field(name=f"VPS #{i}", value=value, inline=False)
    
    embed.add_field(name="🖥️ Management", value=f"Use `{BOT_PREFIX}manage` for detailed control", inline=False)
    await ctx.send(embed=embed)

@bot.command(name="list")
@commands.cooldown(1, 3, commands.BucketType.user)
async def list_command(ctx):
    """Detailed VPS list"""
    await my_vps(ctx)

class VPSManageView(View):
    """Interactive VPS management view with all controls"""
    def __init__(self, ctx, user_id, vps_list, is_admin_view=False, target_user=None):
        super().__init__(timeout=300)
        self.ctx = ctx
        self.user_id = user_id
        self.vps_list = vps_list
        self.current_index = 0
        self.is_admin_view = is_admin_view
        self.target_user = target_user
        self.message = None
        self.console_mode = False
        self.current_container = None
        self.live_updates = False
        
        self.update_buttons()
    
    def update_buttons(self):
        """Update view with current VPS"""
        self.clear_items()
        
        if len(self.vps_list) > 1:
            # Add navigation
            prev_btn = Button(label="◀️", style=discord.ButtonStyle.secondary)
            prev_btn.callback = self.prev_callback
            self.add_item(prev_btn)
            
            counter_btn = Button(label=f"{self.current_index + 1}/{len(self.vps_list)}", style=discord.ButtonStyle.secondary, disabled=True)
            self.add_item(counter_btn)
            
            next_btn = Button(label="▶️", style=discord.ButtonStyle.secondary)
            next_btn.callback = self.next_callback
            self.add_item(next_btn)
        
        # Action buttons - Row 1
        start_btn = Button(label="▶️ Start", style=discord.ButtonStyle.success)
        start_btn.callback = self.start_callback
        self.add_item(start_btn)
        
        stop_btn = Button(label="⏹️ Stop", style=discord.ButtonStyle.danger)
        stop_btn.callback = self.stop_callback
        self.add_item(stop_btn)
        
        restart_btn = Button(label="🔄 Restart", style=discord.ButtonStyle.primary)
        restart_btn.callback = self.restart_callback
        self.add_item(restart_btn)
        
        # Row 2
        stats_btn = Button(label="📊 Stats", style=discord.ButtonStyle.secondary)
        stats_btn.callback = self.stats_callback
        self.add_item(stats_btn)
        
        console_btn = Button(label="📟 Console", style=discord.ButtonStyle.secondary)
        console_btn.callback = self.console_callback
        self.add_item(console_btn)
        
        ssh_btn = Button(label="🔑 SSH", style=discord.ButtonStyle.secondary)
        ssh_btn.callback = self.ssh_callback
        self.add_item(ssh_btn)
        
        # Row 3
        cmd_btn = Button(label="⚡ Run Command", style=discord.ButtonStyle.secondary)
        cmd_btn.callback = self.cmd_callback
        self.add_item(cmd_btn)
        
        refresh_btn = Button(label="🔄 Refresh", style=discord.ButtonStyle.secondary)
        refresh_btn.callback = self.refresh_callback
        self.add_item(refresh_btn)
        
        if self.live_updates:
            live_btn = Button(label="⏹️ Stop Live", style=discord.ButtonStyle.danger)
        else:
            live_btn = Button(label="🔴 Live", style=discord.ButtonStyle.danger)
        live_btn.callback = self.live_callback
        self.add_item(live_btn)
    
    async def get_current_embed(self) -> discord.Embed:
        """Get embed for current VPS with full stats"""
        vps = self.vps_list[self.current_index]
        container = vps['container_name']
        self.current_container = container
        
        # Get live stats
        stats = await get_container_real_time_stats(container)
        
        status_emoji = "🟢" if stats['status'] == 'running' and not vps['suspended'] else "⛔" if vps['suspended'] else "🔴"
        status_text = stats['status'].upper()
        if vps['suspended']:
            status_text = "SUSPENDED"
        
        title = f"VPS Management: {container}"
        if self.is_admin_view and self.target_user:
            title = f"Admin: {self.target_user.display_name}'s VPS - {container}"
        
        embed = create_embed(title)
        
        # Basic Info
        basic = f"```fix\n"
        basic += f"Status : {status_text}\n"
        basic += f"Plan   : {vps['plan_name']}\n"
        basic += f"OS     : {vps['os_version']}\n"
        basic += f"RAM    : {vps['ram']}GB\n"
        basic += f"CPU    : {vps['cpu']} Core(s)\n"
        basic += f"Disk   : {vps['disk']}GB\n"
        basic += f"IP     : {stats['ipv4'][0] if stats['ipv4'] else vps.get('ip_address', 'N/A')}\n"
        basic += f"MAC    : {stats['mac'] if stats['mac'] != 'N/A' else vps.get('mac_address', 'N/A')}\n"
        basic += f"```"
        embed.add_field(name="📋 Basic Info", value=basic, inline=False)
        
        if stats['status'] == 'running' and not vps['suspended']:
            # CPU Graph
            cpu_bar = "█" * int(stats['cpu_usage'] / 10) + "░" * (10 - int(stats['cpu_usage'] / 10))
            cpu_display = f"`[{cpu_bar}] {stats['cpu_usage']:.1f}%`"
            
            # Memory Graph
            mem_bar = "█" * int(stats['memory_percent'] / 10) + "░" * (10 - int(stats['memory_percent'] / 10))
            mem_display = f"`[{mem_bar}] {stats['memory_percent']:.1f}%`"
            
            # Disk Graph
            disk_bar = "█" * int(stats['disk_percent'] / 10) + "░" * (10 - int(stats['disk_percent'] / 10))
            disk_display = f"`[{disk_bar}] {stats['disk_percent']:.1f}%`"
            
            live = f"**CPU Usage:** {cpu_display}\n"
            live += f"**Memory:** {mem_display}\n"
            live += f"**Disk:** {disk_display}\n"
            live += f"**Uptime:** `{stats['uptime']}`\n"
            live += f"**Processes:** `{stats['processes']}`\n"
            live += f"**Load:** `{stats['load']}`\n"
            embed.add_field(name="📊 Live Stats", value=live, inline=True)
            
            # Network Stats
            network = f"**IPv4:** `{', '.join(stats['ipv4'][:2]) if stats['ipv4'] else 'N/A'}`\n"
            network += f"**RX:** `{stats['network_rx']}`\n"
            network += f"**TX:** `{stats['network_tx']}`\n"
            network += f"**Users:** `{stats['users']}`\n"
            embed.add_field(name="🌐 Network", value=network, inline=True)
            
            # System Info
            sysinfo = f"**Hostname:** `{stats['hostname']}`\n"
            sysinfo += f"**Kernel:** `{stats['kernel']}`\n"
            sysinfo += f"**OS:** `{stats['os']}`\n"
            sysinfo += f"**Temp:** `{stats['temperature']}`\n"
            embed.add_field(name="⚙️ System", value=sysinfo, inline=True)
            
            # Top Processes
            if stats['process_list']:
                procs = "\n".join(stats['process_list'][:5])
                embed.add_field(name="🔝 Top Processes", value=f"```fix\n{procs}\n```", inline=False)
        
        return embed
    
    async def prev_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        self.current_index = (self.current_index - 1) % len(self.vps_list)
        self.update_buttons()
        await interaction.response.edit_message(embed=await self.get_current_embed(), view=self)
    
    async def next_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        self.current_index = (self.current_index + 1) % len(self.vps_list)
        self.update_buttons()
        await interaction.response.edit_message(embed=await self.get_current_embed(), view=self)
    
    async def start_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        vps = self.vps_list[self.current_index]
        container = vps['container_name']
        
        if vps['suspended'] and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message(embed=error_embed("Cannot Start", "```diff\n- This VPS is suspended.\n```"), ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            await run_lxc(f"lxc start {container}")
            update_vps_status(container, 'running')
            await interaction.followup.send(embed=success_embed("Started", f"```fix\nVPS {container} started.\n```"), ephemeral=True)
        except Exception as e:
            await interaction.followup.send(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"), ephemeral=True)
        
        await self.refresh_callback(interaction)
    
    async def stop_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        vps = self.vps_list[self.current_index]
        container = vps['container_name']
        
        if vps['suspended'] and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message(embed=error_embed("Cannot Stop", "```diff\n- This VPS is suspended.\n```"), ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            await run_lxc(f"lxc stop {container} --force")
            update_vps_status(container, 'stopped')
            await interaction.followup.send(embed=success_embed("Stopped", f"```fix\nVPS {container} stopped.\n```"), ephemeral=True)
        except Exception as e:
            await interaction.followup.send(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"), ephemeral=True)
        
        await self.refresh_callback(interaction)
    
    async def restart_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        vps = self.vps_list[self.current_index]
        container = vps['container_name']
        
        if vps['suspended'] and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message(embed=error_embed("Cannot Restart", "```diff\n- This VPS is suspended.\n```"), ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        try:
            await run_lxc(f"lxc restart {container}")
            update_vps_status(container, 'running')
            await interaction.followup.send(embed=success_embed("Restarted", f"```fix\nVPS {container} restarted.\n```"), ephemeral=True)
        except Exception as e:
            await interaction.followup.send(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"), ephemeral=True)
        
        await self.refresh_callback(interaction)
    
    async def stats_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        vps = self.vps_list[self.current_index]
        container = vps['container_name']
        stats = await get_container_real_time_stats(container)
        
        embed = info_embed(f"Live Stats: {container}")
        
        stats_text = f"```fix\n"
        stats_text += f"Status : {stats['status'].upper()}\n"
        stats_text += f"CPU    : {stats['cpu']} ({stats['cpu_usage']:.1f}%)\n"
        stats_text += f"Memory : {stats['memory']}\n"
        stats_text += f"Disk   : {stats['disk']}\n"
        stats_text += f"Uptime : {stats['uptime']}\n"
        stats_text += f"Process: {stats['processes']}\n"
        stats_text += f"Load   : {stats['load']}\n"
        stats_text += f"Network: RX {stats['network_rx']} / TX {stats['network_tx']}\n"
        stats_text += f"```"
        
        embed.add_field(name="📊 Statistics", value=stats_text, inline=False)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    async def console_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        vps = self.vps_list[self.current_index]
        container = vps['container_name']
        
        # Show console output
        console = await get_container_console(container, 30)
        
        embed = terminal_embed(f"Console: {container}", console)
        embed.add_field(name="📟 Commands", value=f"`{BOT_PREFIX}execute {container} <cmd>` to run commands", inline=False)
        
        # Add command input button
        view = View(timeout=60)
        cmd_btn = Button(label="⚡ Run Command", style=discord.ButtonStyle.primary)
        
        async def cmd_callback(cmd_interaction):
            await self.cmd_callback(cmd_interaction)
        
        cmd_btn.callback = cmd_callback
        view.add_item(cmd_btn)
        
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    async def cmd_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        vps = self.vps_list[self.current_index]
        container = vps['container_name']
        
        # Create modal for command input
        modal = CommandModal(container, self)
        await interaction.response.send_modal(modal)
    
    async def ssh_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        vps = self.vps_list[self.current_index]
        container = vps['container_name']
        
        await interaction.response.defer(ephemeral=True)
        
        # Call ssh-gen command
        await ssh_gen_command(interaction, container)
    
    async def live_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        self.live_updates = not self.live_updates
        self.update_buttons()
        
        if self.live_updates:
            await interaction.response.edit_message(embed=await self.get_current_embed(), view=self)
            # Start live updates
            self.bot.loop.create_task(self.live_update_task(interaction))
        else:
            await interaction.response.edit_message(embed=await self.get_current_embed(), view=self)
    
    async def live_update_task(self, interaction):
        """Task for live updates"""
        while self.live_updates:
            await asyncio.sleep(5)
            try:
                await interaction.edit_original_response(embed=await self.get_current_embed(), view=self)
            except:
                self.live_updates = False
                break
    
    async def refresh_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and not is_admin(str(interaction.user.id)):
            await interaction.response.send_message("```diff\n- This menu is not for you!\n```", ephemeral=True)
            return
        
        # Refresh VPS list from database
        if self.is_admin_view and self.target_user:
            self.vps_list = get_user_vps(str(self.target_user.id))
        else:
            self.vps_list = get_user_vps(self.user_id)
        
        if not self.vps_list:
            await interaction.response.edit_message(embed=no_vps_embed(), view=None)
            return
        
        if self.current_index >= len(self.vps_list):
            self.current_index = 0
        
        await interaction.response.edit_message(embed=await self.get_current_embed(), view=self)

class CommandModal(Modal):
    """Modal for entering commands"""
    def __init__(self, container_name, parent_view):
        super().__init__(title=f"Run Command in {container_name}")
        self.container_name = container_name
        self.parent_view = parent_view
        
        self.add_item(InputText(
            label="Command",
            placeholder="e.g., apt update, ps aux, etc.",
            style=discord.InputTextStyle.paragraph,
            required=True
        ))
        
        self.add_item(InputText(
            label="Timeout (seconds)",
            placeholder="30",
            required=False,
            value="30"
        ))
    
    async def callback(self, interaction: discord.Interaction):
        command = self.children[0].value
        timeout_str = self.children[1].value or "30"
        
        try:
            timeout = int(timeout_str)
        except:
            timeout = 30
        
        await interaction.response.defer(ephemeral=True)
        
        # Execute command
        out, err, code = await exec_in_container(self.container_name, command, timeout)
        
        output = out if out else err
        
        embed = terminal_embed(f"Command Output: {self.container_name}", f"$ {command}\n\n{output}")
        embed.add_field(name="Exit Code", value=f"```fix\n{code}\n```", inline=True)
        
        await interaction.followup.send(embed=embed, ephemeral=True)

@bot.command(name="manage")
@commands.cooldown(1, 5, commands.BucketType.user)
async def manage_vps(ctx, user: discord.Member = None):
    """Interactive VPS manager with buttons"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    if user and user.id != ctx.author.id:
        if not is_admin(str(ctx.author.id)):
            await ctx.send(embed=error_embed("Access Denied", "```diff\n- Only admins can manage other users' VPS.\n```"))
            return
        target_id = str(user.id)
        target_name = user.display_name
        is_admin_view = True
    else:
        target_id = str(ctx.author.id)
        target_name = ctx.author.display_name
        user = ctx.author
        is_admin_view = False
    
    vps_list = get_user_vps(target_id)
    
    if not vps_list:
        if user != ctx.author:
            await ctx.send(embed=info_embed(f"No VPS", f"{user.mention} has no VPS."))
        else:
            await ctx.send(embed=no_vps_embed())
        return
    
    view = VPSManageView(ctx, target_id, vps_list, is_admin_view, user if is_admin_view else None)
    embed = await view.get_current_embed()
    msg = await ctx.send(embed=embed, view=view)
    view.message = msg

@bot.command(name="rename")
@commands.cooldown(1, 10, commands.BucketType.user)
async def rename_vps(ctx, old_name: str, new_name: str):
    """Rename a VPS container"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    # Verify ownership
    vps_list = get_user_vps(user_id)
    vps = next((v for v in vps_list if v['container_name'] == old_name), None)
    
    if not vps and not is_admin(user_id):
        await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
        return
    
    await ctx.send(embed=info_embed("Renaming", f"```fix\nRenaming {old_name} to {new_name}...\n```"))
    
    try:
        # Stop container if running
        status = await get_container_status(old_name)
        was_running = status == 'running'
        
        if was_running:
            await run_lxc(f"lxc stop {old_name} --force")
        
        # Rename
        await run_lxc(f"lxc move {old_name} {new_name}")
        
        # Update database
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET container_name = ? WHERE container_name = ?', (new_name, old_name))
        cur.execute('UPDATE ipv4 SET container_name = ? WHERE container_name = ?', (new_name, old_name))
        cur.execute('UPDATE port_forwards SET container_name = ? WHERE container_name = ?', (new_name, old_name))
        cur.execute('UPDATE snapshots SET container_name = ? WHERE container_name = ?', (new_name, old_name))
        conn.commit()
        conn.close()
        
        # Start if it was running
        if was_running:
            await run_lxc(f"lxc start {new_name}")
        
        await ctx.send(embed=success_embed("Renamed", f"```fix\nContainer renamed from {old_name} to {new_name}\n```"))
        
    except Exception as e:
        await ctx.send(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"))

# ==================================================================================================
#  📟  CONSOLE & SSH COMMANDS - FIXED SSH ISSUE
# ==================================================================================================

@bot.command(name="ss")
@commands.cooldown(1, 5, commands.BucketType.user)
async def ss_command(ctx, container_name: str = None):
    """Show real-time VPS console"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    # Find the container
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            await ctx.send(embed=no_vps_embed())
            return
        container_name = vps_list[0]['container_name']
    else:
        vps_list = get_user_vps(user_id)
        if not any(v['container_name'] == container_name for v in vps_list) and not is_admin(user_id):
            await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
            return
    
    msg = await ctx.send(embed=info_embed("📸 Taking VPS Snapshot", f"```fix\nGetting console output from {container_name}...\n```"))
    
    # Get console output
    console = await get_container_console(container_name, 40)
    
    # Get stats
    stats = await get_container_real_time_stats(container_name)
    
    # Create terminal-style embed
    terminal_output = f"=== {container_name} Console Output ===\n"
    terminal_output += f"Status: {stats['status'].upper()} | Uptime: {stats['uptime']}\n"
    terminal_output += f"CPU: {stats['cpu']} | Memory: {stats['memory']} | Disk: {stats['disk']}\n"
    terminal_output += f"IP: {', '.join(stats['ipv4']) if stats['ipv4'] else 'N/A'}\n"
    terminal_output += "="*50 + "\n\n"
    terminal_output += console
    
    embed = terminal_embed(f"VPS Console: {container_name}", terminal_output)
    
    # Add command button
    view = View(timeout=60)
    cmd_btn = Button(label="⚡ Run Command", style=discord.ButtonStyle.primary)
    
    async def cmd_callback(interaction):
        modal = CommandModal(container_name, None)
        await interaction.response.send_modal(modal)
    
    cmd_btn.callback = cmd_callback
    view.add_item(cmd_btn)
    
    await msg.edit(embed=embed, view=view)

@bot.command(name="console")
@commands.cooldown(1, 5, commands.BucketType.user)
async def console_command(ctx, container_name: str, *, command: str = None):
    """Interactive console with command input"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    # Verify ownership
    vps_list = get_user_vps(user_id)
    if not any(v['container_name'] == container_name for v in vps_list) and not is_admin(user_id):
        await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
        return
    
    if not command:
        # Show console with command input
        console = await get_container_console(container_name, 30)
        
        embed = terminal_embed(f"Console: {container_name}", console)
        
        view = View(timeout=60)
        cmd_btn = Button(label="⚡ Run Command", style=discord.ButtonStyle.primary)
        
        async def cmd_callback(interaction):
            modal = CommandModal(container_name, None)
            await interaction.response.send_modal(modal)
        
        cmd_btn.callback = cmd_callback
        view.add_item(cmd_btn)
        
        await ctx.send(embed=embed, view=view)
        return
    
    # Execute command
    msg = await ctx.send(embed=info_embed("⚡ Executing Command", f"```fix\nRunning: {command}\n```"))
    
    out, err, code = await exec_in_container(container_name, command, timeout=60)
    
    output = out if out else err
    
    terminal_output = f"$ {command}\n\n"
    terminal_output += output
    
    embed = terminal_embed(f"Command Output: {container_name}", terminal_output)
    embed.add_field(name="Exit Code", value=f"```fix\n{code}\n```", inline=True)
    
    await msg.edit(embed=embed)

@bot.command(name="execute")
@commands.cooldown(1, 5, commands.BucketType.user)
async def execute_command(ctx, container_name: str, *, command: str):
    """Execute a command in VPS"""
    await console_command(ctx, container_name, command=command)

@bot.command(name="top")
@commands.cooldown(1, 5, commands.BucketType.user)
async def top_command(ctx, container_name: str = None):
    """Show live process monitor"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    # Find the container
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            await ctx.send(embed=no_vps_embed())
            return
        container_name = vps_list[0]['container_name']
    else:
        vps_list = get_user_vps(user_id)
        if not any(v['container_name'] == container_name for v in vps_list) and not is_admin(user_id):
            await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
            return
    
    msg = await ctx.send(embed=info_embed("📊 Getting process list...", f"```fix\nFetching top output from {container_name}\n```"))
    
    out, _, _ = await exec_in_container(container_name, "ps aux --sort=-%cpu | head -20")
    
    terminal_output = f"=== Process List: {container_name} ===\n\n"
    terminal_output += out
    
    embed = terminal_embed(f"Process Monitor: {container_name}", terminal_output)
    
    await msg.edit(embed=embed)

@bot.command(name="ps")
@commands.cooldown(1, 3, commands.BucketType.user)
async def ps_command(ctx, container_name: str = None):
    """Show process list"""
    await top_command(ctx, container_name)

@bot.command(name="df")
@commands.cooldown(1, 3, commands.BucketType.user)
async def df_command(ctx, container_name: str = None):
    """Show disk usage with graph"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            await ctx.send(embed=no_vps_embed())
            return
        container_name = vps_list[0]['container_name']
    else:
        vps_list = get_user_vps(user_id)
        if not any(v['container_name'] == container_name for v in vps_list) and not is_admin(user_id):
            await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
            return
    
    out, _, _ = await exec_in_container(container_name, "df -h")
    
    # Parse and add graph
    lines = out.splitlines()
    if len(lines) > 1:
        parts = lines[1].split()
        if len(parts) >= 5:
            used_pct = int(parts[4].replace('%', ''))
            bar = "█" * int(used_pct / 10) + "░" * (10 - int(used_pct / 10))
            out += f"\nDisk Usage: [{bar}] {used_pct}%"
    
    embed = terminal_embed(f"Disk Usage: {container_name}", out)
    await ctx.send(embed=embed)

@bot.command(name="free")
@commands.cooldown(1, 3, commands.BucketType.user)
async def free_command(ctx, container_name: str = None):
    """Show memory usage with graph"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            await ctx.send(embed=no_vps_embed())
            return
        container_name = vps_list[0]['container_name']
    else:
        vps_list = get_user_vps(user_id)
        if not any(v['container_name'] == container_name for v in vps_list) and not is_admin(user_id):
            await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
            return
    
    out, _, _ = await exec_in_container(container_name, "free -h")
    
    # Parse and add graph
    lines = out.splitlines()
    if len(lines) > 1:
        parts = lines[1].split()
        if len(parts) >= 3:
            used = parts[2].replace('Gi', '').replace('Mi', '')
            total = parts[1].replace('Gi', '').replace('Mi', '')
            if 'Mi' in parts[2]:
                used_pct = (float(used) / float(total)) * 100
            else:
                used_pct = (float(used) / float(total)) * 100
            bar = "█" * int(used_pct / 10) + "░" * (10 - int(used_pct / 10))
            out += f"\nMemory Usage: [{bar}] {used_pct:.1f}%"
    
    embed = terminal_embed(f"Memory Usage: {container_name}", out)
    await ctx.send(embed=embed)

@bot.command(name="netstat")
@commands.cooldown(1, 5, commands.BucketType.user)
async def netstat_command(ctx, container_name: str = None):
    """Show network connections"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            await ctx.send(embed=no_vps_embed())
            return
        container_name = vps_list[0]['container_name']
    else:
        vps_list = get_user_vps(user_id)
        if not any(v['container_name'] == container_name for v in vps_list) and not is_admin(user_id):
            await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
            return
    
    out, _, _ = await exec_in_container(container_name, "netstat -tuln | head -20")
    
    embed = terminal_embed(f"Network Connections: {container_name}", out)
    await ctx.send(embed=embed)

@bot.command(name="who")
@commands.cooldown(1, 3, commands.BucketType.user)
async def who_command(ctx, container_name: str = None):
    """Show logged-in users"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            await ctx.send(embed=no_vps_embed())
            return
        container_name = vps_list[0]['container_name']
    else:
        vps_list = get_user_vps(user_id)
        if not any(v['container_name'] == container_name for v in vps_list) and not is_admin(user_id):
            await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
            return
    
    out, _, _ = await exec_in_container(container_name, "who")
    
    if not out:
        out = "No users logged in"
    
    embed = terminal_embed(f"Logged-in Users: {container_name}", out)
    await ctx.send(embed=embed)

@bot.command(name="uptime")
@commands.cooldown(1, 3, commands.BucketType.user)
async def uptime_container_command(ctx, container_name: str = None):
    """Show container uptime"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    if not container_name:
        vps_list = get_user_vps(user_id)
        if not vps_list:
            await ctx.send(embed=no_vps_embed())
            return
        container_name = vps_list[0]['container_name']
    else:
        vps_list = get_user_vps(user_id)
        if not any(v['container_name'] == container_name for v in vps_list) and not is_admin(user_id):
            await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
            return
    
    out, _, _ = await exec_in_container(container_name, "uptime -p")
    
    embed = info_embed(f"Uptime: {container_name}", f"```fix\n{out}\n```")
    await ctx.send(embed=embed)

@bot.command(name="reboot")
@commands.cooldown(1, 10, commands.BucketType.user)
async def reboot_vps(ctx, container_name: str):
    """Reboot VPS"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    # Verify ownership
    vps_list = get_user_vps(user_id)
    if not any(v['container_name'] == container_name for v in vps_list) and not is_admin(user_id):
        await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
        return
    
    await ctx.send(embed=info_embed("🔄 Rebooting", f"```fix\nRebooting VPS {container_name}...\n```"))
    
    try:
        await run_lxc(f"lxc restart {container_name}")
        update_vps_status(container_name, 'running')
        await ctx.send(embed=success_embed("Rebooted", f"```fix\nVPS {container_name} has been rebooted.\n```"))
    except Exception as e:
        await ctx.send(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"))

@bot.command(name="shutdown")
@commands.cooldown(1, 10, commands.BucketType.user)
async def shutdown_vps(ctx, container_name: str):
    """Shutdown VPS"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    # Verify ownership
    vps_list = get_user_vps(user_id)
    if not any(v['container_name'] == container_name for v in vps_list) and not is_admin(user_id):
        await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
        return
    
    await ctx.send(embed=info_embed("⏹️ Shutting Down", f"```fix\nShutting down VPS {container_name}...\n```"))
    
    try:
        await run_lxc(f"lxc stop {container_name}")
        update_vps_status(container_name, 'stopped')
        await ctx.send(embed=success_embed("Shutdown", f"```fix\nVPS {container_name} has been shut down.\n```"))
    except Exception as e:
        await ctx.send(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"))

# ==================================================================================================
#  🔑  SSH-GEN COMMAND - COMPLETELY FIXED
# ==================================================================================================

async def ssh_gen_command(interaction_or_ctx, container_name: str):
    """Generate SSH access for a container - FIXED"""
    
    # Handle both interaction and context
    if isinstance(interaction_or_ctx, discord.Interaction):
        ctx = await bot.get_context(interaction_or_ctx.message)
        user = interaction_or_ctx.user
        send_msg = interaction_or_ctx.followup.send
        is_interaction = True
    else:
        ctx = interaction_or_ctx
        user = ctx.author
        send_msg = ctx.send
        is_interaction = False
    
    user_id = str(user.id)
    
    # Verify ownership
    vps_list = get_user_vps(user_id)
    if not any(v['container_name'] == container_name for v in vps_list) and not is_admin(user_id):
        await send_msg(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
        return
    
    msg = await send_msg(embed=info_embed("🔑 Generating SSH Access", f"```fix\nSetting up SSH for {container_name}...\n```"))
    
    try:
        # Check if container is running
        status = await get_container_status(container_name)
        if status != 'running':
            await msg.edit(embed=error_embed("Container Not Running", f"```diff\n- {container_name} is not running. Start it first with .manage\n```"))
            return
        
        # Install tmate if not present
        out, _, _ = await exec_in_container(container_name, "which tmate")
        if not out:
            await msg.edit(embed=info_embed("Installing SSH Service", "```fix\nInstalling tmate (this may take a moment)...\n```"))
            await exec_in_container(container_name, "apt-get update -qq")
            await exec_in_container(container_name, "apt-get install -y -qq tmate")
        
        # Generate unique session
        session_id = f"svm5-{random.randint(1000, 9999)}-{int(time.time())}"
        
        # Start tmate session with proper error handling
        await exec_in_container(container_name, f"tmate -S /tmp/{session_id}.sock new-session -d")
        await asyncio.sleep(5)
        
        # Get SSH connection string
        out, err, code = await exec_in_container(container_name, f"tmate -S /tmp/{session_id}.sock display -p '#{{tmate_ssh}}'")
        ssh_url = out.strip()
        
        if ssh_url and ssh_url.startswith('ssh'):
            # Try to DM the user
            try:
                dm_embed = success_embed("🔑 SSH Access Generated")
                dm_embed.add_field(name="📦 Container", value=f"```fix\n{container_name}\n```", inline=True)
                dm_embed.add_field(name="🔐 SSH Command", value=f"```bash\n{ssh_url}\n```", inline=False)
                dm_embed.add_field(name="📋 Instructions", 
                                  value="```fix\n1. Copy the command above\n2. Paste in your terminal\n3. You'll have full shell access\n\n⚠️ This link expires in 15 minutes\n```", 
                                  inline=False)
                await user.send(embed=dm_embed)
                
                await msg.edit(embed=success_embed(
                    "SSH Access Generated",
                    f"```fix\n✅ SSH connection details sent to your DMs!\nContainer: {container_name}\n```"
                ))
            except discord.Forbidden:
                # If DM fails, send in channel but ephemeral
                await msg.edit(embed=error_embed(
                    "DM Failed",
                    f"```fix\n❌ Could not send DM. Please enable DMs.\n\nSSH Command:\n{ssh_url}\n```"
                ))
        else:
            # Try alternative method - web URL
            out, _, _ = await exec_in_container(container_name, f"tmate -S /tmp/{session_id}.sock display -p '#{{tmate_web}}'")
            web_url = out.strip()
            
            if web_url:
                await msg.edit(embed=success_embed(
                    "Web Terminal Generated",
                    f"```fix\nWeb URL: {web_url}\n```\n"
                    f"Open this URL in your browser for terminal access."
                ))
            else:
                await msg.edit(embed=error_embed("Failed", "```diff\n- Could not generate SSH access. Try again later.\n```"))
    
    except Exception as e:
        logger.error(f"SSH generation error: {e}")
        await msg.edit(embed=error_embed("SSH Generation Failed", f"```diff\n- {str(e)[:100]}\n```"))

@bot.command(name="ssh-gen")
@commands.cooldown(1, 30, commands.BucketType.user)
async def ssh_gen(ctx, container_name: str):
    """Generate SSH access for your container via tmate - FIXED"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    await ssh_gen_command(ctx, container_name)

# ==================================================================================================
#  🔌  PORT FORWARDING COMMANDS
# ==================================================================================================

@bot.group(name="ports", invoke_without_command=True)
@commands.cooldown(1, 2, commands.BucketType.user)
async def ports_group(ctx):
    """Port forwarding commands"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    allocated = get_port_allocation(user_id)
    forwards = get_user_port_forwards(user_id)
    
    embed = info_embed("Port Forwarding Help")
    embed.add_field(name="📊 Your Quota", value=f"```fix\nAllocated: {allocated}\nUsed: {len(forwards)}\nAvailable: {allocated - len(forwards)}\n```", inline=False)
    embed.add_field(
        name="📋 Commands",
        value=f"`{BOT_PREFIX}ports add <vps_num> <port> [tcp/udp]` - Add forward\n"
              f"`{BOT_PREFIX}ports list` - List your forwards\n"
              f"`{BOT_PREFIX}ports remove <id>` - Remove forward\n"
              f"`{BOT_PREFIX}ports quota` - Check your quota\n"
              f"`{BOT_PREFIX}ports check <port>` - Check if port is available",
        inline=False
    )
    await ctx.send(embed=embed)

@ports_group.command(name="add")
async def ports_add(ctx, vps_num: int, port: int, protocol: str = "tcp+udp"):
    """Add a port forward"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not vps_list:
        await ctx.send(embed=no_vps_embed())
        return
    
    if vps_num < 1 or vps_num > len(vps_list):
        await ctx.send(embed=error_embed("Invalid VPS", f"```diff\n- VPS number must be between 1 and {len(vps_list)}.\n```"))
        return
    
    if port < 1 or port > 65535:
        await ctx.send(embed=error_embed("Invalid Port", "```diff\n- Port must be between 1 and 65535.\n```"))
        return
    
    if protocol not in ["tcp", "udp", "tcp+udp"]:
        await ctx.send(embed=error_embed("Invalid Protocol", "```diff\n- Protocol must be tcp, udp, or tcp+udp\n```"))
        return
    
    # Check quota
    allocated = get_port_allocation(user_id)
    forwards = get_user_port_forwards(user_id)
    if len(forwards) >= allocated and allocated > 0:
        await ctx.send(embed=error_embed("Quota Exceeded", f"```diff\n- You have used all {allocated} port slots.\n```"))
        return
    
    vps = vps_list[vps_num - 1]
    container = vps['container_name']
    
    if vps['suspended']:
        await ctx.send(embed=error_embed("Cannot Add", "```diff\n- VPS is suspended.\n```"))
        return
    
    if vps['status'] != 'running':
        await ctx.send(embed=error_embed("Cannot Add", "```diff\n- VPS must be running to add port forwards.\n```"))
        return
    
    msg = await ctx.send(embed=info_embed("Creating port forward...", f"```fix\nForwarding port {port} ({protocol}) from VPS #{vps_num}\n```"))
    
    host_port = await create_port_forward(user_id, container, port, protocol)
    
    if host_port:
        embed = success_embed("Port Forward Created")
        embed.add_field(name="📦 VPS", value=f"```fix\n#{vps_num} - {container}\n```", inline=True)
        embed.add_field(name="🔌 Container Port", value=f"```fix\n{port}\n```", inline=True)
        embed.add_field(name="🌐 Host Port", value=f"```fix\n{host_port}\n```", inline=True)
        embed.add_field(name="📡 Protocol", value=f"```fix\n{protocol}\n```", inline=True)
        embed.add_field(name="🔗 Access", value=f"Connect to `{SERVER_IP}:{host_port}`", inline=False)
        await msg.edit(embed=embed)
    else:
        await msg.edit(embed=error_embed("Failed", "```diff\n- Could not assign a host port. Try again later.\n```"))

@ports_group.command(name="list")
async def ports_list(ctx):
    """List your port forwards"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    forwards = get_user_port_forwards(user_id)
    allocated = get_port_allocation(user_id)
    
    if not forwards:
        embed = info_embed("Port Forwards", "```fix\nYou have no active port forwards.\n```")
        embed.add_field(name="📊 Quota", value=f"```fix\nAllocated: {allocated}\nUsed: 0\nAvailable: {allocated}\n```")
        await ctx.send(embed=embed)
        return
    
    embed = info_embed(f"Your Port Forwards ({len(forwards)}/{allocated})")
    
    for f in forwards:
        vps_num = next((i+1 for i, v in enumerate(get_user_vps(user_id)) if v['container_name'] == f['container_name']), '?')
        embed.add_field(
            name=f"ID: {f['id']}",
            value=f"```fix\nVPS #{vps_num}: {f['container_port']} → {SERVER_IP}:{f['host_port']} ({f['protocol']})\nCreated: {f['created_at'][:16]}\n```",
            inline=False
        )
    
    embed.add_field(name="❌ Remove", value=f"Use `{BOT_PREFIX}ports remove <id>` to remove a forward", inline=False)
    await ctx.send(embed=embed)

@ports_group.command(name="remove")
async def ports_remove(ctx, forward_id: int):
    """Remove a port forward"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    success, container, host_port = remove_port_forward(forward_id)
    
    if not success:
        await ctx.send(embed=error_embed("Not Found", f"```diff\n- Port forward with ID {forward_id} not found.\n```"))
        return
    
    # Verify ownership
    vps_list = get_user_vps(user_id)
    if not any(v['container_name'] == container for v in vps_list) and not is_admin(user_id):
        await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this port forward.\n```"))
        return
    
    # Remove devices
    await remove_port_forward_device(container, host_port)
    
    await ctx.send(embed=success_embed("Removed", f"```fix\nPort forward ID {forward_id} has been removed.\n```"))

@ports_group.command(name="quota")
async def ports_quota(ctx):
    """Check your port quota"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    allocated = get_port_allocation(user_id)
    used = len(get_user_port_forwards(user_id))
    
    embed = info_embed("Port Quota")
    embed.add_field(name="📊 Allocated", value=f"```fix\n{allocated}\n```", inline=True)
    embed.add_field(name="📊 Used", value=f"```fix\n{used}\n```", inline=True)
    embed.add_field(name="📊 Available", value=f"```fix\n{allocated - used}\n```", inline=True)
    
    await ctx.send(embed=embed)

@ports_group.command(name="check")
async def ports_check(ctx, port: int):
    """Check if a port is available"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    if port < 1 or port > 65535:
        await ctx.send(embed=error_embed("Invalid Port", "```diff\n- Port must be between 1 and 65535.\n```"))
        return
    
    # Check if port is in use
    try:
        result = subprocess.run(['ss', '-tuln'], capture_output=True, text=True)
        port_in_use = False
        for line in result.stdout.splitlines():
            if f":{port}" in line:
                port_in_use = True
                break
        
        if port_in_use:
            await ctx.send(embed=error_embed("Port Unavailable", f"```diff\n- Port {port} is already in use.\n```"))
        else:
            await ctx.send(embed=success_embed("Port Available", f"```fix\nPort {port} is available.\n```"))
    except:
        await ctx.send(embed=info_embed("Port Check", f"```fix\nCould not check port {port}. Assuming available.\n```"))

# ==================================================================================================
#  📦  PANEL INSTALLATION COMMANDS WITH CLOUDFLARED TUNNEL
# ==================================================================================================

class PanelSelectView(View):
    """Panel selection view"""
    def __init__(self, ctx):
        super().__init__(timeout=120)
        self.ctx = ctx
        
        ptero_btn = Button(label="🦅 Pterodactyl", style=discord.ButtonStyle.primary, emoji="🦅")
        ptero_btn.callback = self.ptero_callback
        
        puffer_btn = Button(label="🐡 Pufferpanel", style=discord.ButtonStyle.success, emoji="🐡")
        puffer_btn.callback = self.puffer_callback
        
        cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
        cancel_btn.callback = self.cancel_callback
        
        self.add_item(ptero_btn)
        self.add_item(puffer_btn)
        self.add_item(cancel_btn)
    
    async def ptero_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- Not for you!\n```", ephemeral=True)
            return
        await self.install_panel(interaction, "pterodactyl")
    
    async def puffer_callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("```diff\n- Not for you!\n```", ephemeral=True)
            return
        await self.install_panel(interaction, "pufferpanel")
    
    async def cancel_callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=info_embed("Cancelled", "```fix\nPanel installation cancelled.\n```"), view=None)
    
    async def install_panel(self, interaction: discord.Interaction, panel_type: str):
        await interaction.response.defer()
        
        user_id = str(self.ctx.author.id)
        
        # Check if user has VPS
        vps_list = get_user_vps(user_id)
        if not vps_list:
            await interaction.followup.send(embed=error_embed("No VPS", "```diff\n- You need a VPS to install a panel.\n```"), ephemeral=True)
            return
        
        container = vps_list[0]['container_name']
        
        progress = await interaction.followup.send(
            embed=info_embed(f"Installing {panel_type.title()}", "```fix\nStep 1/5: Preparing installation...\n```"),
            ephemeral=True
        )
        
        try:
            # Generate credentials
            admin_user = generate_username()
            admin_email = generate_email(admin_user)
            admin_pass = generate_password(16)
            
            if panel_type == "pterodactyl":
                # Install Pterodactyl
                await progress.edit(embed=info_embed("Installing Pterodactyl", "```fix\nStep 2/5: Installing dependencies...\n```"))
                
                commands = [
                    "apt-get update -qq",
                    "apt-get install -y -qq curl wget git unzip tar",
                    "apt-get install -y -qq nginx mariadb-server redis-server",
                    "apt-get install -y -qq php8.1 php8.1-{cli,gd,mysql,pdo,mbstring,tokenizer,bcmath,xml,fpm,curl,zip}",
                    "curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer",
                    "mkdir -p /var/www/pterodactyl",
                    "cd /var/www/pterodactyl && curl -Lo panel.tar.gz https://github.com/pterodactyl/panel/releases/latest/download/panel.tar.gz",
                    "cd /var/www/pterodactyl && tar -xzvf panel.tar.gz && chmod -R 755 storage/* bootstrap/cache/"
                ]
                
                for cmd in commands:
                    await exec_in_container(container, cmd)
                    await asyncio.sleep(1)
                
                await progress.edit(embed=info_embed("Installing Pterodactyl", "```fix\nStep 3/5: Configuring environment...\n```"))
                
                # Create .env and install
                env_cmds = [
                    "cd /var/www/pterodactyl && cp .env.example .env",
                    "cd /var/www/pterodactyl && composer install --no-dev --optimize-autoloader --no-interaction",
                    "cd /var/www/pterodactyl && php artisan key:generate --force",
                    "cd /var/www/pterodactyl && php artisan migrate --seed --force",
                    f"cd /var/www/pterodactyl && php artisan p:user:make --email='{admin_email}' --username='{admin_user}' --password='{admin_pass}' --name-first='Admin' --name-last='User' --admin=1 --no-interaction"
                ]
                
                for cmd in env_cmds:
                    await exec_in_container(container, cmd)
                    await asyncio.sleep(1)
                
                # Get IP
                out, _, _ = await exec_in_container(container, "ip -4 addr show eth0 | grep -oP '(?<=inet\\s)\\d+\\.\\d+\\.\\d+\\.\\d+' | head -1")
                ip = out.strip() or SERVER_IP
                panel_url = f"http://{ip}"
                
                # Create cloudflared tunnel
                await progress.edit(embed=info_embed("Installing Pterodactyl", "```fix\nStep 4/5: Creating tunnel...\n```"))
                tunnel_url = await create_cloudflared_tunnel(container, 80)
                if tunnel_url:
                    panel_url = tunnel_url
                
            else:  # pufferpanel
                await progress.edit(embed=info_embed("Installing Pufferpanel", "```fix\nStep 2/5: Installing...\n```"))
                
                commands = [
                    "apt-get update -qq",
                    "apt-get install -y -qq curl wget git",
                    "curl -s https://packagecloud.io/install/repositories/pufferpanel/pufferpanel/script.deb.sh | bash",
                    "apt-get install -y -qq pufferpanel",
                    "systemctl enable pufferpanel",
                    "systemctl start pufferpanel",
                    f"pufferpanel user add --name '{admin_user}' --email '{admin_email}' --password '{admin_pass}' --admin"
                ]
                
                for cmd in commands:
                    await exec_in_container(container, cmd)
                    await asyncio.sleep(1)
                
                out, _, _ = await exec_in_container(container, "ip -4 addr show eth0 | grep -oP '(?<=inet\\s)\\d+\\.\\d+\\.\\d+\\.\\d+' | head -1")
                ip = out.strip() or SERVER_IP
                panel_url = f"http://{ip}:8080"
                
                # Create cloudflared tunnel
                await progress.edit(embed=info_embed("Installing Pufferpanel", "```fix\nStep 4/5: Creating tunnel...\n```"))
                tunnel_url = await create_cloudflared_tunnel(container, 8080)
                if tunnel_url:
                    panel_url = tunnel_url
            
            # Save to database
            add_panel(user_id, panel_type, panel_url, admin_user, admin_pass, admin_email, container, tunnel_url)
            
            await progress.edit(embed=info_embed("Installing Panel", "```fix\nStep 5/5: Finalizing...\n```"))
            
            # Success message
            embed = success_embed(f"✅ {panel_type.title()} Installed Successfully!")
            embed.add_field(name="🌐 Panel URL", value=f"```fix\n{panel_url}\n```", inline=False)
            embed.add_field(name="👤 Username", value=f"||`{admin_user}`||", inline=True)
            embed.add_field(name="📧 Email", value=f"||`{admin_email}`||", inline=True)
            embed.add_field(name="🔑 Password", value=f"||`{admin_pass}`||", inline=False)
            embed.add_field(name="📦 Container", value=f"```fix\n{container}\n```", inline=True)
            
            await progress.edit(embed=embed)
            
            # DM user
            try:
                dm_embed = success_embed(f"🔐 Your {panel_type.title()} Credentials")
                dm_embed.add_field(name="🌐 Panel URL", value=panel_url, inline=False)
                dm_embed.add_field(name="👤 Username", value=admin_user, inline=True)
                dm_embed.add_field(name="📧 Email", value=admin_email, inline=True)
                dm_embed.add_field(name="🔑 Password", value=admin_pass, inline=False)
                await self.ctx.author.send(embed=dm_embed)
            except:
                pass
            
        except Exception as e:
            await progress.edit(embed=error_embed("Installation Failed", f"```diff\n- {str(e)}\n```"))

@bot.command(name="install-panel")
@commands.cooldown(1, 300, commands.BucketType.user)
async def install_panel(ctx):
    """Install Pterodactyl or Pufferpanel on your VPS"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    # Check if user has VPS
    user_id = str(ctx.author.id)
    vps_list = get_user_vps(user_id)
    
    if not vps_list:
        await ctx.send(embed=no_vps_embed())
        return
    
    embed = info_embed(
        "Panel Installation",
        f"```fix\nYour VPS: {vps_list[0]['container_name']}\n```\n\n"
        f"🦅 **Pterodactyl** - Popular game server panel\n"
        f"🐡 **Pufferpanel** - Lightweight alternative\n\n"
        f"Select a panel to install:"
    )
    
    view = PanelSelectView(ctx)
    await ctx.send(embed=embed, view=view)

@bot.command(name="panel-info")
@commands.cooldown(1, 3, commands.BucketType.user)
async def panel_info(ctx):
    """Show your installed panel info"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    panels = get_user_panels(user_id)
    
    if not panels:
        await ctx.send(embed=info_embed("No Panels", "```fix\nYou haven't installed any panels yet.\n```\nUse `.install-panel` to install one."))
        return
    
    embed = info_embed(f"Your Panels ({len(panels)})")
    
    for panel in panels:
        embed.add_field(
            name=f"{'🦅' if panel['panel_type'] == 'pterodactyl' else '🐡'} {panel['panel_type'].title()}",
            value=f"```fix\nURL: {panel['panel_url']}\nUsername: {panel['admin_user']}\nInstalled: {panel['installed_at'][:16]}\n```",
            inline=False
        )
    
    await ctx.send(embed=embed)

@bot.command(name="panel-tunnel")
@commands.cooldown(1, 30, commands.BucketType.user)
async def panel_tunnel(ctx, container_name: str, port: int = 80):
    """Create cloudflared tunnel for panel"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    # Verify ownership
    vps_list = get_user_vps(user_id)
    if not any(v['container_name'] == container_name for v in vps_list) and not is_admin(user_id):
        await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
        return
    
    msg = await ctx.send(embed=info_embed("Creating Tunnel", f"```fix\nCreating cloudflared tunnel for {container_name} on port {port}...\n```"))
    
    tunnel_url = await create_cloudflared_tunnel(container_name, port)
    
    if tunnel_url:
        embed = success_embed("Tunnel Created")
        embed.add_field(name="🌐 Tunnel URL", value=f"```fix\n{tunnel_url}\n```", inline=False)
        embed.add_field(name="📦 Container", value=f"```fix\n{container_name}\n```", inline=True)
        embed.add_field(name="🔌 Port", value=f"```fix\n{port}\n```", inline=True)
        await msg.edit(embed=embed)
    else:
        await msg.edit(embed=error_embed("Failed", "```diff\n- Could not create tunnel. Make sure cloudflared is installed.\n```"))

@bot.command(name="panel-reset")
@commands.cooldown(1, 30, commands.BucketType.user)
async def panel_reset(ctx, container_name: str):
    """Reset panel admin password"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    # Verify ownership
    vps_list = get_user_vps(user_id)
    vps = next((v for v in vps_list if v['container_name'] == container_name), None)
    
    if not vps and not is_admin(user_id):
        await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
        return
    
    # Get panel info
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM panels WHERE container_name = ? ORDER BY installed_at DESC LIMIT 1', (container_name,))
    panel = cur.fetchone()
    
    if not panel:
        await ctx.send(embed=error_embed("No Panel Found", f"```diff\n- No panel found in container {container_name}\n```"))
        conn.close()
        return
    
    new_pass = generate_password(12)
    
    if panel['panel_type'] == 'pterodactyl':
        cmd = f"cd /var/www/pterodactyl && php artisan p:user:password --email={panel['admin_email']} --password={new_pass}"
    else:
        cmd = f"pufferpanel user password --email {panel['admin_email']} --password {new_pass}"
    
    await ctx.send(embed=info_embed("Resetting Password", f"```fix\nResetting password for {panel['panel_type']}...\n```"))
    
    out, err, code = await exec_in_container(container_name, cmd)
    
    if code == 0:
        # Update database
        cur.execute('UPDATE panels SET admin_pass = ? WHERE id = ?', (new_pass, panel['id']))
        conn.commit()
        
        embed = success_embed("Password Reset")
        embed.add_field(name="🌐 Panel URL", value=f"```fix\n{panel['panel_url']}\n```", inline=False)
        embed.add_field(name="👤 Username", value=f"```fix\n{panel['admin_user']}\n```", inline=True)
        embed.add_field(name="📧 Email", value=f"```fix\n{panel['admin_email']}\n```", inline=True)
        embed.add_field(name="🔑 New Password", value=f"```fix\n{new_pass}\n```", inline=False)
        
        # DM user
        try:
            dm_embed = success_embed(f"🔐 Panel Password Reset")
            dm_embed.add_field(name="🌐 Panel URL", value=panel['panel_url'], inline=False)
            dm_embed.add_field(name="👤 Username", value=panel['admin_user'], inline=True)
            dm_embed.add_field(name="📧 Email", value=panel['admin_email'], inline=True)
            dm_embed.add_field(name="🔑 New Password", value=new_pass, inline=False)
            await ctx.author.send(embed=dm_embed)
        except:
            pass
        
        await ctx.send(embed=embed)
    else:
        await ctx.send(embed=error_embed("Failed", f"```diff\n- {err}\n```"))
    
    conn.close()

# ==================================================================================================
#  🌍  IPv4 MANAGEMENT (with UPI payment) - ENHANCED
# ==================================================================================================

@bot.command(name="buy-ipv4")
@commands.cooldown(1, 30, commands.BucketType.user)
async def buy_ipv4(ctx):
    """Buy an IPv4 address via UPI with QR code"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    txn_ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    upi_config = get_upi_config()
    
    embed = create_embed("Buy IPv4 Address")
    embed.add_field(name="💰 Price", value=f"```fix\n₹{IPV4_PRICE_INR}\n```", inline=True)
    embed.add_field(name="📱 UPI ID", value=f"```fix\n{upi_config['upi_id']}\n```", inline=True)
    embed.add_field(name="🔖 Reference", value=f"```fix\n{txn_ref}\n```", inline=True)
    embed.add_field(
        name="📋 Payment Instructions",
        value=f"```fix\n1. Pay ₹{IPV4_PRICE_INR} to {upi_config['upi_id']}\n2. Add reference {txn_ref} in notes\n3. Click ✅ after payment\n```",
        inline=False
    )
    
    # Generate QR code
    qr_bytes = generate_upi_qr(upi_config['upi_id'], IPV4_PRICE_INR, txn_ref)
    
    if qr_bytes:
        file = discord.File(qr_bytes, filename="qr.png")
        embed.set_image(url="attachment://qr.png")
    else:
        file = None
    
    # Create view with payment confirmation button
    view = View(timeout=300)
    
    async def payment_callback(interaction: discord.Interaction):
        if interaction.user.id != ctx.author.id:
            await interaction.response.send_message("```diff\n- Not your purchase!\n```", ephemeral=True)
            return
        
        # Open modal for transaction ID
        modal = TransactionModal(ctx, txn_ref)
        await interaction.response.send_modal(modal)
    
    payment_btn = Button(label="✅ I've Paid", style=discord.ButtonStyle.success)
    payment_btn.callback = payment_callback
    view.add_item(payment_btn)
    
    # Payment link button
    payment_link = f"https://paytm.com/upi/pay?pa={upi_config['upi_id']}&pn={upi_config.get('upi_name', '')}&am={IPV4_PRICE_INR}&tn={txn_ref}"
    link_btn = Button(label="💳 Payment Link", style=discord.ButtonStyle.link, url=payment_link)
    view.add_item(link_btn)
    
    cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    
    async def cancel_callback(interaction: discord.Interaction):
        await interaction.response.edit_message(embed=info_embed("Cancelled", "```fix\nPurchase cancelled.\n```"), view=None)
    
    cancel_btn.callback = cancel_callback
    view.add_item(cancel_btn)
    
    if file:
        await ctx.send(embed=embed, file=file, view=view)
    else:
        await ctx.send(embed=embed, view=view)

class TransactionModal(Modal):
    def __init__(self, ctx, txn_ref):
        super().__init__(title="Enter Transaction ID")
        self.ctx = ctx
        self.txn_ref = txn_ref
        
        self.add_item(InputText(
            label="UPI Transaction ID",
            placeholder="e.g., T25031234567890",
            min_length=8,
            max_length=50,
            required=True
        ))
    
    async def callback(self, interaction: discord.Interaction):
        txn_id = self.children[0].value
        
        # Save transaction
        txn_id_db = add_transaction(str(self.ctx.author.id), self.txn_ref, IPV4_PRICE_INR)
        
        # Notify admins
        embed = warning_embed("New IPv4 Purchase", 
            f"```fix\nUser: {self.ctx.author}\nRef: {self.txn_ref}\nTxn ID: {txn_id}\nAmount: ₹{IPV4_PRICE_INR}\n```")
        
        for admin_id in MAIN_ADMIN_IDS:
            try:
                admin = await bot.fetch_user(admin_id)
                await admin.send(embed=embed)
            except:
                pass
        
        await interaction.response.edit_message(
            embed=info_embed(
                "Payment Submitted",
                f"```fix\nReference: {self.txn_ref}\nTransaction ID: {txn_id}\n```\n\n"
                f"An admin will verify your payment and assign IPv4 shortly."
            ),
            view=None
        )

@bot.command(name="ipv4")
@commands.cooldown(1, 3, commands.BucketType.user)
async def list_ipv4(ctx, user: discord.Member = None):
    """List your IPv4 addresses with full details"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    if user and user.id != ctx.author.id:
        if not is_admin(str(ctx.author.id)):
            await ctx.send(embed=error_embed("Access Denied", "```diff\n- Only admins can view others' IPv4.\n```"))
            return
        target_id = str(user.id)
        target_name = user.display_name
    else:
        target_id = str(ctx.author.id)
        target_name = ctx.author.display_name
        user = ctx.author
    
    ipv4_list = get_user_ipv4(target_id)
    
    if not ipv4_list:
        await ctx.send(embed=info_embed("No IPv4", f"{user.mention} has no IPv4 addresses assigned."))
        return
    
    embed = info_embed(f"IPv4 Addresses - {target_name}", f"```fix\nTotal: {len(ipv4_list)}\n```")
    
    for i, ip in enumerate(ipv4_list, 1):
        value = f"```fix\n"
        value += f"Container: {ip['container_name']}\n"
        if ip['public_ip']:
            value += f"Public IP: {ip['public_ip']}\n"
        if ip['private_ip']:
            value += f"Private IP: {ip['private_ip']}\n"
        if ip['mac_address']:
            value += f"MAC Addr  : {ip['mac_address']}\n"
        if ip['gateway']:
            value += f"Gateway   : {ip['gateway']}\n"
        if ip['netmask']:
            value += f"Netmask   : {ip['netmask']}\n"
        if ip['interface']:
            value += f"Interface : {ip['interface']}\n"
        if ip['tunnel_url']:
            value += f"Tunnel    : {ip['tunnel_url']}\n"
        if ip['tunnel_id']:
            value += f"Tunnel ID : {ip['tunnel_id']}\n"
        value += f"Assigned  : {ip['assigned_at'][:16]}\n"
        value += f"```"
        
        embed.add_field(name=f"IPv4 #{i}", value=value, inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name="ipv4-details")
@commands.cooldown(1, 3, commands.BucketType.user)
async def ipv4_details(ctx, container_name: str):
    """Show detailed IPv4 info for a container"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    # Verify ownership
    vps_list = get_user_vps(user_id)
    if not any(v['container_name'] == container_name for v in vps_list) and not is_admin(user_id):
        await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
        return
    
    # Get IPv4 from database
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM ipv4 WHERE user_id = ? AND container_name = ?', (user_id, container_name))
    ipv4 = cur.fetchone()
    
    # Get live network info
    out, _, _ = await exec_in_container(container_name, "ip addr show")
    routes, _, _ = await exec_in_container(container_name, "ip route show")
    stats = await get_container_real_time_stats(container_name)
    
    conn.close()
    
    embed = info_embed(f"Network Details: {container_name}")
    
    if ipv4:
        embed.add_field(name="🌐 Public IP", value=f"```fix\n{ipv4['public_ip']}\n```", inline=True)
        embed.add_field(name="🏠 Private IP", value=f"```fix\n{ipv4['private_ip']}\n```", inline=True)
        embed.add_field(name="🔌 MAC", value=f"```fix\n{ipv4['mac_address']}\n```", inline=True)
        embed.add_field(name="🚪 Gateway", value=f"```fix\n{ipv4['gateway']}\n```", inline=True)
        embed.add_field(name="🎭 Netmask", value=f"```fix\n{ipv4['netmask']}\n```", inline=True)
        embed.add_field(name="📡 Interface", value=f"```fix\n{ipv4['interface']}\n```", inline=True)
    else:
        embed.add_field(name="🌐 Public IP", value=f"```fix\n{SERVER_IP}\n```", inline=True)
        embed.add_field(name="🏠 Private IP", value=f"```fix\n{stats['ipv4'][0] if stats['ipv4'] else 'N/A'}\n```", inline=True)
        embed.add_field(name="🔌 MAC", value=f"```fix\n{stats['mac']}\n```", inline=True)
    
    embed.add_field(name="📋 Live Network Config", value=f"```bash\n{out[:500]}\n```", inline=False)
    embed.add_field(name="🗺️ Routing Table", value=f"```bash\n{routes[:500]}\n```", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name="ipv4-renew")
@commands.cooldown(1, 5, commands.BucketType.user)
async def ipv4_renew(ctx, container_name: str):
    """Renew IPv4 lease"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    user_id = str(ctx.author.id)
    
    # Verify ownership
    vps_list = get_user_vps(user_id)
    if not any(v['container_name'] == container_name for v in vps_list) and not is_admin(user_id):
        await ctx.send(embed=error_embed("Access Denied", "```diff\n- You don't own this VPS.\n```"))
        return
    
    await ctx.send(embed=info_embed("Renewing IP", f"```fix\nRenewing DHCP lease for {container_name}...\n```"))
    
    try:
        await exec_in_container(container_name, "dhclient -r && dhclient")
        await asyncio.sleep(3)
        
        # Get new IP
        out, _, _ = await exec_in_container(container_name, "ip -4 addr show eth0 | grep -oP '(?<=inet\\s)\\d+\\.\\d+\\.\\d+\\.\\d+' | head -1")
        new_ip = out.strip()
        
        if new_ip:
            embed = success_embed("IP Renewed", f"```fix\nNew IP: {new_ip}\n```")
        else:
            embed = success_embed("IP Renewed", "```fix\nDHCP lease renewed.\n```")
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"))

# ==================================================================================================
#  💳  UPI PAYMENT COMMANDS
# ==================================================================================================

@bot.command(name="upi")
@commands.cooldown(1, 2, commands.BucketType.user)
async def upi_info(ctx):
    """Show current UPI configuration"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    upi_config = get_upi_config()
    
    embed = info_embed("UPI Payment Information")
    embed.add_field(name="📱 UPI ID", value=f"```fix\n{upi_config['upi_id']}\n```", inline=True)
    embed.add_field(name="👤 Name", value=f"```fix\n{upi_config.get('upi_name', 'N/A')}\n```", inline=True)
    embed.add_field(name="💰 IPv4 Price", value=f"```fix\n₹{IPV4_PRICE_INR}\n```", inline=True)
    
    if upi_config.get('qr_code_path'):
        embed.add_field(name="📸 QR Code", value="Available", inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name="upi-qr")
@commands.cooldown(1, 5, commands.BucketType.user)
async def upi_qr(ctx, amount: int = None, *, note: str = None):
    """Generate UPI QR code"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    upi_config = get_upi_config()
    
    if amount and amount <= 0:
        await ctx.send(embed=error_embed("Invalid Amount", "```diff\n- Amount must be positive.\n```"))
        return
    
    if not note:
        note = f"Payment to {BOT_NAME}"
    
    qr_bytes = generate_upi_qr(upi_config['upi_id'], amount, note)
    
    if qr_bytes:
        file = discord.File(qr_bytes, filename="upi_qr.png")
        
        embed = info_embed("UPI QR Code")
        embed.add_field(name="📱 UPI ID", value=f"```fix\n{upi_config['upi_id']}\n```", inline=True)
        if amount:
            embed.add_field(name="💰 Amount", value=f"```fix\n₹{amount}\n```", inline=True)
        if note:
            embed.add_field(name="📝 Note", value=f"```fix\n{note}\n```", inline=False)
        embed.set_image(url="attachment://upi_qr.png")
        
        await ctx.send(embed=embed, file=file)
    else:
        await ctx.send(embed=error_embed("Failed", "```diff\n- Could not generate QR code.\n```"))

@bot.command(name="pay")
@commands.cooldown(1, 5, commands.BucketType.user)
async def pay_command(ctx, amount: int, *, note: str = None):
    """Generate payment link"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    if amount <= 0:
        await ctx.send(embed=error_embed("Invalid Amount", "```diff\n- Amount must be positive.\n```"))
        return
    
    upi_config = get_upi_config()
    
    if not note:
        note = f"Payment to {BOT_NAME}"
    
    # Create UPI payment URL
    payment_url = f"upi://pay?pa={upi_config['upi_id']}&pn={upi_config.get('upi_name', '')}&am={amount}&tn={note}"
    
    # Create view with buttons
    view = View()
    
    # Payment link button
    link_btn = Button(label="💳 Pay Now", style=discord.ButtonStyle.link, url=payment_url)
    view.add_item(link_btn)
    
    # QR button
    qr_btn = Button(label="📸 Show QR", style=discord.ButtonStyle.secondary)
    
    async def qr_callback(interaction):
        qr_bytes = generate_upi_qr(upi_config['upi_id'], amount, note)
        if qr_bytes:
            file = discord.File(qr_bytes, filename="qr.png")
            qr_embed = info_embed("Payment QR Code")
            qr_embed.set_image(url="attachment://qr.png")
            await interaction.response.send_message(embed=qr_embed, file=file, ephemeral=True)
        else:
            await interaction.response.send_message(embed=error_embed("Failed", "Could not generate QR"), ephemeral=True)
    
    qr_btn.callback = qr_callback
    view.add_item(qr_btn)
    
    embed = info_embed("Payment Link Generated")
    embed.add_field(name="💰 Amount", value=f"```fix\n₹{amount}\n```", inline=True)
    embed.add_field(name="📱 UPI ID", value=f"```fix\n{upi_config['upi_id']}\n```", inline=True)
    embed.add_field(name="📝 Note", value=f"```fix\n{note}\n```", inline=False)
    
    await ctx.send(embed=embed, view=view)

@bot.command(name="admin-add-upi")
@admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def admin_add_upi(ctx, upi_id: str, *, name: str = None):
    """Set UPI ID for payments"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    update_upi_config(upi_id, name, updated_by=str(ctx.author.id))
    
    embed = success_embed("UPI Configuration Updated")
    embed.add_field(name="📱 UPI ID", value=f"```fix\n{upi_id}\n```", inline=True)
    if name:
        embed.add_field(name="👤 Name", value=f"```fix\n{name}\n```", inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name="admin-upi-qr")
@admin_only()
@commands.cooldown(1, 10, commands.BucketType.user)
async def admin_upi_qr(ctx):
    """Generate and set UPI QR code"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    upi_config = get_upi_config()
    
    # Generate QR code
    qr_bytes = generate_upi_qr(upi_config['upi_id'])
    
    if not qr_bytes:
        await ctx.send(embed=error_embed("Failed", "```diff\n- Could not generate QR code.\n```"))
        return
    
    # Save QR code
    qr_path = f"/opt/svm5-bot/qr_codes/upi_qr_{int(time.time())}.png"
    with open(qr_path, 'wb') as f:
        f.write(qr_bytes.getvalue())
    
    # Update database
    conn = get_db()
    cur = conn.cursor()
    cur.execute('UPDATE upi_config SET qr_code_path = ? WHERE is_active = 1', (qr_path,))
    conn.commit()
    conn.close()
    
    # Send QR code
    file = discord.File(qr_bytes, filename="upi_qr.png")
    
    embed = success_embed("UPI QR Code Generated")
    embed.add_field(name="📱 UPI ID", value=f"```fix\n{upi_config['upi_id']}\n```", inline=True)
    embed.set_image(url="attachment://upi_qr.png")
    
    await ctx.send(embed=embed, file=file)

# ==================================================================================================
#  🛡️  ADMIN COMMANDS (Partial - continued from before)
# ==================================================================================================

@bot.command(name="create")
@admin_only()
@commands.cooldown(1, 10, commands.BucketType.user)
async def admin_create(ctx, ram: int, cpu: int, disk: int, user: discord.Member):
    """Create a VPS for a user"""
    if ram <= 0 or cpu <= 0 or disk <= 0:
        await ctx.send(embed=error_embed("Invalid Specs", "```diff\n- RAM, CPU, and Disk must be positive integers.\n```"))
        return
    
    # OS selection view
    view = View(timeout=60)
    options = []
    for os in OS_OPTIONS[:25]:
        options.append(discord.SelectOption(
            label=os["label"][:100], 
            value=os["value"], 
            description=os["desc"][:100] if os["desc"] else None,
            emoji=os.get("emoji", "🐧")
        ))
    
    select = Select(placeholder="📋 Select operating system...", options=options)
    
    async def select_callback(interaction: discord.Interaction):
        if interaction.user.id != ctx.author.id:
            await interaction.response.send_message("```diff\n- Not your command!\n```", ephemeral=True)
            return
        
        selected_os = select.values[0]
        
        # Confirm view
        confirm_view = View(timeout=60)
        confirm_btn = Button(label="✅ Create", style=discord.ButtonStyle.success)
        cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
        
        async def confirm_callback(confirm_interaction):
            await create_vps_action(confirm_interaction, user, ram, cpu, disk, selected_os)
        
        async def cancel_callback(cancel_interaction):
            await cancel_interaction.response.edit_message(embed=info_embed("Cancelled", "```fix\nVPS creation cancelled.\n```"), view=None)
        
        confirm_btn.callback = confirm_callback
        cancel_btn.callback = cancel_callback
        confirm_view.add_item(confirm_btn)
        confirm_view.add_item(cancel_btn)
        
        os_name = next((o["label"] for o in OS_OPTIONS if o["value"] == selected_os), selected_os)
        
        embed = warning_embed(
            "Confirm VPS Creation",
            f"```fix\nUser: {user}\nOS: {os_name}\nRAM: {ram}GB\nCPU: {cpu} Core(s)\nDisk: {disk}GB\n```"
        )
        
        await interaction.response.edit_message(embed=embed, view=confirm_view)
    
    select.callback = select_callback
    view.add_item(select)
    
    embed = info_embed("Create VPS", f"```fix\nSelect an operating system for {user}\n```")
    await ctx.send(embed=embed, view=view)

async def create_vps_action(interaction, user, ram, cpu, disk, os_version):
    await interaction.response.defer(ephemeral=True)
    
    user_id = str(user.id)
    container_name = f"svm5-{user_id[:6]}-{random.randint(1000, 9999)}"
    
    progress = await interaction.followup.send(
        embed=info_embed("Creating VPS", "```fix\nStep 1/4: Initializing container...\n```"),
        ephemeral=True
    )
    
    try:
        # Initialize
        ram_mb = ram * 1024
        await run_lxc(f"lxc init {os_version} {container_name} -s {DEFAULT_STORAGE_POOL}")
        
        await progress.edit(embed=info_embed("Creating VPS", "```fix\nStep 2/4: Configuring resources...\n```"))
        
        # Set limits
        await run_lxc(f"lxc config set {container_name} limits.memory {ram_mb}MB")
        await run_lxc(f"lxc config set {container_name} limits.cpu {cpu}")
        await run_lxc(f"lxc config device set {container_name} root size={disk}GB")
        
        # Apply config
        await apply_lxc_config(container_name)
        
        await progress.edit(embed=info_embed("Creating VPS", "```fix\nStep 3/4: Starting container...\n```"))
        
        # Start
        await run_lxc(f"lxc start {container_name}")
        
        # Apply permissions
        await apply_internal_permissions(container_name)
        
        await progress.edit(embed=info_embed("Creating VPS", "```fix\nStep 4/4: Finalizing...\n```"))
        
        # Get container IP and MAC
        out, _, _ = await exec_in_container(container_name, "ip -4 addr show eth0 | grep -oP '(?<=inet\\s)\\d+\\.\\d+\\.\\d+\\.\\d+' | head -1")
        ip = out.strip() if out else "N/A"
        
        out, _, _ = await exec_in_container(container_name, "ip link show eth0 | grep -oP '(?<=link/ether\\s)\\S+'")
        mac = out.strip() if out else "N/A"
        
        # Save to database
        vps = add_vps(
            user_id=user_id,
            container_name=container_name,
            ram=ram,
            cpu=cpu,
            disk=disk,
            os_version=os_version,
            plan_name="Custom"
        )
        
        # Update VPS with IP and MAC
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET ip_address = ?, mac_address = ? WHERE container_name = ?',
                   (ip, mac, container_name))
        conn.commit()
        conn.close()
        
        # Assign role
        if interaction.guild:
            role = discord.utils.get(interaction.guild.roles, name=f"{BOT_NAME} User")
            if not role:
                role = await interaction.guild.create_role(name=f"{BOT_NAME} User", color=discord.Color.purple())
            try:
                await user.add_roles(role)
            except:
                pass
        
        # DM user
        try:
            dm_embed = success_embed("✅ VPS Created for You!")
            dm_embed.add_field(name="📦 Container", value=f"```fix\n{container_name}\n```", inline=True)
            dm_embed.add_field(name="⚙️ Resources", value=f"```fix\n{ram}GB RAM / {cpu} CPU / {disk}GB Disk\n```", inline=True)
            dm_embed.add_field(name="🐧 OS", value=f"```fix\n{os_version}\n```", inline=True)
            dm_embed.add_field(name="🌐 IP", value=f"```fix\n{ip}\n```", inline=True)
            dm_embed.add_field(name="🔌 MAC", value=f"```fix\n{mac}\n```", inline=True)
            dm_embed.add_field(name="🖥️ Management", value=f"Use `{BOT_PREFIX}manage` to control your VPS", inline=False)
            await user.send(embed=dm_embed)
        except:
            pass
        
        # Success
        embed = success_embed("✅ VPS Created Successfully!")
        embed.add_field(name="👤 User", value=user.mention, inline=True)
        embed.add_field(name="📦 Container", value=f"```fix\n{container_name}\n```", inline=True)
        embed.add_field(name="⚙️ Resources", value=f"```fix\n{ram}GB RAM / {cpu} CPU / {disk}GB Disk\n```", inline=False)
        embed.add_field(name="🌐 IP", value=f"```fix\n{ip}\n```", inline=True)
        embed.add_field(name="🔌 MAC", value=f"```fix\n{mac}\n```", inline=True)
        
        await progress.edit(embed=embed)
        logger.info(f"Admin {interaction.user} created VPS {container_name} for {user}")
        
    except Exception as e:
        logger.error(f"VPS creation failed: {e}")
        await progress.edit(embed=error_embed("Creation Failed", f"```diff\n- Error: {str(e)}\n```"))
        try:
            await run_lxc(f"lxc delete {container_name} --force")
        except:
            pass

@bot.command(name="delete")
@admin_only()
@commands.cooldown(1, 10, commands.BucketType.user)
async def admin_delete(ctx, user: discord.Member, vps_num: int, *, reason: str = "No reason provided"):
    """Delete a user's VPS"""
    user_id = str(user.id)
    vps_list = get_user_vps(user_id)
    
    if not vps_list:
        await ctx.send(embed=error_embed("No VPS", f"```diff\n- {user.mention} has no VPS.\n```"))
        return
    
    if vps_num < 1 or vps_num > len(vps_list):
        await ctx.send(embed=error_embed("Invalid Number", f"```diff\n- VPS number must be between 1 and {len(vps_list)}.\n```"))
        return
    
    vps = vps_list[vps_num - 1]
    container = vps['container_name']
    
    # Confirmation view
    view = View(timeout=60)
    confirm_btn = Button(label="✅ Confirm Delete", style=discord.ButtonStyle.danger)
    cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    
    async def confirm_callback(interaction):
        await delete_vps_action(interaction, user, vps, container, reason)
    
    async def cancel_callback(interaction):
        await interaction.response.edit_message(embed=info_embed("Cancelled", "```fix\nDeletion cancelled.\n```"), view=None)
    
    confirm_btn.callback = confirm_callback
    cancel_btn.callback = cancel_callback
    view.add_item(confirm_btn)
    view.add_item(cancel_btn)
    
    embed = warning_embed(
        "⚠️ Confirm VPS Deletion",
        f"```fix\nUser: {user}\nVPS #{vps_num}: {container}\nPlan: {vps['plan_name']}\nResources: {vps['ram']}GB RAM / {vps['cpu']} CPU / {vps['disk']}GB Disk\nReason: {reason}\n```\n\n"
        f"**This action cannot be undone!**"
    )
    
    await ctx.send(embed=embed, view=view)

async def delete_vps_action(interaction, user, vps, container, reason):
    await interaction.response.defer()
    
    try:
        # Stop and delete container
        await run_lxc(f"lxc stop {container} --force")
        await run_lxc(f"lxc delete {container}")
        
        # Remove from database
        delete_vps(container)
        
        # Log
        log_suspension(container, str(user.id), 'delete', reason, str(interaction.user.id))
        
        # DM user
        try:
            dm_embed = warning_embed("VPS Deleted", f"```fix\nYour VPS {container} has been deleted.\nReason: {reason}\n```")
            await user.send(embed=dm_embed)
        except:
            pass
        
        embed = success_embed("VPS Deleted", f"```fix\nVPS {container} has been deleted.\n```")
        await interaction.followup.send(embed=embed)
        logger.info(f"Admin {interaction.user} deleted VPS {container} for {user}")
        
    except Exception as e:
        await interaction.followup.send(embed=error_embed("Deletion Failed", f"```diff\n- {str(e)}\n```"))

@bot.command(name="suspend")
@admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def admin_suspend(ctx, container_name: str, *, reason: str = "Admin action"):
    """Suspend a VPS"""
    # Find the VPS
    all_vps = get_all_vps()
    vps = next((v for v in all_vps if v['container_name'] == container_name), None)
    
    if not vps:
        await ctx.send(embed=error_embed("Not Found", f"```diff\n- VPS {container_name} not found.\n```"))
        return
    
    if vps['suspended']:
        await ctx.send(embed=error_embed("Already Suspended", "```diff\n- This VPS is already suspended.\n```"))
        return
    
    try:
        # Stop the container
        await run_lxc(f"lxc stop {container_name} --force")
        
        # Update database
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET suspended = 1, suspended_reason = ?, status = "stopped" WHERE container_name = ?',
                    (reason, container_name))
        conn.commit()
        conn.close()
        
        # Log
        log_suspension(container_name, vps['user_id'], 'suspend', reason, str(ctx.author.id))
        
        # Notify user
        try:
            user = await bot.fetch_user(int(vps['user_id']))
            dm_embed = warning_embed("VPS Suspended", f"```fix\nYour VPS {container_name} has been suspended.\nReason: {reason}\n```")
            await user.send(embed=dm_embed)
        except:
            pass
        
        embed = success_embed("VPS Suspended", f"```fix\nVPS {container_name} has been suspended.\nReason: {reason}\n```")
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"))

@bot.command(name="unsuspend")
@admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def admin_unsuspend(ctx, container_name: str):
    """Unsuspend a VPS"""
    # Find the VPS
    all_vps = get_all_vps()
    vps = next((v for v in all_vps if v['container_name'] == container_name), None)
    
    if not vps:
        await ctx.send(embed=error_embed("Not Found", f"```diff\n- VPS {container_name} not found.\n```"))
        return
    
    if not vps['suspended']:
        await ctx.send(embed=error_embed("Not Suspended", "```diff\n- This VPS is not suspended.\n```"))
        return
    
    try:
        # Start the container
        await run_lxc(f"lxc start {container_name}")
        
        # Update database
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET suspended = 0, suspended_reason = "", status = "running" WHERE container_name = ?',
                    (container_name,))
        conn.commit()
        conn.close()
        
        # Log
        log_suspension(container_name, vps['user_id'], 'unsuspend', '', str(ctx.author.id))
        
        # Notify user
        try:
            user = await bot.fetch_user(int(vps['user_id']))
            dm_embed = success_embed("VPS Unsuspended", f"```fix\nYour VPS {container_name} has been unsuspended.\n```")
            await user.send(embed=dm_embed)
        except:
            pass
        
        embed = success_embed("VPS Unsuspended", f"```fix\nVPS {container_name} has been unsuspended and started.\n```")
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"))

@bot.command(name="add-resources")
@admin_only()
@commands.cooldown(1, 10, commands.BucketType.user)
async def admin_add_resources(ctx, container_name: str, ram: int = None, cpu: int = None, disk: int = None):
    """Add resources to a VPS"""
    if ram is None and cpu is None and disk is None:
        await ctx.send(embed=error_embed("Missing Parameters", "```diff\n- Specify at least one resource to add.\n```"))
        return
    
    # Find the VPS
    all_vps = get_all_vps()
    vps = next((v for v in all_vps if v['container_name'] == container_name), None)
    
    if not vps:
        await ctx.send(embed=error_embed("Not Found", f"```diff\n- VPS {container_name} not found.\n```"))
        return
    
    if vps['suspended']:
        await ctx.send(embed=error_embed("Suspended", "```diff\n- Cannot modify a suspended VPS.\n```"))
        return
    
    was_running = vps['status'] == 'running' and not vps['suspended']
    
    if was_running:
        await ctx.send(embed=info_embed("Stopping VPS", f"```fix\nStopping {container_name} to apply changes...\n```"))
        await run_lxc(f"lxc stop {container_name} --force")
    
    changes = []
    
    try:
        if ram:
            current_ram = vps['ram']
            new_ram = current_ram + ram
            ram_mb = new_ram * 1024
            await run_lxc(f"lxc config set {container_name} limits.memory {ram_mb}MB")
            changes.append(f"RAM: +{ram}GB (now {new_ram}GB)")
            
            conn = get_db()
            cur = conn.cursor()
            cur.execute('UPDATE vps SET ram = ? WHERE container_name = ?', (new_ram, container_name))
            conn.commit()
            conn.close()
        
        if cpu:
            current_cpu = vps['cpu']
            new_cpu = current_cpu + cpu
            await run_lxc(f"lxc config set {container_name} limits.cpu {new_cpu}")
            changes.append(f"CPU: +{cpu} cores (now {new_cpu})")
            
            conn = get_db()
            cur = conn.cursor()
            cur.execute('UPDATE vps SET cpu = ? WHERE container_name = ?', (new_cpu, container_name))
            conn.commit()
            conn.close()
        
        if disk:
            current_disk = vps['disk']
            new_disk = current_disk + disk
            await run_lxc(f"lxc config device set {container_name} root size={new_disk}GB")
            changes.append(f"Disk: +{disk}GB (now {new_disk}GB)")
            
            conn = get_db()
            cur = conn.cursor()
            cur.execute('UPDATE vps SET disk = ? WHERE container_name = ?', (new_disk, container_name))
            conn.commit()
            conn.close()
        
        if was_running:
            await ctx.send(embed=info_embed("Starting VPS", f"```fix\nStarting {container_name}...\n```"))
            await run_lxc(f"lxc start {container_name}")
            await apply_internal_permissions(container_name)
        
        embed = success_embed("Resources Added", f"```fix\nChanges applied to {container_name}:\n{chr(10).join(changes)}\n```")
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(embed=error_embed("Failed", f"```diff\n- {str(e)}\n```"))
        
        # Try to start if it was running
        if was_running:
            try:
                await run_lxc(f"lxc start {container_name}")
            except:
                pass

@bot.command(name="userinfo")
@admin_only()
@commands.cooldown(1, 3, commands.BucketType.user)
async def admin_userinfo(ctx, user: discord.Member = None):
    """Get detailed user information - shows own info if no user specified"""
    if not await maintenance_check(ctx) or not await license_check(ctx):
        return
    
    if user is None:
        user = ctx.author
    elif not is_admin(str(ctx.author.id)) and user.id != ctx.author.id:
        await ctx.send(embed=error_embed("Access Denied", "```diff\n- You can only view your own information.\n```"))
        return
    
    user_id = str(user.id)
    vps_list = get_user_vps(user_id)
    stats = get_user_stats(user_id)
    ipv4_list = get_user_ipv4(user_id)
    forwards = get_user_port_forwards(user_id)
    port_quota = get_port_allocation(user_id)
    panels = get_user_panels(user_id)
    
    embed = info_embed(f"User Info: {user.display_name}")
    embed.add_field(name="🆔 User ID", value=f"```fix\n{user.id}\n```", inline=True)
    embed.add_field(name="📅 Joined", value=f"```fix\n{user.joined_at.strftime('%Y-%m-%d') if user.joined_at else 'Unknown'}\n```", inline=True)
    
    stats_text = f"```fix\n"
    stats_text += f"Invites : {stats.get('invites', 0)}\n"
    stats_text += f"Boosts  : {stats.get('boosts', 0)}\n"
    stats_text += f"Claimed : {stats.get('claimed_vps_count', 0)}\n"
    stats_text += f"Ports   : {port_quota} (Used: {len(forwards)})\n"
    stats_text += f"API Key : {stats.get('api_key', 'None')[:8]}...\n"
    stats_text += f"```"
    embed.add_field(name="📊 Statistics", value=stats_text, inline=True)
    
    if vps_list:
        vps_text = ""
        for i, vps in enumerate(vps_list, 1):
            status = "🟢" if vps['status'] == 'running' and not vps['suspended'] else "⛔" if vps['suspended'] else "🔴"
            vps_text += f"{status} VPS #{i}: `{vps['container_name']}` ({vps['ram']}GB/{vps['cpu']}C/{vps['disk']}GB)\n"
        embed.add_field(name=f"🖥️ VPS ({len(vps_list)})", value=vps_text, inline=False)
    else:
        embed.add_field(name="🖥️ VPS", value="```fix\nNone\n```", inline=False)
    
    if ipv4_list:
        embed.add_field(name=f"🌍 IPv4 ({len(ipv4_list)})", value="\n".join(f"`{ip['container_name']}`" for ip in ipv4_list), inline=False)
    
    if panels:
        embed.add_field(name=f"📦 Panels ({len(panels)})", value="\n".join(f"`{p['panel_type']}`" for p in panels), inline=False)
    
    await ctx.send(embed=embed)

# ==================================================================================================
#  👑  MAIN ADMIN COMMANDS (Continued)
# ==================================================================================================

@bot.command(name="admin-add")
@main_admin_only()
@commands.cooldown(1, 3, commands.BucketType.user)
async def main_admin_add(ctx, user: discord.Member):
    """Add a new admin"""
    if str(user.id) in [str(a) for a in MAIN_ADMIN_IDS]:
        await ctx.send(embed=error_embed("Already Main Admin", "```diff\n- This user is already a main admin.\n```"))
        return
    
    if is_admin(str(user.id)):
        await ctx.send(embed=error_embed("Already Admin", f"```diff\n- {user.mention} is already an admin.\n```"))
        return
    
    add_admin(str(user.id), str(ctx.author.id))
    
    embed = success_embed("Admin Added", f"```fix\n{user.mention} has been added as an admin.\n```")
    await ctx.send(embed=embed)

@bot.command(name="admin-remove")
@main_admin_only()
@commands.cooldown(1, 3, commands.BucketType.user)
async def main_admin_remove(ctx, user: discord.Member):
    """Remove an admin"""
    if str(user.id) in [str(a) for a in MAIN_ADMIN_IDS]:
        await ctx.send(embed=error_embed("Cannot Remove", "```diff\n- Cannot remove main admin.\n```"))
        return
    
    if not is_admin(str(user.id)):
        await ctx.send(embed=error_embed("Not Admin", f"```diff\n- {user.mention} is not an admin.\n```"))
        return
    
    remove_admin(str(user.id))
    
    embed = success_embed("Admin Removed", f"```fix\n{user.mention} has been removed as an admin.\n```")
    await ctx.send(embed=embed)

@bot.command(name="admin-list")
@main_admin_only()
@commands.cooldown(1, 3, commands.BucketType.user)
async def main_admin_list(ctx):
    """List all admins"""
    admins = get_admins()
    
    embed = info_embed("Admin List")
    
    main_admin_text = ""
    for admin_id in MAIN_ADMIN_IDS:
        try:
            user = await bot.fetch_user(admin_id)
            main_admin_text += f"👑 {user.mention}\n"
        except:
            main_admin_text += f"👑 `{admin_id}`\n"
    
    embed.add_field(name="👑 Main Admin", value=main_admin_text, inline=False)
    
    if admins:
        admin_text = ""
        for admin_id in admins:
            try:
                user = await bot.fetch_user(int(admin_id))
                admin_text += f"🛡️ {user.mention}\n"
            except:
                admin_text += f"🛡️ `{admin_id}`\n"
        embed.add_field(name="🛡️ Admins", value=admin_text, inline=False)
    else:
        embed.add_field(name="🛡️ Admins", value="```fix\nNone\n```", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name="maintenance")
@main_admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def main_maintenance(ctx, mode: str):
    """Toggle maintenance mode"""
    global MAINTENANCE_MODE
    
    mode = mode.lower()
    if mode not in ['on', 'off']:
        await ctx.send(embed=error_embed("Invalid Mode", "```diff\n- Use `on` or `off`.\n```"))
        return
    
    MAINTENANCE_MODE = (mode == 'on')
    set_setting('maintenance_mode', str(MAINTENANCE_MODE).lower())
    
    if MAINTENANCE_MODE:
        await bot.change_presence(status=discord.Status.idle, activity=discord.Game(name="🔧 Maintenance Mode"))
        embed = warning_embed("Maintenance Mode Enabled", "```fix\nOnly admins can use commands now.\n```")
    else:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{BOT_PREFIX}help | {BOT_NAME}"))
        embed = success_embed("Maintenance Mode Disabled", "```fix\nAll commands are now available.\n```")
    
    await ctx.send(embed=embed)

@bot.command(name="set-threshold")
@main_admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def main_set_threshold(ctx, cpu: int, ram: int, disk: int = 90):
    """Set CPU, RAM and Disk thresholds"""
    global CPU_THRESHOLD, RAM_THRESHOLD, DISK_THRESHOLD
    
    if cpu < 0 or cpu > 100 or ram < 0 or ram > 100 or disk < 0 or disk > 100:
        await ctx.send(embed=error_embed("Invalid Values", "```diff\n- Thresholds must be between 0 and 100.\n```"))
        return
    
    CPU_THRESHOLD = cpu
    RAM_THRESHOLD = ram
    DISK_THRESHOLD = disk
    set_setting('cpu_threshold', str(cpu))
    set_setting('ram_threshold', str(ram))
    set_setting('disk_threshold', str(disk))
    
    embed = success_embed("Thresholds Updated", f"```fix\nCPU: {cpu}%\nRAM: {ram}%\nDisk: {disk}%\n```")
    await ctx.send(embed=embed)

@bot.command(name="system-info")
@main_admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def system_info(ctx):
    """Detailed system information"""
    # Get system stats
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    cpu_freq = psutil.cpu_freq()
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk = psutil.disk_usage('/')
    disk_io = psutil.disk_io_counters()
    network = psutil.net_io_counters()
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    users = psutil.users()
    
    embed = create_embed("System Information")
    
    # System Info
    sys_info = f"```fix\n"
    sys_info += f"Hostname : {HOSTNAME}\n"
    sys_info += f"Server IP: {SERVER_IP}\n"
    sys_info += f"MAC Addr : {MAC_ADDRESS}\n"
    sys_info += f"Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    sys_info += f"Users    : {len(users)}\n"
    sys_info += f"```"
    embed.add_field(name="💻 System", value=sys_info, inline=False)
    
    # CPU Info
    cpu_info = f"```fix\n"
    cpu_info += f"Cores    : {psutil.cpu_count()} ({psutil.cpu_count(logical=False)} physical)\n"
    cpu_info += f"Usage    : {cpu_percent[0]:.1f}% (avg)\n"
    cpu_info += f"Frequency: {cpu_freq.current:.0f} MHz\n" if cpu_freq else ""
    cpu_info += f"```"
    embed.add_field(name="⚙️ CPU", value=cpu_info, inline=True)
    
    # Memory Info
    mem_info = f"```fix\n"
    mem_info += f"RAM      : {memory.used//1024//1024}MB/{memory.total//1024//1024}MB ({memory.percent}%)\n"
    mem_info += f"Swap     : {swap.used//1024//1024}MB/{swap.total//1024//1024}MB ({swap.percent}%)\n"
    mem_info += f"```"
    embed.add_field(name="💾 Memory", value=mem_info, inline=True)
    
    # Disk Info
    disk_info = f"```fix\n"
    disk_info += f"Disk     : {disk.used//1024//1024//1024}GB/{disk.total//1024//1024//1024}GB ({disk.percent}%)\n"
    disk_info += f"Read     : {disk_io.read_bytes//1024//1024} MB\n" if disk_io else ""
    disk_info += f"Write    : {disk_io.write_bytes//1024//1024} MB\n" if disk_io else ""
    disk_info += f"```"
    embed.add_field(name="📀 Disk", value=disk_info, inline=True)
    
    # Network Info
    net_info = f"```fix\n"
    net_info += f"Sent     : {network.bytes_sent/1024/1024:.2f} MB\n"
    net_info += f"Received : {network.bytes_recv/1024/1024:.2f} MB\n"
    net_info += f"Packets Sent: {network.packets_sent}\n"
    net_info += f"Packets Recv: {network.packets_recv}\n"
    net_info += f"```"
    embed.add_field(name="🌐 Network", value=net_info, inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name="protect")
@main_admin_only()
@commands.cooldown(1, 2, commands.BucketType.user)
async def main_protect(ctx, user: discord.Member, vps_num: int = None):
    """Protect a VPS from purge"""
    user_id = str(user.id)
    vps_list = get_user_vps(user_id)
    
    if not vps_list:
        await ctx.send(embed=error_embed("No VPS", f"```diff\n- {user.mention} has no VPS.\n```"))
        return
    
    if vps_num is None:
        # Protect all
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET purge_protected = 1 WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
        
        embed = success_embed("Protection Added", f"```fix\nAll VPS of {user.mention} are now protected from purge.\n```")
        await ctx.send(embed=embed)
    else:
        if vps_num < 1 or vps_num > len(vps_list):
            await ctx.send(embed=error_embed("Invalid Number", f"```diff\n- VPS number must be between 1 and {len(vps_list)}.\n```"))
            return
        
        vps = vps_list[vps_num - 1]
        
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET purge_protected = 1 WHERE container_name = ?', (vps['container_name'],))
        conn.commit()
        conn.close()
        
        embed = success_embed("Protection Added", f"```fix\nVPS #{vps_num} of {user.mention} is now protected from purge.\n```")
        await ctx.send(embed=embed)

@bot.command(name="unprotect")
@main_admin_only()
@commands.cooldown(1, 2, commands.BucketType.user)
async def main_unprotect(ctx, user: discord.Member, vps_num: int = None):
    """Remove purge protection from a VPS"""
    user_id = str(user.id)
    vps_list = get_user_vps(user_id)
    
    if not vps_list:
        await ctx.send(embed=error_embed("No VPS", f"```diff\n- {user.mention} has no VPS.\n```"))
        return
    
    if vps_num is None:
        # Unprotect all
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET purge_protected = 0 WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()
        
        embed = success_embed("Protection Removed", f"```fix\nAll VPS of {user.mention} are no longer protected from purge.\n```")
        await ctx.send(embed=embed)
    else:
        if vps_num < 1 or vps_num > len(vps_list):
            await ctx.send(embed=error_embed("Invalid Number", f"```diff\n- VPS number must be between 1 and {len(vps_list)}.\n```"))
            return
        
        vps = vps_list[vps_num - 1]
        
        conn = get_db()
        cur = conn.cursor()
        cur.execute('UPDATE vps SET purge_protected = 0 WHERE container_name = ?', (vps['container_name'],))
        conn.commit()
        conn.close()
        
        embed = success_embed("Protection Removed", f"```fix\nVPS #{vps_num} of {user.mention} is no longer protected from purge.\n```")
        await ctx.send(embed=embed)

@bot.command(name="purge-all")
@main_admin_only()
@commands.cooldown(1, 300, commands.BucketType.user)
async def main_purge_all(ctx):
    """Purge all unprotected VPS"""
    all_vps = get_all_vps()
    
    # Count unprotected
    unprotected = [v for v in all_vps if not v.get('purge_protected', 0)]
    
    if not unprotected:
        await ctx.send(embed=info_embed("No Unprotected VPS", "```fix\nAll VPS are protected.\n```"))
        return
    
    embed = warning_embed(
        "⚠️ PURGE ALL UNPROTECTED VPS",
        f"```fix\nThis will delete {len(unprotected)} unprotected VPS.\nProtected VPS will be skipped.\n```\n\n"
        f"**This action cannot be undone!**"
    )
    
    view = View(timeout=60)
    confirm_btn = Button(label="✅ PURGE", style=discord.ButtonStyle.danger)
    cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    
    async def confirm_callback(interaction):
        await perform_purge(interaction, unprotected)
    
    async def cancel_callback(interaction):
        await interaction.response.edit_message(embed=info_embed("Cancelled", "```fix\nPurge cancelled.\n```"), view=None)
    
    confirm_btn.callback = confirm_callback
    cancel_btn.callback = cancel_callback
    view.add_item(confirm_btn)
    view.add_item(cancel_btn)
    
    await ctx.send(embed=embed, view=view)

async def perform_purge(interaction, unprotected):
    await interaction.response.defer()
    
    progress = await interaction.followup.send(
        embed=info_embed("Purging VPS", f"```fix\nStarting purge of {len(unprotected)} VPS...\n```"),
        ephemeral=True
    )
    
    deleted = 0
    failed = 0
    
    for i, vps in enumerate(unprotected, 1):
        container = vps['container_name']
        
        try:
            # Update progress
            if i % 5 == 0:
                await progress.edit(embed=info_embed("Purging VPS", f"```fix\nProgress: {i}/{len(unprotected)}...\n```"))
            
            # Stop and delete
            await run_lxc(f"lxc stop {container} --force")
            await run_lxc(f"lxc delete {container}")
            
            # Remove from DB
            delete_vps(container)
            
            # Log
            log_suspension(container, vps['user_id'], 'purge', 'Purge all unprotected', str(interaction.user.id))
            
            deleted += 1
            
            # Small delay
            await asyncio.sleep(2)
            
        except Exception as e:
            logger.error(f"Failed to purge {container}: {e}")
            failed += 1
    
    embed = success_embed("Purge Complete", f"```fix\nDeleted: {deleted}\nFailed: {failed}\n```")
    await progress.edit(embed=embed)

@bot.command(name="admin-users")
@main_admin_only()
@commands.cooldown(1, 5, commands.BucketType.user)
async def admin_users(ctx):
    """List all users with VPS"""
    all_vps = get_all_vps()
    
    # Group by user
    users = {}
    for vps in all_vps:
        if vps['user_id'] not in users:
            users[vps['user_id']] = []
        users[vps['user_id']].append(vps)
    
    if not users:
        await ctx.send(embed=info_embed("No Users", "```fix\nNo users have VPS.\n```"))
        return
    
    embed = info_embed(f"Users with VPS ({len(users)})")
    
    for user_id, vps_list in list(users.items())[:10]:
        try:
            user = await bot.fetch_user(int(user_id))
            username = f"{user.name} ({user.id})"
        except:
            username = f"Unknown ({user_id})"
        
        vps_count = len(vps_list)
        running = sum(1 for v in vps_list if v['status'] == 'running' and not v['suspended'])
        
        embed.add_field(
            name=username,
            value=f"```fix\nVPS: {vps_count} (Running: {running})\nContainers: {', '.join([v['container_name'][:10] + '...' for v in vps_list[:3]])}\n```",
            inline=False
        )
    
    if len(users) > 10:
        embed.add_field(name="📝 Note", value=f"Showing 10 of {len(users)} users", inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name="backup-db")
@main_admin_only()
@commands.cooldown(1, 60, commands.BucketType.user)
async def backup_db(ctx):
    """Backup database"""
    backup_name = f"svm5_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    backup_path = f"/opt/svm5-bot/backups/{backup_name}"
    
    try:
        # Copy database
        import shutil
        shutil.copy2(DATABASE_PATH, backup_path)
        
        # Compress
        import gzip
        with open(backup_path, 'rb') as f_in:
            with gzip.open(f"{backup_path}.gz", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        os.remove(backup_path)
        
        embed = success_embed("Database Backup Created", f"```fix\nBackup: {backup_name}.gz\nLocation: /opt/svm5-bot/backups/\n```")
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(embed=error_embed("Backup Failed", f"```diff\n- {str(e)}\n```"))

@bot.command(name="restore-db")
@main_admin_only()
@commands.cooldown(1, 60, commands.BucketType.user)
async def restore_db(ctx, backup_name: str):
    """Restore database from backup"""
    backup_path = f"/opt/svm5-bot/backups/{backup_name}"
    
    if not os.path.exists(backup_path):
        # Try with .gz
        if os.path.exists(f"{backup_path}.gz"):
            backup_path = f"{backup_path}.gz"
        else:
            await ctx.send(embed=error_embed("Backup Not Found", f"```diff\n- Backup {backup_name} not found.\n```"))
            return
    
    # Confirmation view
    view = View(timeout=60)
    confirm_btn = Button(label="✅ Confirm Restore", style=discord.ButtonStyle.danger)
    cancel_btn = Button(label="❌ Cancel", style=discord.ButtonStyle.secondary)
    
    async def confirm_callback(interaction):
        try:
            # Create backup of current database
            import shutil
            import gzip
            current_backup = f"/opt/svm5-bot/backups/current_before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            shutil.copy2(DATABASE_PATH, current_backup)
            
            # Restore
            if backup_path.endswith('.gz'):
                with gzip.open(backup_path, 'rb') as f_in:
                    with open(DATABASE_PATH, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
            else:
                shutil.copy2(backup_path, DATABASE_PATH)
            
            embed = success_embed("Database Restored", f"```fix\nRestored from: {os.path.basename(backup_path)}\nCurrent DB backed up to: {os.path.basename(current_backup)}\n```")
            await interaction.response.edit_message(embed=embed, view=None)
            
        except Exception as e:
            await interaction.response.edit_message(embed=error_embed("Restore Failed", f"```diff\n- {str(e)}\n```"), view=None)
    
    async def cancel_callback(interaction):
        await interaction.response.edit_message(embed=info_embed("Cancelled", "```fix\nRestore cancelled.\n```"), view=None)
    
    confirm_btn.callback = confirm_callback
    cancel_btn.callback = cancel_callback
    view.add_item(confirm_btn)
    view.add_item(cancel_btn)
    
    embed = warning_embed(
        "⚠️ Confirm Database Restore",
        f"```fix\nBackup: {os.path.basename(backup_path)}\n```\n\n"
        f"**This will overwrite the current database!**\n"
        f"A backup of the current database will be created automatically."
    )
    
    await ctx.send(embed=embed, view=view)

@bot.command(name="reset-license")
@main_admin_only()
@commands.cooldown(1, 10, commands.BucketType.user)
async def reset_license(ctx):
    """Reset license verification"""
    set_setting('license_verified', 'false')
    global LICENSE_VERIFIED
    LICENSE_VERIFIED = False
    
    embed = success_embed("License Reset", "```fix\nLicense verification has been reset.\n```")
    await ctx.send(embed=embed)

# ==================================================================================================
#  🚀  RUN THE BOT
# ==================================================================================================

if __name__ == "__main__":
    if BOT_TOKEN == "YOUR_DISCORD_BOT_TOKEN_HERE":
        print("\n" + "="*80)
        print("❌ ERROR: Please set your BOT_TOKEN in the configuration!")
        print("="*80 + "\n")
        sys.exit(1)
    
    # Check license
    if not LICENSE_VERIFIED:
        print("\n" + "="*80)
        print("⚠️  WARNING: License not verified!")
        print("   Valid license keys: AnkitDev99$@, SVM5-PRO-2025, SVM5-ENTERPRISE")
        print("="*80 + "\n")
    
    # Check LXC
    try:
        subprocess.run(['lxc', '--version'], capture_output=True, check=True)
    except:
        print("\n" + "="*80)
        print("❌ ERROR: LXC is not installed or not in PATH!")
        print("Install LXC: sudo apt install lxc lxc-templates")
        print("Then run: sudo lxd init")
        print("="*80 + "\n")
        sys.exit(1)
    
    # Create necessary directories
    os.makedirs("/opt/svm5-bot/backups", exist_ok=True)
    os.makedirs("/opt/svm5-bot/logs", exist_ok=True)
    os.makedirs("/opt/svm5-bot/qr_codes", exist_ok=True)
    
    # Run bot
    try:
        bot.run(BOT_TOKEN)
    except discord.LoginFailure:
        print("\n" + "="*80)
        print("❌ ERROR: Invalid Discord token!")
        print("="*80 + "\n")
    except Exception as e:
        print(f"\n❌ ERROR: {e}\n")
