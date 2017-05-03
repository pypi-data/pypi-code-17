__all__=["ksSys","ksApp"]

import ctypes

DEFAULT_WINDOWS_VKEYS = {   
                            "LBUTTON":0x01, # (Left mouse button)
                            "RBUTTON":0x02, # (Right mouse button)
                            "CANCEL":0x03, # (Control-break processing)
                            "MBUTTON":0x04, # (Middle mouse button)
                            "XBUTTON1":0x05, # (X1 mouse button)
                            "XBUTTON2":0x06, # (X2 mouse button)
                            "BACK":0x08, # (BACKSPACE key)
                            "TAB":0x09, # (TAB key)

                            "CLEAR":0x0C, # (CLEAR key)
                            "RETURN":0x0D, # (ENTER key)
                            "SHIFT":0x10, # (SHIFT key)
                            "CONTROL":0x11, # (CTRL key)
                            "MENU":0x12, # (ALT key)
                            "PAUSE":0x13, # (PAUSE key)
                            "CAPITAL":0x14, # (CAPS LOCK key)
                            "KANA":0x15, # (IME Kana mode)
                            "HANGUL":0x15, # (IME Hangul mode)
                            "HANGUEL":0x15, # (IME Hangeul mode)
                            "JUNJA":0x17, # (IME Jungja mode)
                            "FINAL":0x18, # (IME Final mode)
                            "KANJI":0x19, # (IME Kanji mode)
                            "HANGJA":0x19, # (IME Hangja mode)
                            "ESCAPE":0x1b, # (ESC key)
                            "CONVERT":0x1C, # (IME convert)
                            "NONCONVERT":0x1D, # (IME nonconvert)
                            "ACCEPT":0x1E, # (IME accept)
                            "MODECHANGE":0x1F, # (IME mode change request)
                            "SPACE":0x20, # (SPACEBAR key)
                            "PRIOR":0x21, # (PAGE UP key)
                            "NEXT":0x22, # (PAGE DOWN key)
                            "END":0x23, # (END key)
                            "HOME":0x24, # (HOME key)
                            "LEFT":0x25, # (LEFT ARROW key)
                            "UP":0x26, # (UP ARROW key)
                            "RIGHT":0x27, # (RIGHT ARROW key)
                            "DOWN":0x28, # (DOWN ARROW key)
                            "SELECT":0x29, # (SELECT key)
                            "PRINT":0x2A, # (PRINT key)
                            "EXECUTE":0x2B, # (EXECUTE key)
                            "SNAPSHOT":0x2C, # (PRINT SCREEN key)
                            "INSERT":0x2D, # (INS key)
                            "DELETE":0x2E, # (DEL key)
                            "HELP":0x2F, # (HELP key)
                            "0":0x30, # (0 key)
                            "1":0x31, # (1 key)
                            "2":0x32, # (2 key)
                            "3":0x33, # (3 key)
                            "4":0x34, # (4 key)
                            "5":0x35, # (5 key)
                            "6":0x36, # (6 key)
                            "7":0x37, # (7 key)
                            "8":0x38, # (8 key)
                            "9":0x39, # (9 key)

                            "A":0x41, # (A key)
                            "B":0x42, # (B key)
                            "C":0x43, # (C key)
                            "D":0x44, # (D key)
                            "E":0x45, # (E key)
                            "F":0x46, # (F key)
                            "G":0x47, # (G key)
                            "H":0x48, # (H key)
                            "I":0x49, # (I key)
                            "J":0x4A, # (J key)
                            "K":0x4B, # (K key)
                            "L":0x4C, # (L key)
                            "M":0x4D, # (M key)
                            "N":0x4E, # (N key)
                            "O":0x4F, # (O key)
                            "P":0x50, # (P key)
                            "Q":0x51, # (Q key)
                            "R":0x52, # (R key)
                            "S":0x53, # (S key)
                            "T":0x54, # (T key)
                            "U":0x55, # (U key)
                            "V":0x56, # (V key)
                            "W":0x57, # (W key)
                            "X":0x58, # (X key)
                            "Y":0x59, # (Y key)
                            "Z":0x5A, # (Z key)
                            "LWIN":0x5B, # (Left Windows key)
                            "RWIN":0x5C, # (Right Windows key)
                            "APPS":0x5D, # (Applications/Menu key)
                            "POWER":0x5E, # (Computer Power key)
                            "SLEEP":0x5F, # (Computer Sleep key)
                            "NUMPAD0":0x60, # (Numeric keypad 0 key)
                            "NUMPAD1":0x61, # (Numeric keypad 1 key)
                            "NUMPAD2":0x62, # (Numeric keypad 2 key)
                            "NUMPAD3":0x63, # (Numeric keypad 3 key)
                            "NUMPAD4":0x64, # (Numeric keypad 4 key)
                            "NUMPAD5":0x65, # (Numeric keypad 5 key)
                            "NUMPAD6":0x66, # (Numeric keypad 6 key)
                            "NUMPAD7":0x67, # (Numeric keypad 7 key)
                            "NUMPAD8":0x68, # (Numeric keypad 8 key)
                            "NUMPAD9":0x69, # (Numeric keypad 9 key)
                            "MULTIPLY":0x6A, # (Numeric keypad Multiply key)
                            "ADD":0x6B, # (Numeric keypad Add key)
                            "SEPARATOR":0x6C, # (Separator key)
                            "SUBTRACT":0x6D, # (Numeric keypad Subtract key)
                            "DECIMAL":0x6E, # (Numeric keypad Decimal key)
                            "DIVIDE":0x6F, # (Numeric keypad Divide key)
                            "F1":0x70, # (F1 key)
                            "F2":0x71, # (F2 key)
                            "F3":0x72, # (F3 key)
                            "F4":0x73, # (F4 key)
                            "F5":0x74, # (F5 key)
                            "F6":0x75, # (F6 key)
                            "F7":0x76, # (F7 key)
                            "F8":0x77, # (F8 key)
                            "F9":0x78, # (F9 key)
                            "F10":0x79, # (F10 key)
                            "F11":0x7A, # (F11 key)
                            "F12":0x7B, # (F12 key)
                            "F13":0x7C, # (F13 key)
                            "F14":0x7D, # (F14 key)
                            "F15":0x7E, # (F15 key)
                            "F16":0x7F, # (F16 key)
                            "F17":0x80, # (F17 key)
                            "F18":0x81, # (F18 key)
                            "F19":0x82, # (F19 key)
                            "F20":0x83, # (F20 key)
                            "F21":0x84, # (F21 key)
                            "F22":0x85, # (F22 key)
                            "F23":0x86, # (F23 key)
                            "F24":0x87, # (F24 key)

                            "NUMLOCK":0x90, # (NUM LOCK key)
                            "SCROLL":0x91, # (SCROLL LOCK key)
                            "OEM_FJ_JISHO":0x92, # (OEM Fj Jisho)
                            "OEM_FJ_MASSHOU":0x93, # (OEM Fj Masshou)
                            "OEM_FJ_TOUROKU":0x94, # (OEM Fj Touroku)
                            "OEM_FJ_LOYA":0x95, # (OEM Fj Loya)
                            "OEM_FJ_ROYA":0x96, # (OEM Fj Roya)

                            "LSHIFT":0xA0, # (Left SHIFT key)
                            "RSHIFT":0xA1, # (Right SHIFT key)
                            "LCONTROL":0xA2, # (Left CONTROL key)
                            "RCONTROL":0xA3, # (Right CONTROL key)
                            "LMENU":0xA4, # (Left ALT key)
                            "RMENU":0xA5, # (Right ALT key OR ALTGR key)
                            "BROWSER_BACK":0xA6, # (Browser Back key)
                            "BROWSER_FORWARD":0xA7, # (Browser Forward key)
                            "BROWSER_REFRESH":0xA8, # (Browser Refresh key)
                            "BROWSER_STOP":0xA9, # (Browser Stop key)
                            "BROWSER_SEARCH":0xAA, # (Browser Search key)
                            "BROWSER_FAVORITES":0xAB, # (Browser Favorites key)
                            "BROWSER_HOME":0xAC, # (Browser Start/Home key)
                            "VOLUME_MUTE":0xAD, # (Volume Mute key)
                            "VOLUME_DOWN":0xAE, # (Volume Down key)
                            "VOLUME_UP":0xAF, # (Volume Up key)
                            "MEDIA_NEXT_TRACK":0xB0, # (Next Track key)
                            "MEDIA_PREV_TRACK":0xB1, # (Previous Track key)
                            "MEDIA_STOP":0xB2, # (Stop Media key)
                            "MEDIA_PLAY_PAUSE":0xB3, # (Play/Pause Media key)
                            "LAUNCH_MAIL":0xB4, # (Start Mail key)
                            "LAUNCH_MEDIA_SELECT":0xB5, # (Select Media key)
                            "LAUNCH_APP1":0xB6, # (Start Aapplication 1 key)
                            "LAUNCH_APP2":0xB7, # (Start Application 2 key)

                            "OEM_1":0xBA, # (Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the ';:' key)
                            "OEM_PLUS":0xBB, # (For any country/region, the '+=' key)
                            "OEM_COMMA":0xBC, # (For any country/region, the '<,' key)
                            "OEM_MINUS":0xBD, # (For any country/region, the '_-' key)
                            "OEM_PERIOD":0xBE, # (For any country/region, the '>.' key)
                            "OEM_2":0xBF, # (Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '/?' key)
                            "OEM_3":0xC0, # (Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '`~' key)
                            "ABNT_C1":0xC1, # (ABNT C1)
                            "ABNT_C2":0xC2, # (ABNT C1)

                            "OEM_4":0xDB, # (Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '[{' key)
                            "OEM_5":0xDC, # (Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '\|' key)
                            "OEM_6":0xDD, # (Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the ']}' key)
                            "OEM_7":0xDE, # (Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the ''"' key)
                            "OEM_8":0xDF, # (Used for miscellaneous characters; it can vary by keyboard.)

                            "OEM_AX":0xE1, # (Ax)
                            "OEM_102":0xE2, # (Either the '<>' key or the '\|' key on the RT 102-key keyboard)
                            "OEM_ICO_HELP":0xE3, # (OEM Ico Help)
                            "OEM_ICO_00":0xE4, # (OEM Ico 00)
                            "PROCESSKEY":0xE5, # (IME PROCESS key)
                            "OEM_ICO_CLEAR":0xE6, # (OEM Ico Clear)
                            "PACKET":0xE7, # (Used to pass Unicode characters as if they were keystrokes. Low word 32-bit Virtual Key value used for non-keyboard input methods)
                            "SYSRQ":0xE8, # (SysRq for Linux systems. This is not in the original Windows virtual key table)
                            "OEM_RESET":0xE9, # (OEM Reset)
                            "OEM_JUMP":0xEA, # (OEM Jump)
                            "OEM_PA1":0xEB, # (OEM Pa1)
                            "OEM_PA2":0xEC, # (OEM Pa2)
                            "OEM_PA3":0xED, # (OEM Pa3)
                            "OEM_WSCTRL":0xEE, # (OEM Ws Control)
                            "OEM_CUSEL":0xEF, # (OEM CuSel)
                            "OEM_ATTN":0xF0, # (Oem Attn)
                            "OEM_FINISH":0xF1, # (OEM Finish)
                            "OEM_COPY":0xF2, # (OEM Copy)
                            "OEM_AUTO":0xF3, # (Auto)
                            "OEM_ENLW":0xF4, # (OEM Enlw)
                            "OEM_BACKTAB":0xF5, # (Backtab)
                            "ATTN":0xF6, # (Attn key)
                            "CRSEL":0xF7, # (CrSel key)
                            "EXSEL":0xF8, # (ExSel key)
                            "EREOF":0xF9, # (Erase EOF key)
                            "PLAY":0xFA, # (Play key)
                            "ZOOM":0xFB, # (Zoom key)
                            "NONAME":0xFC, # (Noname)
                            "PA1":0xFD, # (PA1 key)
                            "OEM_CLEAR":0xFE, # (OEM Clear key)
                        }

