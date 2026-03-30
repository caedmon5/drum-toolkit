#!/usr/bin/env python3
"""
Drum Pattern Toolkit Generator
Generates a curated set of MIDI drum patterns for scratch-track production.
Organized by instrument layer for mix-and-match assembly.

General MIDI Drum Map (Channel 10):
  36 = Bass Drum 1
  37 = Side Stick (Rimclick)
  38 = Acoustic Snare
  42 = Closed Hi-Hat
  44 = Hi-Hat Pedal
  46 = Open Hi-Hat
  49 = Crash Cymbal 1
  50 = High Tom
  47 = Mid Tom (Low-Mid Tom)
  45 = Low Tom
  43 = Floor Tom (High Floor Tom)
  41 = Low Floor Tom
  51 = Ride Cymbal
"""

import mido
import os

# --- Constants ---
TPQN = 480  # ticks per quarter note
DEFAULT_BPM = 120
BEAT = TPQN                    # quarter note
HALF = TPQN * 2               # half note
EIGHTH = TPQN // 2            # eighth note
SIXTEENTH = TPQN // 4         # sixteenth note
BAR = TPQN * 4                # one bar of 4/4
BAR_34 = TPQN * 3             # one bar of 3/4
TRIPLET_8TH = TPQN // 3       # eighth-note triplet

# GM Drum Map
KICK = 36
SNARE = 38
RIMCLICK = 37
HIHAT_CLOSED = 42
HIHAT_OPEN = 46
HIHAT_PEDAL = 44
RIDE = 51
CRASH = 49
HIGH_TOM = 50
MID_TOM = 47
LOW_TOM = 45
FLOOR_TOM = 43
LOW_FLOOR_TOM = 41

# Velocity defaults
V_FULL = 100
V_ACCENT = 110
V_MED = 85
V_GHOST = 50
V_LIGHT = 65
V_FLAT = 90  # for Ringo/Barrett-style even hits

# Output directory structure
OUT_BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "midi", "Scratch Drum Toolkit")

# Subfolder names
SUB_KICKS = "Kicks"
SUB_HIHATS = "Hi-Hats"
SUB_SNARES = "Snares"
SUB_FILLS = "Fills"
SUB_JAZZ = "Jazz"
SUB_REGGAE = "Reggae"
SUB_LATIN = "Latin"
SUB_BOSSA = "Bossa Nova"
SUB_SAMBA = "Samba"


def make_midi(filename, notes, subfolder, bars=2, time_sig=(4, 4), bpm=DEFAULT_BPM):
    """
    Create a MIDI file from a list of (tick, pitch, velocity, duration) tuples.
    `bars` controls how many bars of the pattern are written (for looping context).
    `notes` should describe ONE bar; it gets repeated `bars` times.
    """
    mid = mido.MidiFile(ticks_per_beat=TPQN)
    track = mido.MidiTrack()
    mid.tracks.append(track)

    # Tempo
    track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(bpm)))
    # Time signature
    track.append(mido.MetaMessage('time_signature',
                                   numerator=time_sig[0],
                                   denominator=time_sig[1]))
    track.append(mido.MetaMessage('track_name', name=filename))

    bar_len = TPQN * time_sig[0] * (4 // time_sig[1])

    # Collect all events across all bars
    events = []
    for bar_num in range(bars):
        offset = bar_num * bar_len
        for tick, pitch, vel, dur in notes:
            on_time = offset + tick
            off_time = on_time + dur
            events.append((on_time, 'note_on', pitch, vel))
            events.append((off_time, 'note_off', pitch, 0))

    # Sort by time, then note_off before note_on at same time
    events.sort(key=lambda e: (e[0], 0 if e[1] == 'note_off' else 1))

    # Convert to delta times
    prev_time = 0
    for abs_time, msg_type, pitch, vel in events:
        delta = abs_time - prev_time
        if msg_type == 'note_on':
            track.append(mido.Message('note_on', note=pitch, velocity=vel,
                                       time=delta, channel=9))
        else:
            track.append(mido.Message('note_off', note=pitch, velocity=0,
                                       time=delta, channel=9))
        prev_time = abs_time

    outdir = os.path.join(OUT_BASE, subfolder)
    os.makedirs(outdir, exist_ok=True)
    filepath = os.path.join(outdir, filename + ".mid")
    mid.save(filepath)
    return filepath


def make_midi_absolute(filename, events_abs, subfolder, bpm=DEFAULT_BPM, time_sig=(4, 4)):
    """
    Create a MIDI file from absolute-timed events (no bar repetition).
    events_abs: list of (tick, pitch, velocity, duration)
    """
    mid = mido.MidiFile(ticks_per_beat=TPQN)
    track = mido.MidiTrack()
    mid.tracks.append(track)

    track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(bpm)))
    track.append(mido.MetaMessage('time_signature',
                                   numerator=time_sig[0],
                                   denominator=time_sig[1]))
    track.append(mido.MetaMessage('track_name', name=filename))

    events = []
    for tick, pitch, vel, dur in events_abs:
        events.append((tick, 'note_on', pitch, vel))
        events.append((tick + dur, 'note_off', pitch, 0))

    events.sort(key=lambda e: (e[0], 0 if e[1] == 'note_off' else 1))

    prev_time = 0
    for abs_time, msg_type, pitch, vel in events:
        delta = abs_time - prev_time
        if msg_type == 'note_on':
            track.append(mido.Message('note_on', note=pitch, velocity=vel,
                                       time=delta, channel=9))
        else:
            track.append(mido.Message('note_off', note=pitch, velocity=0,
                                       time=delta, channel=9))
        prev_time = abs_time

    outdir = os.path.join(OUT_BASE, subfolder)
    os.makedirs(outdir, exist_ok=True)
    filepath = os.path.join(outdir, filename + ".mid")
    mid.save(filepath)
    return filepath


