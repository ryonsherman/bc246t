#!/usr/bin/env python2

"""
The MIT License (MIT)

Copyright (c) 2013 Ryon Sherman <ryon.sherman@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Protocol and Documentation Copyright (c) 2008-2013 Uniden and its contributing authors.
"""

# TODO: Return constants (or array of) instead of (or along with) raw results.
#   Ex: ['10', {'opt1': Device.const.true, 'opt2': Device.const.false}]
# TODO: return constant instead of value, add __str__ to output value
# TODO: Ensure values passed are constants or their values
# TODO: Change string values to int wher epossible. Ex: '10' => 10

import serial


class Device(object):
    """
        BC246T Device

        BPS rate        : 9600/19200/38400/57600 bps
        Start/Stop bit  : 1 bit, 1 bit
        Data Length     : 8 bit
        Parity Check    : None
        Code            : ASCII
        Flow Control    : None
        Return Code     : Carriage Return only

    """

    class TOGGLE:
        OFF = 0
        ON = 1

    class LINE_DISPLAY_MODE:
        NORMAL = ' '
        REVERSE = '*'
        CURSOR = '_'
        BLINK = '#'

    class ICON_DISPLAY_MODE:
        OFF = '0'
        ON = '1'
        BLINK = '2'

    class KEY_CODE:
        MENU = 'M'
        F = 'F'
        HOLD = 'H'
        SCAN = 'S'
        SEARCH = 'S'
        L_O = 'L'
        LIGHT = '!'
        LOCK = '!'
        ONE = '1'
        PRI = '1'
        TWO = '2'
        WX = '2'
        THREE = '3'
        FOUR = '4'
        FIVE = '5'
        SIX = '6'
        SEVEN = '7'
        RCL = '7'
        EIGHT = '8'
        NINE = '9'
        ZERO = '0'
        DOT = '.'
        NO = '.'
        REV = '.'
        E = 'E'
        YES = 'E'
        ATT = 'E'
        VFO_RIGHT = '>'
        VFO_LEFT = '<'
        VFO_PUSH = '^'
        POWER = 'P'

    class KEY_MODE:
        PRESS = 'P'
        LONG_PRESS = 'L'
        HOLD = 'H'
        RELEASE = 'R'

    class MODULATION:
        AUTO = 'AUTO'
        FM = 'FM'
        NFM = 'NFM'
        AM = 'AM'

    class ID_SEARCH_MODE:
        SCAN = 0
        SEARCH = 1

    class SQUELCH:
        CLOSE = 0
        OPEN = 1

    class ALERT_STATUS:
        NO_ALERT = 0
        ALERT = 1

    def __init__(self, port, baudrate=57600, timeout=0.1):
        """ Initialize Device """

        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = serial.Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.settings = self.Settings(self)
        self.systems = self.Systems(self)

    def command(self, command, *args, **kwargs):
        """ Execute Raw Command """

        args = map(str, [arg for arg in args if arg])
        raw_command = "%s\r" % command if not args else "%s,%s\r" % (command, ','.join(args))
        self.serial.writelines(raw_command)

        response = self.serial.readline().strip()
        split_response = response.split(',')
        if not response:
            raise SerialTimeoutException
        if split_response[-1] == "ERR":
            raise DeviceErrorException
        if split_response[-1] == "NG":
            raise CommandUnavailableException
        if response == "FER":
            raise FramingErrorException
        if response == "ORER":
            raise OverrunErrorException

        response = split_response[1:]

        if 'keys' in kwargs:
            return dict(zip(list(kwargs['keys']), response))

        if len(response) == 1:
            return response[0]

        return response

    @property
    def model(self):
        """
            Get Model Info

            Returns Model Information.

            Controller -> Radio
                1: MDL

            Radio -> Controller
                1: MDL,BC246T

        """

        return self.command('MDL')

    @property
    def firmware(self):
        """
            Get Firmware Version

            Returns Firmware Version.

            Controller -> Radio
                1: VER

            Radio -> Controller
                1: VER,VR1.00

        """

        return self.command('VER')[2:]

    @property
    def program(self):
        """ Get Program Mode """

        return getattr(self, '_program', False)

    @program.setter
    def program(self, mode):
        """
            Set Program Mode

            NOTE: This property has been created in lieu of Enter/Exit Program Mode.
                  The documentation for the two methods is as follows:

            ----------------------------------------------------------------------

            Enter Program Mode

            The scanner goes to Program Mode.
            The scanner displays "Remote Mode" on upper line and "Keypad Lock"
                on lower line in Program Mode.
            POWER key and Function key are valid in Program Mode.

            Controller -> Radio
                1: PRG

            Radio -> Controller
                1: PRG,OK
                2: PRG,NG

            NOTE: This command is invalid when the Scanner is in Menu Mode, during
                  Direct Entry operation, and during Quick Save operation.

            ----------------------------------------------------------------------

            Exit Program Mode

            The Scanner exits from Program Mode.
            Then, the Scanner goes to Scan Hold Mode.

            Controller -> Radio
                1: EPG

            Radio -> Controller
                1: EPG,OK

        """

        self._program = mode if self.command('PRG' if mode else 'EPG') == 'OK' else False

    @property
    def status(self):
        """
            Get Current Status

            Returns current scanner status.

            Controller -> Radio
                1: STS

            Radio -> Controller
                1: STS,[L1_CHAR],[L1_MODE],[L2_CHAR],[L2_MODE],[ICON1],[ICON2],[RESERVE],[SQL],[MUT],[BAT],[WAT]

                    [L1_CHAR]       : Line1 Characters 16char (fixed length)
                    [L1_MODE]       : Line1 Display Mode 16char (See LINE_DISPLAY_MODE class)
                    [L2_CHAR]       : Line2 Characters 16char (fixed length)
                    [L2_MODE]       : Line2 Display Mode 16char (See LINE_DISPLAY_MODE class)
                    [ICON1]         : Icon1 Group Display Mode 15char (See ICON_DISPLAY_MODE class)
                                        SYS/1/2/3/4/5/6/7/8/9/0/ATT/PRI/KEYLOCK/BATT
                    [ICON2]         : Icon2 Group Display Mode 17char (See ICON_DISPLAY_MODE class)
                                        GRP/1/2/3/4/5/6/7/8/9/0/AN/N/FM/LO/F/CC
                    [RESERVE]       : (Reserved area, not used)
                    [SQL]           : Squelch Status (See SQUELCH class)
                    [MUT]           : Mute Status (See TOGGLE class)
                    [BAT]           : Battery Low Status (See ALERT_STATUS class)
                    [WAT]           : Weather Alert Status (See ALERT_STATUS class, ???: NWR-SAME Code)

            NOTE: Line1 or Line2 Characters may include "," as displayed character.

        """

        return self.command('STS', keys=('l1_char', 'l1_mode', 'l2_char', 'l2_mode', 'icon1', 'icon2', 'reserve', 'sql', 'mut', 'bat', 'wat'))

    @property
    def talkgroup(self):
        """
            Get Current Talkgroup ID Status

            This command returns TGID currently displayed on LCD.

            Controller -> Radio
                1: GID

            Radio -> Controller
                1: GID,[SYS_TYPE],[TGID],[ID_SRCH_MODE],[NAME1],[NAME2],[NAME3]

                    [SYS_TYPE]      : System Type
                    [TGID]          : Talkgroup ID
                    [ID_SRCH_MODE]  : ID Search Mode (See ID_SRCH_MODE class)
                    [NAME1]         : SYSTEM NAME (Alpha Tag)
                    [NAME2]         : GROUP NAME (Alpha Tag)
                    [NAME3]         : TGID NAME (Alpha Tag)

        """

        return self.command('GID', keys=('sys_type', 'tgid', 'id_srch_mode', 'name1', 'name2', 'name3'))

    def key(self, key_code, key_mode=KEY_MODE.PRESS):
        """
            Push KEY

            Controller -> Radio
                1: KEY,[KEY_CODE],[KEY_MODE]

                    [KEY_CODE]      : Key Code (See KEY_CODE class)
                    [KEY_MODE]      : Key Mode (See KEY_MODE class)

            Radio -> Controller
                1: KEY,OK

            NOTE: The scanner is not turned off by this command.

        """

        return self.command('KEY', key_code, key_mode)

    def quick_search(self, frq, stp=0, mod=MODULATION.AUTO, att=0, dly=0, skp=0, code_srch=0, scr=00000000, rep=0):
        """
            Go to quick search hold mode

            Specifies arbitrary frequency and changes to Quick Search Hold (VFO) mode.

            Controller -> Radio
                1: QSH,[FRQ],[STP],[MOD],[ATT],[DLY],[SKP],[CODE_SRCH],[SCR],[REP]

                    [FRQ]           : Frequency
                    [STP]           : Search Step (0,500,625,750, ... 5000,10000,20000)
                                        0: AUTO
                                        500: 5k
                                        625: 6.25k
                                        750: 7.5k
                                        1000: 10k
                                        1250: 12.5k
                                        1500: 15k
                                        20000: 20k
                                        25000: 25k
                                        50000: 50k
                                        10000: 100k
                    [MOD]           : Modulation (See MODULATION class)
                    [ATT]           : Attenuation (See TOGGLE class)
                    [DLY]           : Delay Time (0-5)
                    [SKP]           : Data Skip (See TOGGLE class)
                    [CODE_SRCH]     : CTCSS/DCS Search (See TOGGLE class)
                    [SCR]           : Pager/UHF TV Screen (See TOGGLE class)
                                        (8digit: ########) (See TOGGLE class)
                                                 |||||||+- Reserved (always 0)
                                                 ||||||+-- Reserved (always 0)
                                                 |||||+--- Reserved (always 0)
                                                 ||||+---- Reserved (always 0)
                                                 |||+----- Reserved (always 0)
                                                 ||+------ Reserved (always 0)
                                                 |+------- UHF TV
                                                 +-------- Pager
                    [REP]           : Repeater Find (See TOGGLE class)

            Radio -> Controller
                1: QSH,OK
                2: QSH,NG

            NOTE: This command is invalid when the Scanner is in Menu Mode, during
                  Direct Entry operation, and during Quick Save operation.

        """

        return self.command('QSH', frq, stp, mod, att, dly, skp, code_srch, scr, rep)

    def poweroff(self):
        """
            Power OFF

            Turns off the scanner.

            Controller -> Radio
                1: POF

            Radio -> Controller
                1: POF,OK

            NOTE: After this command, the scanner doesn't accept any command.

        """
        return self.command('POF')


    class Settings(object):
        """ Device Settings """

        class BACKLIGHT:
            INFINITE = 'IF'
            TEN_SEC = '10'
            THIRTY_SEC = '30'
            KEYPRESS = 'KY'
            SQUELCH = 'SQ'

        def __init__(self, device):
            """ Initialize Settings """

            self.device = device

        def clear(self):
            """
                Clear All Memory

                All settings are returned to default values.
                Only PC Control (Baud Rate) retains its value.

                Controller -> Radio
                    1: CLR

                Radio -> Controller
                    1: CLR,OK

                NOTE: This command is only acceptable in Programming Mode.
                      This command needs about 10 seconds execution time.

            """

            self.device.serial.timeout = 10
            response = self.device.command('CLR')
            self.device.serial.timeout = self.device.timeout

            return response


        @property
        def backlight(self):
            """
                Get Backlight

                Get Backlight Setting.

                Controller -> Radio
                    1: BLT

                Radio -> Controller
                    1: BLT,##

                        ##              : Backlight Setting (see BACKLIGHT class)

                NOTE: This command is only acceptable in Programming Mode.

            """

            return self.device.command('BLT')

        @backlight.setter
        def backlight(self, value):
            """
                Set Backlight

                Set Backlight Setting.

                Controller -> Radio
                    1: BLT,##

                        ##              : Backlight Setting (see BACKLIGHT class)

                Radio -> Controller
                    1: BLT,OK

                NOTE: This command is only acceptable in Programming Mode.

            """

            self.device.command('BLT', value)

        @property
        def battery_save(self):
            """
                Get Battery Save

                Get Battery Save Setting.

                Controller -> Radio
                    1: BSV

                Radio -> Controller
                    1: BSV,#

                        #               : Battery Save Setting (See TOGGLE class)

                NOTE: This command is only acceptable in Programming Mode.

            """

            return int(self.device.command('BSV'))

        @battery_save.setter
        def battery_save(self, value):
            """
                Set Battery Save

                Set Battery Save Setting.

                Controller -> Radio
                    1: BSV,#

                        #               : Battery Save Setting (See TOGGLE class)

                Radio -> Controller
                    1: BSV,OK

                NOTE: This command is only acceptable in Programming Mode.

            """

            self.device.command('BSV', value)

        @property
        def key_beep(self):
            """
                Get Key Beep

                Get Key Beep Setting.

                Controller -> Radio
                    1: KBP

                Radio -> Controller
                    1: KBP,#

                        #             : Key Beep Setting (See TOGGLE class)

                NOTE: This command is only acceptable in Programming Mode.

            """

            return int(self.device.command('KBP'))

        @key_beep.setter
        def key_beep(self, value):
            """
                Set Key Beep

                Set Key Beep Setting.

                Controller -> Radio
                    1: KBP,#

                        #              : Key Beep Setting (See TOGGLE class)

                Radio -> Controller
                    1: KBP,OK

                NOTE: This command is only acceptable in Programming Mode.

            """

            self.device.command('KBP', value)

        @property
        def opening_message(self):
            """
                Get Opening Message

                Controller -> Radio
                    1: OMS

                Radio -> Controller
                    1: OMS,[L1_CHAR],[L2_CHAR]

                        [L1_CHAR]       : Line1 Characters (max 16char)
                        [L2_CHAR]       : Line2 Characters (max 16char)

                NOTE: This command is only acceptable in Programming Mode.
                      If only space code is set in character area, the command returns the default message.

            """

            return self.device.command('OMS', keys=('l1_char', 'l2_char'))

        @opening_message.setter
        def opening_message(self, (l1_char, l2_char)):
            """
                Set Opening Message

                Controller -> Radio
                    1: OMS,[L1_CHAR],[L2_CHAR]

                        [L1_CHAR]       : Line1 Characters (max 16char)
                        [L2_CHAR]       : Line2 Characters (max 16char)

                Radio -> Controller
                    1: OMS,OK

                NOTE: This command is only acceptable in Programming Mode.

            """

            self.device.command('OMS', l1_char, l2_char)

        @property
        def priority_mode(self):
            """
                Get Priority Mode

                Get Priority Mode Setting.

                Controller -> Radio
                    1: PRI

                Radio -> Controller
                    1: PRI,#

                        #               : Priority Mode Setting (See TOGGLE class)

                NOTE: This command is only acceptable in Programming Mode.

            """

            return int(self.device.command('PRI'))

        @priority_mode.setter
        def priority_mode(self, value):
            """
                Set Priority Mode

                Set Priority Mode Setting.

                Controller -> Radio
                    1: PRI,#

                        #               : Priority Mode Setting (See TOGGLE class)

                Radio -> Controller
                    1: PRI,OK

                NOTE: This command is only acceptable in Programming Mode.

            """

            self.device.command('PRI', value)

    Settings.TOGGLE = TOGGLE


    class System(object):
        """ Device System """

        class SYS_TYPE:
            CONVENTIONAL = 'CNV'
            MOT_800_T2_STD = 'M82S'
            MOT_800_T2_SPL = 'M82P'
            MOT_900_T2 = 'M92'
            MOT_VHF_T2 = 'MV2'
            MOT_UHF_T2 = 'MU2'
            MOT_800_T1_STD = 'M81S'
            MOT_800_T1_SPL = 'M81P'
            EDACS_NARROW = 'EDN'
            EDACS_WIDE = 'EDW'
            EDACS_SCAT = 'EDS'
            LTR = 'LTR'
            MOT_800_T2_CUS = 'M82C'
            MOT_800_T1_CUS = 'M81C'

        class QUICK_KEY:
            ONE = 1
            TWO = 2
            THREE = 3
            FOUR = 4
            FIVE = 5
            SIX = 6
            SEVEN = 7
            EIGHT = 8
            NINE = 9
            TEN = 0
            NONE = '.'

        class LOUT:
            UNLOCKED = 0
            LOCKED = 1

        class EMG:
            IGNORE = 0
            ALERT = 1

        def __init__(self, device, index=None, sys_type=SYS_TYPE.CONVENTIONAL, name=None, quick_key=None, hld=None, lout=None, att=None, dly=None, skp=None, emg=None):
            """ Initialize System """

            self.device = device

            self.index = index
            self.sys_type = sys_type
            self.name = name
            self.quick_key = quick_key
            self.hld = hld
            self.lout = lout
            self.att = att
            self.dly = dly
            self.skp = skp
            self.emg = emg

            self.rev_index = -1
            self.fwd_index = -1
            self.chn_grp_head = -1
            self.chn_grp_tail = -1
            self.seq_no = -1

        @property
        def index(self):
            """ System Index getter """

            return int(getattr(self, '_index', -1))

        @index.setter
        def index(self, index):
            """ System Index setter """

            self._index = index
            if index:
                info = self.device.systems.info(index)
                map(lambda (k, v): setattr(self, k, v), info.items())

        def info(self):
            """ Device.Systems.info pass-through """

            if not self.index:
                raise CommandUnavailableException

            return self.device.systems.info(self.index)

        def remove(self):
            """ Device.Systems.remove pass-through """

            if not self.index:
                raise CommandUnavailableException

            return self.device.systems.remove(self.index)

        def group_quick_lockout(self, value):
            """ Device.Systems.group_quick_lockout pass-through """

            if not self.index:
                raise CommandUnavailableException

            return self.device.systems.group_quick_lockout(self.index)

    System.TOGGLE = TOGGLE


    class Systems(list):
        """ Device Systems """

        def __init__(self, device):
            """ Initialize Systems """

            self.device = device

        def __len__(self):
            """
                Get System Count

                Returns the number of stored Systems.

                Controller -> Radio
                    1: SCT

                Radio -> Controller
                    1:SCT,###

                        ###             : Number of Systems (0-200)

                NOTE: This command is only acceptable in Programming Mode.

            """

            return int(self.device.command('SCT'))

        def __iter__(self):
            for i in range(self.head, self.tail):
                yield self[i]

        def __getitem__(self, index):
            system = Device.System(self.device)
            system.index = index
            return system

        def __str__(self):
            return str(range(self.head, self.tail))

        @property
        def head(self):
            """
                Get System Index Head

                Returns the first index of stored system list.

                Controller -> Radio
                    1: SIH

                Radio -> Controller
                    1:SIH,[SYS_INDEX]

                        [SYS_INDEX]     : System Index

                NOTE: This command is only acceptable in Programming Mode.

            """

            return int(self.device.command('SIH'))

        @property
        def tail(self):
            """
                Get System Index Tail

                Returns the last index of stored system list.

                Controller -> Radio
                    1: SIT

                Radio -> Controller
                    1:SIT,[SYS_INDEX]

                        [SYS_INDEX]     : System Index

                NOTE: This command is only acceptable in Programming Mode.

            """

            return int(self.device.command('SIT'))

        def append(self, system):
            """
                Create System

                Creates a system and returns created system index.

                Controller -> Radio
                    1: CSY,[SYS_TYPE]

                        [SYS_TYPE]      : System Type (See Device.System.SYS_TYPE class)

                Radio -> Controller
                    1: CSY,[SYS_INDEX]

                        [SYS_INDEX]     : The Index if Created System

                NOTE: The index is a handle to get/set system information.
                      Returns -1 if the scanner failed to create because of no resource.
                      This command is only acceptable in Programming Mode.

            """

            system.index = self.device.command('CSY', system.sys_type)

        def remove(self, index):
            """
                Delete System

                Deletes a system.

                Controller -> Radio
                    1: DSY,[SYS_INDEX]

                    [SYS_INDEX]     : System Index

                Radio -> Controller
                    1: DSY,OK

                NOTE: This command is only acceptable in Programming Mode.

            """

            return self.device.command('DSY', index)

        def info(self, index, name=None, quick_key=None, hld=None, lout=None, att=None, dly=None, skp=None, emg=None):
            """
                Get/Set System Info

                Get/Set System Information.

                Controller -> Radio
                    1: SIN,[INDEX]

                    [INDEX]         : System Index

                    2: SIN,[SYS_TYPE],[NAME],[QUICK_KEY],[HLD],[LOUT],[ATT],[DLY],[SKP],[EMG]

                    [SYS_TYPE]      : System Type (See Device.System.SYS_TYPE class)
                    [NAME]          : Name (max 16char)
                    [QUICK_KEY]     : Quick Key (See QUICK_KEY class)
                    [HLD]           : System Hold Time (0-255)
                    [LOUT]          : Lockout (See LOUT class)
                    [ATT]           : Attenuation (See TOGGLE class)
                    [DLY]           : Delay Time (0-5)
                    [SKP]           : Data Skip (See TOGGLE class)
                    [EMG]           : Emergency Alert (See EMG class)

                Radio -> Controller
                    1: SIN,[SYS_TYPE],[NAME],[QUICK_KEY],[HLD],[LOUT],[ATT],[DLY],[SKP],[EMG],[REV_INDEX],[FWD_INDEX],[CHN_GRP_HEAD],[CHN_GRP_TAIL],[SEQ_NO]

                    [SYS_TYPE]      : System Type (See Device.System.SYS_TYPE class)
                    [NAME]          : Name (max 16char)
                    [QUICK_KEY]     : Quick Key (See QUICK_KEY class)
                    [HLD]           : System Hold Time (0-255)
                    [LOUT]          : Lockout (See LOUT class)
                    [ATT]           : Attenuation (See TOGGLE class)
                    [DLY]           : Delay Time (0-5)
                    [SKP]           : Data Skip (See TOGGLE class)
                    [EMG]           : Emergency Alert (See EMG class)
                    [REV_INDEX]     : Reverse System Index
                    [FWD_INDEX]     : Forward System Index
                    [CHN_GRP_HEAD]  : Channel Group Index Head
                    [CHN_GRP_TAIL]  : Channel Group Index Tail
                    [SEQ_NO]        : System Sequence Number (1-200)

                    2: SIN,OK

                NOTE: The scanner does not return a value for parameters which are not appropriate for the system type.
                      The scanner does not set a value for parameters which are not appropriate for the system type.
                      Only provided parameters are changed.
                      The command is aborted if any format error is detected.
                      This command is only acceptable in Programming Mode.

            """

            return self.device.command('SIN', index, keys=('sys_type', 'name', 'quick_key', 'hld', 'lout', 'att', 'dly', 'skp', 'emg', 'rev_index', 'fwd_index', 'chn_grp_head', 'chn_grp_tail', 'seq_no'))

        @property
        def system_quick_lockout(self):
            """
                Get System Quick Lockout

                Returns the System Quick Key status.

                Controller -> Radio
                    1: QSL

                Radio -> Controller
                    1: QSL,##########

                    ##########      : System Quick Key status (See TOGGLE class)

                NOTE: This command is only acceptable in Programming Mode.

            """

            return self.device.command('QSL')

        @system_quick_lockout.setter
        def system_quick_lockout(self, value):
            """
                Set System Quick Lockout

                Sets the System Quick Key status.

                Controller -> Radio
                    1: QSL,##########

                    ##########      : System Quick Key status (See TOGGLE class)

                Radio -> Controller
                    1: QSL,OK

                NOTE: This cannot turn on/off a Quick Key that has no System.
                      This command is only acceptable in Programming Mode.

            """

            return self.device.command('QSL', value)

        def group_quick_lockout(self, index, value=None):
            """
                Get/Set Group Quick Lockout

                Returns/Sets Group Quick Key status of a System

                Controller -> Radio
                    1: QGL,[SYS_INDEX]
                    2: QGL,[SYS_INDEX],##########

                    ##########      : System Quick Key status (See TOGGLE class)

                Radio -> Controller
                    1: QGL,##########
                    2: QGL,OK

                    ##########      : System Quick Key status (See TOGGLE class)

                NOTE: This cannot turn on/off a Quick Key that has no Group.
                      This command is only acceptable in Programming Mode.

            """

            return self.device.command('QGL', index, value)

    Systems.TOGGLE = TOGGLE


