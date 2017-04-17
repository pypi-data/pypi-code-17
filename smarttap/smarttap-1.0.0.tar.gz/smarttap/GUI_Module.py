################################################################################
# PUT COMMENTS HERE
################################################################################
# Python Modules/Libraries
import time
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as msgbox

# Package Modules
import smarttap.Management_Module as MgmtMod


################################################################################
class GoCardApp(object):
    """ GUI for interfacing with SmartTAP """
    def __init__(self, master):
        """ Initialise GUI """
        # SmartTAP Variables
        self.db_name = 'GoCard.db'
        self.direct = ''
        self.raw_name = ''
        self.stop_er = ''

        # GUI Variables
        self._timing = 1  # if =1 timing is on (default), if 0 timing is off
        button_width = 15  # Button width
        self._outline_count = 0

        # Establish App
        master.title('SmartTAP V0.0.1')

        # MENUS #
        # menubar = tk.Menu(master)  # Left for future function expansion

        # Raw Menu
        # rawmenu = tk.Menu(menubar, tearoff=0)
        # rawmenu.add_command(label='Raw DB', command=self.raw_data_db)
        # rawmenu.add_command(label='Raw Input', command=self.raw_data_input)
        # rawmenu.add_command(label='Stop Analysis',
        #                     command=self.raw_data_stopanly)
        # rawmenu.add_command(label='Raw Output', command=self.raw_data_output)
        # menubar.add_cascade(label='  Raw  ', menu=rawmenu)

        # Display Menus
        # master.config(menu=menubar)

        # DATA SETUP WIDGETS #
        # Directory Widget
        direct_frame = tk.Frame(master)
        self._direct_show = tk.Label(direct_frame, text=' ')
        self._direct_show.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self._direct_set = tk.Button(direct_frame, text="Set Directory",
                                     command=self.set_direct,
                                     width=button_width)
        self._direct_set.pack(side=tk.RIGHT)
        direct_frame.pack(side=tk.TOP, fill=tk.X)

        # Raw Data Widget
        raw_frame = tk.Frame(master)
        self._raw_show = tk.Label(raw_frame, text=' ')
        self._raw_show.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self._raw_set = tk.Button(raw_frame, text="Set Raw Data File",
                                  command=self.set_raw, width=button_width)
        self._raw_set.pack(side=tk.RIGHT)
        raw_frame.pack(side=tk.TOP, fill=tk.X)

        # DB Name Widget
        db_frame = tk.Frame(master)
        self._db_set = tk.Button(db_frame, text='Set Database Name',
                                 command=self.set_db_name, width=button_width)
        self._db_set.pack(side=tk.RIGHT)
        self._db_show = tk.Entry(db_frame)
        self._db_show.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=2)
        self._db_show.insert(tk.INSERT, self.db_name)
        db_frame.pack(side=tk.TOP, fill=tk.X)

        # FUNCTION WIDGETS #
        fn_frame = tk.Frame(master)
        # Raw Data Processing
        self._raw_data = tk.Button(fn_frame, text='Raw Data Process',
                                   command=self.raw_data_full,
                                   width=button_width)
        self._raw_data.pack(side=tk.LEFT)

        # Input Data Processing
        self._input_data = tk.Button(fn_frame, text='Input Data Process',
                                     command=self.input_data_full,
                                     width=button_width)
        self._input_data.pack(side=tk.LEFT)

        # Analysis Processing
        self._analysis = tk.Button(fn_frame, text='Analysis Process',
                                   command=self.analysis_full,
                                   width=button_width)
        self._analysis.pack(side=tk.LEFT)

        # All Processing
        self._all_data = tk.Button(fn_frame, text='All Processing',
                                   command=self.all_data_full,
                                   width=button_width)
        self._all_data.pack(side=tk.LEFT)

        # GUI Settings
        self._time_set = tk.Button(fn_frame, text='Time - ON', bg='green',
                                   command=self.time_change, width=button_width)
        self._time_set.pack(side=tk.RIGHT)
        self._clear = tk.Button(fn_frame, text='Clear Output',
                                command=self.clear_out, width=button_width)
        self._clear.pack(side=tk.RIGHT)

        fn_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        # OUTPUT TEXT + SCROLLBAR
        out_frame = tk.Frame(master)
        self._out_scroll = tk.Scrollbar(out_frame, orient=tk.VERTICAL)
        self._out_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self._text_out = tk.Text(out_frame,
                                 yscrollcommand=self._out_scroll.set)
        self._text_out.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)
        self._out_scroll.config(command=self._text_out.yview)
        out_frame.pack(side=tk.BOTTOM, expand=True, fill=tk.BOTH)

        # Line handling/parsing
        self._text_out.insert(tk.INSERT, 'Out [1] >>>\n\n')
        self._outline_count = 1

    def new_line(self):
        """ Generates new output line """
        self._outline_count += 1
        self._text_out.insert(tk.END, '\nOut [{0}] >>>\n\n'.format(
                              self._outline_count))
        self._text_out.see(tk.END)

    def divide_line(self):
        """ Print out line divider in command line output """
        print('\n###########################################################\n')

    def time_change(self):
        """ Set GUI runtime output ON or OFF """
        if self._timing == 1:
            self._timing = 0
            self._time_set.config(text='Time - OFF', bg='red')
        else:
            self._timing = 1
            self._time_set.config(text='Time - ON', bg='green')

    def clear_out(self):
        """ Clears output window and resetting output count """
        self._text_out.delete(1.0, tk.END)
        self._text_out.insert(tk.INSERT, 'Out [1] >>>\n\n')
        self._outline_count = 1

    def set_direct(self):
        """ Set processing workspace directory """
        start = time.time()
        direct = filedialog.askdirectory()
        self.direct = direct + '/'
        self._direct_show.config(text=self.direct)
        self._text_out.insert(tk.END, 'Directory Set: {0}\n'.format(
            self.direct))
        end = time.time()
        if self._timing == 1:
            self._text_out.insert(tk.END, '\nRuntime: {0}\n'.format(
                round(end - start, 8)))
        self.new_line()

    def set_raw(self):
        """ Set raw input data file """
        start = time.time()
        raw_name = filedialog.askopenfilename()
        raw_name_split = raw_name.split('/')
        raw_name_split2 = raw_name_split[-1].split('.')
        try:
            if raw_name_split2[1] == 'csv':
                self.raw_name = raw_name_split[-1]
                self._raw_show.config(text=self.raw_name)
                self._text_out.insert(tk.END, 'Raw Data File Set: {0}\n'.format(
                                      self.raw_name))
            else:
                msgbox.showerror('ERROR', 'Raw data file must be .csv format')
                self._text_out.insert(tk.END, 'Invalid raw data file type!\n')
                self.new_line()
                return
            end = time.time()
            if self._timing == 1:
                self._text_out.insert(tk.END, '\nRuntime: {0}\n'.format(
                    round(end - start, 8)))
            self.new_line()
        except IndexError:
            msgbox.showerror('ERROR', 'Raw data file must be .csv format')
            self._text_out.insert(tk.END, 'Invalid raw data file type!\n')
            self.new_line()

    def set_db_name(self):
        """ Set database name """
        start = time.time()
        db_name = self._db_show.get()
        db_name_split = db_name.split('.')
        try:
            if db_name_split[1] == 'db':
                self.db_name = db_name
                self._text_out.insert(tk.END, 'Database Name Set: {0}\n'.format(
                    db_name))
            else:
                msgbox.showerror('Database Name',
                                 'Invalid database name, name must end in .db')
                self._text_out.insert(tk.END, 'Invalid database name!\n')
                self.new_line()
                return
            end = time.time()
            if self._timing == 1:
                self._text_out.insert(tk.END, '\nRuntime: {0}\n'.format(
                    round(end - start, 8)))
            self.new_line()
        except IndexError:
            msgbox.showerror('Database Name',
                             'Invalid database name, name must end in .db')
            self._text_out.insert(tk.END, 'Invalid database name!\n')
            self.new_line()

    def raw_data_full(self):
        """ GUI interaction for raw data processing """
        start = time.time()
        self.raw_data_setup()
        end = time.time()
        if self._timing == 1:
            self._text_out.insert(tk.END, '\nRuntime: {0} sec\n'.format(
                round(end - start, 8)))
            self.new_line()
        else:
            self.new_line()

    def raw_data_setup(self):
        """ Background GUI interaction (use for _full functions)"""
        self._text_out.insert(tk.END, 'RAW DATA MODULE START\n\n')
        self.divide_line()
        print('RAW DATA MODULE\n')
        if self.direct == '':
            msgbox.showerror("ERROR", "Specify Directory")
            self.new_line()
            return
        if self.raw_name == '':
            msgbox.showerror("ERROR", "Specify Raw Data File")
            self.new_line()
            return
        try:
            self.raw_data_fns()
        except Exception as e:
            msgbox.showerror("ERROR", "Code Error: {0}".format(e))
            self.new_line()
            return
        self._text_out.insert(tk.END, '\nRAW DATA MODULE END\n')

    def raw_data_fns(self):
        """ Functions for raw data processing """
        raw = MgmtMod.RawDataManagement(self.direct, self.db_name)
        time1 = raw.raw_database()
        self._text_out.insert(tk.END, 'Raw DB Established: {0} sec\n'.format(
            round(time1, 8)))
        root.update_idletasks()
        stop_er, route_er, time2 = raw.raw_data_input(self.raw_name)
        self._text_out.insert(tk.END, 'Raw Data Input: {0} sec\n'.format(
            round(time2, 8)))
        root.update_idletasks()
        time3 = raw.stop_analysis(stop_er)
        self._text_out.insert(tk.END, 'Missing Stop Output + Count: {0} '
                                      'sec\n'.format(round(time3, 8)))
        root.update_idletasks()
        time4 = raw.raw_data_output()
        self._text_out.insert(tk.END, 'Raw Data Output: {0} sec\n'.format(
            round(time4, 8)))
        root.update_idletasks()

    def raw_data_db(self):
        """ Establish raw DB/clear existing DB"""
        start = self.func_start('Raw DB Start\n')
        raw = MgmtMod.RawDataManagement(self.direct, self.db_name)
        raw.raw_database()
        self.func_end(start)

    def raw_data_input(self):
        """ Input data into Raw DB """
        start = self.func_start('Raw Input Start\n')
        raw = MgmtMod.RawDataManagement(self.direct, self.db_name)
        self.stop_er, route_er = raw.raw_data_input(self.raw_name)
        self.func_end(start)

    def raw_data_stopanly(self):
        start = self.func_start('Stop Analysis Start\n')
        raw = MgmtMod.RawDataManagement(self.direct, self.db_name)
        if self.stop_er == '':
            msgbox.showerror("ERROR", "Run Raw Data Input Function")
            self.new_line()
            return
        raw.stop_analysis(self.stop_er)
        self.func_end(start)

    def raw_data_output(self):
        start = self.func_start('Raw Ouput Start\n')
        raw = MgmtMod.RawDataManagement(self.direct, self.db_name)
        raw.raw_data_output()
        self.func_end(start)

    def input_data_full(self):
        """ GUI interaction for input data processing """
        start = time.time()
        self.input_data_setup()
        end = time.time()
        if self._timing == 1:
            self._text_out.insert(tk.END, '\nRuntime: {0} sec\n'.format(
                round(end - start, 8)))
            self.new_line()
        else:
            self.new_line()

    def input_data_setup(self):
        """ Background GUI interaction (use for _full functions)"""
        start = time.time()
        self._text_out.insert(tk.END, 'MAIN DATA MODULE START\n\n')
        self.divide_line()
        print('MAIN DATA MODULE\n')
        try:
            if self.direct == '':
                msgbox.showerror("ERROR", "Specify Directory")
                self.new_line()
                return
            self.input_data_fns()
            self._text_out.insert(tk.END, '\nMAIN DATA MODULE END\n')
        except FileNotFoundError:
            self.new_line()
            msgbox.showerror("ERROR", "Run Raw Data Process First!")

    def input_data_fns(self):
        """ Functions for input data processing """
        main = MgmtMod.InputDataManagement(self.direct, self.db_name)
        time1 = main.main_database()
        self._text_out.insert(tk.END, 'Main DB Established: {0} sec\n'.format(
            round(time1, 8)))
        root.update_idletasks()
        time2 = main.main_data_input()
        self._text_out.insert(tk.END, 'Main Data Input: {0} sec\n'.format(
            round(time2[4], 8)))
        root.update_idletasks()

        # Display DB Error Stats
        model = '  # {0}: {1}   # Errors: {2}   % Total: {3}\n'
        s, r, u, t = time2[0], time2[1], time2[2], time2[3]
        self._text_out.insert(tk.END, model.format('Stop', s[1], s[0], s[2]))
        self._text_out.insert(tk.END, model.format('Route', r[1], r[0], r[2]))
        self._text_out.insert(tk.END, model.format('User', u[1], u[0], u[2]))
        self._text_out.insert(tk.END, model.format('Trip', t[1], t[0], t[2]))
        root.update_idletasks()

        # Display Error Dict
        self._text_out.insert(tk.END, 'Error Types\n')
        model = '  {0}: {1}\n'
        for error_type in time2[5]:
            self._text_out.insert(tk.END, model.format(error_type,
                                                       time2[5][error_type]))

    def analysis_full(self):
        """ GUI interaction for analysis processing """
        start = time.time()
        self.analysis_setup()
        end = time.time()
        if self._timing == 1:
            self._text_out.insert(tk.END, '\nRuntime: {0} sec\n'.format(
                round(end-start, 8)))
            self.new_line()
        else:
            self.new_line()

    def analysis_setup(self):
        """ Background GUI interaction (use for _full functions) """
        start = time.time()
        self._text_out.insert(tk.END, 'ANALYSIS MODULE START\n\n')
        self.divide_line()
        print('ANALYSIS DATA MODULE\n')
        try:
            if self.direct == '':
                msgbox.showerror('ERROR', 'Specify Directory')
                self.new_line()
                return
            self.analysis_fns()
            self._text_out.insert(tk.END, '\nANALYSIS MODULE END\n')
        except FileNotFoundError:
            self.new_line()
            msgbox.showerror('ERROR', 'Run Raw Data & Main Data Process First!')

    def analysis_fns(self):
        """ Functions for analysis processing """
        anly = MgmtMod.AnalysisDataManagement(self.direct, self.db_name)
        time1 = anly.anly_database()
        self._text_out.insert(tk.END,
                              'Analysis DB Established: {0} sec\n'.format(
                                  round(time1, 8)))
        root.update_idletasks()
        trip_cnt, jrny_cnt, time2 = anly.jrny_analysis(0, 0)
        # Further room for expansion using dates & commuter info ###############
        self._text_out.insert(tk.END, 'Journey Analysis: {0} sec\n'.format(
                                 round(time2, 8)))
        self._text_out.insert(tk.END,
                              '    Total# of Trips: {0}\n'.format(trip_cnt))
        self._text_out.insert(tk.END,
                              '    Total# of Jrnys: {0}\n'.format(jrny_cnt))
        root.update_idletasks()
        time3 = anly.stop_usage_summary()
        self._text_out.insert(tk.END, 'Basic Trip-to-Stop: {0} sec\n'.format(
                              round(time3, 8)))
        root.update_idletasks()
        time4 = anly.orig_dest_v2()
        self._text_out.insert(tk.END, 'OD-Matrix V2 Calc: {0} sec\n'.format(
                              round(time4, 8)))
        root.update_idletasks()
        time5, time6 = anly.stop_usage_detail()
        self._text_out.insert(tk.END, 'Stop Usage Analysis: {0} sec\n'.format(
                              round(time5, 8)))
        self._text_out.insert(tk.END, 'Analysis Data Input: {0} sec\n'.format(
                              round(time6, 8)))
        root.update_idletasks()
        time7 = anly.route_usage_summary()
        self._text_out.insert(tk.END, 'Route Usage Analysis: {0} sec\n'.format(
                              round(time7, 8)))
        root.update_idletasks()
        time8 = anly.route_usage_detail()
        self._text_out.insert(tk.END,
                              'Detailed Route Usage Analysis: {0} sec\n'.format(
                               round(time8, 8)))

    def all_data_full(self):
        """ GUI interaction for all data processing """
        start = time.time()
        if self.direct == '':
            msgbox.showerror("ERROR", "Specify Directory")
            self.new_line()
            return
        if self.raw_name == '':
            msgbox.showerror("ERROR", "Specify Raw Data File")
            self.new_line()
            return
        try:
            self.raw_data_setup()
            root.update_idletasks()
            self._text_out.insert(tk.END, '\n')
            self.input_data_setup()
            root.update_idletasks()
            self._text_out.insert(tk.END, '\n')
            self.analysis_setup()
            root.update_idletasks()
            end = time.time()
            if self._timing == 1:
                self._text_out.insert(tk.END, '\nRuntime: {0}\n'.format(
                    round(end - start, 8)))
                self.new_line()
            else:
                self.new_line()
        except Exception as e:
            print(e)
            return

    def func_start(self, start_text):
        """ General start for single element function """
        start = time.time()
        self._text_out.insert(tk.END, start_text)
        if self.direct == '':
            msgbox.showerror("ERROR", "Specify Directory")
            self.new_line()
            return
        return start

    def func_end(self, start):
        """ General end for single element function """
        end = time.time()
        if self._timing == 1:
            self._text_out.insert(tk.END, '\nRuntime: {0} sec\n'.format(
                round(end - start, 8)))
            self.new_line()
        else:
            self.new_line()

################################################################################
# Initialise GUI
root = tk.Tk()
root.state('zoomed')
app = GoCardApp(root)
root.mainloop()
