import os
import openai
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Configuração do OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configuração do Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Configuração de logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Função de resposta do bot
async def responder(update: Update, context: CallbackContext) -> None:
    mensagem_usuario = update.message.text

    try:
        # Envia a mensagem para a OpenAI
        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Você é um assistente de IA útil."},
                {"role": "user", "content": mensagem_usuario}
            ]
        )

        texto_resposta = resposta["choices"][0]["message"]["content"]
        await update.message.reply_text(texto_resposta)

    except Exception as e:
        logging.error(f"Erro ao processar mensagem: {e}")
        await update.message.reply_text("Ocorreu um erro ao processar sua solicitação.")

# Inicializar o bot
def
