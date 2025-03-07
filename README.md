# 1dcoinctrl


## Western Electric 1D/2D Payphone Controller Interface for Asterisk


# WARNING - This project involves potentially lethal High-Voltage!

**_The coin relay in most payphones operates using +/- 130VDC.  This project uses a DC-DC converter to boost 12VDC to 130VDC.  Construction and operation of this circuit should only be performed by people familiar with best practices when operating with high voltage, and using extreme caution._**

I WILL NOT BE HELD LIABLE FOR INJURY OR DEATH RESULTING FROM BUILDING OR USING THIS CIRCUIT.   BUILD AND USE THIS CIRCUIT AT YOUR OWN RISK.

THIS HARDWARE AND SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL HOWARD M. HARTE BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE HARDWARE AND SOFTWARE OR THE USE OR OTHER DEALINGS IN THE HARDWARE AND SOFTWARE. 


# Overview

This project aims to emulate a coin line as required by the older "dumb" (ie, non-COCOT) payphones such as the Western Electric 1D "Fortress" series.  This coin line interface connects in between an Asterisk PBX and the payphone.  It provides the coin control functionality as well as the ability to determine whether an initial rate has been deposited, and can also perform the "stuck coin" test.

This project is based on another open-source project (see References below) and has the following goals:



1. Real coin-line signaling, while preserving the payphone earth ground.  This requires both +130VDC (coin collect) and -130VDC (coin refund) as well as +25VDC for the "stuck coin" test and -25VDC for the "initial rate" test.
2. The ability to provide up to four coin lines in a single unit.
3. The ability to count dial pulses from Rotary payphones and provide the digits out-of-band to Asterisk.
4. The ability to be [red-boxed](http://en.wikipedia.org/wiki/Red_box_(phreaking)).

![alt_text](https://raw.githubusercontent.com/hharte/1dcoinctrl/master/photos/1dcoinctrl_iss2.jpg "image_tooltip")


# Pay phone

The payphone is a standard Western Electric 1D phone with a 32B "dumb" chassis.  I also verified that Western Electric 32A and TeleService 4032C chassis work well with this design.


# Coin Line Signaling

All coin line signaling happens with respect to TIP and Ground with the RING open. For the tests, current flowing when voltage is applied indicates that either a coin is present in the hopper, or the initial rate has been deposited.


<table>
  <tr>
   <td>Voltage
   </td>
   <td>Operation
   </td>
  </tr>
  <tr>
   <td>+130VDC
   </td>
   <td>Collect coin.
   </td>
  </tr>
  <tr>
   <td>-130VDC
   </td>
   <td>Refund coin.
   </td>
  </tr>
  <tr>
   <td>+25VDC
   </td>
   <td>Stuck Coin Test
   </td>
  </tr>
  <tr>
   <td>-25VDC
   </td>
   <td>Initial Rate Test
   </td>
  </tr>
</table>



## Controlling the Coin Line Signaling

Control of the coin lines is handled by a PIC18F47Q84 microcontroller.  This microcontroller can sense the line polarity and ON/OFF hook status, the test status, and can control the relays on the controller.

There are three relays that provide common control, and two additional relays per line.


### Common Control Relays

1. **_REFUND_** Relay: When operated will prepare negative voltage to be applied to the TIP when the selected line's COIN_CONTROL relay is operated.  When this relay is operated, either Coin Refund or Initial Rate Test will be performed based on the state of the DISPOSITION relay.

2. **_DISPOSITION_** Relay: When operated will prepare high voltage (either +130VDC or -130VDC, depending on the state of the REFUND relay) to be applied to the TIP when the selected line's COIN_CONTROL relay is operated.  When the DISPOSITION relay is not operated, low voltage (+25VDC or -25VDC) will be applied in order to perform either the initial rate test or the stuck coin test.

3. **_POLE-CHANGER_** Relay: This relay is used to swap the Vout+ and Vout- on the output of the 130VDC DC-DC converter so that both +130VDC and -130VDC are available depending on whether the coin should be collected or refunded.


### Per-Line Relays (one each per coin line:)

1. **_HOLD_** Relay: When operated will shunt the TIP and RING towards the CO (Asterisk PBX in our case) with a 120-ohm resistor.  This will keep the line on hold while coin disposition or rate tests are performed.

2. **_COIN_CONTROL_** Relay: When operated, will apply the coin control voltage to the TIP towards the payphone.  When not operated, the TIP and RING from the CO (Asterisk PBX) will be passed through to the payphone.


### Sensors

There are several opto-isolated sensors in the design to provide status to the microcontroller.

1. **_TEST_STATUS_** sensor will go low when current is flowing during a test.  It will be high when current is not flowing.

2. Per-line **_OFF_HOOK_F and OFF_HOOK_R_** sensors (one per line) will go low when current is flowing through the loop to the CO (Asterisk PBX) and can detect forward and reverse polarity.  This current will be flowing either when the payphone is off-hook or when the line is on hold.


# Microcontroller Firmware

The microcontroller firmware is written in the C programming language, and provides a command-line interface that uses a command set modeled after the familiar Hayes AT command set.

The command syntax is AT followed by a single character command, and an optional number [1-4] for the coin line to operate on.  If the coin line is omitted, the previously used coin line is assumed.

Commands are as follows:


<table>
  <tr>
   <td><strong><em>Command</em></strong>
   </td>
   <td><strong><em>Description</em></strong>
   </td>
   <td><strong><em>Response</em></strong>
   </td>
  </tr>
  <tr>
   <td>AT
   </td>
   <td>Attention
   </td>
   <td>OK
   </td>
  </tr>
  <tr>
   <td>ATZ
   </td>
   <td>Reset
   </td>
   <td>OK
   </td>
  </tr>
  <tr>
   <td>ATC
   </td>
   <td>Collect coin
   </td>
   <td>OK
   </td>
  </tr>
  <tr>
   <td>ATR
   </td>
   <td>Refund coin
   </td>
   <td>OK
   </td>
  </tr>
  <tr>
   <td>ATI
   </td>
   <td>Initial rate test
   </td>
   <td>0 = Initial rate not deposited
<p>
1 = Initial rate deposited
   </td>
  </tr>
  <tr>
   <td>ATS
   </td>
   <td>Stuck coin test
   </td>
   <td>0 = No coin in escrow.
<p>
1 = Coin in escrow.
   </td>
  </tr>
  <tr>
   <td>ATQ
   </td>
   <td>Query hook state
   </td>
   <td>0 = On hook
<p>
1 = Off hook (normal polarity)
<p>
2 = Off hook (reversed polarity)
   </td>
  </tr>
  <tr>
   <td>ATL
   </td>
   <td>Query selected coin line
   </td>
   <td>1-4
   </td>
  </tr>
  <tr>
   <td>ATH
   </td>
   <td>Hold CO line
   </td>
   <td>OK
   </td>
  </tr>
  <tr>
   <td>ATU
   </td>
   <td>Un-hold CO line
   </td>
   <td>OK
   </td>
  </tr>
  <tr>
   <td>ATD
   </td>
   <td>Dump current controller state
   </td>
   <td>OK
   </td>
  </tr>
  <tr>
   <td>ATE
   </td>
   <td>Stress test 100 refunds (1s apart)
   </td>
   <td>OK
   </td>
  </tr>
  <tr>
   <td>ATT
   </td>
   <td>Coin line simulation
   </td>
   <td>Need hard reset to exit.
   </td>
  </tr>
  <tr>
   <td>ATV
   </td>
   <td>Display firmware version
   </td>
   <td>OK
   </td>
  </tr>
  <tr>
   <td>AT?
   </td>
   <td>Help
   </td>
   <td>Display command help
   </td>
  </tr>
</table>


 


# Building the Hardware


## Assembly

To reduce cost, the PCB can be assembled to support fewer than four pay phones.  If only one pay phone is desired, U3 (7406) can be omitted, as well as components associated with lines 2 through 4.


## Issue 3 PCB - Note this PCB has not been fabricated/tested yet!


### Microcontroller Upgrade

The PIC microcontroller was upgraded from a PIC18F45K50 to the newer PIC18F47Q84, which is largely pin compatible with the original part.  The PIC18F47Q84 does not support USB, so an optional FTDI USB UART header is provided, for those who do not wish to use RS-232.


### Other changes between Issue 2 and Issue 3:



* Remove barrel jack, replace with 4-position terminal block with provision for +/- 130VDC input in case the user already has an appropriate power supply and does not want the on-board DC-DC converter.  Note: 130V DC-DC converter PS2, relay K8, C14, D10, and R16 must be omitted during assembly.
* Added bi-color LEDs for line status.
    * Green=Off-hook, normal polarity.
    * Red=Off-hook, reverse polarity.
    * Off=on-hook.
* Add header for FTDI USB UART, if user does not need RS-232 UART levels.  To use the FTDI header, do not populate U1 and other components on pp. 3 of the schematic.


# Asterisk PBX Modifications

Modifications to Asterisk in order to recognize the 1700/2200Hz coin tones is based on [Joshua Stein's project](https://github.com/jcs/payphone) although I modified them to treat the 1700/2200Hz tones as a 5th row/column in the standard [DTMF](http://en.wikipedia.org/wiki/Dual-tone_multi-frequency_signaling) decoding routine in Asterisk's main/dsp.c.

The Asterisk AGI script is not complete, but at present it will prompt for money and can recognize the coin tones.  It will complete the call after 25 cents has been deposited.


## References



* [https://github.com/jcs/payphone](https://github.com/jcs/payphone)
* [Bell System Public Services Crafts' Manual for Station, Network, and Testboard](http://wedophones.com/TheBellSystem/pdf/bsp/coin/PublicServices1.pdf)