def swing_eighth(beat_pos, swing_pct):
    """
    Return tick position for a swung eighth note.
    beat_pos: which beat (0-based, in quarter notes)
    swing_pct: 0.5 = straight, 0.67 = triplet swing
    For upbeats (the 'and'), shift proportionally.
    """
    beat_num = int(beat_pos)
    is_upbeat = (beat_pos % 1) > 0.25
    if is_upbeat:
        return beat_num * BEAT + int(BEAT * swing_pct)
    else:
        return int(beat_pos * BEAT)


# Duration shorthand
DUR_SHORT = SIXTEENTH
DUR_8TH = EIGHTH
DUR_BEAT = BEAT


# ============================================================
# KICK PATTERNS (4/4)
# ============================================================

def build_kick_patterns():
    patterns = []

    # 1. Basic backbeat: kick on 1, 3
    notes = [
        (0, KICK, V_FULL, DUR_SHORT),
        (2 * BEAT, KICK, V_FULL, DUR_SHORT),
    ]
    patterns.append(("pattern_basic_1-3", notes))

    # 2. Anticipated 4: kick on 1, 3, 3+
    notes = [
        (0, KICK, V_FULL, DUR_SHORT),
        (2 * BEAT, KICK, V_FULL, DUR_SHORT),
        (2 * BEAT + EIGHTH, KICK, V_MED, DUR_SHORT),
    ]
    patterns.append(("pattern_anticipated4_1-3-3and", notes))

    # 3. Pushed 2: kick on 1, 2+, 3
    notes = [
        (0, KICK, V_FULL, DUR_SHORT),
        (BEAT + EIGHTH, KICK, V_MED, DUR_SHORT),
        (2 * BEAT, KICK, V_FULL, DUR_SHORT),
    ]
    patterns.append(("pattern_pushed2_1-2and-3", notes))

    # 4. Driving: kick on 1, 2+, 3, 4+
    notes = [
        (0, KICK, V_FULL, DUR_SHORT),
        (BEAT + EIGHTH, KICK, V_MED, DUR_SHORT),
        (2 * BEAT, KICK, V_FULL, DUR_SHORT),
        (3 * BEAT + EIGHTH, KICK, V_MED, DUR_SHORT),
    ]
    patterns.append(("pattern_driving_1-2and-3-4and", notes))

    # 5. Four on the floor: kick on 1, 2, 3, 4
    notes = [
        (0, KICK, V_FULL, DUR_SHORT),
        (BEAT, KICK, V_FULL, DUR_SHORT),
        (2 * BEAT, KICK, V_FULL, DUR_SHORT),
        (3 * BEAT, KICK, V_FULL, DUR_SHORT),
    ]
    patterns.append(("pattern_four_on_floor", notes))

    # 6. Half-time: kick on 1 only (snare moves to 3 — but snare is a
    #    separate layer, so this is just the kick)
    notes = [
        (0, KICK, V_FULL, DUR_SHORT),
    ]
    patterns.append(("pattern_halftime_1_only", notes))

    # 7. One-drop (reggae): kick on 2 and 4 (with snare — but as kick layer)
    notes = [
        (BEAT, KICK, V_FULL, DUR_SHORT),
        (3 * BEAT, KICK, V_FULL, DUR_SHORT),
    ]
    patterns.append(("pattern_onedrop_2-4", notes))

    # 8. Dotted quarter / cross-rhythm: kick on 1, 2+, 4
    notes = [
        (0, KICK, V_FULL, DUR_SHORT),
        (BEAT + EIGHTH, KICK, V_MED, DUR_SHORT),
        (3 * BEAT, KICK, V_FULL, DUR_SHORT),
    ]
    patterns.append(("pattern_dotted_quarter_1-2and-4", notes))

    return patterns


