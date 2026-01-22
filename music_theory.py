import sys
import re

class MusicTheoryEngine:
    def __init__(self):
        # Chromatic pools
        self.sharps = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        self.flats  = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
        
        # Mode Logic
        self.modes = {
            "Ionian":     {"intervals": [0, 2, 4, 5, 7, 9, 11], "trigger": r"maj|major|M7|add9|(?<![a-z])\Z"}, 
            "Dorian":     {"intervals": [0, 2, 3, 5, 7, 9, 10], "trigger": r"m6|dor|13"},
            "Phrygian":   {"intervals": [0, 1, 3, 5, 7, 8, 10], "trigger": r"phryg|b9"},
            "Lydian":     {"intervals": [0, 2, 4, 6, 7, 9, 11], "trigger": r"lyd|#11"},
            "Mixolydian": {"intervals": [0, 2, 4, 5, 7, 9, 10], "trigger": r"7|dom|mix|sus"}, 
            "Aeolian":    {"intervals": [0, 2, 3, 5, 7, 8, 10], "trigger": r"m|min|minor"},
            "Locrian":    {"intervals": [0, 1, 3, 5, 6, 8, 10], "trigger": r"dim|b5|loc"},
        }

    def get_notes_list(self, root):
        if 'b' in root and len(root) > 1: return self.flats
        if '#' in root: return self.sharps
        # Flat preference keys
        if root in ['F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'd', 'g', 'c', 'f']: return self.flats
        return self.sharps

    def parse_input(self, user_input):
        user_input = user_input.strip()
        
        # 1. Handle Slash Chords
        if '/' in user_input:
            parts = user_input.split('/')
            chord_part = parts[0]
            bass_note = parts[1].capitalize()
        else:
            chord_part = user_input
            bass_note = None

        # 2. Extract Root
        root_match = re.match(r"^([A-G][#b]?)", chord_part, re.IGNORECASE)
        if not root_match:
            return None, None, None
        
        root = root_match.group(1).capitalize()
        if len(root) > 1 and root[1] == 'b': root = root[0] + 'b'
        
        # 3. Mode Detection
        quality_str = chord_part[len(root):].lower()
        detected_mode = "Ionian" # Default
        
        # Priority Triggers
        if "maj7" in quality_str: detected_mode = "Ionian"
        elif "m7b5" in quality_str: detected_mode = "Locrian"
        elif "m" in quality_str and "6" in quality_str: detected_mode = "Dorian"
        elif "m" in quality_str: detected_mode = "Aeolian"
        elif "7" in quality_str: detected_mode = "Mixolydian" 
        elif "sus" in quality_str: detected_mode = "Mixolydian"
        elif "dim" in quality_str: detected_mode = "Locrian"
        else:
            for mode, data in self.modes.items():
                if re.search(data['trigger'], quality_str):
                    detected_mode = mode
                    break
        
        return root, detected_mode, bass_note

    def get_scale(self, root, mode_name):
        notes_ref = self.get_notes_list(root)
        if root not in notes_ref:
            notes_ref = self.sharps if root in self.sharps else self.flats
            if root not in notes_ref: return None

        start_index = notes_ref.index(root)
        intervals = self.modes[mode_name]["intervals"]
        
        scale = []
        for interval in intervals:
            idx = (start_index + interval) % 12
            scale.append(notes_ref[idx])
        return scale

    def get_chord_notes(self, root, quality, bass=None):
        notes_ref = self.get_notes_list(root)
        if root not in notes_ref: 
            notes_ref = self.sharps if root in self.sharps else self.flats
        
        start = notes_ref.index(root)
        
        # Intervals dictionary
        q_map = {
            "Major": [0, 4, 7], "Minor": [0, 3, 7], "Diminished": [0, 3, 6],
            "Maj7": [0, 4, 7, 11], "m7": [0, 3, 7, 10], "7": [0, 4, 7, 10],
            "m7b5": [0, 3, 6, 10], "sus2": [0, 2, 7], "sus4": [0, 5, 7],
            "7sus4": [0, 5, 7, 10], "add9": [0, 4, 7, 14], "m9": [0, 3, 7, 10, 14],
            "Maj9": [0, 4, 7, 11, 14], "6": [0, 4, 7, 9], "m6": [0, 3, 7, 9]
        }
        
        intervals = q_map.get(quality, [0, 4, 7]) # Default Major
        notes = [notes_ref[(start + i) % 12] for i in intervals]
        
        if bass:
            if bass in notes_ref:
                notes = [bass] + [n for n in notes if n != bass]
                
        return notes

class GenreFlavorProfile:
    def __init__(self):
        # Suggests starter chords for genres
        self.suggestions = {
            "neo-soul": ["Cmaj9", "Ebm9", "Dbmaj7", "Fm11"],
            "lo-fi": ["Fmaj7", "Cm7", "Ebmaj9", "Abmaj7"],
            "jazz": ["Dm7", "G7", "Cmaj7", "Bb13"],
            "blues": ["A7", "E7#9", "B7", "C7"],
            "rock": ["E5", "A5", "D5", "G"],
            "metal": ["E5", "C#m", "Ddim", "F#5"],
            "pop": ["C", "G", "Am", "F"],
            "funk": ["E9", "Am7", "D7", "G13"],
            "ska": ["Bb", "F", "Gm", "Eb"],
            "gospel": ["Dbmaj9", "Fm7", "Eb/G", "Ab"],
            "shoegaze": ["Emaj7", "Bsus4", "Aadd9", "C#m7"]
        }

    def get_suggestions(self, genre_input):
        results = []
        for key, chords in self.suggestions.items():
            if genre_input.lower() in key:
                results.extend(chords)
        return results if results else ["C", "G", "Am", "F"] # Default Pop

class ProgressionGenerator:
    def __init__(self):
        self.library = {
            "Pop / Rock": [
                ("Walkdown (I - V/vii - vi - IV)", [(0,None,None), (4,None,6), (5,None,None), (3,None,None)]),
                ("Emotional (vi - IV - I - Vsus - V)", [(5,None,None), (3,None,None), (0,None,None), (4,"sus4",None), (4,None,None)]),
                ("Slash Climb (I - I/iii - IV)", [(0,None,None), (0,None,2), (3,None,None)])
            ],
            "Jazz / R&B": [
                ("ii - V - I (Extensions)", [(1,"m7",None), (4,"7",None), (0,"Maj7",None)]),
                ("Backdoor (ii - bVII - I)", [(1,"m7",None), (3,"m7",None), (0,"Maj7",None)]), 
                ("Neo-Soul (IV - iii - ii - I)", [(3,"Maj7",None), (2,"m7",None), (1,"m7",None), (0,"Maj7",None)])
            ],
            "Worship / Ballad": [
                ("The One (I - V/vii - vi - IV/I)", [(0,None,None), (4,None,6), (5,None,None), (3,None,0)]),
                ("Sus Swell (IV - I/iii - ii - Vsus)", [(3,None,None), (0,None,2), (1,None,None), (4,"sus4",None)])
            ],
            "Rock / Metal": [
                ("Pedal Point (I - bVII/I - bVI/I)", [(0,None,None), (6,None,0), (5,None,0)]), 
                ("Grunge (I - bIII - IV)", [(0,None,None), (2,"Major",None), (3,None,None)])
            ],
            "Ska / Reggae": [
                ("Ska Punk (I - V - vi - IV)", [(0,None,None), (4,None,None), (5,None,None), (3,None,None)]),
                ("Two Chord Jam (I - ii)", [(0,"Maj7",None), (1,"m7",None)])
            ]
        }

    def get_progressions(self, genre_query):
        results = {}
        for k, v in self.library.items():
            if genre_query.lower() in k.lower() or genre_query == "":
                results[k] = v
        if not results: return {"Standard Pop": self.library["Pop / Rock"]}
        return results

def main():
    engine = MusicTheoryEngine()
    prog_gen = ProgressionGenerator()
    flavor_db = GenreFlavorProfile()
    
    print("--- Music Theory & Recommendation Engine v5.0 ---")

    while True:
        print("\n" + "="*60)
        print("Start by:")
        print("  [1] Inputting a specific CHORD (e.g., Cmaj7, F#m)")
        print("  [2] Inputting a GENRE to get chord suggestions")
        print("  [q] Quit")
        
        choice = input("\nSelect Option: ").strip().lower()
        
        if choice == 'q': break
        
        chord_input = ""
        user_genre_filter = "" # Keep track if user started with genre

        if choice == '2':
            # --- GENRE PATH ---
            print("\nAvailable Flavor Profiles: Neo-Soul, Lo-Fi, Jazz, Blues, Rock, Metal, Funk, Ska, Gospel, Shoegaze...")
            genre_in = input("Enter Genre: ").strip()
            suggestions = flavor_db.get_suggestions(genre_in)
            
            print(f"\nRecommended Starter Chords for '{genre_in}':")
            print(f"-> {', '.join(suggestions)}")
            
            user_genre_filter = genre_in # Remember this for later
            chord_input = input("\nNow, enter one of these chords (or any other): ").strip()
            
        else:
            # --- CHORD PATH ---
            chord_input = input("\nEnter Chord (e.g., F, Cmaj7, G/B): ").strip()

        # --- ANALYSIS ENGINE ---
        if not chord_input or chord_input.lower() == 'q': continue

        # 1. Parse Input
        root, mode, bass_input = engine.parse_input(chord_input)
        
        if not root:
            print(f"(!) Could not recognize a chord root in '{chord_input}'.")
            continue
            
        # 2. Generate Scale
        scale = engine.get_scale(root, mode)
        if not scale:
            print(f"(!) Error generating scale for {root}.")
            continue
            
        print("\n" + "*"*60)
        print(f"ANALYSIS: {root} {mode}")
        if bass_input: print(f"Slash Bass: /{bass_input}")
        print(f"SCALE: {' - '.join(scale)}")
        print("*"*60)

        # 3. Generate Diatonic Reference
        print(f"{'Deg':<5} {'Diatonic Context':<20} {'Notes'}")
        print("-" * 50)
        
        # Diatonic logic defaults
        if mode == "Ionian": qualities = ["Maj7", "m7", "m7", "Maj7", "7", "m7", "m7b5"]
        elif mode == "Aeolian": qualities = ["m7", "m7b5", "Maj7", "m7", "m7", "Maj7", "7"]
        elif mode == "Mixolydian": qualities = ["7", "m7", "m7b5", "Maj7", "m7", "m7", "Maj7"]
        elif mode == "Dorian": qualities = ["m7", "m7", "Maj7", "7", "m7", "m7b5", "Maj7"]
        else: qualities = ["(Gen)", "(Gen)", "(Gen)", "(Gen)", "(Gen)", "(Gen)", "(Gen)"]

        diatonic_map = []
        for i, note in enumerate(scale):
            q = qualities[i] if i < len(qualities) else "Major"
            notes = engine.get_chord_notes(note, q)
            diatonic_map.append({"note": note, "default_q": q})
            print(f"{i+1:<5} {note}{q:<20} {', '.join(notes)}")
            
        # 4. Progressions
        # If user started with genre, use that. Otherwise ask.
        if user_genre_filter:
            print(f"\n[ Auto-Selected Genre: {user_genre_filter} ]")
            progs = prog_gen.get_progressions(user_genre_filter)
        else:
            print("-" * 50)
            g_in = input("Enter Genre for Progressions (Press Enter for All): ").strip()
            progs = prog_gen.get_progressions(g_in)
        
        # 5. Output Progressions
        found_progs = False
        for cat, p_list in progs.items():
            print(f"\n[{cat}]")
            found_progs = True
            for p_name, steps in p_list:
                chain_str = []
                for (deg_idx, quality_ovr, bass_idx) in steps:
                    if deg_idx >= len(scale): continue
                    
                    root_note = scale[deg_idx]
                    q = quality_ovr if quality_ovr else diatonic_map[deg_idx]["default_q"]
                    
                    slash_str = ""
                    b_note = None
                    if bass_idx is not None and bass_idx < len(scale):
                        b_note = scale[bass_idx]
                        slash_str = f"/{b_note}"
                    
                    chain_str.append(f"{root_note}{q}{slash_str}")
                
                print(f"> {p_name}")
                print(f"  {' -> '.join(chain_str)}")
        
        if not found_progs:
            print("No specific progressions found, but you can build your own using the Diatonic Context above!")

if __name__ == "__main__":
    main()