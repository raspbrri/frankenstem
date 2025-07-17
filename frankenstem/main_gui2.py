import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox


from frankenstem.classes import StemType
from frankenstem.splicer import slice_into_random_beats, slice_by_transients
from frankenstem.config import FrankenstemConfig
from frankenstem.main import generate_frankenstem


class FrankenstemGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FRANKENSTEM GUI")
        self.configure(padx=20, pady=20)


        self.stem_types = [StemType.DRUMS, StemType.BASS, StemType.VOCALS, StemType.OTHER]
        self.slicing_methods = {
            "Random Beats": slice_into_random_beats,
            "Transient Slicing": slice_by_transients
        }


        self.create_widgets()


    def create_widgets(self):
        font_code = ("Courier New", 12)
        font_bold = ("Courier New", 16, "bold")


        tk.Label(self, text="FRANKENSTEM Generator", font=font_bold).pack(pady=(0, 10))


        # BPM and Duration Inputs
        entry_frame = tk.Frame(self)
        entry_frame.pack(pady=5)
        tk.Label(entry_frame, text="BPM:", font=font_code).grid(row=0, column=0, sticky='e')
        self.bpm_entry = tk.Entry(entry_frame, font=font_code)
        self.bpm_entry.insert(0, "160")
        self.bpm_entry.grid(row=0, column=1)


        tk.Label(entry_frame, text="Target Duration (seconds):", font=font_code).grid(row=1, column=0, sticky='e')
        self.duration_entry = tk.Entry(entry_frame, font=font_code)
        self.duration_entry.insert(0, "60")
        self.duration_entry.grid(row=1, column=1)


        # Stem Checkboxes
        tk.Label(self, text="Select Stem Types:", font=font_code).pack(pady=(10, 0))
        self.stem_vars = {}
        for stem in self.stem_types:
            var = tk.BooleanVar()
            tk.Checkbutton(self, text=stem.name.capitalize(), variable=var, font=font_code).pack(anchor='w')
            self.stem_vars[stem] = var


        # Slicing Method Dropdown
        tk.Label(self, text="Slicing Method:", font=font_code).pack(pady=(10, 0))
        self.slicer_combo = ttk.Combobox(self, values=list(self.slicing_methods.keys()), font=font_code)
        self.slicer_combo.set("Random Beats")
        self.slicer_combo.pack()

        # Fragment Length Inputs (only applies to Random Beats)
        tk.Label(self, text="Fragment Length (beats):", font=font_code).pack(pady=(10, 0))
        frag_frame = tk.Frame(self)
        frag_frame.pack()
        tk.Label(frag_frame, text="Min:", font=font_code).grid(row=0, column=0)
        self.min_beats_entry = tk.Entry(frag_frame, width=5, font=font_code)
        self.min_beats_entry.insert(0, "4")
        self.min_beats_entry.grid(row=0, column=1, padx=5)
        tk.Label(frag_frame, text="Max:", font=font_code).grid(row=0, column=2)
        self.max_beats_entry = tk.Entry(frag_frame, width=5, font=font_code)
        self.max_beats_entry.insert(0, "8")
        self.max_beats_entry.grid(row=0, column=3, padx=5)

        # Energy Filter Options
        self.energy_filter_var = tk.BooleanVar()
        tk.Checkbutton(self, text="Filter by Energy", variable=self.energy_filter_var, font=font_code).pack(pady=(10, 0))

        tk.Label(self, text="Energy Target:", font=font_code).pack()
        self.energy_target_combo = ttk.Combobox(self, values=["very_low", "low", "medium", "high"], font=font_code)
        self.energy_target_combo.set("medium")
        self.energy_target_combo.pack()

        self.export_fragments_var = tk.BooleanVar()
        tk.Checkbutton(self, text="Export fragments individually", variable=self.export_fragments_var, font=font_code).pack(pady=(10, 0))


        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Generate Frankenstem", command=self.run_generation, font=font_code).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Exit", command=self.quit, font=font_code).pack(side='left', padx=5)

        # Output Box
        self.output = scrolledtext.ScrolledText(self, width=80, height=20, font=("Courier New", 10))
        self.output.pack(pady=(10, 0))


    def log(self, message):
        self.output.insert(tk.END, message + '\n')
        self.output.see(tk.END)


    def run_generation(self):
        try:
            bpm = int(self.bpm_entry.get())
            duration = float(self.duration_entry.get())


            selected_stems = [stem for stem, var in self.stem_vars.items() if var.get()]
            if not selected_stems:
                self.log("[ERROR] Please select at least one stem type.")
                return


            slicer_func = self.slicing_methods[self.slicer_combo.get()]

            min_beats = int(self.min_beats_entry.get())
            max_beats = int(self.max_beats_entry.get())
            if min_beats >= max_beats:
                self.log("[ERROR] Min beats must be less than max beats.")
                return

            filter_by_energy = self.energy_filter_var.get()
            energy_target = self.energy_target_combo.get()
            export_fragments = self.export_fragments_var.get()


            config = FrankenstemConfig(
                target_duration=duration,
                bpm=bpm,
                selected_stem_types=selected_stems,
                selected_slicing_function=slicer_func,
                min_beats=min_beats,
                max_beats=max_beats,
                export_fragments_individually=export_fragments,
                filter_by_energy=filter_by_energy,
                energy_target=energy_target
            )

            self.log(f"[INFO] Generating Frankenstem with BPM={bpm}, Duration={duration}s, "
                     f"Stems={[s.name for s in selected_stems]}, Slicer={self.slicer_combo.get()}")


            generate_frankenstem(config)


            self.log("[INFO] Frankenstem generation complete.\n")
        except Exception as e:
            self.log(f"[ERROR] {e}")


def main():
    app = FrankenstemGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
