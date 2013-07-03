#!/usr/bin/env python2

import serial


class MetaDevice(type):
    @classmethod
    def keys(cls, *keys):
        def wrapper(func):
            def method(*args, **kwargs):
                return dict(zip(list(keys), func(*args, **kwargs)))
            return method
        return wrapper


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

    __metaclass__ = MetaDevice

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
        LONG_RESS = 'L'
        HOLD = 'H'
        RELEASE = 'R'

    class MODULATION:
        AUTO = 'AUTO'
        FM = 'FM'
        NFM = 'NFM'
        AM = 'AM'

    class BACKLIGHT:
        INFINITE = 'IF'
        TEN_SECONDS = '10'
        THIRTY_SECONDS = '30'
        KEYPRESS = 'KY'
        SQUELCH = 'SQ'

    class DISPLAY_MODE:
        NORMAL = ' '
        REVERSE = '*'
        CURSOR = '_'
        BLINK = '#'

    class ID_SEARCH_MODE:
        SCAN = 0
        SEARCH = 1

    class SQUELCH:
        CLOSE = 0
        OPEN = 1

    class BOOLEAN:
        OFF = 0
        ON = 1

    class BATTERY_SAVE(BOOLEAN):
        pass

    class KEY_BEEP(BOOLEAN):
        pass

    class PRIORITY_MODE(BOOLEAN):
        PLUS_ON = 2

    def __init__(self, port, baudrate=57600, timeout=0.1):
        """ Initialize Device """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = serial.Serial(port, baudrate, timeout=timeout)
        self.settings = Settings(self)
        self.systems = Systems(self)

    def __del__(self):
        """ Close Device """
        if getattr(self, 'serial', False):
            self.serial.close()

    def command(self, command, *args):
        """ Execute Command """
        args = [str(arg) for arg in args]
        command = "%s\r" % command if not args else "%s,%s\r" % (command, ','.join(args))
        self.serial.writelines(command)
        response = self.serial.readline().strip()
        if not response:
            raise SerialTimeoutException
        if response == "ERR":
            raise DeviceErrorException
        if response.split(',')[-1] == "NG":
            raise CommandUnavailableException
        if response == "FER":
            raise FramingErrorException
        if response == "ORER":
            raise OverrunErrorException

        response = response.split(',')[1:] if response.split(',')[0] == command.strip() else response
        return response[0] if len(response) == 1 else response

    @property
    def model(self):
        """
            Get Model Info

            Returns Model Information.

            Controller -> Radio
                1: MDL

            Radio -> Controller
                2: MDL,BC246T

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
    @MetaDevice.keys('sys_type', 'tgid', 'id_srch_mode', 'name1', 'name2', 'name3')
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
                    [ID_SRCH_MODE]  : ID Search Mode (See ID_SEARCH_MODE class)
                    [NAME1]         : SYSTEM NAME (Alpha Tag)
                    [NAME2]         : GROUP NAME (Alpha Tag)
                    [NAME3]         : TGID NAME (Alpha Tag)

        """

        return self.command('GID')

    @property
    @MetaDevice.keys('l1_char', 'l1_mode', 'l2_char', 'l2_mode', 'icon1', 'icon2', 'reserve', 'sql', 'mut', 'bat', 'wat')
    def status(self):
        """
            Get Current Status

            Returns current scanner status.

            Controller -> Radio
                1: STS

            Radio -> Controller
                1: STS,[L1_CHAR],[L1_MODE],[L2_CHAR],[L2_MODE],[ICON1],[ICON2],[RESERVE],[SQL],[MUT],[BAT],[WAT]

                    [L1_CHAR]       : Line1 Characters 16char (fixed length)
                    [L1_MODE]       : Line1 Display Mode 16char (See DISPLAY_MODE class)
                    [L2_CHAR]       : Line2 Characters 16char (fixed length)
                    [L2_MODE]       : Line2 Display Mode 16char (See DISPLAY_MODE class)
                    [ICON1]         : Icon1 Group Display Mode 15char (0: OFF, 1: ON, 2: BLINK)
                                        SYS/1/2/3/4/5/6/7/8/9/0/ATT/PRI/KEYLOCK/BATT
                    [ICON2]         : Icon2 Group Display Mode 17char (0: OFF, 1: ON, 2: BLINK)
                                        GRP/1/2/3/4/5/6/7/8/9/0/AN/N/FM/LO/F/CC
                    [RESERVE]       : (Reserved area, not used)
                    [SQL]           : Squelch Status (See SQUELCH class)
                    [MUT]           : Mute Status (0: OFF, 1: ON)
                    [BAT]           : Battery Low Status (0: No Alert, 1: Alert)
                    [WAT]           : Weather Alert Status (0: No Alert, 1: Alert, ???: NWR-SAME Code)

            NOTE: Line1 or Line2 Characters may include "," as displayed character.

        """

        return self.command('STS')

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

        if self.command('PRG' if mode else 'EPG') == 'OK':
            self._program = mode
        else:
            self._program = False

    def key(self, key_code, key_mode):
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

    def quick_search(self, frq, stp, mod, atty, dly, skp, code_srch, pgr, rep):
        """
            Go to quick search hold mode

            Specifies arbitrary frequency and changes to Quick Search Hold (VFO) mode.

            Controller -> Radio
                1: QSH,[FRQ],[STP],[MOD],[ATT],[DLY],[SKP],[CODE_SRCH],[PGR],[REP]

                    [FRQ]           : Frequency
                    [STP]           : Search Step (0,500,625,750, ... 5000,10000,20000)
                                        0: AUTO
                                        500: 5k
                                        625: 6.25k
                                        750: 7.5k
                                        1000: 10k
                                        1250: 12.5k
                                        1500: 15k
                                        2000: 20k
                                        2500: 25k
                                        5000: 50k
                                        1000: 100k
                                        2000: 200k
                    [MOD]           : Modulation (See MODULATION class)
                    [ATT]           : Attenuation (0: OFF, 1: ON)
                    [DLY]           : Delay Time (0-5)
                    [SKP]           : Data Skip (0: OFF, 1: ON)
                    [CODE_SRCH]     : CTCSS/DCS Search (0: OFF, 1: ON)
                    [PGR]           : Pager Screen (0: OFF, 1: ON)
                    [REP]           : Repeater Find (0: OFF, 1: ON)

            Radio -> Controller
                1: QSH,OK
                2: QSH,NG

            NOTE: This command is invalid when the Scanner is in Menu Mode, during
                  Direct Entry operation, and during Quick Save operation.

        """
        return self.command('QSH', frq, stp, mod, atty, dly, skp, code_srch, pgr, rep)

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

        self.device.serial.timeout = 15
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

                    #               : Battery Save Setting (0: OFF, 1: ON)

            NOTE: This command is only acceptable in Programming Mode.

        """
        return bool(self.device.command('BSV'))

    @battery_save.setter
    def battery_save(self, value):
        """
            Set Battery Save

            Set Battery Save Setting.

            Controller -> Radio
                1: BSV,#

                    #               : Battery Save Setting (0: OFF, 1: ON)

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

                    #             : Key Beep Setting (0: OFF, 1: ON)

            NOTE: This command is only acceptable in Programming Mode.

        """
        return bool(self.device.command('KBP'))

    @key_beep.setter
    def key_beep(self, value):
        """
            Set Key Beep

            Set Key Beep Setting.

            Controller -> Radio
                1: KBP,#

                    #              : Key Beep Setting (0: OFF, 1: ON)

            Radio -> Controller
                1: KBP,OK

            NOTE: This command is only acceptable in Programming Mode.

        """
        self.device.command('KBP', value)

    @property
    @MetaDevice.keys('l1_char', 'l2_char')
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
        return self.device.command('OMS')

    @opening_message.setter
    def opening_message(self, l1_char, l2_char):
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

                    #               : Priority Mode Setting (0: OFF, 1: ON)

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

                    #               : Priority Mode Setting (0: OFF, 1: ON)

            Radio -> Controller
                1: PRI,OK

            NOTE: This command is only acceptable in Programming Mode.

        """
        self.device.command('PRI', value)


