# Drum Pattern Toolkit

A curated set of MIDI drum patterns for scratch-track production. Designed for mix-and-match assembly: pick a kick layer, a hi-hat layer, a snare variation, and optionally a fill or genre gesture. Drop them into REAPER (or any DAW) on the same track and they stack.

All files: General MIDI channel 10, 480 TPQN, 120 BPM default.

---

## KICK PATTERNS

Layer patterns — 2 bars each, loopable.

| File | Hits | Feel / Use |
|------|------|------------|
| `kick_01_basic_1-3` | 1, 3 | Default rock/pop/folk foundation. Pair with almost anything. |
| `kick_02_anticipated4_1-3-3and` | 1, 3, 3+ | Forward momentum. Common in rock/pop choruses. |
| `kick_03_pushed2_1-2and-3` | 1, 2+, 3 | Urgency. Punk-adjacent. |
| `kick_04_driving_1-2and-3-4and` | 1, 2+, 3, 4+ | Uptempo rock, power pop. |
| `kick_05_four_on_floor` | 1, 2, 3, 4 | Dance, disco, Motown uptempo. |
| `kick_06_halftime_1_only` | 1 | Heavy feel. Pair with `snare_04_halftime_3_only`. |
| `kick_07_onedrop_2-4` | 2, 4 | Reggae one-drop (kick layer only). Beat 1 is empty — that's the point. |
| `kick_08_dotted_quarter_1-2and-4` | 1, 2+, 4 | Cross-rhythm feel. Afrobeat-adjacent. |
| `kick_09_waltz_basic_1` | 1 | Standard 3/4. Folk, ballads. (3/4 time sig.) |
| `kick_10_waltz_country_1-3` | 1, 3 | Pushier waltz. Country. (3/4 time sig.) |

### Common pairings

- **Basic rock:** `kick_01` + `hh_01` + `snare_01`
- **Rock shuffle (Get Back):** `kick_01` + `hh_04_shuffle_60pct` + `snare_01`
- **Power pop:** `kick_04` + `hh_01` or `hh_02` + `snare_01`
- **Half-time heavy:** `kick_06` + `hh_03` + `snare_04`
- **Disco/dance:** `kick_05` + `hh_05` + `snare_01`

---

## HI-HAT PATTERNS

Layer patterns — 2 bars each, loopable.

| File | Description | Feel / Use |
|------|-------------|------------|
| `hh_01_straight_8ths` | Closed, every 8th note | Default rock/pop. The workhorse. |
| `hh_02_straight_16ths` | Closed, every 16th | Busier. Funk, R&B, uptempo pop. |
| `hh_03_quarters` | Closed, beats only | Sparse. Ballads, half-time, verses. |
| `hh_04_shuffle_55pct` | Swung 8ths, light swing | Gentle shuffle. Laid-back rock. |
| `hh_04_shuffle_60pct` | Swung 8ths, medium swing | "Get Back" territory. Classic rock shuffle. |
| `hh_04_shuffle_67pct_triplet` | Swung 8ths, true triplet | Blues shuffle. Stones. Early rock & roll. |
| `hh_05_open_upbeats` | Closed on beats, open on +'s | Disco, dance-rock, new wave. |
| `hh_06_upbeats_only_ska` | Hits on +'s only | Ska, upstroke feel. |
| `hh_07_accented_16ths_funk` | 16ths, accented on 1 and 3 of each group | Funk, Motown. Pair with `snare_03`. |
| `hh_08_ride_quarters` | Quarter notes on ride cymbal | Opens up the sound. Verse-to-chorus shift. |

### Shuffle note

The three shuffle variants (55%, 60%, 67%) differ in how far the upbeat is pushed toward the next downbeat. 50% would be straight eighths; 67% is a pure triplet. Most classic rock sits around 58–62%.

---

## SNARE VARIATIONS

Layer patterns — 2 bars each, loopable.

| File | Description | Feel / Use |
|------|-------------|------------|
| `snare_01_full_2-4` | Standard backbeat | Rock, pop. The default. |
| `snare_02_rimclick_2-4` | Cross-stick on 2 and 4 | Folk, ballad, verse feel. |
| `snare_03_ghost_notes_funk` | Full hits 2-4 with ghost notes on e's and a's | Funk, R&B groove. Pair with `hh_07`. |
| `snare_04_halftime_3_only` | Snare on 3 only | Half-time. Heavy, sludgy. Pair with `kick_06`. |

---

## GENRE GESTURES

Complete multi-instrument patterns that signal a tradition. These are *not* designed for layer stacking — they're standalone grooves.

| File | Description | Notes |
|------|-------------|-------|
| `genre_01_reggae_onedrop` | Kick+rimclick on 2 & 4, upbeat hats, beat 1 empty | The fundamental reggae gesture. |
| `genre_02_reggae_steppers` | Four-on-floor kick, upbeat hats, rimclick 2-4 | More driving reggae. Marley's later work. |
| `genre_03_son_clave_3-2` | 3-2 son clave on rimclick | The fundamental Latin timeline. 2-bar pattern. |
| `genre_04_son_clave_2-3` | 2-3 son clave on rimclick | Reversed phrase orientation. 2-bar pattern. |
| `genre_05_tresillo_kick` | Tresillo as a kick pattern (3+3+2 eighths) | The most versatile Latin/Afro rhythm. Works as a layer under straight hats. |
| `genre_06_bossa_nova` | Kick on 1 and 2+, rimclick on 3 and 4 | Bossa nova gesture. |
| `genre_07_samba_surdo` | High tom on 1/3, floor tom on 2/4 | Surdo-style samba feel. Carnival energy. |

