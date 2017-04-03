from __future__ import absolute_import
import os, warnings, six
import time, sys, threading, curses
from prior import *

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import libtorrent as lt

class Client():
    def __init__(self, port=6881,max_download_rate=0,max_upload_rate=0,save_path='.', proxy_host=''):
        self.ses = lt.session()
        self.defaults = {'port': 6881}
        
        if port < 0 or port > 65525:
            self.ses.listen_on(self.defaults['port'], self.defaults['port'] + 10)
        else:
            self.ses.listen_on(port, port+10)
            self.defaults['port'] = port
        
        max_upload_rate *= 1000
        max_download_rate *= 1000
        
        if max_upload_rate <= 0:
            max_upload_rate = -1
        if max_download_rate <= 0:
            max_download_rate = -1
        
        if proxy_host != '':
            ps = lt.proxy_settings()
            ps.type = lt.proxy_type.http
            ps.hostname = proxy_host.split(':')[0]
            ps.port = int(proxy_host.split(':')[1])
            self.ses.set_proxy(ps)        
        
        self.defaults['max_download_rate'] = max_download_rate
        self.defaults['max_upload_rate'] = max_upload_rate
        self.defaults['save_path'] = save_path
        self.defaults['proxy_host'] = proxy_host
        
        self.ses.set_download_rate_limit(int(max_download_rate))
        self.ses.set_upload_rate_limit(int(max_upload_rate))
        self.ses.set_settings(lt.session_settings())
        self.ses.set_alert_mask(0xfffffff)
    
    def add_torrent(self, torrent_files):
        handles = []
        for tf in torrent_files:
            atp = {}
            atp['save_path'] = self.defaults['save_path']
            atp['storage_mode'] = lt.storage_mode_t.storage_mode_sparse
            atp['paused'] = False
            atp['auto_managed'] = True
            atp["duplicate_is_error"] = True
            
            if tf.startswith('magnet:') or tf.startswith('http://') or tf.startswith('https://'):
                atp['url'] = tf
            else:
                info = lt.torrent_info(tf)
                # print('Adding \'%s\'...' % info.name())
        
                try:
                    atp['resume_data'] = open(os.path.join(options.save_path, info.name() + '.fastresume'), 'rb').read()
                except:
                    pass
        
                atp['ti'] = info
                
            h = self.ses.add_torrent(atp)
            h.set_max_connections(60)
            h.set_max_uploads(-1)
            handles.append(h)
        return handles
 
    def query_handle_sp(self, h):        
        
        while (not h.is_seed()):
            s = h.status()
            #six.print_('\r tracker: %s\n' % s.current_tracker)
            state_str = ['queued', 'checking', 'downloading metadata', \
                         'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']
            #six.print_('\r%.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d seeds: %d distributed copies: %d) %s' % \
                       #(s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
                        #s.num_peers, s.num_seeds, s.distributed_copies, state_str[s.state]), end=' ')
            six.print_('%s %.2f%% complete (down: %.1f kB/s up: %.1f kB/s peers: %d seeds: %d distributed copies: %d) %s' % \
                                   (h.name()[:8], s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
                                    s.num_peers, s.num_seeds, s.distributed_copies, state_str[s.state]))            
    
            alerts = self.ses.pop_alerts()
            for a in alerts:
                if a.category() & lt.alert.category_t.error_notification:
                    six.print_(a)
    
            sys.stdout.flush() 
            time.sleep(1)
    
        six.print_('\n', h.name(), 'complete')
    
    def process_handles(self, handles):
        
        #for h in handles:
            #six.print_('starting', h.name())
            #t = threading.Thread(target=self.query_handle, args=(h,))
            #t.setDaemon(True)
            #t.start()
        
        state_str = ['queued', 'checking', 'downloading metadata', \
                                    'downloading', 'finished', 'seeding', 'allocating', 'checking fastresume']        
        stdscr = curses.initscr()
        #s = stdscr.subwin(23, 79, 0, 0)
        #s.box()
        #s.refresh()        
        #curses.start_color()
        while (any(not hand.is_finished() for hand in handles)):
            stdscr.erase()
            for h in handles:
                s = h.status()
                stdscr.addstr("{name} {progress}{padding}{percent}% complete(down: {down} kB/s up: {up} kB/s peers: {peers} seeds: {seeds} copies: {distributed_copies}) {state}\n".format(
                    name = h.name(),
                    progress = "#" * int(s.progress*10),
                    padding = " " * (10 - int(s.progress*10)),
                    percent = round(s.progress*100,2),
                    down = s.download_rate / 1000,
                    up = s.upload_rate / 1000,
                    peers = s.num_peers,
                    seeds = s.num_seeds,
                    distributed_copies = round(s.distributed_copies),
                    state = state_str[s.state]
                ))                
                alerts = self.ses.pop_alerts()
                for a in alerts:
                    if a.category() & lt.alert.category_t.error_notification:
                        #pdb.set_trace()
                        if type(a) == str:
                            stdscr.addstr(a)
                        else:
                            pass
                            #stdscr(a.message())
                time.sleep(1)
            stdscr.refresh()
        curses.endwin()
                                
    def getmodes(self, handles):
        names = []
        for h in handles:
            if h.has_metadata():
                names.append(h.name())
            else:
                names.append('-')
        return names
    
    def getpriorities(self, handles):
        for h in handles:
            if h.has_metadata():
                return h.file_priorities()
            else:
                return 0   
            
    def setpriorities(self, h, priorityList):
        if h.has_metadata():
            h.prioritize_files(priorityList)
    
    def prioritize_file(self,h,fileIndex,priorityIndex):
        if h.has_metadata():
            h.file_priority(fileIndex,priorityIndex)
    
    def run_set_priorities(self, handles):
        if (any(hand.get_torrent_info().num_files()>1 for hand in handles)):
            pApp = PriorityApp()
            pApp.set_handler(handles)
            pApp.run()
            
            for h,pl in get_so().items():
                if h.has_metadata():
                    h.prioritize_files(pl)        
        #six.print_(get_so())

def get(tf):
    client = Client()
    handles = client.add_torrent([tf])
    filenames = client.getmodes(handles)
    client.process_handles(handles)
    return filenames[0]

def version():
    six.print_('Academic Torrents Version 1.7')
        
def test():    
    six.print_('LD_LIBRARY PATH set to: ', os.environ['LD_LIBRARY_PATH'])
    six.print_('PKG_CONFIG_PATH set to: ', os.environ['PKG_CONFIG_PATH'])
    six.print_('Libtorrent Version Installed is: ' + lt.version)
    
    #client = Client()
    #handles = client.add_torrent(['/home/ronald/Downloads/323a0048d87ca79b68f12a6350a57776b6a3b7fb.torrent', '/home/ronald/Downloads/2269d7d1c77375aea732eea0905e370d4741575f.torrent'])
    #handles = client.add_torrent(["/home/ronald/Downloads/42714f859770f1a9d8b27985f9f16ea17e8ba2f6.torrent","/home/ronald/Downloads/2269d7d1c77375aea732eea0905e370d4741575f.torrent"])    
    #client.run_set_priorities(handles)
    #client.process_handles(handles)  
       

if __name__ == "__main__":
    test()
