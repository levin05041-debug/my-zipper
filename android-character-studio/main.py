from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from pathlib import Path

class Studio(App):
    def build(self):
        self.title = "סטודיו לאנימציית דמות"
        self.frames = sorted(Path("assets/walk").glob("*.png"))
        self.index = 0
        self.event = None
        root = BoxLayout(orientation="vertical", padding=12, spacing=8)
        root.add_widget(Label(text="סטודיו לאנימציית דמות", font_size="24sp", size_hint_y=None, height=55))
        self.preview = Image(source=str(self.frames[0]) if self.frames else "", fit_mode="contain")
        root.add_widget(self.preview)
        row = BoxLayout(size_hint_y=None, height=54, spacing=5)
        for action in ["הליכה", "ריצה", "קפיצה", "אגרוף", "בעיטה", "כריעה"]:
            row.add_widget(Button(text=action, on_release=lambda b, a=action: self.select(a)))
        root.add_widget(row)
        controls = BoxLayout(size_hint_y=None, height=54, spacing=8)
        controls.add_widget(Button(text="▶ הפעלה", on_release=self.play))
        controls.add_widget(Button(text="עצירה", on_release=self.stop))
        root.add_widget(controls)
        self.status = Label(text="מוכן")
        root.add_widget(self.status)
        return root

    def select(self, action):
        self.stop()
        self.status.text = f"נבחרה פעולה: {action}"
        if action != "הליכה":
            self.status.text += " (יש להוסיף פריימים לפעולה זו)"

    def play(self, *_):
        if not self.frames:
            self.status.text = "לא נמצאו תמונות בתיקייה assets/walk"
            return
        if self.event is None:
            self.event = Clock.schedule_interval(self.tick, 0.12)
            self.status.text = "ההליכה פועלת"

    def tick(self, _dt):
        self.index = (self.index + 1) % len(self.frames)
        self.preview.source = str(self.frames[self.index])
        self.preview.reload()

    def stop(self, *_):
        if self.event:
            self.event.cancel()
            self.event = None
        self.status.text = "נעצר"

if __name__ == "__main__":
    Studio().run()