# ============================================================
# KICK PATTERNS (3/4)
# ============================================================

def build_kick_34_patterns():
    patterns = []

    # 1. Basic waltz: kick on 1
    notes = [
        (0, KICK, V_FULL, DUR_SHORT),
    ]
    patterns.append(("pattern_waltz_basic_1", notes))

    # 2. Country waltz: kick on 1 and 3
    notes = [
        (0, KICK, V_FULL, DUR_SHORT),
        (2 * BEAT, KICK, V_MED, DUR_SHORT),
    ]
    patterns.append(("pattern_waltz_country_1-3", notes))

    return patterns


# ============================================================
# HI-HAT PATTERNS
# ============================================================

def build_hihat_patterns():
    patterns = []

    # 1. Straight 8ths closed
    notes = []
    for i in range(8):
        notes.append((i * EIGHTH, HIHAT_CLOSED, V_MED, DUR_SHORT))
    patterns.append(("pattern_straight_8ths", notes))

    # 2. Straight 16ths closed
    notes = []
    for i in range(16):
        vel = V_MED if (i % 2 == 0) else V_LIGHT
        notes.append((i * SIXTEENTH, HIHAT_CLOSED, vel, DUR_SHORT))
    patterns.append(("pattern_straight_16ths", notes))

    # 3. Quarter notes closed
    notes = []
    for i in range(4):
        notes.append((i * BEAT, HIHAT_CLOSED, V_MED, DUR_SHORT))
    patterns.append(("pattern_quarters", notes))

    # 4-6. Shuffle 8ths at three swing ratios
    for pct, label in [(0.55, "55pct"), (0.60, "60pct"), (0.67, "67pct_triplet")]:
        notes = []
        for beat in range(4):
            # downbeat
            notes.append((beat * BEAT, HIHAT_CLOSED, V_MED, DUR_SHORT))
            # swung upbeat
            swing_pos = beat * BEAT + int(BEAT * pct)
            notes.append((swing_pos, HIHAT_CLOSED, V_LIGHT, DUR_SHORT))
        patterns.append((f"pattern_shuffle_{label}", notes))

    # 7. Open on upbeats (closed on beats, open on +'s)
    notes = []
    for i in range(8):
        if i % 2 == 0:
            notes.append((i * EIGHTH, HIHAT_CLOSED, V_MED, DUR_SHORT))
        else:
            notes.append((i * EIGHTH, HIHAT_OPEN, V_MED, DUR_SHORT))
    patterns.append(("pattern_open_upbeats", notes))

    # 8. Upbeat 8ths only (ska)
    notes = []
    for i in range(4):
        notes.append((i * BEAT + EIGHTH, HIHAT_CLOSED, V_MED, DUR_SHORT))
    patterns.append(("pattern_upbeats_only_ska", notes))

    # 9. Accented 16ths (funk/Motown) — accent on 1 and 3 of each beat group
    notes = []
    for beat in range(4):
        for sub in range(4):
            tick = beat * BEAT + sub * SIXTEENTH
            vel = V_ACCENT if sub in (0, 2) else V_GHOST
            notes.append((tick, HIHAT_CLOSED, vel, DUR_SHORT))
    patterns.append(("pattern_accented_16ths_funk", notes))

    # 10. Ride quarter notes
    notes = []
    for i in range(4):
        notes.append((i * BEAT, RIDE, V_MED, DUR_SHORT))
    patterns.append(("pattern_ride_quarters", notes))

    return patterns


