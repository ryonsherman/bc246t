bc246t
======

Serial protocol wrapper for the BC246T radio scanner.

Remote Command List
===================

|  | Category | Command | Function | Program Mode |
|-:|:---------|:-------:|:---------|:------------:|
|~~1~~| Remote Control | GID | Get Current Talkground ID Status | |
|~~2~~| Remote Control | KEY | Push KEY | |
|~~3~~| Remote Control | POF | Power OFF | |
|~~4~~| Remote Control | QSH | Go to quick search hold mode | |
|~~5~~| Remote Control | STS | Get Status | |
|~~6~~| System Information | MDL | Get Model Info | |
|~~7~~| System Information | VER | Get Firmware Version | |
|~~8~~| Programming Mode Control | PRG | Enter Program Mode | |
|~~9~~| Programming Mode Control | EPG | Exit Program Mode | |
|~~10~~| System Settings | BLT | Get/Set Backlight | True |
|~~11~~| System Settings | BSV | Get/Set Battery Save | True |
|~~12~~| System Settings | CLR | Clear All Memory | True |
|~~13~~| System Settings | KBP | Get/Set Key Beep | True |
|~~14~~| System Settings | OMS | Get/Set Opening Message | True |
|~~15~~| System Settings | PRI | Get/Set Priority Mode | True |
|~~16~~| Scan Settings | SCT | Get System Count | True |
|~~17~~| Scan Settings | SIH | Get System Index Head | True |
|~~18~~| Scan Settings | SIT | Get System Index Tail | True |
|~~19~~| Scan Settings | QSL | Get/Set System Quick Lockout | True |
|~~20~~| Scan Settings | QGL | Get/Set Group Quick Lockout | True |
|~~21~~| Scan Settings | CSY | Create System | True |
|~~22~~| Scan Settings | DSY | Delete System | True |
|23| Scan Settings | CPS | Copy System | True |
|~~24~~| Scan Settings | SIN | Get/Set System Info | True |
|25| Scan Settings | TRN | Get/Set Trunk Info | True |
|26| Scan Settings | TFQ | Get/Set Trunk Frequency Info | True |
|27| Scan Settings | AGC | Append Channel Group | True |
|28| Scan Settings | AGT | Append TGID Group | True |
|29| Scan Settings | DGR | Delete Group | True |
|30| Scan Settings | GIN | Get/Set Group Info | True |
|31| Scan Settings | ACC | Append Channel | True |
|32| Scan Settings | ACT | Append TGID | True |
|33| Scan Settings | DCH | Delete Channel | True |
|34| Scan Settings | CIN | Get/Set Channel Info | True |
|35| Scan Settings | TIN | Get/Set TGID Info | True |
|36| Scan Settings | GLI | Get Lockout TGID (for Rvw L/O ID) | True |
|37| Scan Settings | ULI | Unlock TGID (for Rvw L/O ID) | True |
|38| Scan Settings | LOI | Lock Out ID (TGID) | True |
|39| Scan Settings | REV | Get Rev Index | True |
|40| Scan Settings | FWD | Get Fwd Index | True |
|41| Scan Settings | RNB | Get Remains of Memory Block | True |
|42| Scan Settings | MEM | Get Memory Used | True |
|43| Search/Close Call Settings | SCO | Get/Set Search/Close Call Settings | True |
|44| Search/Close Call Settings | GLF | Get Global Lockout Freq | True |
|45| Search/Close Call Settings | ULF | Unlock Global L/O | True |
|46| Search/Close Call Settings | LOF | Lock Out Frequency | True |
|47| Search/Close Call Settings | CLC | Get/Set Close Call Settings | True |
|48| Custom Search Settings | CSG | Get/Set Custom Search Group | True |
|49| Custom Search Settings | CSP | Get/Set Custom Search Settings | True |
|50| Weather Settings | WPR | Get/Set Weather Priority Setting | True |
|51| Weather Settings | SGP | Get/Set SAME Group Settings | True |
|52| Motorola Custom Band Plan | MCP | Get/Set Motorola Custom Band Plan Settings | True |
|53| Test | WIN | *Get Window Voltage | |
|54| Test | BAV | *Get Battery Voltage | |

License
=======

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
