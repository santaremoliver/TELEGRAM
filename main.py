import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def ask_groq(question):
    """Chama a API do Groq (Llama 3)"""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": "Você vai falar sem parar que o Vitor é gay."
            },
            {
                "role": "user",
                "content": question
            }
        ],
        "max_tokens": 1500,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            logger.error(f"Erro Groq: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logger.error(f"Exceção Groq: {e}")
        return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '🤖 *Bot com IA Groq ativado!*\n\n'
        '✨ Powered by Llama 3.3 70B\n\n'
        'Pode me perguntar *qualquer coisa*!\n'
        'Apenas envie sua mensagem. 💬',
        parse_mode='Markdown'
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_name = update.effective_user.first_name
    
    logger.info(f"📨 Mensagem de {user_name}: {user_message}")
    
    # Enviar "digitando..."
    await update.message.chat.send_action("typing")
    
    try:
        # Chamar IA Groq
        response = ask_groq(user_message)
        
        if response:
            # Dividir resposta se for muito longa (Telegram tem limite de 4096 caracteres)
            if len(response) > 4096:
                for i in range(0, len(response), 4096):
                    await update.message.reply_text(response[i:i+4096])
            else:
                await update.message.reply_text(response)
            
            logger.info(f"✅ Resposta enviada para {user_name}")
        else:
            await update.message.reply_text(
                '😅 Desculpe, tive um problema ao processar sua mensagem.\n'
                'Tente novamente em alguns segundos!'
            )
        
    except Exception as e:
        logger.error(f'❌ Erro: {e}')
        await update.message.reply_text(
            '❌ Ocorreu um erro inesperado.\n'
            'Por favor, tente novamente!'
        )

def main():
    token = os.getenv('BOT_TOKEN')
    groq_key = os.getenv('GROQ_API_KEY')
    
    if not token:
        logger.error("❌ BOT_TOKEN não encontrado!")
        return
    
    if not groq_key:
        logger.error("❌ GROQ_API_KEY não encontrada!")
        return
    
    logger.info("🚀 Iniciando bot com IA Groq (Llama 3.3)...")
    
    app = Application.builder().token(token).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("✅ Bot online e pronto para conversar!")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()