# ============================================================
# SNARE VARIATIONS
# ============================================================

def build_snare_patterns():
    patterns = []

    # 1. Full hit 2-4
    notes = [
        (BEAT, SNARE, V_FULL, DUR_SHORT),
        (3 * BEAT, SNARE, V_FULL, DUR_SHORT),
    ]
    patterns.append(("pattern_full_2-4", notes))

    # 2. Cross-stick / rimclick 2-4
    notes = [
        (BEAT, RIMCLICK, V_MED, DUR_SHORT),
        (3 * BEAT, RIMCLICK, V_MED, DUR_SHORT),
    ]
    patterns.append(("pattern_rimclick_2-4", notes))

    # 3. Ghost notes on e's and a's (funk)
    #    Full hits on 2 and 4, ghost notes on the e and a of each beat
    notes = [
        (BEAT, SNARE, V_FULL, DUR_SHORT),
        (3 * BEAT, SNARE, V_FULL, DUR_SHORT),
    ]
    for beat in range(4):
        # 'e' = 2nd sixteenth, 'a' = 4th sixteenth
        notes.append((beat * BEAT + SIXTEENTH, SNARE, V_GHOST, DUR_SHORT))
        notes.append((beat * BEAT + 3 * SIXTEENTH, SNARE, V_GHOST, DUR_SHORT))
    patterns.append(("pattern_ghost_notes_funk", notes))

    # 4. Half-time: snare on 3 only
    notes = [
        (2 * BEAT, SNARE, V_FULL, DUR_SHORT),
    ]
    patterns.append(("pattern_halftime_3_only", notes))

    return patterns


# ============================================================
# GENRE GESTURES (complete multi-instrument patterns)
# ============================================================