#This is a table for the US 101-KEY keyboard. This can should be changed for each keyboard layout.
DEFAULT_SCODE_TO_VKEY = { #Scancodes (Extended key)
                    # scancodes | vkeys code
                            0x01:(0x1b,None), # (ESC)
                            0x02:(0x31,None), # (1)
                            0x03:(0x32,None), # (2)
                            0x04:(0x33,None), # (3)
                            0x05:(0x34,None), # (4)
                            0x06:(0x35,None), # (5)
                            0x07:(0x36,None), # (6)
                            0x08:(0x37,None), # (7)
                            0x09:(0x38,None), # (8)
                            0x0A:(0x39,None), # (9)
                            0x0B:(0x30,None), # (0)
                            0x0C:(0xBD,None), # (-)
                            0x0D:(0xBB,None), # (=)
                            0x0E:(0x08,None), # (BKSP)
                            0x0F:(0x09,None), # (TAB)
                            0x10:(0x51,0xB1), # (Q, PREV TRACK)
                            0x11:(0x57,None), # (W)
                            0x12:(0x45,None), # (E)
                            0x13:(0x52,None), # (R)
                            0x14:(0x54,None), # (T)
                            0x15:(0x59,None), # (Y)
                            0x16:(0x55,None), # (U)
                            0x17:(0x49,None), # (I)
                            0x18:(0x4F,None), # (O)
                            0x19:(0x50,0xB0), # (P, NEXT TRACK)
                            0x1A:(0xDB,None), # ([)
                            0x1B:(0xDD,None), # (])
                            0x1C:(0x0D,0x0D), # (ENTER, KP ENTER)
                            0x1D:(0xA2,0xA3), # (L CTRL, R CTRL)
                            0x1E:(0x41,None), # (A)
                            0x1F:(0x53,None), # (S) 
                            0x20:(0x44,0xAD), # (D, MUTE)
                            0x21:(0x46,None), # (F, CALC)
                            0x22:(0x47,0xB3), # (G, PLAY/PAUSE)
                            0x23:(0x48,None), # (H)
                            0x24:(0x4A,0xB2), # (J, STOP)
                            0x25:(0x4B,None), # (K)
                            0x26:(0x4C,None), # (L)
                            0x27:(0xBA,None), # (;)
                            0x28:(0xDE,None), # (')
                            0x29:(0xC0,None), # (`)
                            0x2A:(0xA0,0xA0), # (L SHIFT)
                            0x2B:(0xDC,None), # (\)
                            0x2C:(0x5A,None), # (Z, EJECT)
                            0x2D:(0x58,None), # (X)
                            0x2E:(0x43,0xAE), # (C, VOL DOWN)
                            0x2F:(0x56,None), # (V)
                            0x30:(0x42,0xAF), # (B, VOL UP)
                            0x31:(0x4E,None), # (N)
                            0x32:(0x4D,0xAC), # (M, WEB HOME)
                            0x33:(0xBC,None), # (,)
                            0x34:(0xBE,None), # (.)
                            0x35:(0xBF,0x6F), # (/, KP /)
                            0x36:(0xA1,0xA1), # (R SHIFT)
                            0x37:(0x6A,0x2A), # (KP *, PRT SCRN/STAMP)
                            0x38:(0xA4,0xA5), # (L ALT, R ALT)
                            0x39:(0x20,None), # (SPACE)
                            0x3A:(0x14,None), # (CAPS LOCK)
                            0x3B:(0x70,0x2F), # (F1, HELP)
                            0x3C:(0x71,None), # (F2, MUSIC)
                            0x3D:(0x72,None), # (F3)
                            0x3E:(0x73,None), # (F4)
                            0x3F:(0x74,None), # (F5)
                            0x40:(0x75,None), # (F6)
                            0x41:(0x76,None), # (F7)
                            0x42:(0x77,None), # (F8)
                            0x43:(0x78,None), # (F9)
                            0x44:(0x79,None), # (F10)
                            0x45:(0x13,0x90), # (PAUSE, NUM LOCK)
                            0x46:(0x91,None), # (SCR LOCK)
                            0x47:(0x67,0x24), # (KP 7, HOME)
                            0x48:(0x68,0x26), # (KP 8, U ARROW)
                            0x49:(0x69,0x21), # (KP 9, PG UP)
                            0x4A:(0x6D,None), # (KP -)
                            0x4B:(0x64,0x25), # (KP 4, L ARROW)
                            0x4C:(0x65,None), # (KP 5, RULE)
                            0x4D:(0x66,0x27), # (KP 6, R ARROW)
                            0x4E:(0x6B,None), # (KP +) 
                            0x4F:(0x61,0x23), # (KP 1, END)
                            0x50:(0x62,0x28), # (KP 2, D ARROW)
                            0x51:(0x63,0x22), # (KP 3, PG DOWN)
                            0x52:(0x60,0x2D), # (KP 0, INSERT)
                            0x53:(0x6E,0x2E), # (KP ., DELETE)
                            0x54:(0xE8,None), # (SYSRQ) used only in Linux
                            0x56:(0xE2,None), # (INT 1) mean interrupt
                            0x57:(0x7A,None), # (F11)
                            0x58:(0x7B,None), # (F12)
                            0x5B:(0x7C,0x5B), # (F13, L WIN)
                            0x5C:(0x7D,0x5C), # (F14, R WIN)
                            0x5D:(0x7E,0x5D), # (F15, APPS)
                            0x5E:(None,0x5E), # (nothing?, POWER)
                            0x5F:(None,0x5F), # (nothing?, SLEEP)
                            0x63:(0x7F,None), # (F16, WAKE) idk?
                            0x64:(0x80,None), # (F17, PICTURES) idk?
                            0x65:(0x81,0xAA), # (F18, WEB SEARCH)
                            0x66:(0x82,0xAB), # (F19, WEB FAVORITES)
                            0x67:(0x83,0xA8), # (F20, WEB REFRESH)
                            0x68:(0x84,0xA9), # (F21, WEB STOP)
                            0x69:(0x85,0xA7), # (F22, WEB FORWARD)
                            0x6A:(0x86,0xA6), # (F23, WEB BACK)
                            0x6B:(0x87,None), # (F24, MY PC) idk?
                            0x6C:(0x11,0xB4), # (CTRL, EMAIL)
                            0x6D:(0xF9,0xB5), # (EREOF/RECRD, VIDEO/MEDIA SELECT)
                            0x6F:(0xF2,None), # (COPY/TEST)
                            0x70:(0x15,None), # (KATAKANA) not sure of this
                            0x71:(0xF6,None), # (ATTN/SYSRQ)
                            0x72:(0xF7,None), # (CRSEL)
                            0x74:(0xF8,None), # (EXSEL/SETUP)
                            0x75:(0xF4,None), # (ENL/HELP)
                            0x76:(0x0C,None), # (CLEAR)
                            0x77:(0x15,None), # (FURIGANA)
                            0x79:(0x19,None), # (KANJI)
                            0x7B:(0x15,None), # (HIRAGANA) not sure of this
                            0x21D:(0xA2,None), # (windows ALTGR down)
                        }

