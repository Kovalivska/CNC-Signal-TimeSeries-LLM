
import streamlit as st
import pandas as pd
import duckdb
import json
import os
from datetime import timedelta, date
from typing import List, Dict, Any
import pytz
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Machine Analytics — Extended", layout="wide")

# =============================
# Constants & schema
# =============================
DEFAULT_TZ = "Europe/Central"  # Generic Central European timezone
MACHINE_COL = "name"
TIMESTAMP_COL = "time"

# Helpful optional fields
EXEC_STRING = "exec_STRING"
EXEC_PROG_COMPLETED = "exec_program_completed_BOOL"
EXEC_ACTIVE = "exec_active_BOOL"
EXEC_STOPPED = "exec_stopped_BOOL"
EXEC_READY = "exec_ready_BOOL"
PGM_STRING = "pgm_STRING"
MODE_STRING = "mode_STRING"

# =============================
# Helpers
# =============================
@st.cache_data(show_spinner=False)
def load_files(files: List) -> pd.DataFrame:
    if not files:
        return pd.DataFrame()
    dfs = []
    for f in files:
        fn = f.name.lower()
        try:
            if fn.endswith(".csv"):
                # More robust CSV reading with error handling
                try:
                    # First try with C engine (faster) - auto-detect separator
                    df = pd.read_csv(f, low_memory=False, encoding='utf-8', on_bad_lines='skip', sep=None, engine='python')
                    if len(df.columns) == 1:  # If only one column, separator detection failed
                        raise ValueError("Separator detection failed")
                except Exception:
                    # Fallback: try common separators
                    f.seek(0)  # Reset file position
                    for sep in [';', ',', '\t', '|']:
                        try:
                            df = pd.read_csv(f, encoding='utf-8', on_bad_lines='skip', sep=sep)
                            if len(df.columns) > 1:  # Successfully parsed multiple columns
                                break
                            f.seek(0)  # Reset for next separator
                        except Exception:
                            f.seek(0)
                            continue
                    else:
                        # Last resort: use first line to detect separator
                        f.seek(0)
                        first_line = f.readline()
                        if ';' in first_line and first_line.count(';') > first_line.count(','):
                            sep = ';'
                        elif ',' in first_line:
                            sep = ','
                        elif '\t' in first_line:
                            sep = '\t'
                        else:
                            sep = ','
                        f.seek(0)
                        df = pd.read_csv(f, encoding='utf-8', on_bad_lines='skip', sep=sep)
            elif fn.endswith(".parquet"):
                df = pd.read_parquet(f)
            elif fn.endswith(".json") or fn.endswith(".jsonl"):
                df = pd.read_json(f, lines=fn.endswith(".jsonl"))
            else:
                st.warning(f"Unsupported file: {fn}")
                continue
            dfs.append(df)
            # Debug info
            st.sidebar.info(f"✅ Loaded {fn}: {len(df)} rows, {len(df.columns)} columns")
        except Exception as e:
            st.error(f"Error reading file {fn}: {str(e)}")
            continue
    if not dfs:
        return pd.DataFrame()
    df = pd.concat(dfs, ignore_index=True)
    return df

def coerce_timestamp(df: pd.DataFrame, col: str) -> pd.DataFrame:
    out = df.copy()
    if col in out.columns:
        out[col] = pd.to_datetime(out[col], errors="coerce", utc=True)
    return out

def iqr_bounds(s: pd.Series, k: float = 1.5):
    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    iqr = q3 - q1
    return q1 - k * iqr, q3 + k * iqr

def assign_shift(ts: pd.Series, tz: str = DEFAULT_TZ) -> pd.Series:
    """Map timestamps to shifts: 06–14, 14–22, 22–06 (Central European time)."""
    if ts.dt.tz is None:
        ts = ts.dt.tz_localize("UTC")
    local = ts.dt.tz_convert(pytz.timezone(tz))
    h = local.dt.hour
    shift = pd.Series(index=ts.index, dtype="object")
    shift[(h >= 6) & (h < 14)] = "06-14"
    shift[(h >= 14) & (h < 22)] = "14-22"
    shift[(h >= 22) | (h < 6)] = "22-06"
    return shift.astype(str)