class System(object):
    class TYPE:
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

    def __init__(self, sys_type=TYPE.CONVENTIONAL, name=None, quick_key=None, hld=None, lout=None, att=None, dly=None, skp=None, emg=None):
        """ Initialize System """
        self.index = None
        self.type = sys_type


class Systems(list):
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
        # for i in range(self.head, self.tail):
        for i in range(self.head, self.head + len(self)):
            yield self[i]

    def __getitem__(self, index):
        args = self.device.command('SIN', index)
        system = System(*args)
        system.index = index
        return system

    def append(self, system):
        system.index = self.device.command('CSY', system.type)

    def remove(self, system):
        print self.device.command('DSY', system.index)

    @property
    def head(self):
        return int(self.device.command('SIH'))

    @property
    def tail(self):
        return int(self.device.command('SIT'))


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


import unittest


class TestCase(unittest.TestCase):
    def setUp(self):
        self.port = '/dev/ttyUSB0'
        self.dev = Device(port=self.port)

    def tearDown(self):
        self.dev = None

    def assertStringNotEmpty(self, value):
        self.assertIs(type(value), str)
        self.assertGreater(len(value), 0)

    def assertDictNotEmpty(self, value):
        self.assertIs(type(value), dict)
        self.assertGreater(len(filter(lambda x: x, value.values())), 0)

    def assertValidValue(self, value, obj_type, options):
        self.assertIs(type(value), obj_type)
        self.assertIn(value, [getattr(options, attr) for attr in filter(lambda x: not x.startswith('_'), dir(options))])

    def assertBooleanSet(self, value):
        _value = value
        value = not _value
        getattr(self, 'assert%s' % (not _value))(value)
        value = _value


