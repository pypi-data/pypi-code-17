# coding=utf-8

'''
 :Description:    设备类
 :author          80071482/bony
 :@version         V1.0
 :@Date            2016年11月
'''
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
    Meminfo_Text = None
    Native_Heap_Pss_Total = None
    Native_Heap_Private_Dirty = None
    Native_Heap_Private_Clean = None
    Native_Heap_Swapped_Dirty = None
    Native_Heap_Heap_Size = None
    Native_Heap_Heap_Alloc = None
    Native_Heap_Heap_Free = None
    Dalvik_Heap_Pss_Total = None
    Dalvik_Heap_Private_Dirty = None
    Dalvik_Heap_Private_Clean = None
    Dalvik_Heap_Swapped_Dirty = None
    Dalvik_Heap_Heap_Size = None
    Dalvik_Heap_Heap_Alloc = None
    Dalvik_Heap_Heap_Free = None
    Dalvik_Other_Pss_Total = None
    Dalvik_Other_Private_Dirty = None
    Dalvik_Other_Private_Clean = None
    Dalvik_Other_Swapped_Dirty = None
    Stack_Pss_Total = None
    Stack_Private_Dirty = None
    Stack_Private_Clean = None
    Stack_Swapped_Dirty = None
    Cursor_Pss_Total = None
    Cursor_Private_Dirty = None
    Cursor_Private_Clean = None
    Cursor_Swapped_Dirty = None
    Ashmem_Pss_Total = None
    Ashmem_Private_Dirty = None
    Ashmem_Private_Clean = None
    Ashmem_Swapped_Dirty = None
    Gfx_dev_Pss_Total = None
    Gfx_dev_Private_Dirty = None
    Gfx_dev_Private_Clean = None
    Gfx_dev_Swapped_Dirty = None
    Other_dev_Pss_Total = None
    Other_dev_Private_Dirty = None
    Other_dev_Private_Clean = None
    Other_dev_Swapped_Dirty = None
    file_so_mmap_Pss_Total = None
    file_so_mmap_Private_Dirty = None
    file_so_mmap_Private_Clean = None
    file_so_mmap_Swapped_Dirty = None
    file_apk_mmap_Pss_Total = None
    file_apk_mmap_Private_Dirty = None
    file_apk_mmap_Private_Clean = None
    file_apk_mmap_Swapped_Dirty = None
    file_ttf_mmap_Pss_Total = None
    file_ttf_mmap_Private_Dirty = None
    file_ttf_mmap_Private_Clean = None
    file_ttf_mmap_Swapped_Dirty = None
    file_dex_mmap_Pss_Total = None
    file_dex_mmap_Private_Dirty = None
    file_dex_mmap_Private_Clean = None
    file_dex_mmap_Swapped_Dirty = None
    file_oat_mmap_Pss_Total = None
    file_oat_mmap_Private_Dirty = None
    file_oat_mmap_Private_Clean = None
    file_oat_mmap_Swapped_Dirty = None
    file_art_mmap_Pss_Total = None
    file_art_mmap_Private_Dirty = None
    file_art_mmap_Private_Clean = None
    file_art_mmap_Swapped_Dirty = None
    Other_mmap_Pss_Total = None
    Other_mmap_Private_Dirty = None
    Other_mmap_Private_Clean = None
    Other_mmap_Swapped_Dirty = None
    Unknown_Pss_Total = None
    Unknown_Private_Dirty = None
    Unknown_Private_Clean = None
    Unknown_Swapped_Dirty = None
    TOTAL_Pss_Total = None
    TOTAL_Private_Dirty = None
    TOTAL_Private_Clean = None
    TOTAL_Swapped_Dirty = None
    TOTAL_Heap_Size = None
    TOTAL_Heap_Alloc = None
    TOTAL_Heap_Free = None

    def __init__(self, device=None, packgename=None):
        """
        对象初始化
        """
        self.device = device
        if packgename != None:
            self.get_meminfo_text(device, packgename)
            self.Native_Heap()
            self.Native_Heap()
            self.Native_Heap()
            self.Native_Heap()
            self.Dalvik_Heap()
            self.Dalvik_Other()
            self.Stack()
            self.Cursor()
            self.Native_Heap()
            self.Ashmem()
            self.Gfx_dev()
            self.Other_dev()
            self.file_so_mmap()
            self.file_apk_mmap()
            self.file_ttf_mmap()
            self.file_dex_mmap()
            self.file_oat_mmap()
            self.file_art_mmap()
            self.Other_mmap()
            self.Unknown()
            self.TOTAL()

    def get_meminfo_text(self, device, packgename):
        """
        获取内存信息
        """
        self.Meminfo_Text = device.script("adb shell dumpsys meminfo %s" % (packgename))
        pass

    def getMemoryList(self, category):
        """
        获取某项的内存信息
        """
        if self.Meminfo_Text != None:
            meminfo_list = self.Meminfo_Text.split("\n")
            for meminfo in meminfo_list:
                if category in meminfo:
                    pattern = re.compile(r"\d+")
                    return pattern.findall(meminfo)

    def Native_Heap(self):
        meminfo = self.getMemoryList("Native Heap")
        self.Native_Heap_Pss_Total = meminfo[0]
        self.Native_Heap_Private_Dirty = meminfo[1]
        self.Native_Heap_Private_Clean = meminfo[2]
        self.Native_Heap_Swapped_Dirty = meminfo[3]
        self.Native_Heap_Heap_Size = meminfo[4]
        self.Native_Heap_Heap_Alloc = meminfo[5]
        self.Native_Heap_Heap_Free = meminfo[6]
        return meminfo

    def Dalvik_Heap(self):
        meminfo = self.getMemoryList("Dalvik Heap")
        self.Dalvik_Heap_Pss_Total = meminfo[0]
        self.Dalvik_Heap_Private_Dirty = meminfo[1]
        self.Dalvik_Heap_Private_Clean = meminfo[2]
        self.Dalvik_Heap_Swapped_Dirty = meminfo[3]
        self.Dalvik_Heap_Heap_Size = meminfo[4]
        self.Dalvik_Heap_Heap_Alloc = meminfo[5]
        self.Dalvik_Heap_Heap_Free = meminfo[6]
        return meminfo

    def Dalvik_Other(self):
        meminfo = self.getMemoryList("Dalvik Other")
        self.Dalvik_Other_Pss_Total = meminfo[0]
        self.Dalvik_Other_Private_Dirty = meminfo[1]
        self.Dalvik_Other_Private_Clean = meminfo[2]
        self.Dalvik_Other_Swapped_Dirty = meminfo[3]
        return meminfo

    def Stack(self):
        meminfo = self.getMemoryList("Stack")
        self.Stack_Pss_Total = meminfo[0]
        self.Stack_Private_Dirty = meminfo[1]
        self.Stack_Private_Clean = meminfo[2]
        self.Stack_Swapped_Dirty = meminfo[3]
        return meminfo

    def Cursor(self):
        meminfo = self.getMemoryList("Cursor")
        self.Cursor_Pss_Total = meminfo[0]
        self.Cursor_Private_Dirty = meminfo[1]
        self.Cursor_Private_Clean = meminfo[2]
        self.Cursor_Swapped_Dirty = meminfo[3]
        return meminfo

    def Ashmem(self):
        meminfo = self.getMemoryList("Ashmem")
        self.Ashmem_Pss_Total = meminfo[0]
        self.Ashmem_Private_Dirty = meminfo[1]
        self.Ashmem_Private_Clean = meminfo[2]
        self.Ashmem_Swapped_Dirty = meminfo[3]
        return meminfo

    def Gfx_dev(self):
        meminfo = self.getMemoryList("Gfx dev")
        self.Gfx_dev_Pss_Total = meminfo[0]
        self.Gfx_dev_Private_Dirty = meminfo[1]
        self.Gfx_dev_Private_Clean = meminfo[2]
        self.Gfx_dev_Swapped_Dirty = meminfo[3]
        return meminfo

    def Other_dev(self):
        meminfo = self.getMemoryList("Other dev")
        self.Other_dev_Pss_Total = meminfo[0]
        self.Other_dev_Private_Dirty = meminfo[1]
        self.Other_dev_Private_Clean = meminfo[2]
        self.Other_dev_Swapped_Dirty = meminfo[3]
        return meminfo

    def file_so_mmap(self):
        meminfo = self.getMemoryList(".so mmap")
        self.file_so_mmap_Pss_Total = meminfo[0]
        self.file_so_mmap_Private_Dirty = meminfo[1]
        self.file_so_mmap_Private_Clean = meminfo[2]
        self.file_so_mmap_Swapped_Dirty = meminfo[3]
        return meminfo

    def file_apk_mmap(self):
        meminfo = self.getMemoryList(".apk mmap")
        self.file_apk_mmap_Pss_Total = meminfo[0]
        self.file_apk_mmap_Private_Dirty = meminfo[1]
        self.file_apk_mmap_Private_Clean = meminfo[2]
        self.file_apk_mmap_Swapped_Dirty = meminfo[3]
        return meminfo

    def file_ttf_mmap(self):
        meminfo = self.getMemoryList(".ttf mmap")
        self.file_ttf_mmap_Pss_Total = meminfo[0]
        self.file_ttf_mmap_Private_Dirty = meminfo[1]
        self.file_ttf_mmap_Private_Clean = meminfo[2]
        self.file_ttf_mmap_Swapped_Dirty = meminfo[3]
        return meminfo

    def file_dex_mmap(self):
        meminfo = self.getMemoryList(".dex mmap")
        self.file_dex_mmap_Pss_Total = meminfo[0]
        self.file_dex_mmap_Private_Dirty = meminfo[1]
        self.file_dex_mmap_Private_Clean = meminfo[2]
        self.file_dex_mmap_Swapped_Dirty = meminfo[3]
        return meminfo

    def file_oat_mmap(self):
        meminfo = self.getMemoryList(".oat mmap")
        self.file_oat_mmap_Pss_Total = meminfo[0]
        self.file_oat_mmap_Private_Dirty = meminfo[1]
        self.file_oat_mmap_Private_Clean = meminfo[2]
        self.file_oat_mmap_Swapped_Dirty = meminfo[3]
        return meminfo

    def file_art_mmap(self):
        meminfo = self.getMemoryList(".art mmap")
        self.file_art_mmap_Pss_Total = meminfo[0]
        self.file_art_mmap_Private_Dirty = meminfo[1]
        self.file_art_mmap_Private_Clean = meminfo[2]
        self.file_art_mmap_Swapped_Dirty = meminfo[3]
        return meminfo

    def Other_mmap(self):
        meminfo = self.getMemoryList("Other mmap")
        self.Other_mmap_Pss_Total = meminfo[0]
        self.Other_mmap_Private_Dirty = meminfo[1]
        self.Other_mmap_Private_Clean = meminfo[2]
        self.Other_mmap_Swapped_Dirty = meminfo[3]
        return meminfo

    def Unknown(self):
        meminfo = self.getMemoryList("Unknown")
        self.Unknown_Pss_Total = meminfo[0]
        self.Unknown_Private_Dirty = meminfo[1]
        self.Unknown_Private_Clean = meminfo[2]
        self.Unknown_Swapped_Dirty = meminfo[3]
        return meminfo

    def TOTAL(self):
        meminfo = self.getMemoryList("TOTAL")
        self.TOTAL_Pss_Total = meminfo[0]
        self.TOTAL_Private_Dirty = meminfo[1]
        self.TOTAL_Private_Clean = meminfo[2]
        self.TOTAL_Swapped_Dirty = meminfo[3]
        self.TOTAL_Heap_Size = meminfo[4]
        self.TOTAL_Heap_Alloc = meminfo[5]
        self.TOTAL_Heap_Free = meminfo[6]
        return meminfo
