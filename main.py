import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configurar logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('✅ Bot online e funcionando!')

# Comando /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '📋 Comandos disponíveis:\n'
        '/start - Iniciar bot\n'
        '/help - Ver comandos'
    )

# Função principal
def main():
    # Pegar token da variável de ambiente
    token = os.getenv('BOT_TOKEN')
    
    if not token:
        print("❌ ERRO: BOT_TOKEN não configurado!")
        return
    
    # Criar aplicação
    app = Application.builder().token(token).build()
    
    # Adicionar comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    
    # Iniciar bot
    print("🤖 Bot iniciando...")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
