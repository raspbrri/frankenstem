# About
**Frankenstem** is an experimental audio tool for randomly fragmenting and recombining stems into new 'frankensteined' audio files, used for sampling in music production. 
It’s designed for musicians, producers, and artists interested in playful recombination, post-authorship, and generative sound processes.

#Features 
- *Stem support*: works with vocals, drums, bass, and other instrument stems (as per Ultimate Vocal Remover (HCUS model) and Logic Pro X stem-splitter).
- *Random beat-length splicing* (configurable min/max beats)
- *Transient-based slicing* (onset detection)
- *Silence removal*: removes silent sections before slicing for cleaner results.
- *Energy-based filtering*: select segments based on very low, low, medium, or high RMS energy.
- *GUI*: simple Tkinter-based interface for non-technical use.
- *CLI / Scriptable*: fully configurable via Python for batch or experimental workflows.

# Installation
Clone the repository and install dependencies.

```
git clone https://github.com/yourusername/frankenstem.git
cd frankenstem
pip install -r requirements.txt
```

# Preparing input
Frankenstem expects stems in .wav format, named like:

```
Song_Name (Vocals).wav
Song_Name (Drums).wav
Song_Name (Bass).wav
Song_Name (Other).wav
```

It is advisable to export all stems you would like to recombine within one folder. This folder can be selected as the input folder. 


# TBA
Fixes:
- transient slicing accuracy

Additional features/updates:
- updated UI
- subselection from input folder
- naming convention (user generated)
- half-beats/slider for fragment length range (and one-length, no range)
- packaging as standalone app for Windows/Mac OS