### On the tresillo

`genre_05_tresillo_kick` deserves special attention. It's arguably the single most useful gestural pattern in the set — the 3+3+2 grouping shows up in New Orleans R&B, rock & roll, Latin pop, Afrobeat, and hip-hop. Try it under `hh_01_straight_8ths` with `snare_01_full_2-4` — you get a groove that's neither straight rock nor Latin but has a push to it that's immediately recognizable.

---

## FILLS

Single instances (not looped). Each fill occupies the end of a bar and resolves with a crash + kick on the downbeat of the next bar.

| File | Description | Notes |
|------|-------------|-------|
| `fill_01_16th_descending_toms` | 16th notes, high tom → floor tom, beat 4 | The standard rock fill. 1 beat. |
| `fill_02_triplet_descending_toms` | Triplet figure, same trajectory, beats 3–4 | Blues/rock variant. 2 beats. |
| `fill_03_snare_roll_16ths` | Snare 16ths with slight crescendo, beats 3–4 | Building tension. 2 beats. |
| `fill_04_kick_snare_alternating` | Kick-snare alternating 16ths, beat 4 | Aggressive. Punk/metal. 1 beat. |
| `fill_05_crash_setup` | Snare on 4, crash+kick on 1 | The punctuation mark. Minimal. |
| `fill_06_reggae_hightom_1beat` | Syncopated high toms, beat 4 | Carlton Barrett-style. Flat velocity, tight toms. **Audition carefully — built from feel, not transcription.** |
| `fill_07_reggae_hightom_2beat` | High toms, beats 3–4 | Longer Barrett-style fill. Same caveat. |
| `fill_08_laidback_syncopated` | Snare hits on 3-a, 4-e, 4-a → crash on 1 | Ringo-style lazy syncopation. **Audition carefully — the exact subdivisions may want adjustment.** |
| `fill_09_metric_displacement_2bar` | Dotted-quarter groupings cycling high tom/snare/floor tom over 2 bars | Tony Williams-inspired metric modulation gesture. Groups of 3 over 4/4, resolving on bar 3 beat 1. |

### Reggae tom fills

The key to these is the *voicing*: high, tight-tuned toms with flat, even velocity. In a real Barrett performance, the tuning and damping do as much work as the rhythm. In MIDI, you're dependent on your drum VSTi — map these to the highest available tom voice and tweak the patch if the default sounds too open or ringy.

### Laid-back syncopated fill

What makes this feel "lazy" is that the hits fall on the weakest possible subdivisions (the "a" and "e") rather than on beats or upbeats. Your ear expects the resolution a sixteenth early each time and doesn't get it. If it doesn't feel right when you audition it, try nudging the notes a few ticks late — Ringo's version of this sits slightly behind the grid.

---

## JAZZ PATTERNS

Layer patterns — 2 bars each, loopable.

| File | Description | Notes |
|------|-------------|-------|
| `jazz_01_swing_ride_spangalang` | Classic swing ride with triplet skip, hi-hat pedal 2-4 | The fundamental jazz timekeeping pattern. |
| `jazz_02_straight_ride` | Quarter notes on ride, hi-hat pedal 2-4 | Modal/cool jazz feel. Miles's "So What" territory. |
| `jazz_03_brush_ghost_snare` | Light snare on 2-4 with ghost notes on upbeats | Simulates brush texture. Layer under ride patterns. |

### Jazz pairings

- **Standard swing:** `jazz_01` + `jazz_03` (+ a walking bass line, but that's not our department)
- **Modal/cool:** `jazz_02` + `jazz_03`

---

## TECHNICAL DETAILS

- **Format:** Standard MIDI File Type 0 (single track)
- **Resolution:** 480 ticks per quarter note
- **Channel:** 9 (GM drum channel, 0-indexed; displays as channel 10 in most DAWs)
- **Default tempo:** 120 BPM (embedded in file; your DAW may override this)
- **Time signatures:** 4/4 unless noted (waltz patterns are 3/4)
- **Velocity ranges:** Full hit = 100, Accent = 110, Medium = 85, Light = 65, Ghost = 50, Flat/Barrett = 90

### GM Drum Map Reference

| Note | Instrument |
|------|-----------|
| 36 | Bass Drum |
| 37 | Side Stick / Rimclick |
| 38 | Acoustic Snare |
| 42 | Closed Hi-Hat |
| 44 | Hi-Hat Pedal |
| 46 | Open Hi-Hat |
| 49 | Crash Cymbal |
| 50 | High Tom |
| 47 | Mid Tom |
| 45 | Low Tom |
| 43 | Floor Tom |
| 41 | Low Floor Tom |
| 51 | Ride Cymbal |

---

## REBUILDING

The generator script (`build_drum_toolkit.py`) produces all files from code. To modify patterns, adjust velocities, add new patterns, or change swing ratios, edit the script and re-run:

```bash
python3 build_drum_toolkit.py
```

Requires the `mido` Python library (`pip install mido`).