class SerialTimeoutException(Exception):
    def __init__(self):
        Exception.__init__(self, "No response from device")


class DeviceErrorException(Exception):
    def __init__(self):
        Exception.__init__(self, "Command format error / Value error")


class CommandUnavailableException(Exception):
    def __init__(self):
        Exception.__init__(self, "The command is invalid at this time")


class FramingErrorException(Exception):
    def __init__(self):
        Exception.__init__(self, "Framing error")


class OverrunErrorException(Exception):
    def __init__(self):
        Exception.__init__(self, "Overrun error")


if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser(usage="Usage: %prog [options] command (arguments)")
    parser.add_option('-p', '--port', dest='port', metavar='PORT', default=0, help="a /dev/ttyUSB[PORT] number (default %default) or a device name")
    parser.add_option('-b', '--baud', dest='baud', metavar='BAUDRATE', default=57600, help="set baud rate, default %default")
    parser.add_option('-t', '--timeout', dest='timeout', metavar='TIMEOUT', default=0.1, help="a read timeout value, default %default")
    options, args = parser.parse_args()

    def print_help():
        parser.print_help()
        exit(-1)

    if not len(args):
        print_help()

    try:
        options.port = '/dev/ttyUSB%d' % int(options.port)
    except ValueError:
        pass

    try:
        dev = Device(port=options.port, baudrate=options.baud, timeout=options.timeout)
    except serial.serialutil.SerialException, error:
        exit("%s: %s" % (__file__, error))
