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
    def __init__(self, device=None, package=None):
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
        self._stack_private_dirty_ = None
        self._stack_private_clean_ = None
        self._stack_swapped_dirty_ = None
        self._cursor_pss_total_ = None
        self._cursor_private_dirty_ = None
        self._cursor_private_clean_ = None
        self._cursor_swapped_dirty_ = None
        self._ashmem_pss_total_ = None
        self._ashmem_private_dirty_ = None
        self._ashmem_private_clean_ = None
        self._ashmem_swapped_dirty_ = None
        self._other_dev_pss_total_ = None
        self._other_dev_private_dirty_ = None
        self._other_dev_private_clean_ = None
        self._other_dev_swapped_dirty_ = None
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
        self._other_mmap_pss_total_ = None
        self._other_mmap_private_dirty_ = None
        self._other_mmap_private_clean_ = None
        self._other_mmap_swapped_dirty_ = None
        self._alloc_mmap_pss_total_ = None
        self._alloc_mmap_private_dirty_ = None
        self._alloc_mmap_private_clean_ = None
        self._alloc_mmap_swapped_dirty_ = None
        self._gl_mtrack_pss_total_ = None
        self._gl_mtrack_private_dirty_ = None
        self._gl_mtrack_private_clean_ = None
        self._gl_mtrack_swapped_dirty_ = None
        self._egl_mtrack_pss_total_ = None
        self._egl_mtrack_private_dirty_ = None
        self._egl_mtrack_private_clean_ = None
        self._egl_mtrack_swapped_dirty_ = None
        self._unknown_pss_total_ = None
        self._unknown_private_dirty_ = None
        self._unknown_private_clean_ = None
        self._unknown_swapped_dirty_ = None
        self._total_pss_total_ = None
        self._total_private_dirty_ = None
        self._total_private_clean_ = None
        self._total_swapped_dirty_ = None
        self._total_heap_size_ = None
        self._total_heap_alloc_ = None
        self._total_heap_free_ = None
        self._device_ = None
        self._package_ = package or self._device_.get_focused_package_activity().split("\\")[0]
        """
        对象初始化
        """
        self._device_ = device

    def get_meminfo_text(self):
        """
        获取内存信息
        """
        self._meminfo_text_ = self._device_.script("adb shell dumpsys meminfo %s" % self._package_)
        pass

    def update(self):
        self.get_meminfo_text()
        self.native_heap()
        self.dalvik_heap()
        self.dalvik_alloc()
        self.stack()
        self.cursor()
        self.ashmem()
        self.gfx_dev()
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
        self.other_dev()
        self.other_mmap()
        self.egl_mtrack()
        self.gl_mtrack()

    def get_memory_list(self, category):
        """
        获取某项的内存信息
        """
        if self._meminfo_text_ is not None:
            meminfo_list = self._meminfo_text_.split("\n")
            for meminfo in meminfo_list:
                if category in meminfo:
                    pattern = re.compile(r"\d+")
                    ret = pattern.findall(meminfo)
                    return ret
            return None
        else:
            return None

    def native_heap(self):
        meminfo = self.get_memory_list("Native Heap")
        if meminfo is not None:
            self._native_heap_pss_total_ = meminfo[0]
            self._native_heap_private_dirty_ = meminfo[1]
            self._native_heap_private_clean_ = meminfo[2]
            self._native_heap_swapped_dirty_ = meminfo[3]
            self._native_heap_heap_size_ = meminfo[4]
            self._native_heap_heap_alloc_ = meminfo[5]
            self._native_heap_heap_free_ = meminfo[6]
        return meminfo

    def dalvik_heap(self):
        meminfo = self.get_memory_list("Dalvik Heap")
        if meminfo is not None:
            self._dalvik_heap_pss_total_ = meminfo[0]
            self._dalvik_heap_private_dirty_ = meminfo[1]
            self._dalvik_heap_private_clean_ = meminfo[2]
            self._dalvik_heap_swapped_dirty_ = meminfo[3]
            self._dalvik_heap_heap_size_ = meminfo[4]
            self._dalvik_heap_heap_alloc_ = meminfo[5]
            self._dalvik_heap_heap_free_ = meminfo[6]
        return meminfo

    def dalvik_alloc(self):
        meminfo = self.get_memory_list("Dalvik Alloc")
        if meminfo is not None:
            self._dalvik_alloc_pss_total_ = meminfo[0]
            self._dalvik_alloc_private_dirty_ = meminfo[1]
            self._dalvik_alloc_private_clean_ = meminfo[2]
            self._dalvik_alloc_swapped_dirty_ = meminfo[3]
        return meminfo

    def stack(self):
        meminfo = self.get_memory_list("Stack")
        if meminfo is not None:
            self._stack_pss_total_ = meminfo[0]
            self._stack_private_dirty_ = meminfo[1]
            self._stack_private_clean_ = meminfo[2]
            self._stack_swapped_dirty_ = meminfo[3]
        return meminfo

    def cursor(self):
        meminfo = self.get_memory_list("Cursor")
        if meminfo is not None:
            self._cursor_pss_total_ = meminfo[0]
            self._cursor_private_dirty_ = meminfo[1]
            self._cursor_private_clean_ = meminfo[2]
            self._cursor_swapped_dirty_ = meminfo[3]
        return meminfo

    def ashmem(self):
        meminfo = self.get_memory_list("Ashmem")
        if meminfo is not None:
            self._ashmem_pss_total_ = meminfo[0]
            self._ashmem_private_dirty_ = meminfo[1]
            self._ashmem_private_clean_ = meminfo[2]
            self._ashmem_swapped_dirty_ = meminfo[3]
        return meminfo

    def gfx_dev(self):
        meminfo = self.get_memory_list("Gfx Dev")
        if meminfo is not None:
            self._gfx_dev_pss_total_ = meminfo[0]
            self._gfx_dev_private_dirty_ = meminfo[1]
            self._gfx_dev_private_clean_ = meminfo[2]
            self._gfx_dev_swapped_dirty_ = meminfo[3]
        return meminfo

    def alloc_dev(self):
        meminfo = self.get_memory_list("Alloc Dev")
        if meminfo is not None:
            self._alloc_dev_pss_total_ = meminfo[0]
            self._alloc_dev_private_dirty_ = meminfo[1]
            self._alloc_dev_private_clean_ = meminfo[2]
            self._alloc_dev_swapped_dirty_ = meminfo[3]
        return meminfo

    def other_dev(self):
        meminfo = self.get_memory_list("Other dev")
        if meminfo is not None:
            self._other_dev_pss_total_ = meminfo[0]
            self._other_dev_private_dirty_ = meminfo[1]
            self._other_dev_private_clean_ = meminfo[2]
            self._other_dev_swapped_dirty_ = meminfo[3]
        return meminfo

    def file_so_mmap(self):
        meminfo = self.get_memory_list(".so mmap")
        if meminfo is not None:
            self._file_so_mmap_pss_total_ = meminfo[0]
            self._file_so_mmap_private_dirty_ = meminfo[1]
            self._file_so_mmap_private_clean_ = meminfo[2]
            self._file_so_mmap_swapped_dirty_ = meminfo[3]
        return meminfo

    def file_apk_mmap(self):
        meminfo = self.get_memory_list(".apk mmap")
        if meminfo is not None:
            self._file_apk_mmap_pss_total_ = meminfo[0]
            self._file_apk_mmap_private_dirty_ = meminfo[1]
            self._file_apk_mmap_private_clean_ = meminfo[2]
            self._file_apk_mmap_swapped_dirty_ = meminfo[3]
        return meminfo

    def file_ttf_mmap(self):
        meminfo = self.get_memory_list(".ttf mmap")
        if meminfo is not None:
            self._file_ttf_mmap_pss_total_ = meminfo[0]
            self._file_ttf_mmap_private_dirty_ = meminfo[1]
            self._file_ttf_mmap_private_clean_ = meminfo[2]
            self._file_ttf_mmap_swapped_dirty_ = meminfo[3]
        return meminfo

    def file_dex_mmap(self):
        meminfo = self.get_memory_list(".dex mmap")
        if meminfo is not None:
            self._file_dex_mmap_pss_total_ = meminfo[0]
            self._file_dex_mmap_private_dirty_ = meminfo[1]
            self._file_dex_mmap_private_clean_ = meminfo[2]
            self._file_dex_mmap_swapped_dirty_ = meminfo[3]
        return meminfo

    def file_oat_mmap(self):
        meminfo = self.get_memory_list(".oat mmap")
        if meminfo is not None:
            self._file_oat_mmap_pss_total_ = meminfo[0]
            self._file_oat_mmap_private_dirty_ = meminfo[1]
            self._file_oat_mmap_private_clean_ = meminfo[2]
            self._file_oat_mmap_swapped_dirty_ = meminfo[3]
        return meminfo

    def file_art_mmap(self):
        meminfo = self.get_memory_list(".art mmap")
        if meminfo is not None:
            self._file_art_mmap_pss_total_ = meminfo[0]
            self._file_art_mmap_private_dirty_ = meminfo[1]
            self._file_art_mmap_private_clean_ = meminfo[2]
            self._file_art_mmap_swapped_dirty_ = meminfo[3]
        return meminfo

    def other_mmap(self):
        meminfo = self.get_memory_list("Other mmap")
        if meminfo is not None:
            self._other_mmap_pss_total_ = meminfo[1]
            self._other_mmap_private_dirty_ = meminfo[1]
            self._other_mmap_private_clean_ = meminfo[2]
            self._other_mmap_swapped_dirty_ = meminfo[3]
        return meminfo

    def alloc_mmap(self):
        meminfo = self.get_memory_list("Alloc mmap")
        if meminfo is not None:
            self._alloc_mmap_pss_total_ = meminfo[0]
            self._alloc_mmap_private_dirty_ = meminfo[1]
            self._alloc_mmap_private_clean_ = meminfo[2]
            self._alloc_mmap_swapped_dirty_ = meminfo[3]
        return meminfo

    def egl_mtrack(self):
        meminfo = self.get_memory_list("EGL mtrack")
        if meminfo is not None:
            self._egl_mtrack_pss_total_ = meminfo[0]
            self._egl_mtrack_private_dirty_ = meminfo[1]
            self._egl_mtrack_private_clean_ = meminfo[2]
            self._egl_mtrack_swapped_dirty_ = meminfo[3]
        return meminfo

    def gl_mtrack(self):
        meminfo = self.get_memory_list("GL mtrack")
        if meminfo is not None:
            self._gl_mtrack_pss_total_ = meminfo[0]
            self._gl_mtrack_private_dirty_ = meminfo[1]
            self._gl_mtrack_private_clean_ = meminfo[2]
            self._gl_mtrack_swapped_dirty_ = meminfo[3]
        return meminfo

    def unknown(self):
        meminfo = self.get_memory_list("Unknown")
        if meminfo is not None:
            self._unknown_pss_total_ = meminfo[0]
            self._unknown_private_dirty_ = meminfo[1]
            self._unknown_private_clean_ = meminfo[2]
            self._unknown_swapped_dirty_ = meminfo[3]
        return meminfo

    def total(self):
        meminfo = self.get_memory_list("TOTAL")
        if meminfo is not None:
            print(meminfo)
            self._total_pss_total_ = meminfo[0]
            self._total_private_dirty_ = meminfo[1]
            self._total_private_clean_ = meminfo[2]
            self._total_swapped_dirty_ = meminfo[3]
            self._total_heap_size_ = meminfo[4]
            self._total_heap_alloc_ = meminfo[5]
            self._total_heap_free_ = meminfo[6]
        return meminfo
