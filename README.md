bc246t
======

Serial protocol wrapper for the BC246T radio scanner.

Remote Command List
===================

<tr><th>  </th><th> Category </th><th> Command </th><th> Function </th><th> Program Mode </th></tr>
<tr><th>~~1~~</th><td> Remote Control </td><td> GID </td><td> Get Current Talkground ID Status </td><td> </td></tr>
<tr><th>~~2~~</th><td> Remote Control </td><td> KEY </td><td> Push KEY </td><td> </td></tr>
<tr><th>~~3~~</th><td> Remote Control </td><td> POF </td><td> Power OFF </td><td> </td></tr>
<tr><th>~~4~~</th><td> Remote Control </td><td> QSH </td><td> Go to quick search hold mode </td><td> </td></tr>
<tr><th>~~5~~</th><td> Remote Control </td><td> STS </td><td> Get Status </td><td> </td></tr>
<tr><th>~~6~~</th><td> System Information </td><td> MDL </td><td> Get Model Info </td><td> </td></tr>
<tr><th>~~7~~</th><td> System Information </td><td> VER </td><td> Get Firmware Version </td><td> </td></tr>
<tr><th>~~8~~</th><td> Programming Mode Control </td><td> PRG </td><td> Enter Program Mode </td><td> </td></tr>
<tr><th>~~9~~</th><td> Programming Mode Control </td><td> EPG </td><td> Exit Program Mode </td><td> </td></tr>
<tr><th>~~10~~</th><td> System Settings </td><td> BLT </td><td> Get/Set Backlight </td><td> True </td></tr>
<tr><th>~~11~~</th><td> System Settings </td><td> BSV </td><td> Get/Set Battery Save </td><td> True </td></tr>
<tr><th>~~12~~</th><td> System Settings </td><td> CLR </td><td> Clear All Memory </td><td> True </td></tr>
<tr><th>~~13~~</th><td> System Settings </td><td> KBP </td><td> Get/Set Key Beep </td><td> True </td></tr>
<tr><th>~~14~~</th><td> System Settings </td><td> OMS </td><td> Get/Set Opening Message </td><td> True </td></tr>
<tr><th>~~15~~</th><td> System Settings </td><td> PRI </td><td> Get/Set Priority Mode </td><td> True </td></tr>
<tr><th>~~16~~</th><td> Scan Settings </td><td> SCT </td><td> Get System Count </td><td> True </td></tr>
<tr><th>~~17~~</th><td> Scan Settings </td><td> SIH </td><td> Get System Index Head </td><td> True </td></tr>
<tr><th>~~18~~</th><td> Scan Settings </td><td> SIT </td><td> Get System Index Tail </td><td> True </td></tr>
<tr><th>~~19~~</th><td> Scan Settings </td><td> QSL </td><td> Get/Set System Quick Lockout </td><td> True </td></tr>
<tr><th>~~20~~</th><td> Scan Settings </td><td> QGL </td><td> Get/Set Group Quick Lockout </td><td> True </td></tr>
<tr><th>~~21~~</th><td> Scan Settings </td><td> CSY </td><td> Create System </td><td> True </td></tr>
<tr><th>~~22~~</th><td> Scan Settings </td><td> DSY </td><td> Delete System </td><td> True </td></tr>
<tr><th>23</th><td> Scan Settings </td><td> CPS </td><td> Copy System </td><td> True </td></tr>
<tr><th>~~24~~</th><td> Scan Settings </td><td> SIN </td><td> Get/Set System Info </td><td> True </td></tr>
<tr><th>25</th><td> Scan Settings </td><td> TRN </td><td> Get/Set Trunk Info </td><td> True </td></tr>
<tr><th>26</th><td> Scan Settings </td><td> TFQ </td><td> Get/Set Trunk Frequency Info </td><td> True </td></tr>
<tr><th>27</th><td> Scan Settings </td><td> AGC </td><td> Append Channel Group </td><td> True </td></tr>
<tr><th>28</th><td> Scan Settings </td><td> AGT </td><td> Append TGID Group </td><td> True </td></tr>
<tr><th>29</th><td> Scan Settings </td><td> DGR </td><td> Delete Group </td><td> True </td></tr>
<tr><th>30</th><td> Scan Settings </td><td> GIN </td><td> Get/Set Group Info </td><td> True </td></tr>
<tr><th>31</th><td> Scan Settings </td><td> ACC </td><td> Append Channel </td><td> True </td></tr>
<tr><th>32</th><td> Scan Settings </td><td> ACT </td><td> Append TGID </td><td> True </td></tr>
<tr><th>33</th><td> Scan Settings </td><td> DCH </td><td> Delete Channel </td><td> True </td></tr>
<tr><th>34</th><td> Scan Settings </td><td> CIN </td><td> Get/Set Channel Info </td><td> True </td></tr>
<tr><th>35</th><td> Scan Settings </td><td> TIN </td><td> Get/Set TGID Info </td><td> True </td></tr>
<tr><th>36</th><td> Scan Settings </td><td> GLI </td><td> Get Lockout TGID (for Rvw L/O ID) </td><td> True </td></tr>
<tr><th>37</th><td> Scan Settings </td><td> ULI </td><td> Unlock TGID (for Rvw L/O ID) </td><td> True </td></tr>
<tr><th>38</th><td> Scan Settings </td><td> LOI </td><td> Lock Out ID (TGID) </td><td> True </td></tr>
<tr><th>39</th><td> Scan Settings </td><td> REV </td><td> Get Rev Index </td><td> True </td></tr>
<tr><th>40</th><td> Scan Settings </td><td> FWD </td><td> Get Fwd Index </td><td> True </td></tr>
<tr><th>41</th><td> Scan Settings </td><td> RNB </td><td> Get Remains of Memory Block </td><td> True </td></tr>
<tr><th>42</th><td> Scan Settings </td><td> MEM </td><td> Get Memory Used </td><td> True </td></tr>
<tr><th>43</th><td> Search/Close Call Settings </td><td> SCO </td><td> Get/Set Search/Close Call Settings </td><td> True </td></tr>
<tr><th>44</th><td> Search/Close Call Settings </td><td> GLF </td><td> Get Global Lockout Freq </td><td> True </td></tr>
<tr><th>45</th><td> Search/Close Call Settings </td><td> ULF </td><td> Unlock Global L/O </td><td> True </td></tr>
<tr><th>46</th><td> Search/Close Call Settings </td><td> LOF </td><td> Lock Out Frequency </td><td> True </td></tr>
<tr><th>47</th><td> Search/Close Call Settings </td><td> CLC </td><td> Get/Set Close Call Settings </td><td> True </td></tr>
<tr><th>48</th><td> Custom Search Settings </td><td> CSG </td><td> Get/Set Custom Search Group </td><td> True </td></tr>
<tr><th>49</th><td> Custom Search Settings </td><td> CSP </td><td> Get/Set Custom Search Settings </td><td> True </td></tr>
<tr><th>50</th><td> Weather Settings </td><td> WPR </td><td> Get/Set Weather Priority Setting </td><td> True </td></tr>
<tr><th>51</th><td> Weather Settings </td><td> SGP </td><td> Get/Set SAME Group Settings </td><td> True </td></tr>
<tr><th>52</th><td> Motorola Custom Band Plan </td><td> MCP </td><td> Get/Set Motorola Custom Band Plan Settings </td><td> True </td></tr>
<tr><th>53</th><td> Test </td><td> WIN </td><td> *Get Window Voltage </td><td> </td></tr>
<tr><th>54</th><td> Test </td><td> BAV </td><td> *Get Battery Voltage </td><td> </td></tr>

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
