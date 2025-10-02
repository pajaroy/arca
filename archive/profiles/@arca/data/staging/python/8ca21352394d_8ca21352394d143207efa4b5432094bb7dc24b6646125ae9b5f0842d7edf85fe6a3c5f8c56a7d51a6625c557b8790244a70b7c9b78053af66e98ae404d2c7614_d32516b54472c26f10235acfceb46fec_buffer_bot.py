import os
import logging
import datetime
import tempfile
import subprocess
from typing import List, Dict
from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)
import whisper

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[logging.FileHandler("buffer_bot.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class IdeaBuffer:
    def __init__(self):
        self.buffer: List[Dict[str, str]] = []
        self.last_summary_date = datetime.date.today()
        
    def add_idea(self, transcription: str):
        entry = {
            "hora": datetime.datetime.now().strftime("%H:%M"),
            "texto": transcription
        }
        self.buffer.append(entry)
        logger.info(f"Idea añadida: {entry}")
        
    def get_buffer_content(self) -> str:
        return "\n".join([f"{item['hora']} - {item['texto']}" for item in self.buffer])
    
    def clear_buffer(self):
        self.buffer.clear()
        self.last_summary_date = datetime.date.today()
        logger.info("Buffer limpiado")

model = whisper.load_model("base")
buffer = IdeaBuffer()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🧠 ALMA LIBRE v0.2\nEnvía un audio o usa /resumen para generar un resumen de tus ideas."
    )

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_id, file_ext = await get_file_id(update)
            if not file_id:
                return
            input_path = await download_file(update, file_id, file_ext, tmp_dir)
            wav_path = await convert_to_wav(input_path, tmp_dir)
            transcription = transcribe_audio(wav_path)
            buffer.add_idea(transcription)
            await update.message.reply_text(
                f"💡 Idea registrada ({datetime.datetime.now().strftime('%H:%M')})",
                reply_to_message_id=update.message.message_id
            )
    except Exception as e:
        logger.error(f"Error en handle_audio: {str(e)}")
        await update.message.reply_text("❌ Error procesando el audio")

async def generate_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not buffer.buffer:
        await update.message.reply_text("📭 No hay ideas aún para resumir.")
        return
    try:
        summary_text = extraer_ideas_local(buffer.get_buffer_content())
        await update.message.reply_text(
            f"📝 Resumen del día:\n\n{summary_text}",
            reply_to_message_id=update.message.message_id
        )
    except Exception as e:
        logger.error(f"Error generando resumen: {str(e)}")
        await update.message.reply_text("❌ Error generando el resumen")

async def daily_summary(context: ContextTypes.DEFAULT_TYPE):
    if buffer.buffer:
        try:
            summary_text = extraer_ideas_local(buffer.get_buffer_content())
            save_daily_summary(summary_text)
            await context.bot.send_message(
                chat_id=context.job.chat_id,
                text=f"⏰ Resumen diario guardado:\n\n{summary_text}"
            )
            buffer.clear_buffer()
        except Exception as e:
            logger.error(f"Error en resumen diario: {str(e)}")

def extraer_ideas_local(texto: str) -> str:
    return f"Resumen mock de {len(texto.split())} palabras generado a las {datetime.datetime.now().strftime('%H:%M')}"

def save_daily_summary(content: str):
    os.makedirs("resumenes_diarios", exist_ok=True)
    filename = f"resumenes_diarios/{datetime.date.today()}.md"
    with open(filename, "w") as f:
        f.write(f"# Resumen {datetime.date.today()}\n\n{content}")
    logger.info(f"Resumen guardado en {filename}")

async def get_file_id(update: Update):
    if update.message.voice:
        return update.message.voice.file_id, "ogg"
    elif update.message.audio:
        return update.message.audio.file_id, update.message.audio.file_name.split('.')[-1]
    return None, None

async def download_file(update: Update, file_id: str, file_ext: str, tmp_dir: str):
    file = await update.message.effective_attachment.get_file()
    input_path = os.path.join(tmp_dir, f"audio_{file_id}.{file_ext}")
    await file.download_to_drive(input_path)
    return input_path

async def convert_to_wav(input_path: str, tmp_dir: str):
    wav_path = os.path.join(tmp_dir, "audio.wav")
    subprocess.run(['ffmpeg', '-i', input_path, '-ar', '16000', '-ac', '1', '-y', wav_path], check=True)
    return wav_path

def transcribe_audio(wav_path: str):
    return model.transcribe(wav_path, fp16=False)["text"]

def main():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("Variable de entorno TELEGRAM_TOKEN no definida")
        
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("resumen", generate_summary))
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_audio))
    
    job_queue = app.job_queue
    job_queue.run_daily(
        daily_summary,
        time=datetime.time(23, 50, 0),
        chat_id=os.getenv("CHAT_ID")
    )

    logger.info("Iniciando buffer_bot...")
    app.run_polling()

if __name__ == "__main__":
    main()
