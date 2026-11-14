"""Shared data contract. An eventual API adapter should return validate_frame(df)."""
import numpy as np
import pandas as pd

METRICS = {
    'heart_rate': ('Heart rate', 'bpm'),
    'hrv': ('HRV', 'ms'),
    'sleep_hours': ('Sleep duration', 'h'),
    'activity_minutes': ('Activity', 'min'),
    'spo2': ('Oxygen saturation', '%'),
    'temperature': ('Temperature', '°C'),
    'water_ml': ('Daily fluid intake', 'mL'),
    'calories': ('Daily energy intake', 'kcal'),
    'eva_minutes': ('Daily EVA duration', 'min'),
    'radiation_msv': ('Daily recorded dose', 'mSv'),
    'mood': ('Mood', '/5'),
    'stress': ('Stress', '/5'),
}
COLUMNS = ['timestamp', 'crew', 'metric', 'value', 'unit']

def validate_frame(df):
    missing = set(COLUMNS) - set(df.columns)
    if missing:
        raise ValueError('Missing columns: ' + ', '.join(sorted(missing)))
    if df.empty:
        raise ValueError('The file contains no readings.')
    if len(df) > 100000:
        raise ValueError('Use at most 100,000 readings per upload.')
    df = df[COLUMNS].copy()
    if df.isna().any().any():
        raise ValueError('Every row needs all five fields.')
    for col in ['crew', 'metric', 'unit']:
        df[col] = df[col].astype(str).str.strip()
    if df['crew'].eq('').any() or df['crew'].str.len().gt(80).any():
        raise ValueError('Crew names must contain 1–80 characters.')
    unknown = set(df.metric) - set(METRICS)
    if unknown:
        raise ValueError('Unknown metrics: ' + ', '.join(sorted(unknown)))
    df['timestamp'] = pd.to_datetime(df.timestamp, utc=True, errors='coerce')
    df['value'] = pd.to_numeric(df.value, errors='coerce')
    if df.timestamp.isna().any() or not np.isfinite(df.value).all():
        raise ValueError('Use valid timestamps and finite numeric values.')
    if df.value.lt(0).any():
        raise ValueError('Negative values are not supported by this data contract.')
    for metric, (_, unit) in METRICS.items():
        part = df[df.metric.eq(metric)]
        if not part.unit.eq(unit).all():
            raise ValueError(f'{metric} requires unit {unit}.')
        maximum = {'spo2': 100, 'sleep_hours': 24, 'mood': 5, 'stress': 5,
                   'activity_minutes': 1440, 'eva_minutes': 1440}.get(metric)
        if maximum is not None and part.value.gt(maximum).any():
            raise ValueError(f'{metric} cannot exceed {maximum}.')
        if metric in ['mood', 'stress'] and part.value.lt(1).any():
            raise ValueError(f'{metric} must be between 1 and 5.')
    if df.duplicated(['crew', 'timestamp', 'metric']).any():
        raise ValueError('Duplicate crew / timestamp / metric rows found.')
    return df.sort_values('timestamp').reset_index(drop=True)

def sample_data():
    rng = np.random.default_rng(42)
    dates = pd.date_range('2026-11-01', periods=14, tz='UTC')
    means = [64, 48, 7.4, 42, 98, 36.7, 2350, 2400, 75, .22, 4, 2]
    scales = [5, 6, .65, 12, .5, .15, 250, 180, 18, .03, .5, .5]
    rows = []
    for crew in ['Alex Morgan', 'Sam Rivera', 'Robin Chen']:
        for date in dates:
            for (metric, (_, unit)), mean, scale in zip(METRICS.items(), means, scales):
                value = max(0, float(rng.normal(mean, scale)))
                if metric in ['mood', 'stress']:
                    value = min(5, max(1, round(value)))
                rows.append([date + pd.Timedelta(hours=8), crew, metric, round(value, 2), unit])
    return validate_frame(pd.DataFrame(rows, columns=COLUMNS))