# =============================
# Event detection
# =============================
def detect_part_completed(df: pd.DataFrame) -> pd.DataFrame:
    """Return rows [name, time, cycle_time_s] for completed units."""
    tmp = df.copy()
    # normalize types
    if EXEC_PROG_COMPLETED in tmp.columns:
        tmp[EXEC_PROG_COMPLETED] = tmp[EXEC_PROG_COMPLETED].astype(str).str.lower().isin(["1","true","t","yes","y"])
    if EXEC_STRING in tmp.columns:
        tmp[EXEC_STRING] = tmp[EXEC_STRING].astype(str)
    if PGM_STRING in tmp.columns:
        tmp[PGM_STRING] = tmp[PGM_STRING].astype(str)

    tmp = tmp.sort_values([MACHINE_COL, TIMESTAMP_COL]).reset_index(drop=True)

    marks = []

    # (1) Rising edge of program_completed
    if EXEC_PROG_COMPLETED in tmp.columns:
        tmp["_epc"] = tmp[EXEC_PROG_COMPLETED].fillna(False)
        tmp["_epc_prev"] = tmp.groupby(MACHINE_COL)["_epc"].shift(fill_value=False)
        rising_idx = tmp.index[(tmp["_epc"]) & (~tmp["_epc_prev"])].tolist()
        for i in rising_idx:
            marks.append((tmp.loc[i, MACHINE_COL], tmp.loc[i, TIMESTAMP_COL]))

    # (2) Textual cues in exec string
    if EXEC_STRING in tmp.columns:
        cue = tmp[EXEC_STRING].str.upper().str.contains("COMPLETED|COMPLETE|END|FINISH", regex=True, na=False)
        for i, row in tmp.loc[cue, [MACHINE_COL, TIMESTAMP_COL]].iterrows():
            marks.append((row[MACHINE_COL], row[TIMESTAMP_COL]))

    # (3) For CNC data: use changes in cycle time values as indicators
    if not marks:
        # Look for cycle time columns in CNC data
        cycle_cols = [col for col in tmp.columns if 'cycleTime' in col or 'CycleTime' in col]
        if cycle_cols:
            # Use first cycle time column
            cycle_col = cycle_cols[0]
            tmp[cycle_col] = pd.to_numeric(tmp[cycle_col], errors='coerce')
            # Detect significant changes in cycle time as completion events
            for machine in tmp[MACHINE_COL].unique():
                machine_data = tmp[tmp[MACHINE_COL] == machine].copy()
                machine_data = machine_data.dropna(subset=[cycle_col])
                if len(machine_data) > 1:
                    # Find rows where cycle time changes significantly
                    machine_data['cycle_diff'] = machine_data[cycle_col].diff().abs()
                    if not machine_data['cycle_diff'].isna().all():
                        threshold = machine_data['cycle_diff'].quantile(0.8)  # Top 20% of changes
                        significant_changes = machine_data[machine_data['cycle_diff'] > threshold]
                        for _, row in significant_changes.iterrows():
                            marks.append((row[MACHINE_COL], row[TIMESTAMP_COL]))

    # (4) Fallback: program change
    if not marks and PGM_STRING in tmp.columns:
        tmp["_pgm_change"] = tmp.groupby(MACHINE_COL)[PGM_STRING].transform(lambda s: s.ne(s.shift()))
        idx = tmp.index[tmp["_pgm_change"]].tolist()
        for i in idx:
            marks.append((tmp.loc[i, MACHINE_COL], tmp.loc[i, TIMESTAMP_COL]))

    # (5) Ultimate fallback: create artificial events based on time intervals
    if not marks:
        for machine in tmp[MACHINE_COL].unique():
            machine_data = tmp[tmp[MACHINE_COL] == machine].copy()
            if len(machine_data) > 10:  # Only if we have enough data
                # Create events every ~100 rows (simulating regular production)
                step = max(10, len(machine_data) // 20)  # At least 10, but roughly 20 events total
                for i in range(step, len(machine_data), step):
                    marks.append((machine, machine_data.iloc[i][TIMESTAMP_COL]))

    if not marks:
        return pd.DataFrame(columns=[MACHINE_COL, TIMESTAMP_COL, "cycle_time_s"])

    parts = pd.DataFrame(marks, columns=[MACHINE_COL, TIMESTAMP_COL]).drop_duplicates().dropna()
    parts = parts.sort_values([MACHINE_COL, TIMESTAMP_COL]).reset_index(drop=True)
    parts["cycle_time_s"] = parts.groupby(MACHINE_COL)[TIMESTAMP_COL].diff().dt.total_seconds()
    parts = parts.dropna(subset=["cycle_time_s"])
    if not parts.empty:
        low, high = iqr_bounds(parts["cycle_time_s"])
        parts = parts[(parts["cycle_time_s"] >= max(0, low)) & (parts["cycle_time_s"] <= high)]
    return parts

def detect_setup_intervals(df: pd.DataFrame) -> pd.DataFrame:
    """Return [name, start, end, setup_s] either via explicit setup mode or long gaps around program changes."""
    d = df.copy().sort_values([MACHINE_COL, TIMESTAMP_COL]).reset_index(drop=True)

    # explicit setup via MODE_STRING
    out = []
    explicit_done = False
    if MODE_STRING in d.columns:
        mode = d[MODE_STRING].astype(str).str.upper()
        d["_is_setup"] = mode.str.contains("SETUP|RÜST|RUEST|RUEST", regex=True, na=False)
        for mid, g in d.groupby(MACHINE_COL):
            g = g[[TIMESTAMP_COL, "_is_setup"]].reset_index(drop=True)
            block_start = None
            for i, row in g.iterrows():
                if row["_is_setup"] and block_start is None:
                    block_start = row[TIMESTAMP_COL]
                is_last = (i == len(g) - 1)
                if (block_start is not None) and (not row["_is_setup"] or is_last):
                    end_time = g.iloc[i][TIMESTAMP_COL]
                    setup_s = (end_time - block_start).total_seconds()
                    if setup_s > 0:
                        out.append({MACHINE_COL: mid, "start": block_start, "end": end_time, "setup_s": setup_s})
                    block_start = None
        if out:
            explicit_done = True

    # heuristic via program changes and long gaps
    if not explicit_done:
        THRESHOLD_S = 5 * 60
        if PGM_STRING in d.columns:
            d["_pgm_change"] = d.groupby(MACHINE_COL)[PGM_STRING].transform(lambda s: s.ne(s.shift()))
        else:
            d["_pgm_change"] = False
        for mid, g in d.groupby(MACHINE_COL):
            g = g[[TIMESTAMP_COL, "_pgm_change"]].reset_index(drop=True)
            for i in range(1, len(g)):
                prev_t = g.loc[i-1, TIMESTAMP_COL]
                curr_t = g.loc[i, TIMESTAMP_COL]
                gap = (curr_t - prev_t).total_seconds()
                is_change = bool(g.loc[i, "_pgm_change"])
                if is_change and gap >= THRESHOLD_S:
                    out.append({MACHINE_COL: mid, "start": prev_t, "end": curr_t, "setup_s": gap})

    return pd.DataFrame(out, columns=[MACHINE_COL, "start", "end", "setup_s"]) if out else pd.DataFrame(columns=[MACHINE_COL, "start", "end", "setup_s"])

# =============================
# Dynamic metrics discovery
# =============================
NUMERIC_SUFFIXES = ("_REAL", "_LREAL", "_BOOL", "_INT", "_FLOAT", "_DOUBLE")
EXCLUDE_COLS = {MACHINE_COL, TIMESTAMP_COL}

def numeric_dynamic_columns(df: pd.DataFrame, top_k: int = 5) -> List[str]:
    """Pick top-k numeric columns that actually change over time (by change count)."""
    candidates = []
    for col in df.columns:
        if col in EXCLUDE_COLS: 
            continue
        if col.endswith("_STRING"):
            continue
        # accept numeric dtype or boolean-like columns
        if pd.api.types.is_numeric_dtype(df[col]) or col.endswith(NUMERIC_SUFFIXES):
            candidates.append(col)
    if not candidates:
        return []

    # Score by number of changes > epsilon between consecutive points per machine, then sum
    eps = 1e-9
    scores = {}
    for col in candidates:
        g = df[[MACHINE_COL, TIMESTAMP_COL, col]].dropna().sort_values([MACHINE_COL, TIMESTAMP_COL])
        if g.empty:
            scores[col] = 0
            continue
        
        # Check value range first - if all values are identical, score is 0
        unique_values = g[col].nunique()
        if unique_values <= 1:
            scores[col] = 0
            continue
        
        # coerce bool-like
        if g[col].dtype == bool:
            series = g[col].astype(int)
            changes = (series.groupby(g[MACHINE_COL]).diff().fillna(0).abs() > 0).sum()
        else:
            series = pd.to_numeric(g[col], errors="coerce")
            if series.isna().all():
                scores[col] = 0
                continue
            
            # Count actual changes between consecutive values
            changes = (series.groupby(g[MACHINE_COL]).diff().abs() > eps).sum()
            
            # Bonus for higher variance (more diverse values)
            variance_bonus = series.var() if not series.isna().all() else 0
            if variance_bonus > 0:
                changes += min(10, int(variance_bonus / 1000))  # Small bonus for variance
        
        scores[col] = int(changes)
    
    # Debug: show all scores in Streamlit (only when called from timeseries)
    if hasattr(st, '_is_timeseries_debug') and st._is_timeseries_debug:
        st.write("**🔍 Dynamic Variables Analysis:**")
        st.write(f"Found {len(candidates)} numeric candidates")
        ordered_debug = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
        
        # Filter out constant variables for the actual selection
        varying_variables = [col for col, score in ordered_debug if score > 0]
        constant_variables = [col for col, score in ordered_debug if score == 0]
        
        # Show statistics
        st.write(f"📊 **Summary:** {len(varying_variables)} varying, {len(constant_variables)} constant variables")
        
        # Show top variables with their scores - highlight ALL varying ones
        st.write("**Top dynamic variables:**")
        for i, (col, score) in enumerate(ordered_debug[:20]):  # Show top 20
            # Mark as selected if it's varying (score > 0) AND within reasonable limit
            is_varying = score > 0
            status = "✅ VARYING" if is_varying else "❌ CONSTANT"
            short_name = col.split('/')[-1] if '/' in col else col  # Show short name
            
            if score > 0:
                st.text(f"{i+1:2d}. {short_name}: {score} changes {status}")
            else:
                st.text(f"{i+1:2d}. {short_name}: CONSTANT {status}")
        
        if len(ordered_debug) > 20:
            remaining_varying = sum(1 for _, score in ordered_debug[20:] if score > 0)
            remaining_constant = sum(1 for _, score in ordered_debug[20:] if score == 0)
            st.text(f"... and {remaining_varying} more varying + {remaining_constant} constant variables")
    
    ordered = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    
    # Return ALL varying variables up to top_k limit, not just top_k regardless of variation
    varying_only = [c for c, score in ordered if score > 0]
    return varying_only[:top_k] if top_k > 0 else varying_only

def resample_frame(df: pd.DataFrame, cols: List[str], rule: str):
    """Resample selected numeric columns by mean with the given pandas rule (10s, 1min, 1H, 1D, 1W)."""
    if not cols:
        return pd.DataFrame()
    
    # Create a copy with only needed columns
    d = df[[TIMESTAMP_COL] + [col for col in cols if col in df.columns]].copy()
    
    # Drop rows where ALL selected columns are NaN
    d = d.dropna(subset=[col for col in cols if col in d.columns], how='all')
    
    # Ensure timestamp column is properly formatted
    if not pd.api.types.is_datetime64_any_dtype(d[TIMESTAMP_COL]):
        d[TIMESTAMP_COL] = pd.to_datetime(d[TIMESTAMP_COL], errors="coerce", utc=True)
    
    # Remove rows with invalid timestamps
    d = d.dropna(subset=[TIMESTAMP_COL])
    d = d.set_index(TIMESTAMP_COL).sort_index()
    
    # For raw data, return all points without aggregation
    if rule == "raw":
        # Just return the data as-is, but ensure numeric types
        for col in cols:
            if col in d.columns:
                d[col] = pd.to_numeric(d[col], errors='coerce')
        return d
    
    # For aggregated data, use resampling
    rule_map = {"10s":"10S", "1m":"1T", "1h":"1H", "1d":"1D", "1w":"1W"}
    r = rule_map.get(rule, "10S")
    
    # For boolean-like variables, use mode instead of mean to preserve discrete values
    # For continuous variables, use mean
    result_data = {}
    
    for col in cols:
        if col in d.columns:
            series = pd.to_numeric(d[col], errors='coerce')
            # Check if column has only a few distinct values (likely boolean/categorical)
            unique_count = series.nunique()
            if unique_count <= 10:  # Treat as categorical/boolean
                # Use most frequent value in each interval
                resampled = series.resample(r).agg(lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else x.iloc[0] if len(x) > 0 else 0)
            else:
                # Use mean for continuous variables
                resampled = series.resample(r).mean()
            
            result_data[col] = resampled
    
    # Combine all columns
    resampled = pd.DataFrame(result_data)
    
    # Convert all numeric columns to float64 for consistency
    for col in cols:
        if col in resampled.columns:
            resampled[col] = pd.to_numeric(resampled[col], errors='coerce')
    
    return resampled

# =============================
# Intent parsing and presets
# =============================
def parse_intent(q: str) -> Dict[str, Any]:
    ql = (q or "").lower().strip()
    intent = None
    if any(k in ql for k in ["zyklus", "cycle", "цик"]):
        intent = "avg_cycle_time"
    if any(k in ql for k in ["rüst", "ruest", "setup", "рюст", "перенал"]):
        intent = "setup_time"
    if any(k in ql for k in ["meist", "most", "top", "produziert", "output", "throughput"]):
        intent = "max_output"
    if any(k in ql for k in ["schicht", "shift"]):
        intent = "shift_kpis"
    if any(k in ql for k in ["zeitreihe", "time series", "timeseries"]):
        intent = "dynamic_timeseries_top"
    return {"intent": intent, "machine_id": None, "date_from": None, "date_to": None}

# =============================
# UI
# =============================
st.title("🔧 Machine Analytics — Extended")
st.caption("Fully offline. Presets + text questions. JSON + SQL + Charts.")

uploaded = st.sidebar.file_uploader("Upload CSV/Parquet/JSON files", type=["csv","parquet","json","jsonl"], accept_multiple_files=True)

# Add option to load default CNC dataset
if st.sidebar.button("📊 Load Default CNC Dataset"):
    st.cache_data.clear()  # Clear any existing cache
    default_data_path = "/Users/svitlanakovalivska/Industrial_Signal_Processing_TimeSeriesAnalysis/data_and_eda/cnc_daten.csv"
    if os.path.exists(default_data_path):
        try:
            # Load the default dataset directly
            df_default = pd.read_csv(default_data_path, encoding='utf-8', sep=';', on_bad_lines='skip')
            st.session_state['default_dataset'] = df_default
            st.sidebar.success(f"✅ Loaded default dataset: {len(df_default)} rows, {len(df_default.columns)} columns")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"❌ Error loading default dataset: {str(e)}")
    else:
        st.sidebar.warning(f"⚠️ Default dataset not found at: {default_data_path}")
        # Try alternative paths
        alternative_paths = [
            "../data_and_eda/cnc_daten.csv",
            "../../data_and_eda/cnc_daten.csv",
            "./data_and_eda/cnc_daten.csv"
        ]
        for alt_path in alternative_paths:
            if os.path.exists(alt_path):
                st.sidebar.info(f"🔍 Found dataset at alternative path: {alt_path}")
                try:
                    df_default = pd.read_csv(alt_path, encoding='utf-8', sep=';', on_bad_lines='skip')
                    st.session_state['default_dataset'] = df_default
                    st.sidebar.success(f"✅ Loaded dataset: {len(df_default)} rows, {len(df_default.columns)} columns")
                    st.rerun()
                    break
                except Exception as e:
                    continue

