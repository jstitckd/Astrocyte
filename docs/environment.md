# Homepage environmental overview

The environmental overview is no longer rendered on the homepage. The component and data service are retained for reuse. Open **View options** to choose a recorded Sol/LMST observation, change °C/°F and Pa/mbar, or disable synthetic cabin readings. Expand **Recorded trends & data notes** for Plotly profiles, provenance and monitoring gaps.

## What comes from testing.py

`testing.py` remains unchanged and is not imported: importing it would execute its page configuration and app-wide CSS. The integration adapts its CSV alias/LMST parsing, compact tile/Plotly presentation and deterministic `station_values()` cabin formulas into separate modules.

The temperature dial uses the prototype's 270-degree range display, rendered with CSS so its number remains readable in Streamlit HTML. The arc represents the selected air temperature within the recorded Sol's minimum/maximum; it is not a health or equipment-readiness score.

The prototype's outdoor verdicts, medical-effect claims, safe-range bands and extrapolated forecast are not part of this overview. Graphs show recorded rows and preserve gaps.

| File | Responsibility |
| --- | --- |
| `services/environment.py` | Pure CSV parsing, validation, snapshot selection, provenance, cabin demo formulas and unit conversions. |
| `components/environment.py` | Four cards, display options, data-source labels and expandable notes. |
| `components/environment_charts.py` | Plotly recorded profiles and the selected-time marker. |
| `frontend/environment.css` | Scoped visual styling; leaves the sidebar, map and crew pages intact. |
| `tests/test_environment.py` | Data/provenance validation, missing observations, unit conversion and homepage integration. |

## Current source and limitations

The default file is `mars_sol_1740_combined_20min_sensor_averages(2).csv` beside `app.py`. It supplies 72 observation windows for Sol 1740. Air temperature and pressure have 68 valid readings, with four missing windows. The default selection is 12:00–12:20 LMST.

LMST is the file's local mean solar time, not UTC or the viewer's local clock. No Earth date or current/live time is invented. The source file's origin has not been independently verified; the UI calls it a local recorded CSV snapshot.

- **Temperature:** outside air and ground come from CSV; cabin temperature is an optional synthetic scenario.
- **Radiation:** the bundled CSV contains no ionising dose-rate or accumulated-dose channel. The cabin dose-rate value is explicitly marked DEMO. Outside and accumulated exposure remain unmeasured.
- **Atmosphere:** outside pressure is from CSV. Cabin pressure, oxygen and carbon dioxide are explicitly marked DEMO unless corresponding recorded channels are added. Cabin particulate monitoring is absent; no overall air-quality score is calculated.
- **Regolith/dust:** no dust mass concentration or regolith assay is in the bundled CSV. Values remain blank and toxicity is not assessed.

The five synthetic cabin values are copied from `testing.py`'s formulas and vary by Sol, not observation time. They are visual demo values, not sensors, clinical references or operating thresholds. Turning the demo off shows only supplied CSV values. A missing value in an existing cabin channel is never replaced by a demo.

The CSV's longwave/shortwave irradiance and spectral RDS channels are not treated as ionising dose. A dose rate is also not automatically converted into accumulated exposure without duration and appropriate dosimetry data. [NASA's RAD overview](https://science.nasa.gov/resource/radiation-measurements-on-mars/) provides background on radiation measurement on Mars.

Dust concentration and composition are separate measurements, and weather alone does not establish toxicity. For background, [NASA's regolith research](https://www.nasa.gov/missions/mars-2020-perseverance/perseverance-rover/nasas-perseverance-rover-gets-the-dirt-on-mars/) discusses fine grains and chemical constituents. These resources are not sources for the synthetic numbers and are not used to calculate any threshold in this app.

## Optional recorded channels

The parser already accepts the columns below if your team adds measurements to the local environmental CSV. The table uses the canonical names; aliases are in `ALIASES` in `services/environment.py`. Units are fixed by column name, so convert source units before adding rows.

| Column | Unit / scope |
| --- | --- |
| `Sol` | Non-negative whole Martian day number |
| `LMST_Start` | Start time before 24:00; `HH:MM` or `HH:MM:SS` |
| `LMST_End` | Optional interval-end label; 24:00 is allowed here |
| `Air_Temp_ATS_C` | Outside air, °C |
| `Ground_Temp_C` | Ground, °C |
| `Pressure_Pa` | Outside pressure, Pa |
| `Relative_Humidity_pct` | Outside relative humidity, % |
| `Cabin_Temperature_C` | Cabin, °C |
| `Cabin_Pressure_kPa` | Cabin, kPa |
| `Cabin_O2_pct` | Cabin oxygen, % |
| `Cabin_CO2_ppm` | Cabin carbon dioxide, ppm |
| `Cabin_Radiation_uSv_h` | Cabin dose rate, µSv/h |
| `Surface_Radiation_uSv_h` | Outside dose rate, µSv/h |
| `Recorded_Dose_mSv` | Recorded accumulated dose, mSv; not inferred from a snapshot |
| `Cabin_PM25_ug_m3` | Cabin particulate concentration, µg/m³; not an AQI |
| `Surface_Dust_mg_m3` | Airborne dust concentration, mg/m³ |
| `Regolith_Perchlorate_wt_pct` | Sample assay, weight percent |

Use one station and one row per Sol/start time. The parser rejects duplicate observations, ambiguous headers, invalid Sol/time identifiers, empty files and files over 5 MiB or 50,000 rows. Nonnumeric values, infinities, sentinel values and physically invalid channel values are shown as missing. These are data-integrity checks, not health thresholds. Unknown columns are left unused.

The service returns a `Snapshot` with `Reading(value, unit, source, note)` objects. `source` is `csv`, `demo` or `missing`. Recorded channels take precedence over demo formulas. A file error shows a message while keeping habitat-map navigation available.

No upload screen, API, database or persistent record storage is added by this change. The existing Data & exports page remains a separate team workspace. Display preferences use Streamlit session state; loading the overview does not modify the source CSV.
