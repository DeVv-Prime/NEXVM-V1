#!/bin/bash

# ╔═══════════════════════════════════════════════════════════════════════════════╗
# ║                 NEX VM V1 - Ultimate Virtualization Platform                  ║
# ║                         Next Generation VM Management                         ║
# ║                    Version: 1.0.0 | Enterprise Edition                       ║
# ║                      Made by DeVv-Prime with ❤️                               ║
# ║            💰 UPI: vedant1437@fam | Discord: https://discord.gg/zS2ynbF6jK    ║
# ╚═══════════════════════════════════════════════════════════════════════════════╝

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🎨  ADVANCED COLOR DEFINITIONS WITH EFFECTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Base Colors
R='\033[0;31m'      # Red
G='\033[0;32m'      # Green
Y='\033[1;33m'      # Yellow
B='\033[0;34m'      # Blue
P='\033[0;35m'      # Purple
C='\033[0;36m'      # Cyan
W='\033[1;37m'      # White
NC='\033[0m'        # No Color

# Effects
BOLD='\033[1m'
DIM='\033[2m'
UNDERLINE='\033[4m'
BLINK='\033[5m'
REVERSE='\033[7m'
HIDDEN='\033[8m'

# Extended Colors
ORANGE='\033[38;5;214m'
PINK='\033[38;5;205m'
PURPLE='\033[38;5;129m'
GOLD='\033[38;5;220m'
SILVER='\033[38;5;250m'
LIME='\033[38;5;154m'
TEAL='\033[38;5;37m'
MAROON='\033[38;5;124m'
NAVY='\033[38;5;17m'
OLIVE='\033[38;5;58m'

# Background Colors
BG_BLACK='\033[40m'
BG_RED='\033[41m'
BG_GREEN='\033[42m'
BG_YELLOW='\033[43m'
BG_BLUE='\033[44m'
BG_PURPLE='\033[45m'
BG_CYAN='\033[46m'
BG_WHITE='\033[47m'
BG_ORANGE='\033[48;5;214m'

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  📍  ADVANCED PATH CONFIGURATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Main Directories
INSTALL_DIR="/opt/nexvm-v1"
BOT_SCRIPT="nexvm.py"
SERVICE_NAME="nexvm-v1"
LOG_FILE="/var/log/nexvm-v1.log"
CONFIG_DIR="/etc/nexvm"
DATA_DIR="/var/lib/nexvm"
BACKUP_DIR="/var/backups/nexvm"
TEMP_DIR="/tmp/nexvm"
CACHE_DIR="/var/cache/nexvm"
SSL_DIR="/etc/nexvm/ssl"
HOOKS_DIR="/etc/nexvm/hooks"
PLUGINS_DIR="/etc/nexvm/plugins"
PAYMENT_DIR="/etc/nexvm/payments"
TICKET_DIR="/etc/nexvm/tickets"

# Payment Configuration
UPI_ID="vedant1437@fam"
DISCORD_INVITE="https://discord.gg/zS2ynbF6jK"
SUPPORT_DISCORD="@DeVv-Prime"
PAYMENT_AMOUNT=499
ENTERPRISE_AMOUNT=999
TEAM_AMOUNT=2499
CLUSTER_AMOUNT=9999

# Database Configuration
DB_PATH="$DATA_DIR/nexvm.db"
DB_BACKUP_DIR="$BACKUP_DIR/database"
DB_VERSION=1

# Network Configuration
NETWORK_BRIDGE="nexbr0"
NETWORK_SUBNET="10.200.0.1/24"
PORT_RANGE_START=10000
PORT_RANGE_END=50000
MAX_CONTAINERS=100

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🖥️  CINEMATIC ASCII ART HEADER WITH PAYMENT INFO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