# Add cache clear button
if st.sidebar.button("🔄 Clear Cache"):
    st.cache_data.clear()
    if 'default_dataset' in st.session_state:
        del st.session_state['default_dataset']
    st.rerun()

# Load data from either uploaded files or default dataset
if 'default_dataset' in st.session_state and not uploaded:
    df = st.session_state['default_dataset'].copy()
    st.sidebar.info("📊 Using default CNC dataset")
else:
    df = load_files(uploaded)
if df.empty:
    st.info("Please upload your files to start, or use the default CNC dataset.")
    st.markdown("""
    ### 📋 Expected Data Format
    
    Your data should contain these **required columns**:
    - `name` - Machine identifier (e.g., 'CNC_1', 'Machine_A')
    - `time` - Timestamp column (any standard datetime format)
    
    ### 📁 Supported File Types
    - **CSV**: Comma-separated values
    - **Parquet**: Columnar data format
    - **JSON/JSONL**: JavaScript Object Notation
    
    ### 📊 Optional CNC Signal Columns
    The app recognizes 90+ standard CNC/PLC fields including:
    - `exec_program_completed_BOOL` - Program completion status
    - `mode_STRING` - Operating mode (for setup detection)
    - `pgm_STRING` - Program identifier
    - Various `*_REAL`, `*_BOOL`, `*_STRING` process parameters
    
    ### 🚀 Quick Start
    Click **"📊 Load Default CNC Dataset"** in the sidebar to try the app with sample CNC7 machine data!
    """)
    st.stop()

# Parse/prepare
if TIMESTAMP_COL not in df.columns:
    st.error(f"❌ Required column '{TIMESTAMP_COL}' not found in uploaded files!")
    st.info(f"Available columns: {list(df.columns)}")
    st.info(f"Please ensure your data has a column named '{TIMESTAMP_COL}' containing timestamps.")
    st.stop()

if MACHINE_COL not in df.columns:
    st.error(f"❌ Required column '{MACHINE_COL}' not found in uploaded files!")
    st.info(f"Available columns: {list(df.columns)}")
    st.info(f"Please ensure your data has a column named '{MACHINE_COL}' containing machine identifiers.")
    st.stop()

df = coerce_timestamp(df, TIMESTAMP_COL).dropna(subset=[TIMESTAMP_COL])
df = df.sort_values([MACHINE_COL, TIMESTAMP_COL]).reset_index(drop=True)

