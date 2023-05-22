#!/usr/bin/env python

import logging
import socket

from telegram import __version__ as TG_VER


# Vérifie la version de telegram et du bot
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )   
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, filters

# Constants
TOKEN = ""
UDP_QUERY_IP_ADDRESS = "192.168.1.142"
UDP_PKT_ADDRESS = "127.0.0.1"
TCP_QUERY_IP_ADDRESS = "192.168.1.142"
HTTP_HOST = ""
ALLOWED_USERS = [500763651]   # Liste des utilisateurs autorisés

# Permet de log le bot
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Menus
#
# Menu de démarrage
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Affiche les boutons principaux"""
    user = update.message.from_user
    logger.info("Utilisateur %s a commencé une conversation.", user.full_name)
    keyboard = [
        [
            InlineKeyboardButton("Afficher les logs", callback_data="logs"),
            InlineKeyboardButton("Afficher les status des appareils", callback_data="status"),
        ],
        [
            InlineKeyboardButton("Controles des appareil", callback_data="control")
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Bienvenue sur le Bot Telegram de gestion du musee battelle.", reply_markup=reply_markup)

async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Menu de démarrage après retour au menu principal"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Afficher les logs", callback_data="logs"),
            InlineKeyboardButton("Afficher les status des appareils", callback_data="status")
        ],
        [
            InlineKeyboardButton("Controles des appareil", callback_data="control")
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Bienvenue sur le Bot Telegram de gestion du musee battelle.", reply_markup=reply_markup)


# Buttons
#
# Logs MQTT
async def logs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envoie une query TCP afin de récuperer les 5 dernière lignes du fichier log."""
    query = update.callback_query
    await query.answer()
    logs = await ask_logs("query_logs")
    await query.edit_message_text(text=logs)
    
# Status des appareils
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envoie une query UDP afin de récuperer les 5 dernière lignes du fichier log."""
    query = update.callback_query
    await query.answer()
    status = await ask_status("query_status")
    await query.edit_message_text(text=status)
    
# Controles des appareils
async def controls_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Affche un menu avec les différents appareils à contrôler."""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Allumer/Eteindre la lumière", callback_data="light"),
            InlineKeyboardButton("Allumer/Eteindre l'alarme", callback_data="alarm"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=f"Contrôle des appareils:", reply_markup=reply_markup)
# Controles musee
async def toggle_light(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Active ou désactive la lumière."""
    query = update.callback_query
    await query.answer()
    retour = await udp_controls("toggle_light")
    await query.edit_message_text(text=f"Selected option: {retour}")
    
# Controles alarme    
async def toggle_alarm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Active ou désactive l'alarme."""
    query = update.callback_query
    await query.answer()
    retour = await udp_controls("toggle_alarm")
    await query.edit_message_text(text=f"Selected option: {retour}")
    
# Fonctions
#
# Demande le status des appareils en UDP (Serveur UDP status)
async def ask_status(query) -> str:
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.connect((UDP_QUERY_IP_ADDRESS, 12345))
    UDPClientSocket.sendall(query.encode("UTF-8"))
    msg, coordServer = UDPClientSocket.recvfrom(1024)
    UDPClientSocket.close()
    return msg.decode("UTF-8")
# Envoie une commande en UDP à pkt en local (localhost:12345)
async def udp_controls(query) -> str:
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPClientSocket.connect((UDP_PKT_ADDRESS, 12345))
    UDPClientSocket.sendto(query.encode("UTF-8"), (UDP_PKT_ADDRESS, 12345))
    msg, coordServer = UDPClientSocket.recvfrom(1024)
    UDPClientSocket.close()
    return msg.decode("UTF-8")
# Demande les logs en TCP (Serveur TCP logs)
async def ask_logs(query) -> str:
    TCPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPClientSocket.connect((TCP_QUERY_IP_ADDRESS, 65432))
    TCPClientSocket.sendall(query.encode("UTF-8"))
    msg, coordServer = TCPClientSocket.recvfrom(1024)
    TCPClientSocket.close()
    return msg.decode("UTF-8")


def main() -> None:
    """Fonctionnement du bot la commande start n'est accessible que si l'ID de l'utilisatuer est dans la liste ALLOWED_USERS."""
    # Crée une application et ajoute les handlers
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start, filters.User(ALLOWED_USERS)))
    application.add_handler(CallbackQueryHandler(logs, pattern="^logs$"))
    application.add_handler(CallbackQueryHandler(controls_menu, pattern="^control$"))
    application.add_handler(CallbackQueryHandler(status, pattern="^status$"))
    application.add_handler(CallbackQueryHandler(toggle_light, pattern="^light$"))
    application.add_handler(CallbackQueryHandler(toggle_alarm, pattern="^alarm$"))
    application.add_handler(CallbackQueryHandler(start_over, pattern="^retour$"))

    # Presser ctrl+C pour arrêter le bot
    application.run_polling()


if __name__ == "__main__":
    main()