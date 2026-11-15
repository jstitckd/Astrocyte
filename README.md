# Astrocyte

An open-source Streamlit prototype for exploring astronaut health, habitat tasks and Mars environmental conditions.

Built for the **2026 NASA Space Apps Challenge — Create Health Monitoring Software for Astronauts on Space Missions**.

Astrocyte brings together a mission dashboard, four crew profiles, an interactive habitat map and medical task guides to help users explore how health monitoring could work during a long-duration space mission.

**This prototype uses demo data. It is not a medical device, a validated clinical assessment or a live mission-monitoring system.**

## Features

- Mission dashboard with compact crew health summaries and environmental gauges.
- Profiles for Alex, Petrov, Amara and Milou, including telemetry, recovery and test charts.
- Demonstration cycle-tracking views for Amara and Milou.
- Profile insights and a demonstration test-entry form.
- An AI-generated SVG habitat map with building highlights and task notifications that open relevant guides.
- Urgency-coloured tasks with completion state maintained within each browser session.
- A dark interface using IBM Plex Sans.

## Run locally

Use **Python 3.12**.

### macOS / Linux

```bash
git clone https://github.com/jstitckd/Astrocyte.git
cd Astrocyte
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

### Windows PowerShell

```powershell
git clone https://github.com/jstitckd/Astrocyte.git
cd Astrocyte
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL printed in the terminal. To stop the app, press **Ctrl+C**.

## Using the app

1. Open **Base overview** to view crew summaries, environmental conditions and the habitat map.
2. Select an astronaut in the sidebar to explore their profile.
3. Hover over or focus on habitat buildings to highlight them.
4. Select a task notification to open its guide.
5. Explore the demonstration test-entry and task-completion features.

## Data sources and References

Astrocyte combines Mars environmental data with synthetic astronaut health data. It does not receive live telemetry from astronauts or a Mars habitat.

### Environmental data

Environmental values were obtained for **14 November 2026** at **Syrtis Major, Mars (9.9°N, 70°E; elevation 1,624 m)**.

- **Temperature and UV index:** obtained from NASA Goddard’s [Mars Explorer](https://psg.gsfc.nasa.gov/apps/mars/), which provides model-based Mars environmental information.
- **Atmospheric pressure:** obtained from the [Mars Climate Database](https://www-mars.lmd.jussieu.fr/mcd_python/), configured for the same date and location.
- **Cabin oxygen and carbon dioxide:** synthetic demonstration values.

The dashboard displays the **12:00 entry** from the supplied diurnal CSV rather than a live feed. Temperature and pressure represent outdoor conditions, not conditions inside the habitat.

**UV index is not a measure of ionising-radiation dose.** It does not represent exposure to galactic cosmic rays or solar energetic particles.

### Synthetic astronaut health data

All astronaut health data were generated artificially using **ChatGPT** based off of publically available research (see references). For each metric, the team supplied a relevant publication or NASA resource to inform the generated values and trends.

These references provided scientific context; the displayed values are **not measurements extracted from those studies or records of real astronauts**. Providing research sources to an AI model does not validate its generated data.

Health scores, recovery indicators and insights are demonstration outputs, not validated clinical assessments. The cited studies do not establish or validate Astrocyte’s scoring algorithms.

### Health-data references

| Metric or feature | Reference |
|---|---|
| Heart rate | Fritsch-Yelle et al. (1996). Shuttle astronaut 24-hour heart rate and blood pressure study. *Journal of Applied Physiology*, 80, 910–914. |
| Oxygen saturation | Conkin et al. (2017). Hemoglobin Oxygen Saturation with Mild Hypoxia and Microgravity. *Aerospace Medicine and Human Performance*, 88(6), 527–534. |
| Cardiovascular load | Downs et al. Contributions of Astronauts Aerobic Exercise Intensity and Time on Change in VO₂peak during Spaceflight. [NASA NTRS 20140003747](https://ntrs.nasa.gov/citations/20140003747). |
| Overnight heart-rate variability | Otsuka et al. (2021). Astronauts well-being and possibly anti-aging improved during long-duration spaceflight. *Scientific Reports*. |
| Sleep score | Barger et al. (2014). Sleep deficiency and hypnotic use in astronauts before, during and after spaceflight. *The Lancet Neurology*. |
| VO₂ max estimate | Moore et al. (2014). Peak Oxygen Uptake during and after Long-duration Space Flight. *Journal of Applied Physiology*, 117(3), 231–238. |
| Dominant handgrip | Puglia et al. (2018). Long-Term Microgravity Effects on Isometric Handgrip and Precision Pinch Force. *International Journal of Aerospace Engineering*. [doi:10.1155/2018/1952630](https://doi.org/10.1155/2018/1952630). |
| Reaction time | Dinges. Psychomotor Vigilance Self Test on ISS: Reaction Self Test on Expeditions 21 and 22. [NASA NTRS 20090029851](https://ntrs.nasa.gov/citations/20090029851). |
| Hip bone density | Lang et al. (2006). Adaptation of the Proximal Femur to Skeletal Reloading After Long-Duration Spaceflight. *Journal of Bone and Mineral Research*. [doi:10.1359/jbmr.060509](https://doi.org/10.1359/jbmr.060509). |
| Isometric mid-thigh pull | Strock et al. SpacePhys study poster, NASA Human Research Program. [NASA NTRS 20240000934](https://ntrs.nasa.gov/citations/20240000934). |
| Seated leg press, row cable and chest cable | Lamoreaux and Landeck (2006). Mechanism Development, Testing, and Lessons Learned for the Advanced Resistive Exercise Device. [NASA NTRS 20060028227](https://ntrs.nasa.gov/citations/20060028227). |
| Menstrual cycle | Jain and Wotring (2016). Medically induced amenorrhea in female astronauts. *npj Microgravity*, 2, 16008. |

These sources cover different mission conditions, study populations and research purposes. They should not be interpreted as a single validated dataset or as direct predictions of health during a Mars mission.

## AI assistance

- **Synthetic health data:** ChatGPT generated demonstration values using the publications and NASA resources listed above as context since personal health data is private.
- **Habitat map:** the SVG habitat illustration was AI assisted using ChatGPT
- **Design and documentation:** ChatGPT assisted with dashboard design concepts and README drafting.

AI-generated content is included as prototype material and should not be treated as independently verified scientific evidence.

## Third-party credits

Astrocyte uses third-party software and assets, which remain subject to their respective licences.

- **Streamlit:** application framework — https://streamlit.io/
- **IBM Plex Sans:** interface typeface — https://github.com/IBM/plex
- **Python dependencies:** listed in [requirements.txt](requirements.txt).