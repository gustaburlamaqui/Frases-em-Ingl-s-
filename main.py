import os
import openai
import logging
from gtts import gTTS
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Configuração de logs
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Obtendo as chaves de API do ambiente
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Configuração da OpenAI
openai.api_key = OPENAI_API_KEY

# Função para responder mensagens
async def responder(update: Update, context: CallbackContext):
    mensagem_usuario = update.message.text

    try:
        # Enviar a mensagem para a OpenAI
        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": mensagem_usuario}]
        )

        texto_resposta = resposta["choices"][0]["message"]["content"]

        # Converter texto para áudio
        tts = gTTS(texto_resposta, lang="pt")
        audio_path = "resposta.mp3"
        tts.save(audio_path)

        # Enviar resposta de texto
        await update.message.reply_text(texto_resposta)

        # Enviar áudio no Telegram
        with open(audio_path, "rb") as audio:
            await update.message.reply_voice(voice=audio)

    except Exception as e:
        logging.error(f"Erro: {e}")
        await update.message.reply_text("Ocorreu um erro ao processar sua solicitação.")

# Configuração do bot
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Adicionar handler para receber mensagens
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    # Iniciar o bot
    logging.info("Bot iniciado...")
    app.run_polling()

if __name__ == "__main__":
    main()
