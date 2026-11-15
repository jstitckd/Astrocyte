# Editing the dashboard

| Change | File |
| --- | --- |
| Homepage layout | `views/home.py` |
| Crew cards and environmental readings | `components/dashboard.py` |
| Homepage dimensions and styling | `frontend/dashboard.css` |
| Website-wide font, background and card surface | `frontend/styles.css` |
| Crew names, roles and displayed dashboard scores | `models/astronauts.py` |
| Assignments, due labels and urgency | `SAMPLE_TASKS` in `services/dashboard.py` |
| Task instructions | `models/task_guides.py` |
| Task guide layout | `views/task_guide.py` |
| Environmental CSV selection | `services/dashboard_weather.py` |
| Gauge ranges and colours | `GAUGE_SCALES` in `services/environment_colours.py` |
| Gauge markup | `components/environment_gauge.py` |
| Map artwork, cards and connectors | `frontend/map/` |

## Appearance

The shared font is IBM Plex Sans, the page background is `#0b0f12`, and card surfaces blend `#141b1f` to `#11171b`. Profile pages and popups use the same theme. The map is an iframe and loads its font independently. Branding is described in [branding.md](branding.md).

Crew cards open their health profiles. Check marks complete individual tasks without opening the profile. Crew cards have equal heights; the completed message occupies the same-sized row as a task.

## Tasks

Set `urgent: True` to make an assignment urgent. Map cards use a slim yellow left edge and due badge, or red for urgency. Crew task cards share one neutral background; their due text and task-count badge show urgency. The badge is green when clear, yellow with ordinary tasks, or red when any urgent task remains. Task guide completion uses the same session state as the dashboard.

## Gauges

The environmental panel has no icons or history charts. Each gauge shows its actual value and a marker over a smooth green–yellow–red gradient. UV and CO₂ are green at low values and become yellow/red as values rise. Outside temperature, outside pressure and O₂ have green middle bands and red extremes. Missing values have no marker; values beyond the plotted range retain their actual numeric value while the pointer stops at the endpoint.

These are configurable display ranges, not certified alarm thresholds or a breathability indicator. UV category boundaries reference the [EPA guide](https://www.epa.gov/sites/default/files/documents/uviguide.pdf); the oxygen concentration band references [OSHA definitions](https://webapps.dol.gov/elaws/osha/confined/definitions.asp). The CO₂ display bands do not calculate exposure duration or apply a time-weighted limit to a single reading.