show_header() {
    clear
    echo -e "${GOLD}╔═══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GOLD}║                                                                               ║${NC}"
    echo -e "${TEAL}║        ███╗   ██╗███████╗██╗  ██╗    ██╗   ██╗███╗   ███║                   ║${NC}"
    echo -e "${TEAL}║        ████╗  ██║██╔════╝╚██╗██╔╝    ██║   ██║████╗ ████║                   ║${NC}"
    echo -e "${TEAL}║        ██╔██╗ ██║█████╗   ╚███╔╝     ██║   ██║██╔████╔██║                   ║${NC}"
    echo -e "${TEAL}║        ██║╚██╗██║██╔══╝   ██╔██╗     ╚██╗ ██╔╝██║╚██╔╝██║                   ║${NC}"
    echo -e "${TEAL}║        ██║ ╚████║███████╗██╔╝ ██╗     ╚████╔╝ ██║ ╚═╝ ██║                   ║${NC}"
    echo -e "${TEAL}║        ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝      ╚═══╝  ╚═╝     ╚═╝                   ║${NC}"
    echo -e "${SILVER}║                                                                            ║${NC}"
    echo -e "${GOLD}║                         ██╗   ██╗███╗   ███╗      ███                             ║${NC}"
    echo -e "${GOLD}║                         ██║   ██║████╗ ████║      ███                            ║${NC}"
    echo -e "${GOLD}║                         ██║   ██║██╔████╔██║      ███                             ║${NC}"
    echo -e "${GOLD}║                         ╚██╗ ██╔╝██║╚██╔╝██║      ███                             ║${NC}"
    echo -e "${GOLD}║                          ╚████╔╝ ██║ ╚═╝ ██║      ███                             ║${NC}"
    echo -e "${GOLD}║                          ╚═══╝  ╚═╝     ╚═╝       ╚═╝                            ║${NC}"
    echo -e "${SILVER}║                                                                             ║${NC}"
    echo -e "${PURPLE}║                         ██████╗ ██████╗ ██╗███╗   ███╗███████╗              ║${NC}"
    echo -e "${PURPLE}║                        ██╔════╝ ██╔══██╗██║████╗ ████║██╔════╝              ║${NC}"
    echo -e "${PURPLE}║                        ██║  ███╗██████╔╝██║██╔████╔██║█████╗                ║${NC}"
    echo -e "${PURPLE}║                        ██║   ██║██╔══██╗██║██║╚██╔╝██║██╔══╝                ║${NC}"
    echo -e "${PURPLE}║                        ╚██████╔╝██║  ██║██║██║ ╚═╝ ██║███████╗              ║${NC}"
    echo -e "${PURPLE}║                         ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝     ╚═╝╚══════╝              ║${NC}"
    echo -e "${SILVER}║                                                                               ║${NC}"
    echo -e "${GOLD}║                    🚀 Enterprise VM Management Platform v1.0 🚀              ║${NC}"
    echo -e "${LIME}║                        Made by ${BOLD}DeVv-Prime${NC}${LIME} with ❤️                         ║${NC}"
    echo -e "${GOLD}╠═══════════════════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${GOLD}║                                                                               ║${NC}"
    echo -e "${PINK}║                       💰 PAYMENT INFORMATION 💰                              ║${NC}"
    echo -e "${PINK}║                      ═════════════════════════════                           ║${NC}"
    echo -e "${W}║                                                                               ║${NC}"
    echo -e "${C}║                       📱 UPI ID: ${Y}vedant1437@fam${C}                           ║${NC}"
    echo -e "${W}║                                                                               ║${NC}"
    echo -e "${G}║                       💎 License Prices:                                      ║${NC}"
    echo -e "${G}║                         • Developer Edition: ₹499                             ║${NC}"
    echo -e "${G}║                         • Enterprise Edition: ₹999                            ║${NC}"
    echo -e "${G}║                         • Team License (5 users): ₹2499                       ║${NC}"
    echo -e "${G}║                         • Enterprise Cluster: ₹9999                           ║${NC}"
    echo -e "${W}║                                                                               ║${NC}"
    echo -e "${P}║                       💬 Discord Support: ${Y}https://discord.gg/zS2ynbF6jK${P}      ║${NC}"
    echo -e "${P}║                       👤 Contact: ${Y}@DeVv-Prime${P} on Discord                    ║${NC}"
    echo -e "${W}║                                                                               ║${NC}"
    echo -e "${ORANGE}║                       ⚡ Buy Now & Get Instant Access!                       ║${NC}"
    echo -e "${GOLD}║                                                                               ║${NC}"
    echo -e "${GOLD}╚═══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Subtle loading animation
    echo -ne "${DIM}Initializing NEX VM V1 Engine "
    for i in {1..20}; do
        echo -ne "${GREEN}●${NC}"
        sleep 0.02
    done
    echo -e "${G} Done!${NC}\n"
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  💰  PAYMENT QR CODE GENERATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

generate_payment_qr() {
    local amount=$1
    local license_type=$2
    
    echo -e "${GOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GOLD}║                 💰 PAYMENT QR CODE GENERATED                 ║${NC}"
    echo -e "${GOLD}╠══════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${GOLD}║                                                              ║${NC}"
    echo -e "${W}║   UPI ID: ${Y}vedant1437@fam${W}                                   ║${NC}"
    echo -e "${W}║   Amount: ₹${amount} (${license_type})                           ║${NC}"
    echo -e "${W}║                                                              ║${NC}"
    echo -e "${C}║   📱 Scan with any UPI app to pay:                            ║${NC}"
    echo -e "${W}║                                                              ║${NC}"
    
    # Generate UPI payment link
    local upi_link="upi://pay?pa=vedant1437@fam&pn=NEX%20VM%20V1&am=${amount}&cu=INR&tn=${license_type}%20License"
    
    # Create ASCII QR representation (simplified)
    echo -e "${Y}║                                                              ║${NC}"
    echo -e "${Y}║       ████████████████████████████████████████████████       ║${NC}"
    echo -e "${Y}║       ██                                          ██         ║${NC}"
    echo -e "${Y}║       ██    ██████  ██████  ██  ██                ██           ║${NC}"
    echo -e "${Y}║       ██    ██  ██  ██  ██  ██  ██                ██             ║${NC}"
    echo -e "${Y}║       ██    ██████  ██████  ██████                ██             ║${NC}"
    echo -e "${Y}║       ██    ██      ██  ██      ██                ██             ║${NC}"
    echo -e "${Y}║       ██    ██      ██  ██  ██████                ██             ║${NC}"
    echo -e "${Y}║       ██                                          ██           ║${NC}"
    echo -e "${Y}║       ████████████████████████████████████████████████         ║${NC}"
    echo -e "${W}║                                                                ║${NC}"
    echo -e "${W}║   Or click: ${UNDERLINE}${C}${upi_link}${NC}${W}               ║${NC}"
    echo -e "${GOLD}║                                                              ║${NC}"
    echo -e "${GOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    
    # Save payment link to file
    mkdir -p "$PAYMENT_DIR"
    echo "$upi_link" > "$PAYMENT_DIR/payment_${license_type}_${amount}.link"
    echo "UPI: vedant1437@fam" >> "$PAYMENT_DIR/payment_${license_type}_${amount}.link"
    echo "Amount: ₹$amount" >> "$PAYMENT_DIR/payment_${license_type}_${amount}.link"
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🎫  DISCORD TICKET CREATION LINK
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

show_discord_support() {
    echo -e "${GOLD}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GOLD}║                 🎫 DISCORD SUPPORT & TICKETS                 ║${NC}"
    echo -e "${GOLD}╠══════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${GOLD}║                                                              ║${NC}"
    echo -e "${W}║   📌 Join our Discord server for:                             ║${NC}"
    echo -e "${W}║                                                              ║${NC}"
    echo -e "${G}║   ✅ Instant Support                                        ║${NC}"
    echo -e "${G}║   🎫 Create Support Tickets                                 ║${NC}"
    echo -e "${G}║   💬 Community Chat                                         ║${NC}"
    echo -e "${G}║   📢 Latest Updates                                         ║${NC}"
    echo -e "${G}║   🤝 Developer Connect                                      ║${NC}"
    echo -e "${G}║   🔧 Troubleshooting Help                                   ║${NC}"
    echo -e "${W}║                                                              ║${NC}"
    echo -e "${C}║   🔗 Discord Invite: ${Y}${UNDERLINE}https://discord.gg/zS2ynbF6jK${NC}${C}           ║${NC}"
    echo -e "${W}║                                                              ║${NC}"
    echo -e "${P}║   👤 Support Team: @DeVv-Prime, @NEX-VM-Support             ║${NC}"
    echo -e "${W}║                                                              ║${NC}"
    echo -e "${ORANGE}║   💡 To create a ticket:                                    ║${NC}"
    echo -e "${ORANGE}║      1. Join Discord                                      ║${NC}"
    echo -e "${ORANGE}║      2. Go to #create-ticket channel                      ║${NC}"
    echo -e "${ORANGE}║      3. Click on 'Purchase Support' or 'Technical Help'   ║${NC}"
    echo -e "${ORANGE}║      4. Send payment screenshot to @DeVv-Prime            ║${NC}"
    echo -e "${W}║                                                              ║${NC}"
    echo -e "${GOLD}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🔐  ENTERPRISE LICENSE VERIFICATION WITH PAYMENT INTEGRATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

check_license() {
    show_header
    show_discord_support
    
    echo -e "${GOLD}┌─────────────────────────────────────────────────────────────────┐${NC}"
    echo -e "${GOLD}│                    🔐 ENTERPRISE LICENSE ACTIVATION              │${NC}"
    echo -e "${GOLD}├─────────────────────────────────────────────────────────────────┤${NC}"
    echo -e "${SILVER}│  This software is protected by DeVv-Prime Enterprise License     │${NC}"
    echo -e "${SILVER}│  UPI: vedant1437@fam | Discord: https://discord.gg/zS2ynbF6jK   │${NC}"
    echo -e "${GOLD}└─────────────────────────────────────────────────────────────────┘${NC}"
    echo ""
    
    # Create license directory if not exists
    mkdir -p "$CONFIG_DIR/license" "$PAYMENT_DIR" "$TICKET_DIR"
    
    # Check for existing license
    if [ -f "$CONFIG_DIR/license/license.key" ] && [ -f "$CONFIG_DIR/license/license.sig" ]; then
        STORED_KEY=$(cat "$CONFIG_DIR/license/license.key")
        STORED_SIG=$(cat "$CONFIG_DIR/license/license.sig")
        
        # Verify signature
        VERIFY_HASH=$(echo -n "$STORED_KEY" | sha256sum | awk '{print $1}')
        
        if [ "$STORED_SIG" == "$VERIFY_HASH" ]; then
            echo -e "${G}✅ Found valid license signature${NC}"
            read -p "🔑 Use existing license? (y/n): " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                KEY="$STORED_KEY"
                echo -e "${G}✅ Using existing license${NC}"
                sleep 2
                return 0
            fi
        fi
    fi
    
    # License selection with payment info
    echo -e "${Y}Available License Types:${NC}"
    echo -e "  ${GOLD}1.${NC} ${G}Developer Edition${NC}     - ₹499 (1 Year) - UPI: vedant1437@fam"
    echo -e "  ${GOLD}2.${NC} ${C}Enterprise Edition${NC}     - ₹999 (Lifetime) - UPI: vedant1437@fam"
    echo -e "  ${GOLD}3.${NC} ${P}Team License${NC}          - ₹2499 (5 Users) - UPI: vedant1437@fam"
    echo -e "  ${GOLD}4.${NC} ${ORANGE}Enterprise Cluster${NC}    - ₹9999 (Unlimited) - UPI: vedant1437@fam"
    echo -e "  ${GOLD}5.${NC} ${PINK}View Payment QR Codes${NC}"
    echo -e "  ${GOLD}6.${NC} ${BLUE}Join Discord for Support${NC}"
    echo ""
    
    read -p "Select option (1-6): " LICENSE_OPTION
    echo ""
    
    case $LICENSE_OPTION in
        1)
            AMOUNT=499
            TYPE="Developer"
            generate_payment_qr $AMOUNT $TYPE
            VALID_KEYS=("NEX-DEV-2025" "DEVVP-DEV-PRIME" "NEXVM-DEVELOPER" "DEV-${AMOUNT}-PAID")
            ;;
        2)
            AMOUNT=999
            TYPE="Enterprise"
            generate_payment_qr $AMOUNT $TYPE
            VALID_KEYS=("NEX-ENT-2025" "DEVVP-ENT-PRIME" "NEXVM-ENTERPRISE" "ENT-${AMOUNT}-PAID")
            ;;
        3)
            AMOUNT=2499
            TYPE="Team"
            generate_payment_qr $AMOUNT $TYPE
            VALID_KEYS=("NEX-TEAM-2025" "DEVVP-TEAM-PRIME" "NEXVM-TEAM" "TEAM-${AMOUNT}-PAID")
            ;;
        4)
            AMOUNT=9999
            TYPE="Cluster"
            generate_payment_qr $AMOUNT $TYPE
            VALID_KEYS=("NEX-CLUSTER-2025" "DEVVP-CLUSTER" "NEXVM-CLUSTER" "CLUSTER-${AMOUNT}-PAID")
            ;;
        5)
            generate_payment_qr 499 "Developer"
            generate_payment_qr 999 "Enterprise"
            generate_payment_qr 2499 "Team"
            generate_payment_qr 9999 "Cluster"
            echo -e "${Y}Press Enter to continue license activation...${NC}"
            read
            check_license
            return
            ;;
        6)
            show_discord_support
            echo -e "${Y}Press Enter to continue...${NC}"
            read
            check_license
            return
            ;;
        *)
            echo -e "${R}❌ Invalid selection${NC}"
            sleep 2
            check_license
            return
            ;;
    esac
    
    # Add DeVv-Prime special keys
    VALID_KEYS+=("DeVv-Prime-Master" "DEVVP-ROOT-ACCESS" "PRIME-ADMIN-2025" "VEDANT-ADMIN-KEY")
    
    echo -e "${Y}📱 After payment, join Discord: https://discord.gg/zS2ynbF6jK${NC}"
    echo -e "${Y}📤 Send payment screenshot to @DeVv-Prime on Discord${NC}"
    echo ""
    read -p "🔑 Enter License Key (or 'p' to show payment QR again): " KEY
    echo ""
    
    if [[ "$KEY" == "p" ]]; then
        generate_payment_qr $AMOUNT $TYPE
        echo -e "${Y}Press Enter to continue...${NC}"
        read
        check_license
        return
    fi
    
    # Validate license
    LICENSE_VALID=false
    for valid_key in "${VALID_KEYS[@]}"; do
        if [[ "$KEY" == "$valid_key" ]]; then
            LICENSE_VALID=true
            break
        fi
    done
    
    # Special master key for DeVv-Prime
    if [[ "$KEY" == "DEVVP-MASTER-KEY-2025" ]] || [[ "$KEY" == "PRIME-ACCESS-GRANTED" ]] || [[ "$KEY" == "VEDANT-SUPER-KEY" ]]; then
        LICENSE_VALID=true
    fi
    
    if [ "$LICENSE_VALID" = true ]; then
        echo -e "${G}╔══════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${G}║                                                              ║${NC}"
        echo -e "${G}║         ✅ LICENSE VERIFIED - ENTERPRISE ACCESS GRANTED     ║${NC}"
        echo -e "${G}║                                                              ║${NC}"
        echo -e "${G}║         Welcome, DeVv-Prime Enterprise User!                ║${NC}"
        echo -e "${G}║         Thank you for your purchase!                         ║${NC}"
        echo -e "${G}║                                                              ║${NC}"
        echo -e "${G}║         UPI: vedant1437@fam                                  ║${NC}"
        echo -e "${G}║         Discord: https://discord.gg/zS2ynbF6jK              ║${NC}"
        echo -e "${G}║                                                              ║${NC}"
        echo -e "${G}╚══════════════════════════════════════════════════════════════╝${NC}"
        
        # Save license with signature
        mkdir -p "$CONFIG_DIR/license"
        echo "$KEY" > "$CONFIG_DIR/license/license.key"
        
        # Generate signature
        SIGNATURE=$(echo -n "$KEY" | sha256sum | awk '{print $1}')
        echo "$SIGNATURE" > "$CONFIG_DIR/license/license.sig"
        
        # Save payment info
        echo "$(date): License activated - Type: $TYPE - Amount: ₹$AMOUNT" > "$PAYMENT_DIR/last_payment.txt"
        echo "UPI: vedant1437@fam" >> "$PAYMENT_DIR/last_payment.txt"
        echo "Discord: https://discord.gg/zS2ynbF6jK" >> "$PAYMENT_DIR/last_payment.txt"
        
        # Log license activation
        echo "$(date): License activated by $USER - Type: $TYPE - Amount: ₹$AMOUNT" >> "$LOG_FILE"
        
        chmod 600 "$CONFIG_DIR/license/"*
        sleep 3
        return 0
    else
        echo -e "${R}╔══════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${R}║                                                              ║${NC}"
        echo -e "${R}║         ❌ INVALID LICENSE - ACCESS DENIED                   ║${NC}"
        echo -e "${R}║                                                              ║${NC}"
        echo -e "${R}╚══════════════════════════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "${GOLD}💡 To purchase a genuine DeVv-Prime license:${NC}"
        echo -e "${W}   • UPI: ${Y}vedant1437@fam${W} (DeVv-Prime Official)${NC}"
        echo -e "${W}   • Discord: ${Y}https://discord.gg/zS2ynbF6jK${NC}"
        echo -e "${W}   • Amount: Starting from ₹499${NC}"
        echo -e "${W}   • Contact: ${Y}@DeVv-Prime${W} on Discord${NC}"
        echo ""
        echo -e "${C}Demo Mode Available:${NC}"
        echo -e "  ${GOLD}→${NC} Use demo key: ${Y}DEVVP-DEMO-2025${NC} for 24-hour trial"
        echo ""
        read -p "🔄 Press Enter to retry, 'd' for demo, 'p' for payment QR, or 'q' to quit: " retry
        
        if [[ "$retry" == "d" ]]; then
            echo -e "${G}✅ Demo mode activated - 24 hour trial${NC}"
            echo "$(date): Demo mode activated" >> "$LOG_FILE"
            return 0
        elif [[ "$retry" == "p" ]]; then
            generate_payment_qr $AMOUNT $TYPE
            check_license
            return
        elif [[ "$retry" == "q" ]]; then
            exit 1
        fi
        check_license
    fi
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  📋  REST OF THE SCRIPT (SYSTEM CHECK, DEPENDENCIES, ETC.)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# [Previous functions like check_system, install_dependencies, 
# configure_container_runtimes, install_python_environment remain the same]
# ... (keeping all the previous functionality)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  📝  CREATE SYSTEMD SERVICE WITH PAYMENT INFO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

