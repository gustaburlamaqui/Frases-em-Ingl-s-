import openai
from gtts import gTTS
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler
from telegram.ext.filters import TEXT
import os

# Configuração da OpenAI (substitua pela sua API Key)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Token do Bot do Telegram (substitua pelo seu Token do BotFather)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def responder(update: Update, context: CallbackContext) -> None:
    mensagem_usuario = update.message.text

    # Enviar a mensagem para o ChatGPT
    resposta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Você é um professor de inglês e responde apenas em inglês."},
            {"role": "user", "content": mensagem_usuario}
        ]
    )

    texto_resposta = resposta["choices"][0]["message"]["content"]

    # Converter texto para áudio com gTTS
    tts = gTTS(texto_resposta, lang="en")
    audio_path = "resposta.mp3"
    tts.save(audio_path)

    # Enviar áudio no Telegram
    update.message.reply_voice(voice=open(audio_path, "rb"))

# Configuração do Telegram
app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
dispatcher = updater.dispatcher

dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, responder))

updater.start_polling()