DEFAULT_EXIT_KEY_CODE = DEFAULT_WINDOWS_VKEYS.get("ESCAPE") #ESC key
DEFAULT_KEY_STATE_STRING = ("UP","DOWN")


class KeyInput: 
    """Base input class.
Should be used if you need key or character as the only one input. Does not echo to the screen. 

    Method list:
        __call__
        vkey_index
        vkeys_index
        _test
    
    Attribute List:
        WINDOWS_VKEY - Windows Virtual Keys table. Dict key is vkey string, dict value is vkey code.
        SCODE_TO_VKEY - Scancodes to Virtual Keys association table. Dict key is scan code number, value is a 2-element tuple of vkey codes (normal, extended).
        KEY_STATE_STRING - 2-element tuple of key (press and release) state.     
        
    """ 

    def __init__(self,windowsVKeysTable=DEFAULT_WINDOWS_VKEYS,scancodeToVKeysTable=DEFAULT_SCODE_TO_VKEY,keyStateString=DEFAULT_KEY_STATE_STRING): 
        """Initialize the base instance for the current OS.

        Parameters:
            windowsVKeysTable - Use custom Virtual key table. Associate with WINDOWS_VKEYS attribute.
            scancodeToVKeysTable - Use custom Scancode Virtual key table. Associate with SCODE_TO_VKEY attribute.
            keyStateString - Use custom state string. Associate with KEY_STATE_STRING attribute.
        """

        self.WINDOWS_VKEYS = windowsVKeysTable
        self.SCODE_TO_VKEY = scancodeToVKeysTable
        self.KEY_STATE_STRING = keyStateString
        self._impl = KeyInput._OSImpl()
        
    def __call__(self):
        """Return the pressed key as tuple (virual key code, event state code) then exit."""
        self.keycode = None
        def _keyEvent():
            self.keycode = self._impl._retkey   
            self._impl.set_exit(True)
        self._impl.key_event = _keyEvent
        self._impl()
        code,ext,state = self.keycode #valid state code only > 0
        return (self.SCODE_TO_VKEY[code][ext],state)

    def vkey_index(self,vkeycode):
        """Return the string representation of the windows virtual keys code. Only the first key occurrence is returned as a string."""
        for (k, v) in self.WINDOWS_VKEYS.iteritems():
            if v == vkeycode:
                return k

    def vkeys_index(self,vkeycode):
        """Return the string representation of the windows virtual keys code. Multiple keys can be returned into a list of strings."""
        return [k for (k, v) in self.WINDOWS_VKEYS.iteritems() if v == vkeycode]
   
    def _test(self):
        """Try if the class implementation work well. Print on screen the pressed virtual key string, pressing state and vkey code.
Use this as example for understand how the class work.

        """

        print 'Press a key' 
        code,state = self.__call__()
        print 'you pressed vkey:',self.vkeys_index(code),' with state:',self.KEY_STATE_STRING[state],' and vkey code:',code       
     
           
