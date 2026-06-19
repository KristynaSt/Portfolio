"""
Remote DLL injection using ctypes.
1. Allocate memory in a remote process.
2. Write a DLL location into the remote memory.
3. Have the external process load the DLL using load library. 
"""


from ctypes import *
from ctypes import wintypes

kernel32 = windll.kernel32
LPCTSTR = c_char_p #Long Pointer to Constant TCHAR String
SIZE_T = c_size_t

