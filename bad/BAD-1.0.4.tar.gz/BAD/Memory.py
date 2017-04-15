# coding=utf-8

"""
 :Description:    设备类
 :author          80071482/bony
 :@version         V1.0
 :@Date            2016年11月
"""
import os
import re
import platform

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

# 判断系统类型，windows使用findstr，linux使用grep
sys_info = platform.system()
if sys_info is "Windows":
    find_util = "findstr"
else:
    find_util = "grep"


class Memory(object):

    def __init__(self, device=None, packgename=None):
        self._meminfo_text_ = None
        self._native_heap_pss_total_ = None
        self._native_heap_private_dirty_ = None
        self._native_heap_private_clean_ = None
        self._native_heap_swapped_dirty_ = None
        self._native_heap_heap_size_ = None
        self._native_heap_heap_alloc_ = None
        self._native_heap_heap_free_ = None
        self._dalvik_heap_pss_total_ = None
        self._dalvik_heap_private_dirty_ = None
        self._dalvik_heap_private_clean_ = None
        self._dalvik_heap_swapped_dirty_ = None
        self._dalvik_heap_heap_size_ = None
        self._dalvik_heap_heap_alloc_ = None
        self._dalvik_heap_heap_free_ = None
        self._dalvik_alloc_pss_total_ = None
        self._dalvik_alloc_private_dirty_ = None
        self._dalvik_alloc_private_clean_ = None
        self._dalvik_alloc_swapped_dirty_ = None
        self._stack_pss_total_ = None
        self._Stack_private_dirty_ = None
        self._Stack_private_clean_ = None
        self._Stack_swapped_dirty_ = None
        self._Cursor_pss_total_ = None
        self._Cursor_private_dirty_ = None
        self._Cursor_private_clean_ = None
        self._Cursor_swapped_dirty_ = None
        self._ashmem_pss_total_ = None
        self._ashmem_private_dirty_ = None
        self._ashmem_private_clean_ = None
        self._ashmem_swapped_dirty_ = None
        self._gfx_dev_pss_total_ = None
        self._gfx_dev_private_dirty_ = None
        self._gfx_dev_private_clean_ = None
        self._gfx_dev_swapped_dirty_ = None
        self._alloc_dev_pss_total_ = None
        self._alloc_dev_private_dirty_ = None
        self._alloc_dev_private_clean_ = None
        self._alloc_dev_swapped_dirty_ = None
        self._file_so_mmap_pss_total_ = None
        self._file_so_mmap_private_dirty_ = None
        self._file_so_mmap_private_clean_ = None
        self._file_so_mmap_swapped_dirty_ = None
        self._file_apk_mmap_pss_total_ = None
        self._file_apk_mmap_private_dirty_ = None
        self._file_apk_mmap_private_clean_ = None
        self._file_apk_mmap_swapped_dirty_ = None
        self._file_ttf_mmap_pss_total_ = None
        self._file_ttf_mmap_private_dirty_ = None
        self._file_ttf_mmap_private_clean_ = None
        self._file_ttf_mmap_swapped_dirty_ = None
        self._file_dex_mmap_pss_total_ = None
        self._file_dex_mmap_private_dirty_ = None
        self._file_dex_mmap_private_clean_ = None
        self._file_dex_mmap_swapped_dirty_ = None
        self._file_oat_mmap_pss_total_ = None
        self._file_oat_mmap_private_dirty_ = None
        self._file_oat_mmap_private_clean_ = None
        self._file_oat_mmap_swapped_dirty_ = None
        self._file_art_mmap_pss_total_ = None
        self._file_art_mmap_private_dirty_ = None
        self._file_art_mmap_private_clean_ = None
        self._file_art_mmap_swapped_dirty_ = None
        self._alloc_mmap_pss_total_ = None
        self._alloc_mmap_private_dirty_ = None
        self._alloc_mmap_private_clean_ = None
        self._alloc_mmap_swapped_dirty_ = None
        self._Unknown_pss_total_ = None
        self._Unknown_private_dirty_ = None
        self._Unknown_private_clean_ = None
        self._Unknown_swapped_dirty_ = None
        self._total_pss_total_ = None
        self._total_private_dirty_ = None
        self._total_private_clean_ = None
        self._total_swapped_dirty_ = None
        self._total_heap_size_ = None
        self._total_heap_alloc_ = None
        self._total_heap_free_ = None
        """
        对象初始化
        """
        self.device = device
        if packgename != None:
            self.get_meminfo_text(device, packgename)
            self.native_heap()
            self.native_heap()
            self.native_heap()
            self.native_heap()
            self.dalvik_heap()
            self.dalvik_alloc()
            self.Stack()
            self.Cursor()
            self.native_heap()
            self.ashmem()
            # self.gfx_dev()
            self.alloc_dev()
            self.file_so_mmap()
            self.file_apk_mmap()
            self.file_ttf_mmap()
            self.file_dex_mmap()
            self.file_oat_mmap()
            self.file_art_mmap()
            self.alloc_mmap()
            self.unknown()
            self.total()

    def get_meminfo_text(self, device, packgename):
        """
        获取内存信息
        """
        self._meminfo_text_ = device.script("adb shell dumpsys meminfo %s" % (packgename))
        pass

    def get_memory_list(self, category):
        """
        获取某项的内存信息
        """
        if self._meminfo_text_ != None:
            meminfo_list = self._meminfo_text_.split("\n")
            for meminfo in meminfo_list:
                if category in meminfo:
                    pattern = re.compile(r"\d+")
                    return pattern.findall(meminfo)

    def native_heap(self):
        meminfo = self.get_memory_list("native heap")
        self._native_heap_pss_total_ = meminfo[0]
        self._native_heap_private_dirty_ = meminfo[1]
        self._native_heap_private_clean_ = meminfo[2]
        self._native_heap_swapped_dirty_ = meminfo[3]
        self._native_heap_heap_size_ = meminfo[4]
        self._native_heap_heap_alloc_ = meminfo[5]
        self._native_heap_heap_free_ = meminfo[6]
        return meminfo

    def dalvik_heap(self):
        meminfo = self.get_memory_list("dalvik heap")
        self._dalvik_heap_pss_total_ = meminfo[0]
        self._dalvik_heap_private_dirty_ = meminfo[1]
        self._dalvik_heap_private_clean_ = meminfo[2]
        self._dalvik_heap_swapped_dirty_ = meminfo[3]
        self._dalvik_heap_heap_size_ = meminfo[4]
        self._dalvik_heap_heap_alloc_ = meminfo[5]
        self._dalvik_heap_heap_free_ = meminfo[6]
        return meminfo

    def dalvik_alloc(self):
        meminfo = self.get_memory_list("dalvik alloc")
        self._dalvik_alloc_pss_total_ = meminfo[0]
        self._dalvik_alloc_private_dirty_ = meminfo[1]
        self._dalvik_alloc_private_clean_ = meminfo[2]
        self._dalvik_alloc_swapped_dirty_ = meminfo[3]
        return meminfo

    def Stack(self):
        meminfo = self.get_memory_list("Stack")
        self._Stack_pss_total_ = meminfo[0]
        self._Stack_private_dirty_ = meminfo[1]
        self._Stack_private_clean_ = meminfo[2]
        self._Stack_swapped_dirty_ = meminfo[3]
        return meminfo

    def Cursor(self):
        meminfo = self.get_memory_list("Cursor")
        self._Cursor_pss_total_ = meminfo[0]
        self._Cursor_private_dirty_ = meminfo[1]
        self._Cursor_private_clean_ = meminfo[2]
        self._Cursor_swapped_dirty_ = meminfo[3]
        return meminfo

    def ashmem(self):
        meminfo = self.get_memory_list("ashmem")
        self._ashmem_pss_total_ = meminfo[0]
        self._ashmem_private_dirty_ = meminfo[1]
        self._ashmem_private_clean_ = meminfo[2]
        self._ashmem_swapped_dirty_ = meminfo[3]
        return meminfo

    def gfx_dev(self):
        meminfo = self.get_memory_list("gfx dev")
        self._gfx_dev_pss_total_ = meminfo[0]
        self._gfx_dev_private_dirty_ = meminfo[1]
        self._gfx_dev_private_clean_ = meminfo[2]
        self._gfx_dev_swapped_dirty_ = meminfo[3]
        return meminfo

    def alloc_dev(self):
        meminfo = self.get_memory_list("alloc dev")
        self._alloc_dev_pss_total_ = meminfo[0]
        self._alloc_dev_private_dirty_ = meminfo[1]
        self._alloc_dev_private_clean_ = meminfo[2]
        self._alloc_dev_swapped_dirty_ = meminfo[3]
        return meminfo

    def file_so_mmap(self):
        meminfo = self.get_memory_list(".so mmap")
        self._file_so_mmap_pss_total_ = meminfo[0]
        self._file_so_mmap_private_dirty_ = meminfo[1]
        self._file_so_mmap_private_clean_ = meminfo[2]
        self._file_so_mmap_swapped_dirty_ = meminfo[3]
        return meminfo

    def file_apk_mmap(self):
        meminfo = self.get_memory_list(".apk mmap")
        self._file_apk_mmap_pss_total_ = meminfo[0]
        self._file_apk_mmap_private_dirty_ = meminfo[1]
        self._file_apk_mmap_private_clean_ = meminfo[2]
        self._file_apk_mmap_swapped_dirty_ = meminfo[3]
        return meminfo

    def file_ttf_mmap(self):
        meminfo = self.get_memory_list(".ttf mmap")
        self._file_ttf_mmap_pss_total_ = meminfo[0]
        self._file_ttf_mmap_private_dirty_ = meminfo[1]
        self._file_ttf_mmap_private_clean_ = meminfo[2]
        self._file_ttf_mmap_swapped_dirty_ = meminfo[3]
        return meminfo

    def file_dex_mmap(self):
        meminfo = self.get_memory_list(".dex mmap")
        self._file_dex_mmap_pss_total_ = meminfo[0]
        self._file_dex_mmap_private_dirty_ = meminfo[1]
        self._file_dex_mmap_private_clean_ = meminfo[2]
        self._file_dex_mmap_swapped_dirty_ = meminfo[3]
        return meminfo

    def file_oat_mmap(self):
        meminfo = self.get_memory_list(".oat mmap")
        self._file_oat_mmap_pss_total_ = meminfo[0]
        self._file_oat_mmap_private_dirty_ = meminfo[1]
        self._file_oat_mmap_private_clean_ = meminfo[2]
        self._file_oat_mmap_swapped_dirty_ = meminfo[3]
        return meminfo

    def file_art_mmap(self):
        meminfo = self.get_memory_list(".art mmap")
        self._file_art_mmap_pss_total_ = meminfo[0]
        self._file_art_mmap_private_dirty_ = meminfo[1]
        self._file_art_mmap_private_clean_ = meminfo[2]
        self._file_art_mmap_swapped_dirty_ = meminfo[3]
        return meminfo

    def alloc_mmap(self):
        meminfo = self.get_memory_list("alloc mmap")
        self._alloc_mmap_pss_total_ = meminfo[0]
        self._alloc_mmap_private_dirty_ = meminfo[1]
        self._alloc_mmap_private_clean_ = meminfo[2]
        self._alloc_mmap_swapped_dirty_ = meminfo[3]
        return meminfo

    def unknown(self):
        meminfo = self.get_memory_list("Unknown")
        self._Unknown_pss_total_ = meminfo[0]
        self._Unknown_private_dirty_ = meminfo[1]
        self._Unknown_private_clean_ = meminfo[2]
        self._Unknown_swapped_dirty_ = meminfo[3]
        return meminfo

    def total(self):
        meminfo = self.get_memory_list("total")
        self._total_pss_total_ = meminfo[0]
        self._total_private_dirty_ = meminfo[1]
        self._total_private_clean_ = meminfo[2]
        self._total_swapped_dirty_ = meminfo[3]
        self._total_heap_size_ = meminfo[4]
        self._total_heap_alloc_ = meminfo[5]
        self._total_heap_free_ = meminfo[6]
        return meminfo