# Show basic data info after successful validation
dataset_source = "📊 Default CNC Dataset" if 'default_dataset' in st.session_state and not uploaded else "📁 Uploaded Files"
st.sidebar.markdown(f"""
### 📊 Data Overview
**Source:** {dataset_source}
- **Rows**: {len(df):,}
- **Columns**: {len(df.columns)}
- **Machines**: {df[MACHINE_COL].nunique()}
- **Time range**: {df[TIMESTAMP_COL].min().strftime('%Y-%m-%d %H:%M')} to {df[TIMESTAMP_COL].max().strftime('%Y-%m-%d %H:%M')}
""")

# Filters
with st.sidebar:
    st.subheader("Filters")
    machines = sorted(df[MACHINE_COL].astype(str).unique().tolist()) if MACHINE_COL in df.columns else []
    selected_machines = st.multiselect("Machines (name)", machines, default=machines)
    date_min = df[TIMESTAMP_COL].min().date()
    date_max = df[TIMESTAMP_COL].max().date()
    date_range = st.date_input("Date range", value=(date_min, date_max), min_value=date_min, max_value=date_max)

# Apply filters
mask = df[MACHINE_COL].astype(str).isin([str(x) for x in selected_machines])
from_dt = pd.to_datetime(date_range[0]).tz_localize("UTC")
to_dt = pd.to_datetime(date_range[1]).tz_localize("UTC") + timedelta(days=1)
mask &= (df[TIMESTAMP_COL] >= from_dt) & (df[TIMESTAMP_COL] < to_dt)
df_f = df.loc[mask].copy()

# Derived tables for SQL
parts = detect_part_completed(df_f)
setups = detect_setup_intervals(df_f)

# Add debugging information
st.sidebar.write("---")
st.sidebar.subheader("🔍 Debug Info")
st.sidebar.write(f"**Filtered data:** {len(df_f)} rows")
st.sidebar.write(f"**Parts detected:** {len(parts)} events")
st.sidebar.write(f"**Setups detected:** {len(setups)} intervals")

# Show sample of actual data columns
if not df_f.empty:
    st.sidebar.write("**Available columns:**")
    st.sidebar.write(f"{len(df_f.columns)} total")
    numeric_cols = df_f.select_dtypes(include=['number']).columns.tolist()
    st.sidebar.write(f"**Numeric columns:** {len(numeric_cols)}")
    
# Show parts/setups data preview if available
if not parts.empty:
    st.sidebar.write("**Parts sample:**")
    try:
        # Fix data types for Arrow compatibility
        parts_display = parts.head(3).copy()
        for col in parts_display.columns:
            if parts_display[col].dtype == 'object':
                parts_display[col] = parts_display[col].astype(str)
            elif pd.api.types.is_datetime64_any_dtype(parts_display[col]):
                parts_display[col] = parts_display[col].dt.strftime('%Y-%m-%d %H:%M:%S')
            elif pd.api.types.is_numeric_dtype(parts_display[col]):
                parts_display[col] = pd.to_numeric(parts_display[col], errors='coerce').astype('float64')
        st.sidebar.dataframe(parts_display)
    except Exception as e:
        st.sidebar.text("Parts events detected but preview unavailable")
        st.sidebar.text(f"Sample: {len(parts)} events from {parts[TIMESTAMP_COL].min()} to {parts[TIMESTAMP_COL].max()}")

if not setups.empty:
    st.sidebar.write("**Setups sample:**")
    try:
        # Fix data types for Arrow compatibility
        setups_display = setups.head(3).copy()
        for col in setups_display.columns:
            if setups_display[col].dtype == 'object':
                setups_display[col] = setups_display[col].astype(str)
            elif pd.api.types.is_datetime64_any_dtype(setups_display[col]):
                setups_display[col] = setups_display[col].dt.strftime('%Y-%m-%d %H:%M:%S')
            elif pd.api.types.is_numeric_dtype(setups_display[col]):
                setups_display[col] = pd.to_numeric(setups_display[col], errors='coerce').astype('float64')
        st.sidebar.dataframe(setups_display)
    except Exception as e:
        st.sidebar.text("Setup intervals detected but preview unavailable")
        st.sidebar.text(f"Sample: {len(setups)} intervals")

con = duckdb.connect(database=":memory:")
con.register("events", df_f)
con.register("part_events", parts)
con.register("setup_intervals", setups)

# Presets
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
presets_path = os.path.join(script_dir, "templates", "presets.json")

try:
    with open(presets_path, "r", encoding="utf-8") as f:
        presets = json.load(f)
except FileNotFoundError:
    st.error("❌ Presets file not found. Creating default presets...")
    st.info(f"🔍 Looking for: {presets_path}")
    presets = [
        {"name": "Zeitreihe: Top-5 dynamische Variablen (auto)", "id": "timeseries_top5"},
        {"name": "Zeitreihe: Alle dynamischen Variablen (auto)", "id": "timeseries_auto"},
        {"name": "Zeitreihe: Auswahl bis zu 10 dynamischer numerischer Kennzahlen", "id": "timeseries_select"},
        {"name": "Durchschnittliche Zykluszeit (alle Maschinen)", "id": "avg_cycle_time"},
        {"name": "Gesamte Rüstzeit (Maschine 1)", "id": "setup_time_m1"},
        {"name": "Meiste Produktion (Top-Maschine)", "id": "top_production"},
        {"name": "KPIs pro Schicht", "id": "shift_kpis"}
    ]

preset_names = [p["name"] for p in presets]
preset = st.selectbox("Preset question", preset_names, index=0 if preset_names else None)
agg_rule = None
selected_columns_for_preset2 = []

# Dynamic controls for timeseries presets
if preset and "Zeitreihe" in preset:
    st.sidebar.subheader("Aggregation")
    agg_rule = st.sidebar.selectbox("Rule", ["raw","10s","1m","1h","1d","1w"], index=1)  # Default to 10s instead of 1m
    
    # Show aggregation info
    if agg_rule == "raw":
        st.sidebar.info("📊 Raw data: All data points")
    elif agg_rule == "10s":
        st.sidebar.info("📊 10-second intervals: Best for dynamic variables")
    elif agg_rule == "1m":
        st.sidebar.warning("⚠️ 1-minute intervals: May smooth out rapid changes")
    else:
        st.sidebar.warning("⚠️ Large intervals: Will lose fast dynamics")
        
    if "Top-5" in preset or "Alle dynamischen" in preset:
        pass
    else:
        # second preset: user-selected metrics up to 10
        st.sidebar.write("**📊 Analyzing all variables...**")
        # Enable debug temporarily to get scores
        st._is_timeseries_debug = True  # Enable debug to show analysis
        dyn_cols = numeric_dynamic_columns(df_f, top_k=0)  # Get ALL varying variables, no limit
        st._is_timeseries_debug = False  # Disable for UI selection
        st.sidebar.write(f"Found {len(dyn_cols)} dynamic variables")
        
        # Show ALL dynamic variables in sidebar
        st.sidebar.write(f"**All {len(dyn_cols)} dynamic variables:**")
        for i, col in enumerate(dyn_cols):
            st.sidebar.text(f"{i+1}. {col.split('/')[-1]}")  # Show just the last part
        
        # Default to ALL dynamic variables (up to 10)
        default_selection = dyn_cols[:min(10, len(dyn_cols))]
        selected_columns_for_preset2 = st.sidebar.multiselect("Select up to 10 metrics", dyn_cols, default=default_selection)
        if len(selected_columns_for_preset2) > 10:
            st.sidebar.warning("Please select no more than 10 metrics.")
            selected_columns_for_preset2 = selected_columns_for_preset2[:10]

run_preset = st.button("Run preset")