class KeyEvent(KeyInput):
    """Inherits from KeyInput class.
Run keyInput.__call__() method in a loop. Return the pressed virtual key from an handler function. 
This is the equivalent class used in ksApp.py module, but instead of an per-app call use system calls inside the handler loop.
The loop will be executed under the same main thread. 
If initialized after a KeyThread instance may cause some weird events when executed.

    Method list:
        __call__
        vkey_index
        vkeys_index
        set_event
        _test    
            
    Attribute List:
        WINDOWS_VKEY - Windows Virtual Keys table. Dict key is vkey string, dict value is vkey code.
        SCODE_TO_VKEY - Scancodes to Virtual Keys association table. Dict key is scan code number, value is a 2-element tuple of vkey codes (normal, extended).
        KEY_STATE_STRING - 2-element tuple of key (press and release) state.     
        EXIT_KEY_CODE - Virtual key code that will be used to stop input keys. Default value is 0x1B (ESC key).
                 
    """

    def __init__(self,exitKeycode=DEFAULT_EXIT_KEY_CODE,windowsVKeysTable=DEFAULT_WINDOWS_VKEYS,scancodeToVKeysTable=DEFAULT_SCODE_TO_VKEY,keyStateString=DEFAULT_KEY_STATE_STRING):
        """Initialize itself and the inherited class.

        Parameters:
            exitkeycode - Use custom exit code. Associated with EXIT_KEY_CODE attribute.
            windowsVKeysTable - Use custom Virtual key table. Associate with WINDOWS_VKEYS attribute.
            scancodeToVKeysTable - Use custom Scancode Virtual key table. Associate with SCODE_TO_VKEY attribute.
            keyStateString - Use custom state string. Associate with KEY_STATE_STRING attribute.

        """

        KeyInput.__init__(self,windowsVKeysTable,scancodeToVKeysTable,keyStateString)
        self.EXIT_KEY_CODE=exitKeycode
        self.set_exit=self._impl.set_exit

    def __call__(self):
        """Start the key event handler. 
Initialize the event handler and put the *keyEvent.set_event()* method inside it, then starts it.
The pressed key is saved as tuple in the self.keycode variable (virual key code, event state code).

        """

        def _keyEvent():
            code,ext,state = self._impl._retkey
            self.keycode = (self.SCODE_TO_VKEY[code][ext],state)
            self.set_event()   
            if self.keycode[0]==self.EXIT_KEY_CODE: #improve, check the type before the condition.
                self._impl.set_exit(True)
        self._impl.key_event=_keyEvent
        self._impl()

    def set_event(self):
        """Override this method if you would to loop inside the handler. Use self.keycode inside it for extract the pressed key.
        
        """

        pass
    
    def _test(self):
        """Try if the class implementation work well. Print on screen the pressed virtual key string, pressing state and vkey code.
Use this as example for understand how the class work.

        """

        print 'Press a key'
        def testEvent():
            code,state = self.keycode
            print 'you pressed vkey:',self.vkeys_index(code),' with state:',self.KEY_STATE_STRING[state],' and vkey code:',code   
        self.set_event=testEvent
        self.__call__()


