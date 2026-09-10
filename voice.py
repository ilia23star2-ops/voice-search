import platform

if platform.system() == 'Android':
    from jnius import autoclass, cast
    from android.permissions import request_permissions, Permission
    from android import activity

    class VoiceRecognizer:
        def __init__(self):
            self.model_path = 'N/A'
            self._callback = None

        def listen(self, on_result, on_error, timeout=10):
            self._callback = {'on_result': on_result, 'on_error': on_error}
            
            # Запрашиваем разрешение на микрофон
            request_permissions([Permission.RECORD_AUDIO])
            
            try:
                Intent = autoclass('android.content.Intent')
                RecognizerIntent = autoclass('android.speech.RecognizerIntent')
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                
                intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, 'ru-RU')
                intent.putExtra(RecognizerIntent.EXTRA_PREFER_OFFLINE, True) # <-- ОФФЛАЙН РЕЖИМ
                
                current_activity = cast('android.app.Activity', PythonActivity.mActivity)
                
                def on_activity_result(request_code, result_code, intent_data):
                    if request_code == 100:
                        if result_code == -1:  # RESULT_OK
                            results = intent_data.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)
                            if results and results.size() > 0:
                                self._callback['on_result'](results.get(0))
                            else:
                                self._callback['on_error']('Ничего не распознано')
                        else:
                            self._callback['on_error']('Распознавание отменено')
                        
                        # Отписываемся от события после первого срабатывания
                        activity.unbind(on_activity_result=on_activity_result)
                        
                activity.bind(on_activity_result=on_activity_result)
                current_activity.startActivityForResult(intent, 100)
                
            except Exception as e:
                self._callback['on_error'](f'Ошибка инициализации: {str(e)}')
else:
    # Заглушка для ПК (чтобы приложение не падало при тесте на компьютере)
    class VoiceRecognizer:
        def __init__(self):
            self.model_path = 'N/A'
            
        def listen(self, on_result, on_error, timeout=10):
            on_error("Голосовой ввод доступен только на Android. Используйте поле ручного ввода на ПК.")
