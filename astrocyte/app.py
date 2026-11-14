"""Astrocyte: a runnable Mars habitat health-dashboard prototype."""
from pathlib import Path
from datetime import datetime, timezone
import io
import json
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit.components.v1 import declare_component
from data_model import METRICS, sample_data, validate_frame

ROOT = Path(__file__).parent
st.set_page_config(page_title='Astrocyte · Crew health', page_icon='🪐', layout='wide')
base_map = declare_component('mars_base', path=str(ROOT / 'frontend'))
AREAS = {
    'sleep': ('Sleeping quarters', 'Recovery starts here.', ['heart_rate', 'hrv', 'sleep_hours']),
    'medical': ('Medical bay', 'Your daily health overview.', ['spo2', 'temperature', 'heart_rate']),
    'exercise': ('Exercise area', 'Keep moving, wherever you are.', ['activity_minutes', 'heart_rate']),
    'nutrition': ('Kitchen', 'Fuel your next mission.', ['water_ml', 'calories']),
    'wellbeing': ('Greenhouse', 'Take a moment for yourself.', ['mood', 'stress']),
    'eva': ('Airlock', 'Prepare for the world outside.', ['eva_minutes', 'radiation_msv']),
}
TASKS = {
    'sleep': ['Review overnight heart rate and HRV', 'Review sleep duration'],
    'medical': ['Review recorded vital signs', 'Complete symptom check-in'],
    'exercise': ['Review activity minutes', 'Record exercise notes'],
    'nutrition': ['Review fluid intake', 'Review energy intake'],
    'wellbeing': ['Complete mood and stress check-in'],
    'eva': ['Review mission-approved EVA procedure', 'Confirm equipment check with your team', 'Review exposure records'],
}
st.markdown('''<style>
.block-container{max-width:1450px;padding-top:2rem}h1{font-weight:500!important;letter-spacing:-1.5px}h3{font-weight:500!important}div[data-testid="stMetric"]{background:#1b232c;border:1px solid #354049;border-radius:12px;padding:17px}div[data-testid="stMetricLabel"]{color:#9daeb6}section[data-testid="stSidebar"]{border-right:1px solid #303b44}.eyebrow{color:#d7a17c;font-size:11px;letter-spacing:3px;margin:10px 0}.subtitle{color:#a9b6be;font-size:16px;margin-bottom:25px}.brand{font-size:25px;letter-spacing:3px;color:#f0eee7;margin-bottom:3px}.muted{color:#8fa0ad;font-size:12px}
</style>''', unsafe_allow_html=True)
for key, value in {'page':'base','records':[],'done':{},'last_map_event':None}.items():
    if key not in st.session_state:
        st.session_state[key] = value

def go(page):
    st.session_state.page = page

with st.sidebar:
    st.markdown('<div class="brand">✳ ASTROCYTE</div><div class="muted">CREW HEALTH / MARS HABITAT</div>', unsafe_allow_html=True)
    st.divider()
    source = st.radio('Data source', ['Demo mission', 'Upload CSV'])
    uploaded = None
    if source == 'Upload CSV':
        uploaded = st.file_uploader('Health readings', type=['csv'], help='Use the template in Data & exports. Maximum 5 MB.')
    if source == 'Demo mission':
        df = sample_data()
    elif uploaded is None:
        df = pd.DataFrame(columns=['timestamp', 'crew', 'metric', 'value', 'unit'])
        st.info('Upload a CSV or select Demo mission.')
    else:
        try:
            if uploaded.size > 5_000_000:
                raise ValueError('Please upload a CSV smaller than 5 MB.')
            df = validate_frame(pd.read_csv(uploaded))
            st.success(f'{len(df):,} readings imported')
        except (ValueError, UnicodeDecodeError, pd.errors.ParserError) as exc:
            st.error(str(exc))
            df = pd.DataFrame(columns=['timestamp', 'crew', 'metric', 'value', 'unit'])
    crew = st.selectbox('Crew member', sorted(df.crew.unique()) if not df.empty else ['No crew loaded'])
    st.divider()
    st.button('⌂  Base overview', on_click=go, args=('base',), width='stretch')
    for key, (label, _, _) in AREAS.items():
        st.button(label, key='nav_'+key, on_click=go, args=(key,), width='stretch')
    st.button('Data & exports', on_click=go, args=('data',), width='stretch')
    st.divider()
    st.caption('Prototype · Not a medical device. Demo readings are synthetic. Check-ins and task progress last only for this browser session; export them before closing.')

