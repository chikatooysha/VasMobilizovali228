import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button

class GameCharacter(Widget):
    def __init__(self, texture_source, size, **kwargs):
        super().__init__(**kwargs)
        self.size = size
        self.texture_source = texture_source
        with self.canvas:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(source=self.texture_source, pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class MobileGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.score = 0
        self.game_over = False
        self.is_victory = False
        
        self.enemy_min_speed = 6
        self.enemy_max_speed = 12
        self.doc_min_speed = 4
        self.doc_max_speed = 8

        # Слой заднего фона
        with self.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = Rectangle(source='bg.jpg', pos=self.pos, size=Window.size)
        self.bind(size=self.update_bg, pos=self.update_bg)
        
        # Игрок
        self.player = GameCharacter(texture_source='player.png', size=(120, 120))
        self.add_widget(self.player)
        
        self.enemies = []
        self.documents = []
        
        # Счетчик очков
        self.score_label = Label(
            text=f"Score: {self.score}", 
            font_size='24sp',
            size_hint=(None, None),
            size=(Window.width, 100),
            halign='center',
            valign='middle'
        )
        self.add_widget(self.score_label)
        
        # Слой рисования графических рамок
        with self.canvas.after:
            self.frame_color = Color(1, 1, 1, 1) # Белый цвет для рамки очков
            self.score_frame = Line(rect=(0, 0, 1, 1), width=2)
            
            self.alert_color = Color(0, 0, 0, 0) # Прозрачный цвет (появится при проигрыше/победе)
            self.end_frame = Line(rect=(0, 0, 1, 1), width=4)
            
        Clock.schedule_once(self.init_game, 0.2)

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        # Обновляем рамку счета при изменении размеров экрана
        if hasattr(self, 'w_height'):
            self.update_score_frame()

    def update_score_frame(self):
        # Рисуем рамку вокруг текста очков с небольшим отступом
        frame_width = 500
        frame_height = 80
        frame_x = self.w_width / 2 - frame_width / 2
        frame_y = self.w_height - 110
        self.score_frame.rect = (frame_x, frame_y, frame_width, frame_height)

    def init_game(self, dt):
        self.w_width = Window.width if Window.width > 100 else 800
        self.w_height = Window.height if Window.height > 100 else 1200
        
        self.player.pos = (self.w_width / 2 - 60, 150)
        
        self.score_label.size = (self.w_width, 100)
        self.score_label.pos = (0, self.w_height - 120)
        self.score_label.text = f"Povestok sozhzheno: {self.score}"
        
        # Активируем рамку для повесток
        self.update_score_frame()
        
        # Спавн ТЦК
        for _ in range(5):
            enemy = GameCharacter(texture_source='enemy.png', size=(100, 100))
            self.reset_object(enemy, "enemy")
            self.enemies.append(enemy)
            self.add_widget(enemy)
            
        # Спавн повесток
        for _ in range(3):
            doc = GameCharacter(texture_source='doc.png', size=(70, 90))
            self.reset_object(doc, "doc")
            self.documents.append(doc)
            self.add_widget(doc)

        Clock.schedule_interval(self.update, 1.0 / 60.0)

    def reset_object(self, obj, obj_type):
        width_limit = max(10, int(self.w_width - obj.width))
        obj.x = random.randint(0, width_limit)
        obj.y = random.randint(int(self.w_height), int(self.w_height + 400))
        
        if obj_type == "enemy":
            obj.speed = random.randint(self.enemy_min_speed, self.enemy_max_speed)
        else:
            obj.speed = random.randint(self.doc_min_speed, self.doc_max_speed)

    def on_touch_move(self, touch):
        if not self.game_over and not self.is_victory:
            self.player.center_x = touch.x
            self.player.center_y = touch.y + 70

    def check_collision(self, w1, w2):
        padding = 15
        return (w1.x < w2.x + w2.width - padding and
                w1.x + w1.width > w2.x + padding and
                w1.y < w2.y + w2.height - padding and
                w1.y + w1.height > w2.y + padding)

    def update(self, dt):
        if self.game_over or self.is_victory:
            return

        for enemy in self.enemies:
            enemy.y -= enemy.speed
            if enemy.y < -enemy.height:
                self.reset_object(enemy, "enemy")
            
            if self.check_collision(self.player, enemy):
                self.trigger_game_over()

        for doc in self.documents:
            doc.y -= doc.speed
            if doc.y < -doc.height:
                self.reset_object(doc, "doc")
                
            if self.check_collision(self.player, doc):
                self.score += 1
                self.score_label.text = f"Povestok sozhzheno: {self.score}"
                
                if self.score >= 1488:
                    self.trigger_victory()
                    return
                
                if self.score % 10 == 0:
                    self.enemy_min_speed += 2
                    self.enemy_max_speed += 2
                    self.doc_min_speed += 1
                    self.doc_max_speed += 1
                
                self.reset_object(doc, "doc")

    def trigger_game_over(self):
        self.game_over = True
        # Делаем рамку красной и позиционируем её вокруг текста проигрыша
        self.alert_color.rgba = (1, 0, 0, 1)
        self.setup_end_frame()
        self.show_end_screen("VAS MOBILIZOVALI!", (1, 0, 0, 1), "Try Again")

    def trigger_victory(self):
        self.is_victory = True
        # Делаем рамку зеленой и позиционируем её вокруг текста победы
        self.alert_color.rgba = (0, 1, 0, 1)
        self.setup_end_frame()
        self.show_end_screen("NEPRIZYVNOY VOZRAST!", (0, 1, 0, 1), "Play Again")

    def setup_end_frame(self):
        # Размеры рамки для финального уведомления
        f_width = 650
        f_height = 140
        f_x = self.w_width / 2 - f_width / 2
        f_y = self.w_height / 2 + 40
        self.end_frame.rect = (f_x, f_y, f_width, f_height)

    def show_end_screen(self, title_text, text_color, btn_text):
        self.end_label = Label(
            text=title_text, 
            font_size='30sp', 
            center=(self.w_width/2, self.w_height/2 + 100),
            color=text_color
        )
        
        self.restart_btn = Button(
            text=btn_text, 
            size_hint=(None, None), 
            size=(400, 120),
            center=(self.w_width/2, self.w_height/2 - 100)
        )
        self.restart_btn.bind(on_press=self.restart_game)
        
        self.add_widget(self.end_label)
        self.add_widget(self.restart_btn)

    def restart_game(self, instance):
        self.remove_widget(self.end_label)
        self.remove_widget(self.restart_btn)
        
        # Скрываем финальную рамку (делаем прозрачной)
        self.alert_color.rgba = (0, 0, 0, 0)
        
        self.score = 0
        self.enemy_min_speed = 6
        self.enemy_max_speed = 12
        self.doc_min_speed = 4
        self.doc_max_speed = 8
        
        self.score_label.text = f"Povestok sozhzheno: {self.score}"
        self.player.pos = (self.w_width / 2 - 60, 150)
        
        for enemy in self.enemies:
            self.reset_object(enemy, "enemy")
        for doc in self.documents:
            self.reset_object(doc, "doc")
            
        self.game_over = False
        self.is_victory = False

class TckEscapeApp(App):
    def build(self):
        return MobileGame()

if __name__ == '__main__':
    TckEscapeApp().run()