class DeviceTestCase(TestCase):
    def test_get_port(self):
        self.assertIs(type(self.dev.port), str)
        self.assertEqual(self.dev.port, self.port)

    def test_get_baudrate(self):
        self.assertIs(type(self.dev.baudrate), int)
        self.assertGreater(self.dev.baudrate, 0)

    def test_get_model(self):
        self.assertStringNotEmpty(self.dev.model)

    def test_get_firmware(self):
        self.assertStringNotEmpty(self.dev.firmware)

    def test_get_talkgroup(self):
        self.assertIs(type(self.dev.talkgroup), dict)

    def test_get_status(self):
        self.assertDictNotEmpty(self.dev.status)

    def test_get_program(self):
        self.assertIs(type(self.dev.program), bool)

    def test_set_program(self):
        self.assertBooleanSet(self.dev.program)


class SettingsTestCase(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        self.dev.program = True

    def tearDown(self):
        self.dev.program = False
        TestCase.tearDown(self)

    def test_get_backlight(self):
        self.assertValidValue(self.dev.settings.backlight, str, Device.BACKLIGHT)

    def test_set_backlight(self):
        pass

    def test_get_battery_save(self):
        self.assertValidValue(self.dev.settings.battery_save, bool, Device.BATTERY_SAVE)

    def test_set_battery_save(self):
        pass

    def test_get_key_beep(self):
        self.assertValidValue(self.dev.settings.key_beep, bool, Device.KEY_BEEP)

    def test_set_key_beep(self):
        pass

    def test_get_opening_message(self):
        self.assertDictNotEmpty(self.dev.settings.opening_message)

    def test_set_opening_message(self):
        pass

    def test_get_priority_mode(self):
        self.assertValidValue(self.dev.settings.priority_mode, int, Device.PRIORITY_MODE)

    def test_set_priority_mode(self):
        pass


if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser(usage="Usage: %prog [options] command (arguments)")
    parser.add_option('-p', '--port', dest='port', metavar='PORT', default=0, help="a /dev/ttyUSB[PORT] number (default %default) or a device name")
    parser.add_option('-b', '--baud', dest='baud', metavar='BAUDRATE', default=57600, help="set baud rate, default %default")
    parser.add_option('-t', '--timeout', dest='timeout', metavar='TIMEOUT', default=0.1, help="a read timeout value, default %default")
    options, args = parser.parse_args()

    try:
        options.port = '/dev/ttyUSB%d' % int(options.port)
    except ValueError:
        pass

    try:
        dev = Device(port=options.port, baudrate=options.baud, timeout=options.timeout)
    except serial.serialutil.SerialException, error:
        exit("%s: %s" % (__file__, error))

    def print_help():
        parser.print_help()
        exit(-1)

    if not len(args):
        print_help()

    command = args.pop(0)

    ret = dev
    for attr in command.split('.'):
        try:
            ret = getattr(ret, attr)
        except CommandUnavailableException:
            dev.program = True
            ret = getattr(ret, attr)
            dev.program = False
        except AttributeError, error:
            print_help()

    if callable(ret):
        if not len(args):
            print_help()
        ret = ret(*args)
    print ret

    # dev.program = True
    # if dev.program:
    #     # print "System Count: %s" % len(dev.systems)
    #     # for i in range(1, 2):
    #     #     sys = System()
    #     #     dev.systems.append(sys)

    #     print "System Count: %s" % len(dev.systems)
    #     for sys in dev.systems:
    #         print "Index: %s" % sys.index
    #         # dev.systems.remove(sys)
    #     print "System Count: %s" % len(dev.systems)

    #     print "System Head: %s" % dev.systems.head
    #     print "System Tail: %s" % dev.systems.tail

    #     # print "Clearing settings..."
    #     # dev.settings.clear()

    #     dev.program = False
