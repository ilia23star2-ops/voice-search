import os
import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer

class VoiceRecognizer:
    def __init__(self, model_path='vosk-model-small-ru-0.22'):
        self.model_path = model_path
        self.model = None
        self.q = queue.Queue()
        self.load_model()
    
    def load_model(self):
        """Загрузка модели Vosk"""
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Модель не найдена: {self.model_path}\n"
                f"Скачайте с https://alphacephei.com/vosk/models"
            )
        
        self.model = Model(self.model_path)
    
    def callback(self, indata, frames, time, status):
        """Коллбэк для записи аудио"""
        if status:
            print(status)
        self.q.put(bytes(indata))
    
    def listen(self, on_result, on_error, timeout=10):
        """Слушать микрофон и распознать речь"""
        try:
            rec = KaldiRecognizer(self.model, 16000)
            
            with sd.RawInputStream(
                samplerate=16000,
                blocksize=8000,
                dtype='int16',
                channels=1,
                callback=self.callback
            ):
                # Слушаем до таймаута или пустого результата
                import time
                start_time = time.time()
                
                while time.time() - start_time < timeout:
                    data = self.q.get()
                    if rec.AcceptWaveform(data):
                        result = json.loads(rec.Result())
                        text = result.get('text', '').strip()
                        if text:
                            on_result(text)
                            return
                
                # Финальный результат
                final = json.loads(rec.FinalResult())
                text = final.get('text', '').strip()
                if text:
                    on_result(text)
                else:
                    on_error('Ничего не распознано')
        
        except Exception as e:
            on_error(str(e))