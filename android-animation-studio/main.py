from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.metrics import dp

class Animator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=dp(10), spacing=dp(8), **kwargs)
        self.frames=[]; self.index=0; self.playing=False; self.event=None; self.fps=8
        self.status=Label(text="טען תמונות של הדמות כדי להתחיל", size_hint_y=None, height=dp(36))
        self.add_widget(self.status)
        self.preview=Image(allow_stretch=True, keep_ratio=True); self.add_widget(self.preview)
        row=BoxLayout(size_hint_y=None,height=dp(48),spacing=dp(6))
        for label,fn in [("טען פריימים",self.pick),("הקודם",self.prev),("נגן / עצור",self.toggle),("הבא",self.next)]:
            row.add_widget(Button(text=label,on_release=lambda _,f=fn:f()))
        self.add_widget(row)
        self.add_widget(Label(text="מהירות האנימציה",size_hint_y=None,height=dp(24)))
        self.speed=Slider(min=2,max=24,value=8,step=1,size_hint_y=None,height=dp(36))
        self.speed.bind(value=self.set_speed); self.add_widget(self.speed)
        actions=GridLayout(cols=3,size_hint_y=None,height=dp(104),spacing=dp(5))
        for name in ["הליכה","ריצה","קפיצה","אגרוף","בעיטה","כריעה"]:
            actions.add_widget(Button(text=name,on_release=lambda _,n=name:self.choose_action(n)))
        self.add_widget(actions)
    def pick(self):
        chooser=FileChooserListView(path="/storage/emulated/0/Download", filters=["*.png","*.jpg","*.jpeg"], multiselect=True)
        box=BoxLayout(orientation="vertical"); box.add_widget(chooser)
        buttons=BoxLayout(size_hint_y=None,height=dp(48)); pop=Popup(title="בחר תמונות",content=box,size_hint=(.95,.9))
        def load(*_):
            paths=sorted(chooser.selection)
            if paths: self.load_paths(paths)
            pop.dismiss()
        buttons.add_widget(Button(text="טען",on_release=load)); buttons.add_widget(Button(text="ביטול",on_release=pop.dismiss))
        box.add_widget(buttons); pop.open()
    def load_paths(self,paths):
        self.stop(); self.frames=[p for p in paths if p.lower().endswith((".png",".jpg",".jpeg"))]; self.index=0; self.show()
    def show(self):
        if self.frames:
            self.preview.source=self.frames[self.index]; self.preview.reload()
            self.status.text=f"פריים {self.index+1} מתוך {len(self.frames)}"
    def next(self):
        if self.frames: self.index=(self.index+1)%len(self.frames); self.show()
    def prev(self):
        if self.frames: self.index=(self.index-1)%len(self.frames); self.show()
    def tick(self,dt): self.next()
    def toggle(self):
        if not self.frames: self.status.text="קודם טען תמונות"; return
        if self.playing: self.stop()
        else: self.playing=True; self.event=Clock.schedule_interval(self.tick,1.0/self.fps)
    def stop(self):
        self.playing=False
        if self.event: self.event.cancel(); self.event=None
    def set_speed(self,_,v):
        self.fps=int(v)
        if self.playing: self.stop(); self.toggle()
    def choose_action(self,name):
        self.stop(); self.status.text=f"מצב: {name} — טען את פריימי התנועה הזו כדי לנגן אותה"

class CharacterAnimationApp(App):
    def build(self):
        self.title="סטודיו אנימציה לדמות"; return Animator()

if __name__=="__main__": CharacterAnimationApp().run()
