from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from database import Database
from voice import VoiceRecognizer

class VoiceSearchApp(App):
    def build(self):
        self.db = Database()
        self.voice = VoiceRecognizer()
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Кнопка голосового поиска
        self.btn_speak = Button(
            text='🎤 ГОВОРИ',
            size_hint=(1, 0.3),
            font_size='32sp'
        )
        self.btn_speak.bind(on_press=self.start_listening)
        layout.add_widget(self.btn_speak)
        
        # Поле результата
        self.lbl_result = Label(
            text='Нажми кнопку и скажи номер пробы',
            size_hint=(1, 0.4),
            font_size='24sp',
            halign='center'
        )
        layout.add_widget(self.lbl_result)
        
        # Поле ручного ввода
        self.txt_manual = TextInput(
            hint_text='Или введи номер вручную (например: ABC123)',
            size_hint=(1, 0.15),
            font_size='20sp',
            multiline=False
        )
        self.txt_manual.bind(on_text_validate=self.manual_search)
        layout.add_widget(self.txt_manual)
        
        # Кнопка ручного поиска
        self.btn_search = Button(
            text='🔍 НАЙТИ',
            size_hint=(1, 0.15),
            font_size='24sp'
        )
        self.btn_search.bind(on_press=self.manual_search)
        layout.add_widget(self.btn_search)
        
        return layout
    
    def start_listening(self, instance):
        self.lbl_result.text = 'Слушаю...'
        self.btn_speak.disabled = True
        
        def on_result(text):
            self.lbl_result.text = f'Распознано: {text}'
            self.search_probe(text)
            self.btn_speak.disabled = False
        
        def on_error(error):
            self.lbl_result.text = f'Ошибка: {error}'
            self.btn_speak.disabled = False
        
        self.voice.listen(on_result, on_error)
    
    def manual_search(self, instance):
        text = self.txt_manual.text.strip()
        if text:
            self.search_probe(text)
    
    def search_probe(self, text):
        # Нормализация: убираем пробелы, приводим к верхнему регистру
        normalized = text.replace(' ', '').upper()
        
        # Поиск в БД
        result = self.db.find_work_order(normalized)
        
        if result:
            self.lbl_result.text = f'Проба: {normalized}\nНаряд: {result}'
        else:
            self.lbl_result.text = f'Проба {normalized} не найдена'

if __name__ == '__main__':
    VoiceSearchApp().run()