def build_genre_gestures():
    patterns = []

    # 1. Reggae one-drop (kick+snare on 2 & 4, beat 1 empty, upbeat hats)
    notes = [
        (BEAT, KICK, V_FULL, DUR_SHORT),
        (BEAT, RIMCLICK, V_MED, DUR_SHORT),
        (3 * BEAT, KICK, V_FULL, DUR_SHORT),
        (3 * BEAT, RIMCLICK, V_MED, DUR_SHORT),
    ]
    # Upbeat hi-hats
    for i in range(4):
        notes.append((i * BEAT + EIGHTH, HIHAT_CLOSED, V_LIGHT, DUR_SHORT))
    patterns.append(("pattern_reggae_onedrop", notes, SUB_REGGAE))

    # 2. Reggae steppers (four-on-floor kick, upbeat hats, rimclick 2-4)
    notes = [
        (0, KICK, V_FULL, DUR_SHORT),
        (BEAT, KICK, V_FULL, DUR_SHORT),
        (BEAT, RIMCLICK, V_MED, DUR_SHORT),
        (2 * BEAT, KICK, V_FULL, DUR_SHORT),
        (3 * BEAT, KICK, V_FULL, DUR_SHORT),
        (3 * BEAT, RIMCLICK, V_MED, DUR_SHORT),
    ]
    for i in range(4):
        notes.append((i * BEAT + EIGHTH, HIHAT_CLOSED, V_LIGHT, DUR_SHORT))
    patterns.append(("pattern_reggae_steppers", notes, SUB_REGGAE))

    # 3. Son clave 3-2 (two bars)
    #    Bar 1 (3-side): 1, 1+, 2+  |  Bar 2 (2-side): 2, 3
    events = [
        (0, RIMCLICK, V_FULL, DUR_SHORT),
        (EIGHTH, RIMCLICK, V_FULL, DUR_SHORT),  # actually "1 and-a" — let me fix
    ]
    # Standard son clave 3-2 in sixteenths over 2 bars:
    # Bar 1: X..X..X...X.X... -> positions 0, 3, 6, 10, 12 in sixteenths
    # Actually let me use the standard notation:
    # 3-side: beat 1, beat 2+, beat 4  (in the first bar)
    # 2-side: beat 2, beat 3  (in the second bar)
    # More precisely in a 2-bar pattern:
    # Hits at: 1, 1-and, 2-and-a, 3-and, 4 (of first bar-pair)
    # Let me use the definitive version:
    # 3-2 son clave (8 beats, 2 bars):
    #   1 . . 1 . . 1 . . . 1 . 1 . . .  (in 16th grid, 0-indexed)
    #   pos: 0, 3, 6, 10, 12
    events = []
    clave_positions = [0, 3, 6, 10, 12]  # in sixteenths over 2 bars
    for pos in clave_positions:
        events.append((pos * SIXTEENTH, RIMCLICK, V_FULL, DUR_SHORT))
    make_midi_absolute("pattern_latin_son_clave_3-2", events, SUB_LATIN)

    # 4. Son clave 2-3 (reversed)
    events = []
    clave_23 = [2, 4, 6, 9, 12]  # 2-side first, then 3-side  -- wait
    # Correction: 2-3 clave is the 2-bar pattern reversed:
    # 2-side: . . 1 . 1 . . . | 3-side: 1 . . 1 . . 1 . . . (wait no)
    # Let me be precise. 3-2: bar1=[0,3,6] bar2=[2,4] in 8th positions
    # In 16th positions over 2 bars (32 sixteenths):
    # 3-2: 0, 6, 12, 20, 24  (in 16ths) -- no let me just use the standard
    # 3-2 son clave in eighth-note positions over 2 bars (16 eighths):
    #   X . . X . . X . . . X . X . . .
    #   0     3     6       10  12
    # So in tick positions: 0, 3*E, 6*E, 10*E, 12*E where E=EIGHTH
    # 2-3 is simply shifted by one bar:
    #   . . X . X . . . X . . X . . X .
    #   i.e. the 2-side first: 10, 12 -> 2, 4
    #   then the 3-side: 0, 3, 6 -> 8, 11, 14
    # In eighth positions: 2, 4, 8, 11, 14
    clave_23_eighths = [2, 4, 8, 11, 14]
    events = []
    for pos in clave_23_eighths:
        events.append((pos * EIGHTH, RIMCLICK, V_FULL, DUR_SHORT))
    make_midi_absolute("pattern_latin_son_clave_2-3", events, SUB_LATIN)

    # Fix clave 3-2 to use eighth positions too for consistency
    # 3-2 in eighth positions: 0, 3, 6, 10, 12
    # Already done above with sixteenths — let me redo properly
    os.remove(os.path.join(OUT_BASE, SUB_LATIN, "pattern_latin_son_clave_3-2.mid"))
    events = []
    clave_32_eighths = [0, 3, 6, 10, 12]
    for pos in clave_32_eighths:
        events.append((pos * EIGHTH, RIMCLICK, V_FULL, DUR_SHORT))
    make_midi_absolute("pattern_latin_son_clave_3-2", events, SUB_LATIN)

    # 5. Tresillo (the 3-side of clave as a standalone 1-bar kick pattern)
    #    Hits on 1, 1+, 2+ in a bar  -> ticks: 0, 3*EIGHTH (dotted quarter), 6*EIGHTH
    #    Wait — tresillo in one bar of 4/4:
    #    3 + 3 + 2 in eighth notes: positions 0, 3, 6 in eighths
    notes = [
        (0, KICK, V_FULL, DUR_SHORT),
        (3 * EIGHTH, KICK, V_FULL, DUR_SHORT),
        (6 * EIGHTH, KICK, V_FULL, DUR_SHORT),
    ]
    patterns.append(("pattern_latin_tresillo_kick", notes, SUB_LATIN))

    # 6. Bossa nova kick (dotted quarter feel)
    #    Kick on 1 and 2+ (the "and" of 2)
    notes = [
        (0, KICK, V_MED, DUR_SHORT),
        (BEAT + EIGHTH, KICK, V_MED, DUR_SHORT),
    ]
    # Add cross-stick on rim for the bossa pattern
    notes.append((2 * BEAT, RIMCLICK, V_LIGHT, DUR_SHORT))
    notes.append((3 * BEAT, RIMCLICK, V_LIGHT, DUR_SHORT))
    patterns.append(("pattern_bossa_nova", notes, SUB_BOSSA))

    # 7. Basic samba surdo (low on 2, high on 1)
    notes = [
        (0, MID_TOM, V_MED, DUR_8TH),       # higher surdo on 1
        (BEAT, FLOOR_TOM, V_FULL, DUR_8TH),  # lower surdo on 2
        (2 * BEAT, MID_TOM, V_MED, DUR_8TH),
        (3 * BEAT, FLOOR_TOM, V_FULL, DUR_8TH),
    ]
    patterns.append(("pattern_samba_surdo", notes, SUB_SAMBA))

    return patterns


