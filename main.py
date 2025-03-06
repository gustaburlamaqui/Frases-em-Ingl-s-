import os
import openai
from gtts import gTTS
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler

# Configuração da API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Token do Bot do Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Função para responder mensagens do usuário
async def responder(update: Update, context):
    mensagem_usuario = update.message.text

    # Enviar a mensagem para o ChatGPT
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um assistente útil."},
            {"role": "user", "content": mensagem_usuario},
        ]
    )

    texto_resposta = resposta["choices"][0]["message"]["content"]

    # Converter texto para áudio
    tts = gTTS(texto_resposta, lang="pt")
    audio_path = "resposta.mp3"
    tts.save(audio_path)

    # Enviar áudio no Telegram
    await update.message.reply_voice(voice=open(audio_path, "rb"))

# Função para comando de start
async def start(update: Update, context):
    await update.message.reply_text("Olá! Envie uma mensagem e eu responderei com áudio!")

# Configuração do Bot no Telegram
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Adicionar handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    # Iniciar o bot
    app.run_polling()

# Iniciar a aplicação
if __name__ == "__main__":
    main()
