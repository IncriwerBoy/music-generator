import glob
from music21 import converter, instrument, note, chord

cnt = 0

for file in glob.glob("music_midi/*.mid"):
    if cnt < 2:
        midi = converter.parse(file)
        print(midi)
        
        notes_to_parse = None
                
        parts = instrument.partitionByInstrument(midi)
        
        #file has instruments part
        if parts:
            notes_to_parse = parts.parts[0].recurse()
        else:
            notes_to_parse = midi.flat.notes
            
        print(notes_to_parse)
        
        cnt += 1
    else:
        break