class KeyThread:
    """Used with build-in threading package. Should be used when you need a fast input response, independently from the main process execution.
Run and instance of the KeyEvent class in a separate thread and return any pressed virtual key in asynchronous mode. (best mode)
Virtual key 0x1B (default ESC key) to stop the code loop. 

    Method list:
        __call__
        vkey_index
        vkeys_index
        stop
        _thread_event
        _runcode
        _check_buffer
        _test

    Property list:
        keycode

    Attribute List:
        WINDOWS_VKEY - Windows Virtual Keys table. Dict key is vkey string, dict value is vkey code.
        SCODE_TO_VKEY - Scancodes to Virtual Keys association table. Dict key is scan code number, value is a 2-element tuple of vkey codes (normal, extended).
        KEY_STATE_STRING - 2-element tuple of key (press and release) state.     
        EXIT_KEY_CODE - Virtual key code that will be used to stop input keys. Default value is 0x1B (ESC key).

    """

    from Queue import Queue as _Queue
    import Queue

    def __init__(self,thread_id=None,max_buffer=0,exitkeycode=DEFAULT_EXIT_KEY_CODE,windowsVKeysTable=DEFAULT_WINDOWS_VKEYS,scancodeToVKeysTable=DEFAULT_SCODE_TO_VKEY,keyStateString=DEFAULT_KEY_STATE_STRING): 
        """Initialize thread object. Check if the system support the build-in threading package. If thread_id is None create a new thread, check if the given thread id is associated with an existing thread otherwise. If this is true join the thread with the class instance.
    
    Parameters:
        thread_id - Unique thread id number associated with the run threading object.
        max_buffer - Maximum characters buffer which serves for transfer characters from the child thread to the main thread. Default value=0 (unlimited characters).
        exitkeycode - Use custom exit code. Associated with EXIT_KEY_CODE attribute.
        windowsVKeysTable - Use custom Virtual key table. Associate with WINDOWS_VKEYS attribute.
        scancodeToVKeysTable - Use custom Scancode Virtual key table. Associate with SCODE_TO_VKEY attribute.
        keyStateString - Use custom state string. Associate with KEY_STATE_STRING attribute.

        """

        try:
            import threading as _threading
        except ImportError:
            try:
                import dummy_threading as _threading
            except (ImportError):              
                raise ImportError ("""Threading not supported.
You can't instanciate this class.

                      """)
                del self   
        else:                
            self.keybuffer = KeyThread._Queue(self._check_buffer(max_buffer))
            self.quitevent = _threading.Event()

            keyev = KeyEvent(exitkeycode,windowsVKeysTable,scancodeToVKeysTable,keyStateString)
            self.EXIT_KEY_CODE = keyev.EXIT_KEY_CODE
            self.WINDOWS_VKEYS = keyev.WINDOWS_VKEYS
            self.SCODE_TO_VKEY = keyev.SCODE_TO_VKEY
            self.KEY_STATE_STRING = keyev.KEY_STATE_STRING
            self.vkey_index = keyev.vkey_index
            self.vkeys_index = keyev.vkeys_index

            KeyEvent.set_event = KeyThread._thread_event #could be overwritten as instance method instead of class method, but give me some errors. This may raise some implementation problems if you instantiathe this class before the KeyEvent class. 
            keyev.keybuffer = self.keybuffer
            keyev.quitevent = self.quitevent

            if thread_id != None and type(thread_id)!= int and type(thread_id)!= object:
                raise TypeError("thread_id parameter must be a thread Number or thread Object.")
            else:
                if thread_id == None:
                    self._thread=_threading.Thread(target=KeyThread._runcode,args=(keyev,))
                else:
                    for tobj in _threading.enumerate():
                        if tobj.ident or tobj==thread_id:
                            self._thread = tobj
                            break                            

    def __call__(self):
        """Start the thread if it isn't alive and return the thread ID, if it exist returns None instead.
   
        """
        if not self._thread.isAlive():
            self._thread.start()
            return self._thread.ident

    @property
    def keycode(self):
        """If the thread is alive return a queue of pressed keys as tuples (virual key code, event state code). This is a property method.

The main thread programm can countinue the execution of its code and if the key buffer queue is empty returns None.

        """            
        keyqueue = self.keybuffer.queue
        keyslist = tuple(keyqueue)
        if keyslist:
            keyqueue.clear()
            return keyslist     

    @staticmethod
    def _thread_event(this):
        """Core event that overwrites the *KeyEvent.set_event* method. Implemented as Static method.

This method overwrites the KeyEvent.set_event method as key press detection event.
Do not overwrite it unless you know what you're doing. 

        """

        this.keybuffer.put(this.keycode)
            
        if this.quitevent.is_set():
            this.quitevent.clear()
            this.set_exit(True)
 
    @staticmethod
    def _runcode(keyinstance):
        """The core of the key thread acquisition code. Implemented as Static method.
Overwrites the threading run() method with the key press detection event.

Do not overwrite it unless you know what you're doing. 
        
        """  

        keyinstance()

    def _check_buffer(self,max=0):
        """Check the buffer length which serves for transfer characters from the asynchronous thread to the main thread. 

    Parameters:
        max - The maximum characters buffer. Default value = 1 (character).
        
        """

        if type(max)!=int:
            raise TypeError("max_buffer parameter value must be an integer")
        if max <0 :
            raise ValueError("max_buffer parameter value must be greather than or equal to 0")
        return max

    def stop(self, force=0, retry=3, wait=1):
        """Abort thread instance. *force* parameter set the strenght of abort state (default=0).

        Parameters:
            force = 0 - recomended: only verify if the thread is alive and set a stop event in the thread (the thread will close softly).
            force = 1 - not recomended: verify if the thread is alive and if the thread do not join in a few millisecond, the function send to it and exception that force the abort state (if the thread respond will close softly otherwise, it will close in the middle of its execution).
            force = 2 - strongly not recomended: verify if the thread is alive and stop it by sending an exception that force the abort state (it will close in the middle of its execution).
            retry - how many times try to stop the thread and wait it's join.
            wait - waiting time every retry loop in a join state.

        """

        if force<0 or force>2:
            raise ValueError("*force* param in KeyThread.stop() must be between 0 and 2")
        if retry<0:
            raise ValueError("*retry* parameter in KeyThread.stop() must be greather than 0")
        if wait<0:
            raise ValueError("*wait_time* parameter in KeyThread.stop() must be greather than 0")

        res=0
        
        if self._thread.isAlive() == True and force == 0 and force == 1:
            #softly thread stop
            for i in xrange(retry): 
                self.quitevent.set() #set the thread stop variable on true.
                self._thread.join(wait)
                if not self._thread.isAlive(): 
                    break

        if self._thread.isAlive() == True and force == 1 and force == 2:
            #force thread stop
            for i in xrange(retry):
                exc = ctypes.py_object(SystemExit)
                res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), exc)
                if res<1:
                    raise ValueError("Invalid keyThread id")
                else: #elif res >1:  1 is the tID of the main thread.
                    ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
                    #raise SystemError("KeyThread force stop failed") useless?
                self._thread.join(wait)
                if not self._thread.isAlive(): 
                    break
                
        return self._thread.isAlive()

    def _test(self):
        """Try if the class implementation work well. Print on screen the pressed virtual key string, pressing state and vkey code. 
Use this as example for understand how the class work.

        """

        print 'Press a key' 
        self.__call__()
        while 1:
            keycode=self.keycode
            if keycode is not None:
                for keyc in keycode:
                    code,state = keyc
                    print 'you pressed vkey:',self.vkeys_index(code),' with state:',self.KEY_STATE_STRING[state],' and vkey code:',code  