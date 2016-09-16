
class step(object):
    def __init__(self):
        self.time = 0.0
        self.widget = None
        self.process_time = None

    def reset(self) :
        self.time = 0.0
        self.update_view()

    def count_down (self):
        self.time = self.time + 1
        self.time = min(self.time, self.process_time)

    def is_finish(self):
        return self.time == self.process_time

    def skip(self):
        self.time = self.process_time 

    @property
    def status(self):
        return ( '%s - %s  %.2f' %  ( self.time, self.process_time,  self.time *100.0 / self.process_time ) )  + '%'

    @status.setter
    def status(self, value):
        pass
    
    def set_view(self, widget):
        self.widget = widget
    
    def update_view(self):
        if self.widget :
            self.widget.config(text=self.status)

