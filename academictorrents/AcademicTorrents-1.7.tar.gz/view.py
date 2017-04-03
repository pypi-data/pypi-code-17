import urwid
import math
import time

from academictorrents import *
import pdb
UPDATE_INTERVAL = 0.2

class GraphView(urwid.WidgetWrap):
    """
    A class responsible for providing the application's interface and
    graph display.
    """
    palette = [
        ('body',         'black',      'light gray', 'standout'),
        ('header',       'white',      'dark red',   'bold'),
        ('screen edge',  'light blue', 'dark cyan'),
        ('main shadow',  'dark gray',  'black'),
        ('line',         'black',      'light gray', 'standout'),
        ('bg background','light gray', 'black'),
        ('bg 1',         'black',      'dark blue', 'standout'),
        ('bg 1 smooth',  'dark blue',  'black'),
        ('bg 2',         'black',      'dark cyan', 'standout'),
        ('bg 2 smooth',  'dark cyan',  'black'),
        ('button normal','light gray', 'dark blue', 'standout'),
        ('button select','white',      'dark green'),
        ('line',         'black',      'light gray', 'standout'),
        ('pg normal',    'white',      'black', 'standout'),
        ('pg complete',  'white',      'dark magenta'),
        ('pg smooth',     'dark magenta','black')
        ]

    graph_samples_per_bar = 10
    graph_num_bars = 5
    graph_offset_per_second = 2

    def __init__(self, controller):
        self.controller = controller
        self.started = True
        self.start_time = None
        self.offset = 0
        self.last_offset = None        
        urwid.WidgetWrap.__init__(self, self.main_window())
        
    def get_offset_now(self):
        if self.start_time is None:
            return 0
        if not self.started:
            return self.offset
        tdelta = time.time() - self.start_time
        return int(self.offset + (tdelta*self.graph_offset_per_second))    

    def update_graph(self, force_update=False):
        
        #o = self.get_offset_now()
        #if o == self.last_offset and not force_update:
            #return False        
        #self.last_offset = o
       
        #d, max_value, repeat = self.controller.get_data( o, r )
        max_value = 100
        repeat = 100
        l = []
        h = self.controller.handles[self.controller.tindex]
        
        if (not h.is_seed()):
            s = h.status()
            prog = s.progress
            peers = h.get_peer_info()
            for p in peers:
                if p.downloading_piece_index >= 0:
                    l.append([0,float(p.downloading_progress)/p.downloading_total])
                else:
                    l.append([0,0])
        else:
            prog = 1
        
        #if ((o//5)%2==0):
            #l.append([0,15])
            #l.append([0,35])
            #l.append([20,0])
            #l.append([0,45])
            #l.append([85,0])
            #l.append([0,100])
            #l.append([100,0])
        #else:
            #l.append([0,10])
            #l.append([0,35])
            #l.append([30,0])
            #l.append([20,45])
            #l.append([8,0])
            #l.append([0,50])
            #l.append([10,0])            
    
        time.sleep(1)   
        self.graph.set_data(l,max_value)

        # also update progress
        
        #prog = float(time.time()%100) /100
        self.animate_progress.set_completion( prog )
        return True

    def on_animate_button(self, button):
        """Toggle started state and button text."""
        if self.started:
            button.set_label("Start")
            self.offset = self.get_offset_now()
            self.started = False
            self.controller.stop_animation()           
        else:
            self.start_time = time.time()            
            h = self.controller.handles[self.controller.tindex]
            s = h.status()
            button.set_label("Started")
            
            if (h.is_paused()):
                button.set_label("Resuming")
                h.resume()
            
            self.controller.animate_graph()           

    def on_reset_button(self, w):
        self.offset = 0
        self.start_time = time.time()
        self.update_graph(True)

    def on_mode_button(self, button, state):
        """Notify the controller of a new mode setting."""
        if state:
            # The new mode is the label of the button
            self.controller.set_mode( button.get_label() )
        self.last_offset = None

    def on_mode_change(self, m):
        """Handle external mode change by updating radio buttons."""
        for rb in self.mode_buttons:
            if rb.get_label() == m:
                rb.set_state(True, do_callback=False)
                break
        self.last_offset = None

    def on_unicode_checkbox(self, w, state):
        self.graph = self.bar_graph( state )
        self.graph_wrap._w = self.graph
        self.animate_progress = self.progress_bar( state )
        self.animate_progress_wrap._w = self.animate_progress
        self.update_graph( True )


    def main_shadow(self, w):
        """Wrap a shadow and background around widget w."""
        bg = urwid.AttrWrap(urwid.SolidFill(u"\u2592"), 'screen edge')
        shadow = urwid.AttrWrap(urwid.SolidFill(u" "), 'main shadow')

        bg = urwid.Overlay( shadow, bg,
            ('fixed left', 3), ('fixed right', 1),
            ('fixed top', 2), ('fixed bottom', 1))
        w = urwid.Overlay( w, bg,
            ('fixed left', 2), ('fixed right', 3),
            ('fixed top', 1), ('fixed bottom', 2))
        return w

    def bar_graph(self, smooth=False):
        satt = None
        if smooth:
            satt = {(1,0): 'bg 1 smooth', (2,0): 'bg 2 smooth'}
        w = urwid.BarGraph(['bg background','bg 1','bg 2'], satt=satt)
        return w

    def button(self, t, fn):
        w = urwid.Button(t, fn)
        w = urwid.AttrWrap(w, 'button normal', 'button select')
        return w

    def radio_button(self, g, l, fn):
        w = urwid.RadioButton(g, l, False, on_state_change=fn)
        w = urwid.AttrWrap(w, 'button normal', 'button select')
        return w

    def progress_bar(self, smooth=False):
        if smooth:
            return urwid.ProgressBar('pg normal', 'pg complete',
                0, 1, 'pg smooth')
        else:
            return urwid.ProgressBar('pg normal', 'pg complete',
                0, 1)

    def exit_program(self, w):
        raise urwid.ExitMainLoop()

    def graph_controls(self):
        modes = self.controller.get_modes()
        # setup mode radio buttons
        self.mode_buttons = []
        group = []
        for m in modes:
            rb = self.radio_button( group, m, self.on_mode_button )
            self.mode_buttons.append( rb )
        # setup animate button
        self.animate_button = self.button( "", self.on_animate_button)
        self.on_animate_button( self.animate_button )
        self.offset = 0
        self.animate_progress = self.progress_bar()
        animate_controls = urwid.GridFlow( [
            self.animate_button,
            self.button("Details", self.on_reset_button),
            ], 11, 2, 0, 'center')

        if urwid.get_encoding_mode() == "utf8":
            unicode_checkbox = urwid.CheckBox(
                "Enable Unicode Graphics",
                on_state_change=self.on_unicode_checkbox)
        else:
            unicode_checkbox = urwid.Text(
                "UTF-8 encoding not detected")

        self.animate_progress_wrap = urwid.WidgetWrap(
            self.animate_progress)

        l = [    urwid.Text("Torrent Files",align="center"),
            ] + self.mode_buttons + [
            urwid.Divider(),
            urwid.Text("Actions",align="center"),
            animate_controls,
            self.animate_progress_wrap,
            urwid.Divider(),
            urwid.LineBox( unicode_checkbox ),
            urwid.Divider(),
            self.button("Quit", self.exit_program ),
            ]
        w = urwid.ListBox(urwid.SimpleListWalker(l))
        return w

    def main_window(self):
        self.graph = self.bar_graph()
        self.graph_wrap = urwid.WidgetWrap( self.graph )
        vline = urwid.AttrWrap( urwid.SolidFill(u'\u2502'), 'line')
        c = self.graph_controls()
        w = urwid.Columns([('weight',2,self.graph_wrap),
            ('fixed',1,vline), c],
            dividechars=1, focus_column=2)
        w = urwid.Padding(w,('fixed left',1),('fixed right',0))
        w = urwid.AttrWrap(w,'body')
        w = urwid.LineBox(w)
        w = urwid.AttrWrap(w,'line')
        w = self.main_shadow(w)
        return w
    
