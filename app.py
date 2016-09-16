# -*- coding: utf-8 -*-  

from Tkinter import *
from threading import Thread
import tkMessageBox

from scrolable_frame import ScrollableFrame
from step import *
from utils import *

class MessageBox():
    def __init__(self):
        self.root = Tk()
        self.frame = Frame(self.root)
        self.label = StringVar( self.frame )
        
        self.label.set("hello")

        self.label_widget = Label(self.frame, textvariable=self.label)
        self.label_widget.pack()

    def say_hi(self, msg=''):
        self.label.set(msg)
        self.label_widget.config(textvariable=self.label)
        self.show()

    def show(self):
        self.frame.pack()
        self.root.mainloop()

'''
    目标是写一个展示半自动洗衣机的工作阶段的app
    准备：
        1 进水
        2 浸泡
    洗衣
        3 洗涤
        4 排水
    漂洗*3
        5 进水
        6 漂洗
        7 排水
    甩干
        8 甩干
'''

class water_in(step):
    def __init__(self, process_time=60*2):
        step.__init__(self)
        self.process_time = process_time
        self.name = '进水'

class water_out(step):
    def __init__(self, process_time=60*2):
        step.__init__(self)
        self.process_time = process_time
        self.name = '放水'

class soak(step):
    def __init__(self, process_time=60*3):
        step.__init__(self)
        self.process_time = process_time
        self.name = '浸泡'
    
class wash(step):
    def __init__(self, process_time=60*6):
        step.__init__(self)
        self.process_time = process_time
        self.name = '洗涤'

class rinse(step):
    def __init__(self, process_time=60*3):
        step.__init__(self)
        self.process_time = process_time
        self.name = '漂洗'

class spin_dry(step):
    def __init__(self, process_time=60*1):
        step.__init__(self)
        self.process_time = process_time
        self.name = '甩干'


class processing(step):
    def __init__(self):
        step.__init__(self)

        self.steps = []
        self._current_step = 0


    def add(self, step):
        self.steps.append(step)
        return self


    def reset(self):

        self._current_step = 0

        for step in self.steps :
            step.reset()
    @property
    def process_time(self):
        sum = 0.0
        for _step in self.steps:
            sum += _step.process_time
        return sum

    @process_time.setter
    def process_time(self, val):
        pass

    @property
    def current_step(self):
        return self.steps[self._current_step]

    @current_step.setter
    def current_step(self):
        pass
    
    def is_finish(self):
        current_step = self.current_step
        return current_step == self.steps[-1] and current_step.is_finish()

    def step(self):
        current_step = self.current_step
        current_step.count_down()
        self.count_down()

        if current_step.is_finish(): 
            if not self.is_finish():
                tkMessageBox.showinfo( '状态更新', current_step.name + ' 完成，操作洗衣机进行下一步.' ) 
                self._current_step = self._current_step + 1
            else :
                tkMessageBox.showinfo( 'all done','全部完成，晾衣服吧'  )

    def skip(self):
        self.current_step.skip()

    @property
    def status(self):
        curret_step = self.current_step  
        return curret_step.name + ' ' + curret_step.status + (' ')

    @status.setter
    def status(self, value):
        pass



class App:

    def __init__(self, master):
        self.master = master
        self.running = False

        self.process = processing().add(water_in()).add(soak()).add(wash()).add(water_out())

        self.process.add(water_in()).add(rinse()).add(water_out())
        self.process.add(water_in()).add(rinse()).add(water_out())
        self.process.add(water_in()).add(rinse()).add(water_out())

        self.process.add(spin_dry())

        scrollable_frame = ScrollableFrame(master)
        frame_main = Frame(scrollable_frame.frame)

        status_label = self.status_label= Label(frame_main, text="")
        status_label.pack()
        status_label.grid(row=0, column=0, columnspan=2)

        for idx in xrange(len(self.process.steps)) :
            step = self.process.steps[idx]

            step_label = Label(frame_main, text=step.name)
            step_label.pack(side=RIGHT)
            step_label.grid(row=idx + 1, column=0)

            status_label =  Label(frame_main)
            status_label.pack(side=LEFT)
            status_label.grid(row=idx + 1, column=1)

            step.set_view(status_label)
            step.update_view()
        
        frame_main.pack()

        frame_buttons = Frame(scrollable_frame.frame)
        button_start = self.button_start = Button( frame_buttons, text="start",  command=self.start )
        button_start.pack(side=BOTTOM)
        button_start.grid(row=1,column=0)
        
        button_pause = self.button_pause = Button( frame_buttons, text="pause",  command=self.pause )
        button_pause.pack(side=BOTTOM)
        button_pause.grid(row=1,column=1)
        
        button_reset = self.button_reset = Button( frame_buttons, text="reset",  command=self.reset )
        button_reset.pack(side=BOTTOM)
        button_reset.grid(row=1,column=2)

        button_skip = self.button_skip = Button( frame_buttons, text="skip",  command=self.skip )
        button_skip.pack(side=BOTTOM)
        button_skip.grid(row=1,column=3)

        frame_buttons.pack(side=BOTTOM, pady=10)

        scrollable_frame.pack(side="top", fill="both", expand=True)

        self.update_view()

    def say_hi(self):
        MessageBox().say_hi('hello my friend')

    def start(self):
        self.running= True
        self.do_process()

    def pause(self):
        self.running= False
        self.update_view()

    def reset(self):
        self.running= False
        self.process.reset()
        self.update_status()

    def skip(self):
        self.process.skip()
        self.update_status()

    def update_status(self):
        self.button_start.config(state= NORMAL if not self.running else DISABLED)
        self.button_pause.config(state= NORMAL if self.running else DISABLED)
        self.status_label.config(text= "状态 ： " + self.process.status)

    def update_view(self):
        self.update_status()
        self.process.current_step.update_view()

    def do_process(self):

        self.process.step()
        self.update_view()

        if self.running and not self.process.is_finish():
            self.master.after(int(1e3), self.do_process)




if __name__ == '__main__':
    root = Tk()
   
    root.minsize(width=400, height=300)
    root.title('洗衣机计时器')

    center(root)

    App(root)

    root.mainloop()