part = df[df.crew.eq(crew)].copy()
page = st.session_state.page
st.markdown('<div class="eyebrow">ARES OUTPOST / HEALTH OPERATIONS</div>', unsafe_allow_html=True)
if page == 'base':
    st.title('A little closer to home.')
    st.markdown('<div class="subtitle">Explore your habitat. Check in with yourself. Make every sol count.</div>', unsafe_allow_html=True)
else:
    st.title(AREAS[page][0] if page in AREAS else 'Data & exports')
    st.caption(AREAS[page][1] if page in AREAS else 'Bring your own readings and take your session records with you.')

if source == 'Demo mission':
    st.caption('SIMULATED MISSION · 1–14 NOV 2026 · Not live sensor data')
else:
    st.caption('UPLOADED DATA · Readings are not automatically refreshed')

filtered = part
if not part.empty:
    date_range = st.date_input('Reading window (UTC)', (part.timestamp.min().date(), part.timestamp.max().date()), min_value=part.timestamp.min().date(), max_value=part.timestamp.max().date(), key=f'dates_{source}_{crew}')
    if len(date_range) == 2:
        start, end = date_range
        filtered = part[part.timestamp.dt.date.between(start, end)]
    else:
        filtered = part.iloc[:0]
        st.info('Select an end date to display readings.')
    st.caption(f'Crew: {crew} · {len(filtered):,} readings in selected window')
else:
    st.info('No health readings loaded. You can still explore the base.')

def metric_cards(metrics):
    for col, metric in zip(st.columns(len(metrics)), metrics):
        title, unit = METRICS[metric]
        values = filtered[filtered.metric.eq(metric)]
        with col:
            st.metric(title, f'{values.iloc[-1].value:g} {unit}' if not values.empty else '—')
            if not values.empty:
                st.caption('Latest: ' + values.iloc[-1].timestamp.strftime('%d %b %Y, %H:%M UTC'))
            else:
                st.caption('No readings in this window')

def task_key(area, task):
    return json.dumps([source, crew, datetime.now(timezone.utc).date().isoformat(), area, task])

def task_list(area):
    st.subheader('Today’s tasks')
    st.caption('Your completion checklist, not an automated assessment.')
    for task in TASKS[area]:
        key = task_key(area, task)
        done = st.checkbox(task, value=st.session_state.done.get(key, False), key='task_'+key)
        st.session_state.done[key] = done

if page == 'base':
    metric_cards(['heart_rate', 'sleep_hours', 'activity_minutes', 'water_ml'])
    st.write('')
    event = base_map(key='base_map', default=None)
    if event and event.get('event') != st.session_state.last_map_event and event.get('zone') in AREAS:
        st.session_state.last_map_event = event['event']
        st.session_state.page = event['zone']
        st.rerun()
    left, right = st.columns([2, 1])
    with left:
        st.subheader('Your mission today')
        total = sum(len(tasks) for tasks in TASKS.values())
        complete = sum(st.session_state.done.get(task_key(area, task), False) for area, tasks in TASKS.items() for task in tasks)
        st.progress(complete / total, text=f'{complete} of {total} tasks completed for {crew}')
        st.caption('Select a building to view its tasks. The sidebar offers the same navigation.')
    with right:
        st.subheader('Data status')
        if not part.empty:
            st.write('Last record: ' + part.timestamp.max().strftime('%d %b %Y, %H:%M UTC'))
        st.caption('Missing readings appear as dashes. This prototype does not infer health status from missing data.')