# ============================================================
# FILLS
# ============================================================

def build_fills():
    # Fills are single instances — no bar repetition.
    # Most are 1-beat or 2-beat fills that lead into beat 1.
    # We'll write them as 1-bar items where the fill occupies the end
    # and resolves to a crash on the downbeat of bar 2.

    # 1. 16th descending toms (classic rock fill, 1 beat on beat 4)
    events = [
        (3 * BEAT, HIGH_TOM, V_FULL, DUR_SHORT),
        (3 * BEAT + SIXTEENTH, MID_TOM, V_FULL, DUR_SHORT),
        (3 * BEAT + 2 * SIXTEENTH, LOW_TOM, V_FULL, DUR_SHORT),
        (3 * BEAT + 3 * SIXTEENTH, FLOOR_TOM, V_FULL, DUR_SHORT),
        (4 * BEAT, CRASH, V_ACCENT, DUR_8TH),
        (4 * BEAT, KICK, V_FULL, DUR_SHORT),
    ]
    make_midi_absolute("fill_16th_descending_toms", events, SUB_FILLS)

    # 2. Triplet descending toms (beats 3-4)
    trip = TRIPLET_8TH
    events = [
        (2 * BEAT, HIGH_TOM, V_FULL, DUR_SHORT),
        (2 * BEAT + trip, HIGH_TOM, V_MED, DUR_SHORT),
        (2 * BEAT + 2 * trip, MID_TOM, V_FULL, DUR_SHORT),
        (3 * BEAT, MID_TOM, V_MED, DUR_SHORT),
        (3 * BEAT + trip, LOW_TOM, V_FULL, DUR_SHORT),
        (3 * BEAT + 2 * trip, FLOOR_TOM, V_FULL, DUR_SHORT),
        (4 * BEAT, CRASH, V_ACCENT, DUR_8TH),
        (4 * BEAT, KICK, V_FULL, DUR_SHORT),
    ]
    make_midi_absolute("fill_triplet_descending_toms", events, SUB_FILLS)

    # 3. Single-stroke snare roll (16ths, beats 3-4)
    events = []
    for i in range(8):
        tick = 2 * BEAT + i * SIXTEENTH
        vel = V_MED + (i * 3)  # slight crescendo
        events.append((tick, SNARE, min(vel, 127), DUR_SHORT))
    events.append((4 * BEAT, CRASH, V_ACCENT, DUR_8TH))
    events.append((4 * BEAT, KICK, V_FULL, DUR_SHORT))
    make_midi_absolute("fill_snare_roll_16ths", events, SUB_FILLS)

    # 4. Kick-snare alternating 16ths (beat 4)
    events = [
        (3 * BEAT, KICK, V_FULL, DUR_SHORT),
        (3 * BEAT + SIXTEENTH, SNARE, V_FULL, DUR_SHORT),
        (3 * BEAT + 2 * SIXTEENTH, KICK, V_FULL, DUR_SHORT),
        (3 * BEAT + 3 * SIXTEENTH, SNARE, V_FULL, DUR_SHORT),
        (4 * BEAT, CRASH, V_ACCENT, DUR_8TH),
        (4 * BEAT, KICK, V_FULL, DUR_SHORT),
    ]
    make_midi_absolute("fill_kick_snare_alternating", events, SUB_FILLS)

    # 5. Simple crash setup (snare on 4, crash+kick on 1)
    events = [
        (3 * BEAT, SNARE, V_ACCENT, DUR_SHORT),
        (4 * BEAT, CRASH, V_ACCENT, DUR_8TH),
        (4 * BEAT, KICK, V_FULL, DUR_SHORT),
    ]
    make_midi_absolute("fill_crash_setup", events, SUB_FILLS)

    # 6. Reggae high-tom fill (1 beat) — syncopated tight toms, Barrett-style
    #    Even velocity, rapid, on beat 4
    events = [
        (3 * BEAT, HIGH_TOM, V_FLAT, DUR_SHORT),
        (3 * BEAT + SIXTEENTH, HIGH_TOM, V_FLAT, DUR_SHORT),
        (3 * BEAT + 2 * SIXTEENTH + SIXTEENTH // 2, HIGH_TOM, V_FLAT, DUR_SHORT),  # slightly syncopated
        (3 * BEAT + 3 * SIXTEENTH, HIGH_TOM, V_FLAT, DUR_SHORT),
        (4 * BEAT, KICK, V_FULL, DUR_SHORT),
    ]
    make_midi_absolute("fill_reggae_hightom_1beat", events, SUB_FILLS)

    # 7. Reggae high-tom fill (2 beat) — beats 3-4, flat velocity
    events = [
        (2 * BEAT, HIGH_TOM, V_FLAT, DUR_SHORT),
        (2 * BEAT + EIGHTH, HIGH_TOM, V_FLAT, DUR_SHORT),
        (2 * BEAT + EIGHTH + SIXTEENTH, HIGH_TOM, V_FLAT, DUR_SHORT),
        (3 * BEAT, HIGH_TOM, V_FLAT, DUR_SHORT),
        (3 * BEAT + SIXTEENTH, HIGH_TOM, V_FLAT, DUR_SHORT),
        (3 * BEAT + EIGHTH, HIGH_TOM, V_FLAT, DUR_SHORT),
        (3 * BEAT + EIGHTH + SIXTEENTH, HIGH_TOM, V_FLAT, DUR_SHORT),
        (4 * BEAT, KICK, V_FULL, DUR_SHORT),
    ]
    make_midi_absolute("fill_reggae_hightom_2beat", events, SUB_FILLS)

    # 8. Laid-back syncopated fill (Ringo-style, beats 3-4)
    #    Hits on the "wrong" subdivisions — 3a, 4e, 4a → 1
    #    "3a" = beat 3 + 3 sixteenths, "4e" = beat 4 + 1 sixteenth,
    #    "4a" = beat 4 + 3 sixteenths
    events = [
        (2 * BEAT + 3 * SIXTEENTH, SNARE, V_MED, DUR_SHORT),       # 3-a
        (3 * BEAT + SIXTEENTH, SNARE, V_MED, DUR_SHORT),            # 4-e
        (3 * BEAT + 3 * SIXTEENTH, SNARE, V_MED, DUR_SHORT),        # 4-a
        (4 * BEAT, CRASH, V_ACCENT, DUR_8TH),
        (4 * BEAT, KICK, V_FULL, DUR_SHORT),
    ]
    make_midi_absolute("fill_laidback_syncopated", events, SUB_FILLS)

    # 9. Metric displacement fill (2-bar, groups of 3 over 4/4)
    #    Dotted-quarter pattern (3 eighths per group) running across 2 bars,
    #    resolving on beat 1 of bar 3.
    #    Dotted quarter = 3 * EIGHTH = 720 ticks
    #    Over 2 bars (3840 ticks), hits at: 0, 720, 1440, 2160, 2880, 3600
    #    That's ~5.33 groups, so hit at 3600 then resolve at 3840 (bar 3 beat 1)
    dot_q = 3 * EIGHTH
    events = []
    pos = 0
    voices = [HIGH_TOM, SNARE, FLOOR_TOM]  # cycle through voices for interest
    i = 0
    while pos < 2 * BAR:
        voice = voices[i % len(voices)]
        events.append((pos, voice, V_MED, DUR_SHORT))
        pos += dot_q
        i += 1
    # Resolution: crash + kick on bar 3 beat 1
    events.append((2 * BAR, CRASH, V_ACCENT, DUR_8TH))
    events.append((2 * BAR, KICK, V_FULL, DUR_SHORT))
    make_midi_absolute("fill_metric_displacement_2bar", events, SUB_FILLS)


# ============================================================
# JAZZ PATTERNS
# ============================================================

def build_jazz_patterns():
    patterns = []

    # 1. Swing ride (spang-a-lang) with hi-hat pedal on 2-4
    #    Ride: 1, 2, trip-3-of-2, 3, 4, trip-3-of-4
    #    i.e., quarter notes with a triplet pickup to beats 2 and 4
    #    Classic: 1, trip-let-3-of-1, 2, trip-let-3-of-2, 3, trip-let-3-of-3, 4, trip-let-3-of-4
    #    Simplified spang-a-lang: ride on 1, 2, (2+trip), 3, 4, (4+trip)
    trip = TPQN * 2 // 3  # position of the 3rd triplet partial within a beat
    notes = [
        (0, RIDE, V_MED, DUR_SHORT),                           # 1
        (BEAT, RIDE, V_MED, DUR_SHORT),                        # 2
        (BEAT + trip, RIDE, V_LIGHT, DUR_SHORT),               # trip of 2
        (2 * BEAT, RIDE, V_MED, DUR_SHORT),                    # 3
        (3 * BEAT, RIDE, V_MED, DUR_SHORT),                    # 4
        (3 * BEAT + trip, RIDE, V_LIGHT, DUR_SHORT),           # trip of 4
        # Hi-hat pedal on 2 and 4
        (BEAT, HIHAT_PEDAL, V_LIGHT, DUR_SHORT),
        (3 * BEAT, HIHAT_PEDAL, V_LIGHT, DUR_SHORT),
    ]
    patterns.append(("pattern_swing_ride_spangalang", notes))

    # 2. Straight ride (modal/cool jazz) — quarters on ride, hat pedal 2-4
    notes = [
        (0, RIDE, V_MED, DUR_SHORT),
        (BEAT, RIDE, V_MED, DUR_SHORT),
        (2 * BEAT, RIDE, V_MED, DUR_SHORT),
        (3 * BEAT, RIDE, V_MED, DUR_SHORT),
        (BEAT, HIHAT_PEDAL, V_LIGHT, DUR_SHORT),
        (3 * BEAT, HIHAT_PEDAL, V_LIGHT, DUR_SHORT),
    ]
    patterns.append(("pattern_straight_ride", notes))

    # 3. Brush-like ghost snare pattern (simulates brush texture)
    #    Light ghost notes throughout with very slight accents on 2 and 4
    notes = [
        (BEAT, SNARE, V_LIGHT, DUR_SHORT),                    # 2
        (3 * BEAT, SNARE, V_LIGHT, DUR_SHORT),                # 4
    ]
    # Ghost notes on various subdivisions
    ghost_positions = [
        EIGHTH,                     # 1+
        BEAT + EIGHTH,              # 2+
        2 * BEAT + EIGHTH,          # 3+
        2 * BEAT,                   # 3
    ]
    for pos in ghost_positions:
        notes.append((pos, SNARE, V_GHOST, DUR_SHORT))
    patterns.append(("pattern_brush_ghost_snare", notes))

    return patterns


# ============================================================
# MAIN
# ============================================================

def main():
    # Clean and recreate output tree
    import shutil
    if os.path.exists(OUT_BASE):
        shutil.rmtree(OUT_BASE)
    os.makedirs(OUT_BASE, exist_ok=True)

    files_created = []

    # Kick patterns (4/4)
    for name, notes in build_kick_patterns():
        f = make_midi(name, notes, SUB_KICKS, bars=2, time_sig=(4, 4))
        files_created.append(f)

    # Kick patterns (3/4)
    for name, notes in build_kick_34_patterns():
        f = make_midi(name, notes, SUB_KICKS, bars=2, time_sig=(3, 4))
        files_created.append(f)

    # Hi-hat patterns
    for name, notes in build_hihat_patterns():
        f = make_midi(name, notes, SUB_HIHATS, bars=2, time_sig=(4, 4))
        files_created.append(f)

    # Snare patterns
    for name, notes in build_snare_patterns():
        f = make_midi(name, notes, SUB_SNARES, bars=2, time_sig=(4, 4))
        files_created.append(f)

    # Genre gestures (some use make_midi, some use make_midi_absolute internally)
    for item in build_genre_gestures():
        name, notes, subfolder = item
        f = make_midi(name, notes, subfolder, bars=2, time_sig=(4, 4))
        files_created.append(f)

    # Fills (all use make_midi_absolute internally)
    build_fills()

    # Jazz patterns
    for name, notes in build_jazz_patterns():
        f = make_midi(name, notes, SUB_JAZZ, bars=2, time_sig=(4, 4))
        files_created.append(f)

    # Count all generated files
    total = 0
    for dirpath, dirnames, filenames in os.walk(OUT_BASE):
        total += len([f for f in filenames if f.endswith('.mid')])

    # Summary
    print(f"\n{'=' * 60}")
    print(f"Scratch Drum Toolkit — {total} files generated")
    print(f"Output: {OUT_BASE}")
    print(f"{'=' * 60}\n")

    for sub in sorted(os.listdir(OUT_BASE)):
        subpath = os.path.join(OUT_BASE, sub)
        if os.path.isdir(subpath):
            files = sorted(os.listdir(subpath))
            print(f"  {sub} ({len(files)}):")
            for f in files:
                print(f"    {f}")
            print()


if __name__ == "__main__":
    main()
