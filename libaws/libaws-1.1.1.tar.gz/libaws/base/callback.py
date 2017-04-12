#coding:utf-8
import threading
import time
import os
import sys

class Monitor(object):
    '''
        监控下载上传速度和进度的计时器类
    '''
    #监控下载/上传速度的时间间隔 
    timer_interval = 1 

    def __init__(self,progress):
        self.daemon = True
        self._progress = progress
        self._seen_so_far = progress.seen_so_far
        self._exit = False
        self._progress_type = ''

        if progress.type == progress.DOWNLOAD_PROGRESS:
            self._progress_type= u'↓'
        elif progress.type == progress.UPLOAD_PROGRESS:
            self._progress_type= u'↑'

    @property
    def seen_so_far(self):
        '''
            上一次下载/上传的字节数
        '''
        return self._seen_so_far

    @seen_so_far.setter
    def seen_so_far(self,value):
        self._seen_so_far = value

    @property
    def exit(self):
        '''
            停止监控
        '''
        return self._exit

    @exit.setter
    def exit(self,v):
        self._exit = v 

    def start_timer(self):
        t = threading.Timer(self.timer_interval,self.monitor)  
        t.start()

    def calc_sec_speed(self,time_bytes):
        
        sec_bytes = time_bytes/float(self.timer_interval)
        if sec_bytes < 1024*1024:
            sec_speed = "%7.2f KB/S" % (sec_bytes/1024)
        else:
            sec_speed = "%7.2f MB/S" % (sec_bytes/1024/1024)

        return sec_speed

    def calc_remain_time(self,time_bytes):

        remain_size = self.progress.size - self.progress.seen_so_far
        if remain_size < 0:
            remain_size = 0
        sec_speed = time_bytes/float(self.timer_interval)

        if 0 == int(sec_speed):
            return ("%7s" % ('----'))

        remain_time_sec = remain_size / sec_speed
        if remain_time_sec < 60:
            remain_time = "%5.1f S"  %(remain_time_sec)
        elif remain_time_sec < (60*60):
            remain_time = "%5.1f M" % (remain_time_sec/60)
        elif remain_time_sec < (60*60*24):
            remain_time = "%5.1f H" % (remain_time_sec/(60*60))
        else:
            remain_time = "%5.1f D" % (remain_time_sec/(60*60*24))

        return remain_time

    def monitor(self):
        '''
            实时打印下载/上传速度
        '''
        if 0 == self.progress.size:
            return

        seen_so_far = self.progress.seen_so_far
        percentage = (seen_so_far / float(self.progress.size)) * 100
        time_bytes = seen_so_far - self.seen_so_far
        #sec_speed = (time_bytes/1024.0)/self.timer_interval
        sec_speed = self.calc_sec_speed(time_bytes)
        remain_time = self.calc_remain_time(time_bytes)

        sys.stdout.write("\r%s %s  %ld / %ld  (%.2f%%),speed:%s,remain time:%s" % (self.progress.filename,\
                                self._progress_type,self.progress.seen_so_far,self.progress.size, percentage,sec_speed,remain_time))

#        if percentage == 100:
 #           sys.stdout.write('\n')
        sys.stdout.flush()
        self.seen_so_far = seen_so_far

        if not self.exit:
            self.start_timer()
        else:
            sys.stdout.write('\n')
            
    @property
    def progress(self):
        return self._progress

class ProgressPercentage(object):
    ''' 
        进度条
    '''

    #上传进度条
    UPLOAD_PROGRESS = 1
    #下载进度条
    DOWNLOAD_PROGRESS = 2

    def __init__(self, filename,progress_type,seen_so_far=0): 
        self._filename = filename
        self._size = 0.0 
        self._seen_so_far = seen_so_far 
        #进度条类型
        self._type = progress_type
        self._lock = threading.Lock()
        self._monitor = Monitor(self)
        #监控计时器是否启动,刚开始时未启动
        #self._is_timer_start = False

    def __enter__(self):  
        self.monitor.start_timer()
        return self
                        
    def __exit__(self, e_t, e_v, t_b):  
        self.monitor.exit = True

    @property
    def lock(self):
        '''
            互斥锁
        '''
        return self._lock
    
    @property
    def filename(self):
        return self._filename
    
    @property
    def seen_so_far(self):
        return self._seen_so_far

    @seen_so_far.setter
    def seen_so_far(self,value):
        self._seen_so_far = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self,value):
        if value < 0:
            raise ValueError('progress size must not less 0')

        self._size = value

    @property
    def monitor(self):
        return self._monitor

    @property
    def type(self):
        return self._type

    def __call__(self, bytes_amount):
    
        with self.lock:
            #只启动一次计时器就可以了
         #   if not self._is_timer_start: 
          #      self.monitor.start_timer()
           #     self._is_timer_start = True

            self.seen_so_far += bytes_amount   
            if self.seen_so_far >= self.size:
                self.monitor.exit = True

class DownloadProgressPercentage(ProgressPercentage):
    '''
        下载进度条类
    '''
    def __init__(self, filename,size,seen_so_far=0): 
        super(DownloadProgressPercentage,self).__init__(filename,self.DOWNLOAD_PROGRESS,seen_so_far)
        self.size = size
        assert(self.size >= 0)

class UploadProgressPercentage(ProgressPercentage):
    '''
        上传进度条
    '''
    def __init__(self, filename,seen_so_far=0): 
        super(UploadProgressPercentage,self).__init__(filename,self.UPLOAD_PROGRESS,seen_so_far)
        self.size = os.path.getsize(filename) 
        assert(self.size >= 0)