elif page in AREAS:
    metrics = AREAS[page][2]
    metric_cards(metrics)
    chart_col, task_col = st.columns([2, 1])
    with chart_col:
        st.subheader('Reading history')
        selected = st.selectbox('Metric', metrics, format_func=lambda m: METRICS[m][0])
        values = filtered[filtered.metric.eq(selected)]
        if values.empty:
            st.info('No readings available for this metric and date range.')
        else:
            fig = px.line(values, x='timestamp', y='value', markers=True, labels={'timestamp':'Time (UTC)', 'value':METRICS[selected][1]})
            fig.update_traces(line_color='#edb18a', marker_size=7)
            fig.update_layout(height=330, margin=dict(l=10,r=10,t=15,b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='#bac5ca')
            st.plotly_chart(fig, width='stretch')
    with task_col:
        task_list(page)
    st.subheader('Crew check-in')
    st.caption('Self-reported entries are stored separately from imported sensor readings.')
    with st.form('checkin_'+page, clear_on_submit=True):
        if page == 'wellbeing':
            a,b = st.columns(2)
            mood = a.slider('Mood (1 = low, 5 = high)',1,5,3)
            stress = b.slider('Stress (1 = low, 5 = high)',1,5,3)
        notes = st.text_area('Notes / observations', max_chars=2000, placeholder='How are you feeling? Anything to discuss with the crew?')
        submit = st.form_submit_button('Save check-in', disabled=part.empty)
        if submit:
            if page != 'wellbeing' and not notes.strip():
                st.warning('Add a note before saving.')
            else:
                record = {'timestamp':datetime.now(timezone.utc).isoformat(), 'source':source, 'crew':crew, 'area':page, 'notes':notes.strip()}
                if page == 'wellbeing':
                    record.update(mood=mood, stress=stress)
                st.session_state.records.append(record)
                st.success('Check-in saved for this session. Export it from Data & exports.')
    records = [r for r in st.session_state.records if r['crew']==crew and r['area']==page and r['source']==source]
    if records:
        st.dataframe(pd.DataFrame(records), width='stretch', hide_index=True)
else:
    st.subheader('CSV data contract')
    st.write('One row per measurement. Timestamps use ISO 8601; timestamps without an offset are treated as UTC. Daily intake, activity and exposure metrics represent a daily total per timestamp, not incremental events.')
    st.code('timestamp,crew,metric,value,unit\n2026-11-14T08:00:00Z,Alex Morgan,heart_rate,64,bpm', language='text')
    st.dataframe(pd.DataFrame([{'metric':m,'label':label,'unit':unit} for m,(label,unit) in METRICS.items()]), hide_index=True, width='stretch')
    st.download_button('Download sample CSV', sample_data().to_csv(index=False), 'sample_health_data.csv', 'text/csv')
    st.subheader('Export your data')
    # JSON is used for check-ins to preserve arbitrary notes without spreadsheet formulas.
    st.download_button('Export session check-ins and tasks (JSON)', json.dumps({'checkins':st.session_state.records,'tasks':st.session_state.done}, indent=2), 'astrocyte_session.json','application/json')
    if not df.empty:
        st.download_button('Export loaded readings (JSON)', df.to_json(orient='records', date_format='iso'), 'astrocyte_readings.json','application/json')
        st.dataframe(df, hide_index=True, width='stretch')
    st.info('External API integration is not connected yet. Add an adapter that returns the same five columns and pass its output through validate_frame() in data_model.py. Keep credentials in Streamlit secrets.')
    with st.expander('Clear session check-ins and task progress'):
        confirm = st.checkbox('I have exported anything I need')
        if st.button('Clear session records', disabled=not confirm):
            st.session_state.records = []
            st.session_state.done = {}
            for key in list(st.session_state):
                if key.startswith('task_'):
                    del st.session_state[key]
            st.rerun()