question = st.text_input("Or ask a question in free text", "")
intent = parse_intent(question) if question else None

left, right = st.columns([1,2])
with left:
    st.subheader("Structured request (JSON)")
    st.json(intent or {"preset": preset})

    st.subheader("SQL used")
    sql_placeholder = st.empty()

with right:
    st.subheader("Result & Chart")

def show_sql(sql: str):
    sql_placeholder.code(sql, language="sql")

def timeseries_chart(cols: List[str], rule: str):
    if not cols:
        st.warning("No numeric metrics selected/found.")
        show_sql("-- N/A: pandas resample used for dynamic timeseries (no SQL)")
        return
    
    # Enable debug mode for dynamic columns analysis
    st._is_timeseries_debug = True
    
    # Debug: show what we're getting as input
    st.write(f"**🔍 Input Debug:**")
    st.write(f"- Selected columns: {cols}")
    st.write(f"- Aggregation rule: {rule}")
    st.write(f"- Source data shape: {df_f.shape}")
    
    data = resample_frame(df_f, cols, rule or "1m")
    if data.empty:
        st.warning("No data available for the selected metrics/date range.")
        show_sql("-- N/A: pandas resample used for dynamic timeseries (no SQL)")
        return
    
    try:
        # Display summary information
        st.write(f"**📊 Timeseries Data:** {len(data)} data points")
        
        # Debug: show raw data shape and content
        st.write(f"**🔍 Debug - Raw data shape:** {data.shape}")
        st.write(f"**🔍 Debug - Columns:** {list(data.columns)}")
        st.write(f"**🔍 Debug - Index type:** {type(data.index)}")
        if not data.empty:
            st.write(f"**🔍 Debug - Time range:** {data.index.min()} to {data.index.max()}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Data Points", len(data))
        with col2:
            if len(data) > 0:
                st.metric("Time Span", f"{(data.index[-1] - data.index[0]).total_seconds() / 3600:.1f} hours")
        with col3:
            st.metric("Metrics", len(cols))
        
        # Create interactive Plotly chart
        st.write("**📈 Interactive Time Series Chart:**")
        
        # Reset index to work with Plotly
        chart_data = data.reset_index()
        
        # Fix datetime column for Plotly compatibility - convert to string
        chart_data[TIMESTAMP_COL] = chart_data[TIMESTAMP_COL].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Ensure all numeric columns are properly typed
        for col in cols:
            if col in chart_data.columns:
                chart_data[col] = pd.to_numeric(chart_data[col], errors='coerce').astype('float64')
        
        # Analyze value ranges to decide on scaling strategy
        ranges = {}
        for col in cols:
            if col in chart_data.columns:
                values = chart_data[col].dropna()
                if not values.empty:
                    ranges[col] = {
                        'min': values.min(),
                        'max': values.max(),
                        'range': values.max() - values.min()
                    }
        
        # Check if we need multiple y-axes (ranges differ by more than 100x)
        # Also filter out variables with zero range (constant values)
        # BUT be more lenient - if we have very few data points, show variables anyway
        if len(chart_data) <= 10:  # For small datasets, be more permissive
            varying_ranges = {k: v for k, v in ranges.items() if k in chart_data.columns}
            st.info("📊 **Small dataset detected** - showing all available variables regardless of variation")
        else:
            varying_ranges = {k: v for k, v in ranges.items() if v['range'] > 0}
        
        # Debug: show all ranges
        st.write("**🔍 Value Ranges Analysis:**")
        for col in cols:
            if col in ranges:
                r = ranges[col]
                variation_status = "VARYING" if r['range'] > 0 else "CONSTANT"
                st.text(f"{col}: min={r['min']:.2f}, max={r['max']:.2f}, range={r['range']:.2f} [{variation_status}]")
            else:
                st.text(f"{col}: NO VALID DATA")
        
        if not varying_ranges:
            st.warning("⚠️ All selected variables have constant values (no variation over time). Try selecting different metrics or check your data.")
            
            # Show constant values anyway for reference
            st.write("**Constant Values:**")
            for col in cols:
                if col in chart_data.columns:
                    value = chart_data[col].iloc[0] if not chart_data[col].empty else "N/A"
                    st.text(f"{col}: {value}")
            return
        
        max_range = max([r['range'] for r in varying_ranges.values()]) if varying_ranges else 1
        min_range = min([r['range'] for r in varying_ranges.values()]) if varying_ranges else 1
        needs_multi_axis = (max_range / min_range) > 100 if min_range > 0 else False
        
        # Filter columns to only show those with variation
        varying_cols = list(varying_ranges.keys())
        if len(varying_cols) < len(cols):
            st.info(f"📊 **Filtered view**: Showing only {len(varying_cols)} variables with variation. Constant variables: {', '.join([c for c in cols if c not in varying_cols])}")
        
        # Force showing all varying variables, even if they have different scales
        st.write(f"**📊 Will display {len(varying_cols)} varying variables**")
        st.write(f"**Multi-axis needed:** {needs_multi_axis} (range ratio: {max_range/min_range:.1f})")
        
        # Create multi-axis chart to show all variables
        fig = go.Figure()
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
        
        # Smart axis assignment based on value ranges
        axis_assignment = {}
        y_axes = ['y', 'y2', 'y3', 'y4']
        
        # Sort variables by range size to distribute across axes
        range_sorted = sorted(varying_ranges.items(), key=lambda x: x[1]['range'], reverse=True)
        
        for i, (col, range_info) in enumerate(range_sorted):
            # Assign to different axes to spread out the ranges
            axis_idx = i % len(y_axes)
            axis_assignment[col] = y_axes[axis_idx]
        
        st.write(f"**📊 Axis Assignment for {len(varying_cols)} Variables:**")
        for col in varying_cols:
            if col in axis_assignment:
                range_info = varying_ranges[col]
                st.text(f"• {col.split('/')[-1]}: {axis_assignment[col]} (range: {range_info['range']:.2f})")
        
        # Add all traces
        for i, col in enumerate(varying_cols):
            if col in chart_data.columns and col in axis_assignment:
                display_name = col.split('/')[-1] if '/' in col else col
                color = colors[i % len(colors)]
                y_axis = axis_assignment[col]
                
                # Clean data
                y_values = pd.to_numeric(chart_data[col], errors='coerce')
                
                # Add trace
                fig.add_trace(go.Scatter(
                    x=chart_data[TIMESTAMP_COL],
                    y=y_values,
                    mode='lines',
                    name=f"{display_name} [{y_axis}]",
                    line=dict(width=2, color=color),
                    yaxis=y_axis if y_axis != 'y' else None,
                    connectgaps=False
                ))
        
        # Setup layout with all y-axes
        layout = {
            'title': f"CNC Time Series - All {len(varying_cols)} Variables (Multi-Axis)",
            'xaxis': {'title': "Time"},
            'height': 600,
            'showlegend': True,
            'legend': {'x': 1.05, 'y': 1}
        }
        
        # Add y-axis configurations for all used axes
        used_axes = set(axis_assignment.values())
        
        # Primary axis (left)
        if 'y' in used_axes:
            layout['yaxis'] = {'title': 'Primary', 'side': 'left'}
        
        # Secondary axis (right)  
        if 'y2' in used_axes:
            layout['yaxis2'] = {'title': 'Secondary', 'side': 'right', 'overlaying': 'y'}
        
        # Tertiary axis (left, shifted)
        if 'y3' in used_axes:
            layout['yaxis3'] = {'title': 'Tertiary', 'side': 'left', 'overlaying': 'y', 'position': 0.05}
        
        # Quaternary axis (right, shifted)
        if 'y4' in used_axes:
            layout['yaxis4'] = {'title': 'Quaternary', 'side': 'right', 'overlaying': 'y', 'position': 0.95}
        
        fig.update_layout(**layout)
        st.plotly_chart(fig, use_container_width=True)
        
        # Normalized chart for trend comparison
        st.write("**📈 Normalized View (0-1 scale) - Trend Comparison:**")
        
        fig_norm = go.Figure()
        
        for i, col in enumerate(varying_cols):
            if col in chart_data.columns:
                values = pd.to_numeric(chart_data[col], errors='coerce')
                
                # Normalize to 0-1 scale
                if not values.isna().all() and values.max() != values.min():
                    normalized = (values - values.min()) / (values.max() - values.min())
                else:
                    normalized = pd.Series([0.5] * len(values))  # Constant at 0.5 if no variation
                
                display_name = col.split('/')[-1] if '/' in col else col
                color = colors[i % len(colors)]
                
                fig_norm.add_trace(go.Scatter(
                    x=chart_data[TIMESTAMP_COL],
                    y=normalized,
                    mode='lines',
                    name=display_name,
                    line=dict(width=2, color=color),
                    connectgaps=False
                ))
        
        fig_norm.update_layout(
            title="All Variables Normalized (0-1 Scale) - Compare Trends",
            xaxis_title="Time",
            yaxis_title="Normalized Value (0=min, 1=max)",
            height=400,
            showlegend=True,
            legend={'x': 1.05, 'y': 1}
        )
        
        st.plotly_chart(fig_norm, use_container_width=True)
        
        # Summary info
        st.write("**📊 Summary:**")
        st.write(f"• **{len(varying_cols)}** variables with changes displayed")
        st.write(f"• **{len(chart_data)}** data points over time")
        # Fix the time span calculation
        if len(chart_data) > 1:
            try:
                # Use the original data index for time calculation
                time_span_hours = (data.index[-1] - data.index[0]).total_seconds() / 3600
                st.write(f"• **{time_span_hours:.1f}** hours")
            except Exception:
                st.write(f"• Time span calculation error")
        else:
            st.write("• Single time point")
        
        # Show variable details
        st.write("**🔍 Variable Details:**")
        for col in varying_cols:
            if col in varying_ranges:
                r = varying_ranges[col]
                st.text(f"• {col.split('/')[-1]}: {r['min']:.2f} to {r['max']:.2f} (range: {r['range']:.2f})")
        
        show_sql("-- N/A: pandas resample used for dynamic timeseries (no SQL)")
        
    except Exception as e:
        st.error(f"Error creating chart: {str(e)}")
        st.write("**Data Available:**")
        st.write(f"- Rows: {len(data)}")
        st.write(f"- Columns: {len(data.columns)}")
        if hasattr(data.index, 'min') and hasattr(data.index, 'max'):
            st.write(f"- Time range: {data.index.min()} to {data.index.max()}")
        show_sql("-- N/A: pandas resample used for dynamic timeseries (no SQL)")

