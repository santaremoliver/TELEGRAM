import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import anthropic

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Cliente da IA
client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '🤖 Olá! Sou um bot com IA.\n\n'
        'Pode me perguntar qualquer coisa!\n'
        'Apenas envie sua mensagem e eu respondo. 💬'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_name = update.effective_user.first_name
    
    logger.info(f"Mensagem de {user_name}: {user_message}")
    
    try:
        # Chamar a IA
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[
                {
                    "role": "user", 
                    "content": f"Responda de forma direta, concisa e amigável: {user_message}"
                }
            ]
        )
        
        # Enviar resposta
        response = message.content[0].text
        await update.message.reply_text(response)
        
        logger.info(f"Resposta enviada para {user_name}")
        
    except Exception as e:
        logger.error(f'Erro: {e}')
        await update.message.reply_text(
            '😅 Desculpe, tive um problema ao processar sua mensagem. '
            'Tente novamente!'
        )

def main():
    token = os.getenv('BOT_TOKEN')
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    if not token:
        logger.error("❌ BOT_TOKEN não encontrado!")
        return
    
    if not api_key:
        logger.error("❌ ANTHROPIC_API_KEY não encontrada!")
        return
    
    logger.info("🤖 Iniciando bot com IA...")
    
    app = Application.builder().token(token).build()
    
    # Comando /start
    app.add_handler(CommandHandler("start", start))
    
    # TODAS as mensagens vão para a IA
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("✅ Bot online! Respondendo TUDO com IA.")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
