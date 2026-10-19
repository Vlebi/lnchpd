import time
from machine import Pin
import usb_midi


PIN_NUMBERS = [0, 1, 2, 3, 4, 5, 6, 7]
buttons = [Pin(p, Pin.IN, Pin.PULL_UP) for p in PIN_NUMBERS]

#Pages & Instrument Mappings
PAGE_NAMES = ["Drums", "Sound FX", "4-Track Looper", "Synth / Piano"]
current_page = 0  #0: Drums, 1: SFX, 2: Looper, 3: Synth

DRUM_NOTES  = [36, 38, 42, 39]  # Kick, Snare, Closed HH, Clap
SFX_NOTES   = [60, 62, 64, 65]  # Sample triggers
SYNTH_NOTES = [60, 62, 64, 67]  # C4, D4, E4, G4

#states: 0 = IDLE, 1 = RECORDING, 2 = PLAYING, 3 = STOPPED
track_states = [0, 0, 0, 0]
track_events = [[], [], [], []]
track_start_ticks = [0, 0, 0, 0]
track_duration_ms = [0, 0, 0, 0]
playback_start_ticks = [0, 0, 0, 0]
next_event_idx = [0, 0, 0, 0]


last_states = [1 for _ in buttons]
press_start_time = [0 for _ in buttons]

def send_midi(status, note, velocity):
    msg = bytes([status, note, velocity])
    usb_midi.ports[0].write(msg)

print("8-Button Controller Initialized (Drums, SFX, 4-Track Looper, Synth)...")

while True:
    current_time = time.ticks_ms()
    
    
    for t in range(4):
        if track_states[t] == 2 and track_duration_ms[t] > 0:  # PLAYING
            elapsed = time.ticks_diff(current_time, playback_start_ticks[t])
            if elapsed >= track_duration_ms[t]:
                playback_start_ticks[t] = current_time
                next_event_idx[t] = 0
                elapsed = 0
                
            while next_event_idx[t] < len(track_events[t]) and track_events[t][next_event_idx[t]][0] <= elapsed:
                _, status, note, velocity = track_events[t][next_event_idx[t]]
                send_midi(status, note, velocity)
                next_event_idx[t] += 1

   
    for i, btn in enumerate(buttons):
        state = btn.value()
        
        if state != last_states[i]:
            time.sleep_ms(15)  # Debounce
            if btn.value() == state:
                
                
                if state == 0:
                    press_start_time[i] = current_time
                    
                    
                    if i < 4:
                        if current_page == 2:
                           
                            pass
                        else:
                            
                            if current_page == 0:
                                note = DRUM_NOTES[i]
                            elif current_page == 1:
                                note = SFX_NOTES[i]
                            else:
                                note = SYNTH_NOTES[i]
                                
                            status = 0x90  
                            velocity = 127
                            send_midi(status, note, velocity)
                            print(f"[{PAGE_NAMES[current_page]}] Pad {i+1} -> Note {note} (On)")
                            
                           
                            for t in range(4):
                                if track_states[t] == 1:
                                    rel_time = time.ticks_diff(current_time, track_start_ticks[t])
                                    track_events[t].append((rel_time, status, note, velocity))

                    # Button 5: Page Switcher
                    elif i == 4:
                        current_page = (current_page + 1) % 4
                        print(f"Switched to Page {current_page}: {PAGE_NAMES[current_page]}")

                    # Button 6: Global Looper Control
                    elif i == 5:
                        pass  

                    # Button 7: FX 1 Control Change
                    elif i == 6:
                        send_midi(0xB0, 16, 127)
                        print("FX 1 (CC 16) On")

                    # Button 8: FX 2 Control Change
                    elif i == 7:
                        send_midi(0xB0, 17, 127)
                        print("FX 2 (CC 17) On")

                
                else:
                    press_duration = time.ticks_diff(current_time, press_start_time[i])
                    
                    
                    if i < 4:
                        if current_page == 2:
                           
                            track_idx = i
                            if press_duration > 1000:
                                track_states[track_idx] = 0
                                track_events[track_idx] = []
                                track_duration_ms[track_idx] = 0
                                print(f"Looper Track {track_idx+1}: ERASED.")
                            else:  
                                st = track_states[track_idx]
                                if st == 0 or st == 3:
                                    track_events[track_idx] = []
                                    track_start_ticks[track_idx] = current_time
                                    track_states[track_idx] = 1
                                    print(f"Looper Track {track_idx+1}: RECORDING...")
                                elif st == 1:
                                    track_duration_ms[track_idx] = time.ticks_diff(current_time, track_start_ticks[track_idx])
                                    track_states[track_idx] = 2
                                    playback_start_ticks[track_idx] = current_time
                                    next_event_idx[track_idx] = 0
                                    print(f"Looper Track {track_idx+1}: PLAYING ({track_duration_ms[track_idx]}ms).")
                                elif st == 2:
                                    track_states[track_idx] = 3
                                    print(f"Looper Track {track_idx+1}: STOPPED.")
                        else:
                            
                            if current_page == 0:
                                note = DRUM_NOTES[i]
                            elif current_page == 1:
                                note = SFX_NOTES[i]
                            else:
                                note = SYNTH_NOTES[i]
                                
                            status = 0x80  # Note Off
                            velocity = 0
                            send_midi(status, note, velocity)
                            
                            
                            for t in range(4):
                                if track_states[t] == 1:
                                    rel_time = time.ticks_diff(current_time, track_start_ticks[t])
                                    track_events[t].append((rel_time, status, note, velocity))

                    # Button 6: Global Looper Command Release
                    elif i == 5:
                        if press_duration > 1000: 
                            for t in range(4):
                                track_states[t] = 0
                                track_events[t] = []
                                track_duration_ms[t] = 0
                            print("Global Looper: ALL tracks ERASED.")
                        else:
                            print("Global Looper: Global action shortcut.")

                    # Button 7 Release
                    elif i == 6:
                        send_midi(0xB0, 16, 0)
                        print("FX 1 Off")

                    # Button 8 Release
                    elif i == 7:
                        send_midi(0xB0, 17, 0)
                        print("FX 2 Off")

                last_states[i] = state

    time.sleep_ms(2)