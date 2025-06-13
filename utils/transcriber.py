import whisper
import os
model = whisper.load_model("tiny")
def transcribe_audio(file_path):
    if not file_path or not os.path.exists(file_path):
        return None
    result = model.transcribe(file_path)
    return result['text']