if run_preset and preset:
    # Handle presets
    if "Zeitreihe: Alle dynamischen" in preset:
        # Enable debug mode
        st._is_timeseries_debug = True
        # Show ALL varying variables automatically - no limit
        all_varying = numeric_dynamic_columns(df_f, top_k=0)  # 0 means no limit - all varying variables
        st.caption(f"Found {len(all_varying)} dynamic variables - showing ALL with changes")
        timeseries_chart(all_varying, agg_rule or "1m")

    elif "Top-5" in preset or "Top 5" in preset:
        # Enable debug mode for top 5 preset
        st._is_timeseries_debug = True
        # Show top 5 dynamic variables
        top5_vars = numeric_dynamic_columns(df_f, top_k=5)  # Limit to top 5
        st.caption(f"Found {len(top5_vars)} top dynamic variables")
        timeseries_chart(top5_vars, agg_rule or "10s")

    elif "Zeitreihe: Auswahl" in preset:
        # Enable debug mode
        st._is_timeseries_debug = True
        # First show analysis of all variables
        st.write("**🔍 Available Dynamic Variables Analysis:**")
        all_dynamic = numeric_dynamic_columns(df_f, top_k=0)  # Show ALL varying variables
        
        cols = selected_columns_for_preset2[:10]
        st.caption(f"Selected metrics ({len(cols)}): {', '.join(cols) if cols else 'none'}")
        timeseries_chart(cols, agg_rule or "1m")

    elif "Durchschnittliche Zykluszeit" in preset:
        if parts.empty:
            st.warning("No part completion events detected.")
            show_sql("-- No data in part_events")
        else:
            sql = f"""
            SELECT AVG(cycle_time_s) AS avg_cycle_time_s
            FROM part_events
            WHERE time >= TIMESTAMP '{from_dt}' AND time < TIMESTAMP '{to_dt}'
            """
            show_sql(sql)
            res = con.execute(sql).df()
            if not res.empty:
                st.metric("Average Cycle Time", f"{res['avg_cycle_time_s'].iloc[0]:.2f} s")
            # time trend (rolling mean)
            if not parts.empty:
                try:
                    s = parts.set_index(TIMESTAMP_COL)["cycle_time_s"].rolling(20, min_periods=1).mean()
                    # Create Plotly chart
                    chart_data = s.reset_index()
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=chart_data[TIMESTAMP_COL],
                        y=chart_data["cycle_time_s"],
                        mode='lines',
                        name='Cycle Time (20-point rolling mean)',
                        line=dict(width=2, color='blue')
                    ))
                    
                    fig.update_layout(
                        title="Cycle Time Trend",
                        xaxis_title="Time",
                        yaxis_title="Cycle Time (seconds)",
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                except Exception:
                    st.info("Cycle time data available but chart cannot be displayed")

    elif "Gesamte Rüstzeit (Maschine 1)" in preset:
        st.write("**🔍 Setup Analysis Debug:**")
        st.write(f"- Setup intervals found: {len(setups)}")
        st.write(f"- Available machines: {df_f[MACHINE_COL].unique().tolist()}")
        st.write(f"- Date range: {from_dt} to {to_dt}")
        
        if setups.empty:
            st.warning("No setup intervals detected.")
            show_sql("-- No data in setup_intervals")
            
            # Try to show why no setups were detected
            st.write("**🔍 Debug: Why no setups detected?**")
            if MODE_STRING in df_f.columns:
                mode_values = df_f[MODE_STRING].dropna().unique()
                st.write(f"- Mode values found: {mode_values[:10]}")
                setup_patterns = df_f[MODE_STRING].astype(str).str.upper().str.contains("SETUP|RÜST|RUEST", regex=True, na=False).sum()
                st.write(f"- Rows with setup patterns: {setup_patterns}")
            else:
                st.write(f"- {MODE_STRING} column not found in data")
                
            if PGM_STRING in df_f.columns:
                pgm_changes = df_f.groupby(MACHINE_COL)[PGM_STRING].transform(lambda s: s.ne(s.shift())).sum()
                st.write(f"- Program changes detected: {pgm_changes}")
            else:
                st.write(f"- {PGM_STRING} column not found in data")
        else:
            sql = f"""
            SELECT SUM(setup_s)/60.0 AS total_setup_min
            FROM setup_intervals
            WHERE start >= TIMESTAMP '{from_dt}' AND start < TIMESTAMP '{to_dt}'
              AND name = '1'
            """
            show_sql(sql)
            res = con.execute(sql).df()
            if not res.empty and not res['total_setup_min'].iloc[0] == 0:
                st.metric("Total Setup Time (M1)", f"{res['total_setup_min'].iloc[0]:.1f} min")
            else:
                st.warning("No setup intervals found for Machine 1 in the selected date range.")
                st.write("**Available setup data:**")
                st.dataframe(setups.head())
            
            if not setups.empty:
                try:
                    s = setups.set_index("start")["setup_s"]
                    # Create Plotly bar chart
                    chart_data = s.reset_index()
                    
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=chart_data["start"],
                        y=chart_data["setup_s"] / 60,  # Convert to minutes
                        name='Setup Time',
                        marker_color='orange'
                    ))
                    
                    fig.update_layout(
                        title="Setup Time Distribution",
                        xaxis_title="Time",
                        yaxis_title="Setup Time (minutes)",
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                except Exception:
                    st.info("Setup data available but chart cannot be displayed")

    elif "Meiste Produktion" in preset:
        if parts.empty:
            st.warning("No production events found.")
            show_sql("-- No data in part_events")
        else:
            sql = f"""
            SELECT name, COUNT(*) AS pieces
            FROM part_events
            WHERE time >= TIMESTAMP '{from_dt}' AND time < TIMESTAMP '{to_dt}'
            GROUP BY name
            ORDER BY pieces DESC
            """
            show_sql(sql)
            res = con.execute(sql).df()
            
            # Create Plotly bar chart
            if not res.empty:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=res["name"],
                    y=res["pieces"],
                    name='Production Count',
                    marker_color='green'
                ))
                
                fig.update_layout(
                    title="Production by Machine",
                    xaxis_title="Machine",
                    yaxis_title="Pieces Produced",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)

    elif "KPIs pro Schicht" in preset:
        if parts.empty and setups.empty:
            st.warning("Not enough data for shift KPIs.")
            show_sql("-- Uses computed tables part_events/setup_intervals in Python for shift mapping.")
        else:
            # Show SQL that explains the logic
            show_sql("""
-- KPI Calculation Logic (performed in Python/Pandas):
-- 1. Assign shifts based on Central European timezone:
--    06-14: Morning shift (6 AM - 2 PM)
--    14-22: Afternoon shift (2 PM - 10 PM) 
--    22-06: Night shift (10 PM - 6 AM)
-- 
-- 2. Calculate metrics per shift:
--    pieces: COUNT of part completion events
--    avg_ct_s: AVERAGE cycle time in seconds
--    setup_min: SUM of setup time in minutes
--
-- Equivalent SQL would be:
-- SELECT 
--   shift,
--   COUNT(*) as pieces,
--   AVG(cycle_time_s) as avg_ct_s,
--   SUM(setup_s)/60.0 as setup_min
-- FROM (
--   SELECT *,
--     CASE 
--       WHEN EXTRACT(HOUR FROM time AT TIME ZONE 'Europe/Central') BETWEEN 6 AND 13 THEN '06-14'
--       WHEN EXTRACT(HOUR FROM time AT TIME ZONE 'Europe/Central') BETWEEN 14 AND 21 THEN '14-22'
--       ELSE '22-06'
--     END as shift
--   FROM part_events
-- ) 
-- GROUP BY shift
-- ORDER BY shift;
            """)
            
            p = parts.copy()
            p["shift"] = assign_shift(p[TIMESTAMP_COL])
            k1 = p.groupby("shift")["cycle_time_s"].mean().rename("avg_ct_s")
            k2 = p.groupby("shift").size().rename("pieces")
            if not setups.empty:
                s = setups.copy()
                s["shift"] = assign_shift(s["start"])
                k3 = (s.groupby("shift")["setup_s"].sum()/60.0).rename("setup_min")
            else:
                k3 = pd.Series(dtype=float, name="setup_min")
            res = pd.concat([k2, k1, k3], axis=1)
            res = res.fillna(0.0).reindex(["06-14","14-22","22-06"])
            
            # Fix data types for Arrow compatibility - ensure integers for piece counts
            try:
                res_display = res.copy()
                # Convert pieces to integer, others to float
                res_display["pieces"] = res_display["pieces"].astype('int64')
                res_display["avg_ct_s"] = pd.to_numeric(res_display["avg_ct_s"], errors='coerce').astype('float64')
                res_display["setup_min"] = pd.to_numeric(res_display["setup_min"], errors='coerce').astype('float64')
                st.dataframe(res_display)
            except Exception as e:
                st.warning(f"Cannot display table due to data type issues: {str(e)}")
                # Show data as text instead
                st.write("**Shift KPIs Results:**")
                for shift_name in ["06-14", "14-22", "22-06"]:
                    if shift_name in res.index:
                        row = res.loc[shift_name]
                        st.write(f"**{shift_name}:** Pieces: {int(row['pieces'])}, Avg Cycle: {row['avg_ct_s']:.1f}s, Setup: {row['setup_min']:.1f}min")
            
            # Create Plotly bar chart for shift pieces
            if not res.empty:
                try:
                    fig = go.Figure()
                    # Convert data to simple arrays to avoid Arrow issues
                    x_data = list(res.index)
                    y_data = [int(x) for x in res["pieces"].values]  # Convert to int
                    
                    fig.add_trace(go.Bar(
                        x=x_data,
                        y=y_data,
                        name='Pieces per Shift',
                        marker_color='blue',
                        text=y_data,
                        textposition='auto'
                    ))
                    
                    fig.update_layout(
                        title="Production by Shift",
                        xaxis_title="Shift",
                        yaxis_title="Pieces Produced",
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Chart display error: {str(e)}")
                    st.info("Shift KPI data available but chart cannot be displayed")

# Free text handling
if intent and intent.get("intent"):
    if intent["intent"] == "avg_cycle_time":
        if parts.empty:
            st.warning("No part completion events detected.")
            show_sql("-- No data in part_events")
        else:
            sql = f"""
            SELECT AVG(cycle_time_s) AS avg_cycle_time_s
            FROM part_events
            WHERE time >= TIMESTAMP '{from_dt}' AND time < TIMESTAMP '{to_dt}'
            """
            show_sql(sql)
            res = con.execute(sql).df()
            st.metric("Average Cycle Time", f"{res['avg_cycle_time_s'].iloc[0]:.2f} s")
            if not parts.empty:
                try:
                    s = parts.set_index(TIMESTAMP_COL)["cycle_time_s"].rolling(20, min_periods=1).mean()
                    
                    # Create Plotly line chart for cycle time trend
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=s.index,
                        y=s.values,
                        mode='lines',
                        name='Rolling Average Cycle Time',
                        line=dict(color='red', width=2)
                    ))
                    
                    fig.update_layout(
                        title="Cycle Time Rolling Average (20 points)",
                        xaxis_title="Time",
                        yaxis_title="Cycle Time (s)",
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                except Exception:
                    st.info("Cycle time data available but chart cannot be displayed")

    elif intent["intent"] == "setup_time":
        if setups.empty:
            st.warning("No setup intervals detected.")
            show_sql("-- No data in setup_intervals")
        else:
            sql = f"""
            SELECT SUM(setup_s)/60.0 AS total_setup_min
            FROM setup_intervals
            WHERE start >= TIMESTAMP '{from_dt}' AND start < TIMESTAMP '{to_dt}'
            """
            show_sql(sql)
            res = con.execute(sql).df()
            st.metric("Total Setup Time", f"{res['total_setup_min'].iloc[0]:.1f} min")
            if not setups.empty:
                try:
                    s = setups.set_index("start")["setup_s"]
                    
                    # Create Plotly bar chart for setup times
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        x=s.index.strftime('%Y-%m-%d %H:%M:%S'),
                        y=s.values,
                        name='Setup Time (seconds)',
                        marker_color='orange'
                    ))
                    
                    fig.update_layout(
                        title="Setup Times",
                        xaxis_title="Time",
                        yaxis_title="Setup Time (s)",
                        height=400,
                        xaxis_tickangle=-45
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                except Exception:
                    st.info("Setup data available but chart cannot be displayed")

    elif intent["intent"] == "max_output":
        if parts.empty:
            st.warning("No production events found.")
            show_sql("-- No data in part_events")
        else:
            sql = f"""
            SELECT name, COUNT(*) AS pieces
            FROM part_events
            WHERE time >= TIMESTAMP '{from_dt}' AND time < TIMESTAMP '{to_dt}'
            GROUP BY name
            ORDER BY pieces DESC
            """
            show_sql(sql)
            res = con.execute(sql).df()
            
            # Create Plotly bar chart
            if not res.empty:
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=res["name"],
                    y=res["pieces"],
                    name='Production Count',
                    marker_color='green'
                ))
                
                fig.update_layout(
                    title="Production by Machine",
                    xaxis_title="Machine",
                    yaxis_title="Pieces Produced",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)

    elif intent["intent"] == "shift_kpis":
        if parts.empty and setups.empty:
            st.warning("Not enough data for shift KPIs.")
            show_sql("-- Uses computed tables part_events/setup_intervals in Python for shift mapping.")
        else:
            p = parts.copy()
            p["shift"] = assign_shift(p[TIMESTAMP_COL])
            k1 = p.groupby("shift")["cycle_time_s"].mean().rename("avg_ct_s")
            k2 = p.groupby("shift").size().rename("pieces")
            if not setups.empty:
                s = setups.copy()
                s["shift"] = assign_shift(s["start"])
                k3 = (s.groupby("shift")["setup_s"].sum()/60.0).rename("setup_min")
            else:
                k3 = pd.Series(dtype=float, name="setup_min")
    elif intent["intent"] == "shift_kpis":
        if parts.empty and setups.empty:
            st.warning("Not enough data for shift KPIs.")
            show_sql("-- Uses computed tables part_events/setup_intervals in Python for shift mapping.")
        else:
            # Show SQL that explains the logic
            show_sql("""
-- KPI Calculation Logic (performed in Python/Pandas):
-- 1. Assign shifts based on Central European timezone:
--    06-14: Morning shift (6 AM - 2 PM)
--    14-22: Afternoon shift (2 PM - 10 PM) 
--    22-06: Night shift (10 PM - 6 AM)
-- 
-- 2. Calculate metrics per shift:
--    pieces: COUNT of part completion events
--    avg_ct_s: AVERAGE cycle time in seconds
--    setup_min: SUM of setup time in minutes
--
-- Equivalent SQL would be:
-- SELECT 
--   shift,
--   COUNT(*) as pieces,
--   AVG(cycle_time_s) as avg_ct_s,
--   SUM(setup_s)/60.0 as setup_min
-- FROM (
--   SELECT *,
--     CASE 
--       WHEN EXTRACT(HOUR FROM time AT TIME ZONE 'Europe/Central') BETWEEN 6 AND 13 THEN '06-14'
--       WHEN EXTRACT(HOUR FROM time AT TIME ZONE 'Europe/Central') BETWEEN 14 AND 21 THEN '14-22'
--       ELSE '22-06'
--     END as shift
--   FROM part_events
-- ) 
-- GROUP BY shift
-- ORDER BY shift;
            """)
            
            p = parts.copy()
            p["shift"] = assign_shift(p[TIMESTAMP_COL])
            k1 = p.groupby("shift")["cycle_time_s"].mean().rename("avg_ct_s")
            k2 = p.groupby("shift").size().rename("pieces")
            if not setups.empty:
                s = setups.copy()
                s["shift"] = assign_shift(s["start"])
                k3 = (s.groupby("shift")["setup_s"].sum()/60.0).rename("setup_min")
            else:
                k3 = pd.Series(dtype=float, name="setup_min")
            res = pd.concat([k2, k1, k3], axis=1)
            res = res.fillna(0.0).reindex(["06-14","14-22","22-06"])
            
            # Fix data types for Arrow compatibility - ensure integers for piece counts
            try:
                res_display = res.copy()
                # Convert pieces to integer, others to float
                res_display["pieces"] = res_display["pieces"].astype('int64')
                res_display["avg_ct_s"] = pd.to_numeric(res_display["avg_ct_s"], errors='coerce').astype('float64')
                res_display["setup_min"] = pd.to_numeric(res_display["setup_min"], errors='coerce').astype('float64')
                st.dataframe(res_display)
            except Exception as e:
                st.warning(f"Cannot display table due to data type issues: {str(e)}")
                # Show data as text instead
                st.write("**Shift KPIs Results:**")
                for shift_name in ["06-14", "14-22", "22-06"]:
                    if shift_name in res.index:
                        row = res.loc[shift_name]
                        st.write(f"**{shift_name}:** Pieces: {int(row['pieces'])}, Avg Cycle: {row['avg_ct_s']:.1f}s, Setup: {row['setup_min']:.1f}min")
            
            # Create Plotly bar chart for shift pieces
            if not res.empty:
                try:
                    fig = go.Figure()
                    # Convert data to simple arrays to avoid Arrow issues
                    x_data = list(res.index)
                    y_data = [int(x) for x in res["pieces"].values]  # Convert to int
                    
                    fig.add_trace(go.Bar(
                        x=x_data,
                        y=y_data,
                        name='Pieces per Shift',
                        marker_color='blue',
                        text=y_data,
                        textposition='auto'
                    ))
                    
                    fig.update_layout(
                        title="Production by Shift",
                        xaxis_title="Shift",
                        yaxis_title="Pieces Produced",
                        height=400
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Chart display error: {str(e)}")
                    st.info("Shift KPI data available but chart cannot be displayed")

# Footer
with st.expander("Raw telemetry preview"):
    try:
        # Fix data types for display
        display_df = df_f.head(100).copy()
        # Ensure all columns are properly typed for Arrow compatibility
        for col in display_df.columns:
            if col == MACHINE_COL:
                # Machine names should be strings
                display_df[col] = display_df[col].astype(str)
            elif col == TIMESTAMP_COL:
                # Convert datetime to string for display
                display_df[col] = display_df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
            elif display_df[col].dtype == 'object':
                # Try to convert to numeric first, then fallback to string
                numeric_series = pd.to_numeric(display_df[col], errors='coerce')
                if not numeric_series.isna().all():
                    display_df[col] = numeric_series.astype('float64')
                else:
                    display_df[col] = display_df[col].astype(str)
            elif pd.api.types.is_numeric_dtype(display_df[col]):
                # Convert all numeric types to float64 to avoid Arrow issues
                display_df[col] = pd.to_numeric(display_df[col], errors='coerce').astype('float64')
            elif pd.api.types.is_datetime64_any_dtype(display_df[col]):
                # Convert datetime to string
                display_df[col] = display_df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
        st.dataframe(display_df)
    except Exception as e:
        st.error(f"Error displaying data preview: {str(e)}")
        st.info("Data loaded successfully but cannot be displayed due to formatting issues.")
        # Show basic info instead
        st.write(f"**Data Shape:** {df_f.shape}")
        st.write(f"**Columns:** {', '.join(df_f.columns[:10])}{'...' if len(df_f.columns) > 10 else ''}")
        
        # Show data types info
        st.write("**Column Types:**")
        for i, col in enumerate(df_f.columns[:10]):
            st.text(f"{col}: {df_f[col].dtype}")
        if len(df_f.columns) > 10:
            st.text("...")