class GraphController:
    """
    A class responsible for setting up the model and view and running
    the application.
    """
    
    def __init__(self, torrentFiles):
        self.animate_alarm = None
        self.client = Client()
        self.handles = self.client.add_torrent(torrentFiles)
        self.view = GraphView(self)
        # use the first mode as the default
        mode = self.get_modes()[0]
        self.tindex = 0
        # update the view
        self.view.on_mode_change( mode )
        self.view.update_graph(True)

    def get_modes(self):
        """Allow our view access to the list of modes."""
        return self.client.getmodes(self.handles)

    def set_mode(self, m):
        """Allow our view to set the mode."""
        self.tindex = self.client.getmodes(self.handles).index(m)
        self.view.update_graph(True)
        return self.tindex

    def get_data(self, offset, range):
        """Provide data to our view for the graph."""
        return self.client.get_data( offset, range )

    def main(self):
        self.loop = urwid.MainLoop(self.view, self.view.palette)
        self.loop.run()

    def animate_graph(self, loop=None, user_data=None):
        """update the graph and schedule the next update""" 
        self.view.update_graph()
        self.animate_alarm = self.loop.set_alarm_in(
            UPDATE_INTERVAL, self.animate_graph)

    def stop_animation(self):
        """stop animating the graph"""
        if self.animate_alarm:
            self.loop.remove_alarm(self.animate_alarm)
        self.animate_alarm = None