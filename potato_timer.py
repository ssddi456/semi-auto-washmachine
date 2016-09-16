# -*- coding: utf-8 -*-  

from Tkinter import *
from threading import Thread
import tkMessageBox

from scrolable_frame import ScrollableFrame
from step import *
from utils import *

class counter_loop(object) :
    def __init__ (self, working, sleep ):
        self.working = step()
        self.working.process_time = float(working)
        self.sleep = step()
        self.sleep.process_time = float(sleep)

        self.__count = 0.0
        self.__working = True
        self.current_step = False

    def step(self):
        if self.current_step == False :
            self.current_step = self.working
        
        if self.current_step.is_finish() :
            self.current_step.reset()
            if self.__working :
                self.__working = False
                tkMessageBox.showinfo( '状态更新', '休息一下吧' )
                self.current_step = self.sleep
            else:
                self.__working = True
                tkMessageBox.showinfo( '状态更新', '继续干活儿吧' )
                self.current_step = self.working
        
        self.current_step.count_down()

            
    @property
    def status(self):
        return 'working' if self.__working else 'relax' 

    @status.setter
    def status(self, value):
        pass
    
    def set_view(self, widget):
        self.widget = widget

    def set_progress_view(self, widget):
        self.working.set_view(widget)
        self.sleep.set_view(widget)

    def skip(self):
        if self.current_step == False :
            self.current_step = self.working
        
        self.current_step.skip()

    def update_view(self):
        self.widget.config(text=self.status)

        if self.current_step == False :
            self.current_step = self.working

        self.current_step.update_view()

class App :
    def __init__ (self, master):
        self.master = master
        self.running = False

        _counter_loop = self.counter_loop = counter_loop( 20*60, 3*60)

        scrollable_frame = ScrollableFrame(master)
        frame_main = Frame(scrollable_frame.frame)

        text_running_status = Label(frame_main, text='')
        text_running_status.pack(side=BOTTOM)
        text_running_status.grid(row=0,column=0)
        _counter_loop.set_view( text_running_status )

        text_running_info = Label(frame_main, text='')
        text_running_info.pack(side=BOTTOM)
        text_running_info.grid(row=0,column=1)
        _counter_loop.set_progress_view( text_running_info )

        frame_main.pack()

        frame_buttons = Frame(scrollable_frame.frame)
        button_start = self.button_start = Button( frame_buttons, text="start",  command=self.start )
        button_start.pack(side=BOTTOM)
        button_start.grid(row=1,column=0)
        
        button_pause = self.button_pause = Button( frame_buttons, text="pause",  command=self.pause )
        button_pause.pack(side=BOTTOM)
        button_pause.grid(row=1,column=1)
        
        button_skip = self.button_skip = Button( frame_buttons, text="skip",  command=self.skip )
        button_skip.pack(side=BOTTOM)
        button_skip.grid(row=1,column=3)

        frame_buttons.pack(side=BOTTOM, pady=10)

        scrollable_frame.pack(side="top", fill="both", expand=True)

        self.update_view()

    def start(self):
        self.running = True
        self.do_process()

    def pause(self):
        self.running= False
        self.update_view()

    def skip(self):
        self.counter_loop.skip()
        self.update_view()

    def do_process(self):

        self.counter_loop.step()
        self.update_view()

        if self.running :
            self.master.after(int(1e3), self.do_process)

    def update_view(self) :
        self.counter_loop.update_view()

if __name__ == '__main__':
    root = Tk()
   
    root.minsize(width=400, height=300)
    root.title('番茄计时器')

    center(root)

    App(root)

    root.mainloop()
