# 🤖 NEXVM-1-BOT - Complete Discord VPS Management Bot

<div align="center">
  <img src="https://cdn.discordapp.com/attachments/1429752932756361267/1478323497179807837/1763894084589.jpg" width="200">
  
  **Version 1.0.0** | Made by **DeVv-Prime** with ❤️
  
  [![Discord](https://img.shields.io/badge/Discord-SVM5--BOT-5865F2?logo=discord&logoColor=white)](https://discord.gg)
  [![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://python.org)
  [![License](https://img.shields.io/badge/License-Proprietary-red)](LICENSE)
  [![GitHub](https://img.shields.io/badge/GitHub-AnkitKing7-181717?logo=github)](https://github.com/DeVv-Prime/nexvm)
</div>

## 📋 **Table of Contents**
- [✨ Features](#-features)
- [🐛 Fixed Issues](#-fixed-issues)
- [💻 Requirements](#-requirements)
- [🚀 Quick Installation](#-quick-installation)
- [📥 Manual Installation](#-manual-installation)
- [⚙️ Configuration](#️-configuration)
- [📖 Commands](#-commands)
- [🌐 Node Management](#-node-management)
- [📦 Panel Installation](#-panel-installation)
- [🔌 Port Forwarding](#-port-forwarding)
- [🌍 IPv4 Management](#-ipv4-management)
- [💳 UPI Payments](#-upi-payments)
- [🤖 AI Chat](#-ai-chat)
- [📟 Console Commands](#-console-commands)
- [🛡️ Admin Commands](#️-admin-commands)
- [👑 Main Admin Commands](#-main-admin-commands)
- [📁 File Structure](#-file-structure)
- [🚀 Running the Bot](#-running-the-bot)
- [🛠️ Troubleshooting](#️-troubleshooting)
- [🔐 License & Purchase](#-license--purchase)
- [📞 Support](#-support)

---

## ✨ **Features**

### 🖥️ **VPS Management (Direct LXC)**
- ✅ Create/Delete VPS containers automatically
- ✅ Start/Stop/Restart containers with interactive buttons
- ✅ Real-time statistics with live graphs (CPU, RAM, Disk, Uptime)
- ✅ 30+ OS options (Ubuntu, Debian, Fedora, Rocky, Alma, CentOS, Alpine, Arch, FreeBSD, OpenSUSE)
- ✅ Resource limits per container
- ✅ View container logs
- ✅ SSH access via tmate (temporary SSH links)
- ✅ Reboot and shutdown commands
- ✅ Rename containers
- ✅ Live console output with command input

### 🌐 **Node Management**
- ✅ Add/Remove multiple LXC nodes
- ✅ Monitor node health and resources in real-time
- ✅ Distributed container management
- ✅ Node statistics and health checks
- ✅ API key authentication for nodes
- ✅ Region-based node grouping
- ✅ Sync containers from remote nodes

### 🔌 **Port Forwarding**
- ✅ Forward ports from container to host
- ✅ TCP/UDP protocol support
- ✅ Quota system per user
- ✅ List and manage active forwards
- ✅ Random port allocation (20000-50000)
- ✅ Protocol selection (tcp, udp, tcp+udp)
- ✅ Port availability checker

### 📦 **Panel Installation**
- ✅ Install Pterodactyl game panel
- ✅ Install Pufferpanel lightweight panel
- ✅ Automatic credential generation
- ✅ Cloudflared tunnel support for public URLs
- ✅ Panel information storage
- ✅ Automatic DM with credentials
- ✅ Password reset functionality

### 💰 **Free VPS System**
- ✅ Earn VPS by inviting users
- ✅ Multiple plans (Bronze to Legendary)
- ✅ Automatic claim system
- ✅ Invite tracking
- ✅ Boost rewards
- ✅ 7 plans with increasing resources
- ✅ Top inviters leaderboard

### 🌍 **IPv4 Management**
- ✅ Purchase IPv4 via UPI
- ✅ Automatic payment verification
- ✅ Admin assignment with full network details
- ✅ MAC address, gateway, netmask tracking
- ✅ View your IPv4 addresses
- ✅ ₹50 per IPv4 (configurable)
- ✅ DHCP lease renewal
- ✅ Cloudflared tunnel URLs

### 💳 **UPI Payments**
- ✅ QR code generation for payments
- ✅ Payment links for easy access
- ✅ Configurable UPI ID
- ✅ Transaction tracking
- ✅ Admin approval system
- ✅ Payment history

### 🤖 **AI Assistant**
- ✅ Groq LLaMA 3.3 integration (updated working model)
- ✅ Chat history per user
- ✅ Server management help
- ✅ 24/7 availability
- ✅ Reset conversation option
- ✅ AI help on specific topics

### 📟 **Console Commands**
- ✅ `.ss` - Take VPS screenshot/console output (real-time)
- ✅ `.console` - Interactive console with command input
- ✅ `.execute` - Run commands in VPS
- ✅ `.top` - Show live process monitor with graphs
- ✅ `.df` - Show disk usage with visual graphs
- ✅ `.free` - Show memory usage with visual graphs
- ✅ `.netstat` - Show network connections
- ✅ `.ps` - Show process list
- ✅ `.who` - Show logged-in users
- ✅ `.uptime` - Show container uptime

### 👤 **User Features**
- ✅ Account generator (username/email/password)
- ✅ View your generated accounts
- ✅ Check invite statistics
- ✅ Interactive help menu with glow effects
- ✅ Bot info and uptime
- ✅ Server hardware info
- ✅ API key generation per user

### 🛡️ **Admin Features**
- ✅ Full admin panel
- ✅ User management
- ✅ Resource allocation
- ✅ Suspension system
- ✅ Purge protection
- ✅ Server statistics
- ✅ Add/Remove admins
- ✅ List all users and VPS
- ✅ Database backup/restore
- ✅ View pending IPv4 purchases

### 👑 **Main Admin Features**
- ✅ Maintenance mode
- ✅ Purge all unprotected VPS
- ✅ Protect VPS from purge
- ✅ Set CPU/RAM/Disk thresholds
- ✅ View all users
- ✅ System information
- ✅ Reset license verification

### 🔒 **Security**
- ✅ License key verification
- ✅ Role-based access control
- ✅ Suspension system
- ✅ Audit logs
- ✅ Firewall configuration
- ✅ Fail2ban integration
- ✅ Per-user API keys

---

## 🐛 **Fixed Issues**

| Issue | Status | Fix |
|-------|--------|-----|
| Database closed error | ✅ FIXED | Added proper connection handling with try/finally blocks |
| `.help` interaction failed | ✅ FIXED | Added proper defer pattern and view handling |
| AI model deprecated | ✅ FIXED | Updated to `llama-3.3-70b-versatile` |
| SSH generation timeout | ✅ FIXED | Increased wait time and added error handling |
| `.node` command missing | ✅ FIXED | Added complete node management system |
| Port forwarding quota | ✅ FIXED | Added quota tracking and validation |
| Panel installation errors | ✅ FIXED | Added cloudflared tunnel support |
| IPv4 details incomplete | ✅ FIXED | Added MAC, gateway, netmask, interface |
| Console commands not working | ✅ FIXED | Added `.ss`, `.console`, `.top`, `.df`, `.free`, `.netstat` |
| Database backup missing | ✅ FIXED | Added backup/restore commands |
| UPI QR codes missing | ✅ FIXED | Added QR code generation with Pillow |
| API keys per user | ✅ FIXED | Added automatic API key generation |
| Real-time stats missing | ✅ FIXED | Added live graphs and updates |
| Command input modal | ✅ FIXED | Added interactive command input |

---

## 💻 **Requirements**

| Requirement | Minimum | Recommended |
|------------|---------|-------------|
| **OS** | Ubuntu 20.04 | Ubuntu 22.04/24.04 |
| **RAM** | 2 GB | 4 GB+ |
| **CPU** | 2 cores | 4 cores+ |
| **Disk** | 20 GB | 50 GB+ |
| **Python** | 3.8 | 3.10+ |
| **LXC/LXD** | 5.0 | 5.21+ |

---

## 🚀 **Quick Installation**

### **One-Line Install (Recommended)**
```bash
curl -sSL https://raw.githubusercontent.com/DeVv-Prime/NEXVM-V1/main/install.sh | sudo bash