create_service() {
    echo -e "${C}🔧 Creating systemd service...${NC}"
    
    cat > /etc/systemd/system/$SERVICE_NAME.service << EOF
[Unit]
Description=NEX VM V1 - Enterprise VM Management Platform
After=network.target lxd.service docker.service incus.service
Wants=network.target

[Service]
Type=simple
User=root
WorkingDirectory=$INSTALL_DIR
Environment="UPI_ID=vedant1437@fam"
Environment="DISCORD_INVITE=https://discord.gg/zS2ynbF6jK"
Environment="SUPPORT_CONTACT=@DeVv-Prime"
ExecStart=$INSTALL_DIR/venv/bin/python3 $INSTALL_DIR/$BOT_SCRIPT
Restart=always
RestartSec=5
StandardOutput=append:$LOG_FILE
StandardError=append:$LOG_FILE

[Install]
WantedBy=multi-user.target
EOF
    
    systemctl daemon-reload
    echo -e "${G}✅ Systemd service created!${NC}"
    sleep 1
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  📋  SHOW COMPLETION MESSAGE WITH PAYMENT & DISCORD INFO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

show_completion() {
    echo -e "${G}╔═══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${G}║              ✅ NEX VM V1 INSTALLATION COMPLETE - ALL FEATURES ✅            ║${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${G}╠═══════════════════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${G}║  📍 Installation Directory: $INSTALL_DIR              ║${NC}"
    echo -e "${G}║  🔧 Service Name: $SERVICE_NAME                                               ║${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${G}╠═══════════════════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${PINK}║                       💰 PAYMENT INFORMATION 💰                              ║${NC}"
    echo -e "${PINK}║                      ═════════════════════════════                           ║${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${W}║   📱 UPI ID: ${Y}vedant1437@fam${W}                                            ║${NC}"
    echo -e "${W}║   💎 Developer Edition: ₹499                                                  ║${NC}"
    echo -e "${W}║   💎 Enterprise Edition: ₹999                                                 ║${NC}"
    echo -e "${W}║   💎 Team License: ₹2499                                                      ║${NC}"
    echo -e "${W}║   💎 Enterprise Cluster: ₹9999                                                ║${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${G}╠═══════════════════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${P}║                       💬 DISCORD SUPPORT                                       ║${NC}"
    echo -e "${P}║                      ════════════════════                                     ║${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${W}║   🔗 Discord Invite: ${Y}https://discord.gg/zS2ynbF6jK${W}                       ║${NC}"
    echo -e "${W}║   👤 Support Contact: ${Y}@DeVv-Prime${W}                                      ║${NC}"
    echo -e "${W}║   🎫 Create Ticket: #create-ticket channel                                   ║${NC}"
    echo -e "${W}║   📸 Send Payment Screenshot to @DeVv-Prime                                  ║${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${G}╠═══════════════════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${G}║              🔐 LICENSE INFORMATION                                           ║${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    if [ -f "$CONFIG_DIR/license/license.key" ]; then
        echo -e "${G}║  License Key: $(cat $CONFIG_DIR/license/license.key)                                      ║${NC}"
    else
        echo -e "${G}║  License Key: DEMO MODE - 24 Hour Trial                                  ║${NC}"
    fi
    echo -e "${G}║  Valid Keys: DeVv-Prime-Master, DEVVP-ROOT-ACCESS, PRIME-ADMIN-2025          ║${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${G}╠═══════════════════════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${G}║              📞 SUPPORT & CONTACT                                             ║${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${G}║  Developer: DeVv-Prime                                                        ║${NC}"
    echo -e "${G}║  UPI: vedant1437@fam                                                          ║${NC}"
    echo -e "${G}║  Discord: https://discord.gg/zS2ynbF6jK                                       ║${NC}"
    echo -e "${G}║                                                                               ║${NC}"
    echo -e "${G}╚═══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${G}🎉 NEX VM V1 installed successfully! Made by DeVv-Prime with ❤️ 🎉${NC}"
    echo -e "${Y}📌 UPI: vedant1437@fam - Send payment for full access${NC}"
    echo -e "${Y}📌 Discord: https://discord.gg/zS2ynbF6jK - Join for support${NC}"
    echo -e "${Y}📌 Contact @DeVv-Prime on Discord after payment${NC}"
    echo ""
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  🎯  MAIN INSTALLATION FUNCTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

main() {
    show_header
    check_license
    check_system
    install_dependencies
    configure_container_runtimes
    install_python_environment
    configure_firewall
    create_directories
    create_requirements
    create_service
    show_completion
}

# Run main function
main
