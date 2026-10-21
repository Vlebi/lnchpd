A compact, custom-designed USB-MIDI controller built for live DJ performance, sample triggering, and live looping. Powered by a Raspberry Pi Pico (RP2040) and custom-routed PCBs, running native MicroPython.

Features:

USB-MIDI: Works out of the box with any DAW without requiring custom drivers (i think so).

Multi-Page: 4 dynamic performance pads that switch their uses by paging, providing lots of features from a compact size.

4-Track Looper: Dedicated loop page where each pad handles its own loop track (Record, Playback, Stop, and Long-Press Erase). Supports cross-page recording.

Hardware Design: Built on a 2-layer 57mm x 62.1mm PCB with a copper ground pour (might need to let this one go for budget porpuses) and TACTR-12x12x7.5 tactile switches.

Button Layout and Controls:

Pads 1 to 4 (GPIO 0 to 3): Dynamic performance pads. Function changes based on the active page:

Page 0 (Drums): General MIDI drum map (Kick, Snare, Closed Hi-Hat, Clap).

Page 1 (samples): Sample triggers.

Page 2 (4-Track Looper): Control independent loop tracks 1 to 4.

Page 3 (Synth / Piano): Monophonic and polyphonic melodic scale leads.

Button 5 (GPIO 4): Page Switcher (Cycles through Drums, SFX, Looper, and Synth).

Button 6 (GPIO 5): Global Looper Command (Long press to wipe all tracks globally).

Button 7 (GPIO 6): FX Control 1 (Sends Control Change CC 16).

Button 8 (GPIO 7): FX Control 2 (Sends Control Change CC 17).


BOM:

Microcontroller: Raspberry Pi Pico

Switches: 8x TACTR-12x12x7.5 THT tactile microswitches

PCB: 2-layer FR4 board (57mm x 62.1mm) with a common ground rail layout



Getting Started and Firmware Installation:

Flash MicroPython.

Connect your Pico via USB.

Copy the main.py script and save it directly onto the Pico as main.py so it boots automatically.

Open your music software's MIDI settings, enable the Pico as an active input device, and map it.
