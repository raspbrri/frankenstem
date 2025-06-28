from frankenstem.classes import StemType
from frankenstem.splicer import slice_into_random_beats, slice_by_transients

stem_type_key = {
    "V": StemType.VOCALS,
    "B": StemType.BASS,
    "D": StemType.DRUMS,
    "O": StemType.OTHER
}

slice_type_key = {
    "R": slice_into_random_beats,
    "T": slice_by_transients
}

def get_user_inputs():
    print(f"\n ---- WELCOME TO FRANKENSTEM! ----\n")

    # --- USER INPUT FOR TARGET DURATION ---
    while True:
        user_input = input("Enter target FRANKENSTEM duration in seconds (10-60 seconds, default 20): ") or "20"
        try:
            target_duration = float(user_input)
            if 10 <= target_duration <= 60:
                break
            else:
                print("Please enter a duration between 10 and 60 seconds.")
        except ValueError:
            print("Invalid input. Please enter a valid number in seconds.")

    # --- USER INPUT FOR SOURCE BPM ---
    while True:
        user_input = input("Enter source BPM: ")
        try:
            bpm = float(user_input)
            if 20 <= bpm <= 300:
                break
            else:
                print("Please enter a BPM between 20 and 300.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    print(f"---- Target duration: {target_duration} seconds, BPM: {bpm} ----\n")

    # --- USER INPUT FOR STEM TYPES ---
    frankenstem_type_selection = input(
        "List stem types to combine separated by commas:\n"
        "VOCALS = V\nBASS = B\nDRUMS = D\nOTHER = O\n(e.g. 'V,B,O'): "
    )
    selected_keys = [s.strip().upper() for s in frankenstem_type_selection.split(",")]

    try:
        selected_stem_types = [stem_type_key[k] for k in selected_keys]
    except KeyError as e:
        raise ValueError(f"Invalid stem type selected: {e}")

    print(f"---- Selected stem types: {[t.name for t in selected_stem_types]} ----\n")

    # --- USER INPUT FOR SLICE TYPE ---
    while True:
        user_input = input("Select slice type:\nRANDOM BEATS = R\nTRANSIENTS = T\n(e.g. 'R'): ").strip().upper()
        if user_input in slice_type_key:
            selected_slicing_function = slice_type_key[user_input]
            break
        else:
            print("Please select a valid slice type (R or T).")

    print(f"---- SLICE TYPE: {selected_slicing_function.__name__} ----\n")

    return target_duration, bpm, selected_stem_types, selected_slicing_function
