import PySimpleGUI as sg
from frankenstem.classes import StemType
from frankenstem.splicer import slice_into_random_beats, slice_by_transients
from frankenstem.config import FrankenstemConfig
from main import generate_frankenstem

def main():
    sg.theme('DarkTeal2')

    code_font = ('Courier New', 12)
    code_font_bold = ('Courier New', 16, 'bold')

    stem_types = [StemType.DRUMS, StemType.BASS, StemType.VOCALS, StemType.OTHER]
    slicing_methods = {
        "Random Beats": slice_into_random_beats,
        "Transient Slicing": slice_by_transients
    }

    layout = [
        [sg.Text('FRANKENSTEM Generator', font=code_font_bold, justification='center')],
        [sg.Text('BPM:', font=code_font), sg.InputText('130', key='BPM', font=code_font)],
        [sg.Text('Target Duration (seconds):', font=code_font), sg.InputText('10', key='DURATION', font=code_font)],
        [sg.Text('Select Stem Types:', font=code_font)],
        [sg.Checkbox(stem_type.name.capitalize(), key=stem_type.name, font=code_font) for stem_type in stem_types],
        [sg.Text('Slicing Method:', font=code_font)],
        [sg.Combo(list(slicing_methods.keys()), default_value="Transient Slicing", key='SLICER', font=code_font)],
        [sg.Button('Generate Frankenstem', font=code_font), sg.Button('Exit', font=code_font)],
        [sg.Output(size=(80, 20), font=('Courier New', 10))]
    ]

    window = sg.Window('FRANKENSTEM GUI', layout, finalize=True, font=code_font)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        if event == 'Generate Frankenstem':
            try:
                bpm = int(values['BPM'])
                duration = float(values['DURATION'])

                selected_stems = [stem_type for stem_type in stem_types if values[stem_type.name]]
                if not selected_stems:
                    print("[ERROR] Please select at least one stem type.")
                    continue

                slicer_func = slicing_methods[values['SLICER']]

                config = FrankenstemConfig(
                    target_duration=duration,
                    bpm=bpm,
                    selected_stem_types=selected_stems,
                    selected_slicing_function=slicer_func
                )

                print(f"[INFO] Generating Frankenstem with BPM={bpm}, Duration={duration}s, "
                      f"Stems={[s.name for s in selected_stems]}, Slicer={values['SLICER']}")

                generate_frankenstem(config)

                print("[INFO] Frankenstem generation complete.\n")
            except Exception as e:
                print(f"[ERROR] {e}")

    window.close()

if __name__ == "__main__":
    main()
