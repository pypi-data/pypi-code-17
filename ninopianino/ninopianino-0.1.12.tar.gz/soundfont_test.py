import sys, json
from ninopianino import generator, template_utils

def seconds_to_min(seconds):
    return str(seconds/60) + ':' + str(seconds%60)

def instrument_play_time(block):
    return [seconds_to_min((block['program_number']-1)*4), seconds_to_min(block['program_number']*4)]

def generate_blocks():
    blocks = []
    for i in range(1, 90):
        new_block = {
            'program_number' : i, 
            'play_at' : [(i-1) * 8], 
            'number_of_bars' : 2, 
            'number_of_beats_per_bar' : 4,
            'default_accent' : 80,
        }
        blocks.append(new_block)
        play_time = instrument_play_time(new_block)
        print 'Program number ', i, 'between ', play_time[0], 'and', play_time[1] 
    return blocks

def main():
    base_block = template_utils.create_base_block()
    base_block['channel'] = 1
    base_block['root_note'] = 'C'
    base_block['scale'] = 'major'
    base_block['blocks'] = generate_blocks()
    base_block['low_end'] = 'C2'
    base_block['high_end'] = 'C3'
    mid = generator.generate(base_block)
    try: 
        soundfont = sys.argv[1]
    except: 
        import traceback
        traceback.print_exc()
        soundfont = 'soundfonts/FluidR3_GM.sf2' 
    print 'Testing ', soundfont

    song_path = generator.write_mid(mid, 'soundfont_test' )

    generator.to_wav(song_path, soundfont)

    instruments_json = [
        {
            'id' : 'nesho', 
            'friendly' : 'Nesho', 
            'base_volume' : 80, 
            'program_number' : i['program_number'], 
            'instrument_play_time' : instrument_play_time(i)[0] + ' - ' + instrument_play_time(i)[1]
        } for i in base_block['blocks']
    ]

    with open('instruments.json', 'w') as f: 
        f.write(json.dumps(instruments_json, indent = 4))




main()
