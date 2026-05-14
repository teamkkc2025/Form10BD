import streamlit as st
import pandas as pd
import re
from io import BytesIO

# ✅ Must be first
st.set_page_config(
    page_title="Form 10BD | Data Cleaner",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #F4F7F0; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

.navbar {
    background: #2D4A1E; padding: 0 48px; height: 64px;
    display: flex; align-items: center; justify-content: space-between;
    position: sticky; top: 0; z-index: 999;
    box-shadow: 0 2px 12px rgba(0,0,0,0.20);
}
.navbar-brand { display: flex; align-items: center; gap: 14px; }
.navbar-logo-box {
    width: 38px; height: 38px; background: #7cb452; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 19px; font-weight: 700; color: #fff;
    font-family: 'DM Mono', monospace; box-shadow: 0 2px 8px rgba(124,180,82,0.4);
}
.navbar-title    { color: #FFFFFF; font-size: 17px; font-weight: 600; }
.navbar-subtitle { color: #9DC878; font-size: 12px; font-weight: 400; letter-spacing: 0.5px; text-transform: uppercase; }
.navbar-badge    { background: #7cb452; color: #fff; font-size: 11px; font-weight: 600; padding: 4px 14px; border-radius: 20px; }

.page-body { padding: 40px 48px 60px 48px; }

.section-label  { font-size: 11px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; color: #5a9a30; margin-bottom: 8px; }
.section-title  { font-size: 26px; font-weight: 600; color: #1E3510; margin-bottom: 4px; }
.section-desc   { font-size: 14px; color: #6B7A60; margin-bottom: 28px; }

.info-box {
    background: #EFF6E8; border: 1px solid #B8D99A; border-radius: 10px;
    padding: 14px 20px; font-size: 13px; color: #2D4A1E; margin-bottom: 24px; line-height: 1.7;
}

.stats-row { display: flex; gap: 16px; margin-bottom: 28px; flex-wrap: wrap; }
.stat-card {
    background: #fff; border-radius: 12px; padding: 20px 26px;
    flex: 1; min-width: 150px; border: 1px solid #D8E8CC;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.stat-label  { font-size: 11px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase; color: #9DB890; margin-bottom: 6px; }
.stat-value  { font-size: 30px; font-weight: 600; font-family: 'DM Mono', monospace; line-height: 1; color: #1E3510; }
.stat-value.green  { color: #7cb452; }
.stat-value.dgreen { color: #4A8A20; }
.stat-value.orange { color: #D4831E; }
.stat-value.red    { color: #C94040; }

.upload-card {
    background: #fff; border: 2px dashed #B8D99A; border-radius: 16px;
    padding: 52px 32px; text-align: center;
}
.upload-icon  { font-size: 44px; margin-bottom: 12px; }
.upload-title { font-size: 17px; font-weight: 600; color: #1E3510; margin-bottom: 6px; }
.upload-hint  { font-size: 13px; color: #9DB890; }

.stButton > button {
    background: #7cb452 !important; color: #fff !important;
    border: none !important; border-radius: 10px !important; padding: 14px 40px !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 15px !important; font-weight: 600 !important;
    box-shadow: 0 4px 14px rgba(124,180,82,0.35) !important; width: 100% !important;
}
.stButton > button:hover { background: #5f9a36 !important; }

[data-testid="stDownloadButton"] > button {
    background: #4A8A20 !important; color: #fff !important;
    border: none !important; border-radius: 10px !important; padding: 14px 40px !important;
    font-family: 'DM Sans', sans-serif !important; font-size: 15px !important; font-weight: 600 !important;
    box-shadow: 0 4px 14px rgba(74,138,32,0.30) !important; width: 100% !important;
}
[data-testid="stDownloadButton"] > button:hover { background: #3A6E18 !important; }

[data-testid="stDataFrame"] {
    border-radius: 12px !important; overflow: hidden !important;
    border: 1px solid #D8E8CC !important; box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
}

.stSuccess > div { background: #EFF6E8 !important; border-left: 4px solid #7cb452 !important; border-radius: 8px !important; color: #1E3510 !important; }
.stError   > div { background: #FDECEA !important; border-left: 4px solid #C94040 !important; border-radius: 8px !important; }
.stInfo    > div { background: #EFF6E8 !important; border-left: 4px solid #5a9a30 !important; border-radius: 8px !important; color: #2D4A1E !important; }

.divider { height: 1px; background: #D8E8CC; margin: 28px 0; }

.results-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; }
.results-title  { font-size: 18px; font-weight: 600; color: #1E3510; }
.results-count  { font-size: 13px; color: #6B7A60; background: #EFF6E8; border-radius: 20px; padding: 4px 14px; font-family: 'DM Mono', monospace; }

.export-box {
    background: #EFF6E8; border: 1px solid #B8D99A; border-radius: 10px;
    padding: 16px 20px; font-size: 13px; color: #2D4A1E; line-height: 2;
}
.col-info-box {
    background: #fff; border: 1px solid #D8E8CC; border-radius: 12px;
    padding: 20px; font-size: 13px; color: #3A4A30; line-height: 2.3;
}

.footer {
    background: #2D4A1E; padding: 20px 48px;
    display: flex; align-items: center; justify-content: space-between; margin-top: 60px;
}
.footer-text  { color: #6A8A58; font-size: 13px; }
.footer-brand { color: #9DC878; font-size: 13px; font-weight: 500; }

[data-testid="column"] { padding: 0 8px !important; }
</style>
""", unsafe_allow_html=True)


# ============================================================
#  HELPER — safe string coercion
# ============================================================
def to_str(val):
    """Convert any value to a clean string, handling NaN/None/NaT."""
    if val is None:
        return ''
    s = str(val).strip()
    return '' if s.lower() in ('nan', 'none', 'nat', 'n/a', 'na') else s


# ============================================================
#  CLEANING
# ============================================================
def strip_all_special(val):
    """Keep ONLY letters, digits, and spaces. Remove everything else."""
    s = to_str(val)
    return re.sub(r'[^A-Za-z0-9 ]', '', s).strip()


def clean_uid_str(val):
    """Keep only alphanumeric characters from a UID value."""
    s = to_str(val)
    return re.sub(r'[^A-Za-z0-9]', '', s)


def format_date(val):
    s = to_str(val)
    if s == '':
        return ''
    try:
        parsed = pd.to_datetime(val, errors='coerce')
        return '' if pd.isna(parsed) else parsed.strftime('%d-%b-%Y')
    except Exception:
        return ''


def convert_amount(val):
    s = to_str(val)
    if s == '':
        return ''
    try:
        return int(float(s.replace(',', '')))
    except Exception:
        return s


# ============================================================
#  UID VALIDATION  (returns three plain Python strings)
# ============================================================
def validate_uid_row(row):
    uid_raw  = row.get('Unique Identification Number', '')
    id_code  = to_str(row.get('ID Code', '')).title()
    uid_s    = to_str(uid_raw)

    # Missing UID
    if uid_s == '' or uid_s.lower() in ('not available',):
        return 'Permanent Account Number', 'NNNNN0000N', 'Filled default PAN for missing UID'

    uid_clean    = clean_uid_str(uid_s)
    correct_code = id_code
    is_valid     = False
    change       = ''

    if uid_clean.isdigit() and len(uid_clean) == 12:
        correct_code = 'Aadhaar Number'
        is_valid     = True
        # Keep as STRING — we handle int conversion only inside Excel export
        # This avoids the dtype crash on pandas 3.x

    elif re.fullmatch(r'[A-Za-z]{5}[0-9]{4}[A-Za-z]', uid_clean):
        correct_code = 'Permanent Account Number'
        is_valid     = True
        uid_clean    = uid_clean.upper()

    elif re.fullmatch(r'[A-Za-z0-9]{8,10}', uid_clean):
        correct_code = 'Passport Number'
        is_valid     = True

    elif re.fullmatch(r'[A-Za-z]{2}[0-9]{11,13}', uid_clean):
        correct_code = 'Driving Licence'
        is_valid     = True

    if not is_valid:
        change = 'Invalid UID Format - Needs Review'
    elif id_code != correct_code:
        change = 'ID Code mismatch'
    elif uid_s != uid_clean:
        change = 'Formatted UID'

    # Always return strings — never int — to avoid pandas dtype conflict
    return correct_code, str(uid_clean), change


# ============================================================
#  MAIN PROCESSOR
# ============================================================
def process_dataframe(raw_df: pd.DataFrame) -> pd.DataFrame:
    df = raw_df.copy()
    df.columns = [str(c).strip() for c in df.columns]

    for col in ['ID Code', 'Unique Identification Number']:
        if col not in df.columns:
            st.error(f"Missing required column: **{col}**")
            st.stop()

    # ── 1. UID validation — collect results as plain Python lists ──
    id_codes, uid_values, change_notes = [], [], []
    for _, row in df.iterrows():
        ic, uid, ch = validate_uid_row(row)
        id_codes.append(ic)
        uid_values.append(uid)      # always str
        change_notes.append(ch)

    # Assign as new object-dtype columns — no dtype conflict
    df['ID Code']                       = id_codes
    df['Unique Identification Number']  = uid_values
    df['Change Note']                   = change_notes

    # ── 2. Format dates ──
    date_col = 'Date of Issuance of Unique Registration Number'
    if date_col in df.columns:
        df[date_col] = df[date_col].apply(format_date)

    # ── 3. Convert amounts ──
    amt_col = 'Amount of donation (Indian rupees)'
    if amt_col in df.columns:
        df[amt_col] = df[amt_col].apply(convert_amount)

    # ── 4. Strip ALL special characters from every remaining text column ──
    protected = {
        'Unique Identification Number',
        'ID Code',
        'Change Note',
        date_col,
        amt_col,
    }
    for col in df.columns:
        if col not in protected:
            df[col] = df[col].apply(strip_all_special)

    return df


# ============================================================
#  EXCEL EXPORT  — dtype-safe
# ============================================================
def to_excel_bytes(df: pd.DataFrame) -> bytes:
    output = BytesIO()

    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Work on a plain copy; write everything as-is first
        export = df.copy()

        # Convert Aadhaar UIDs (12-digit strings) to int ONLY in the
        # export copy, using a list comprehension — no .at[] or .loc[]
        def uid_to_excel_val(val):
            s = str(val).strip()
            if s.isdigit() and len(s) == 12:
                return int(s)
            return val

        aadhaar_converted = [uid_to_excel_val(v)
                             for v in export['Unique Identification Number']]

        # Write sheet without UID column first, then add it manually
        export.to_excel(writer, sheet_name='CleanedData',
                        index=False, startrow=1, header=False)

        wb  = writer.book
        ws  = writer.sheets['CleanedData']

        # Header row — styled
        hdr_fmt = wb.add_format({
            'bold': True, 'bg_color': '#2D4A1E', 'font_color': '#FFFFFF',
            'font_name': 'Calibri', 'font_size': 10, 'border': 0,
        })
        for c, name in enumerate(export.columns):
            ws.write(0, c, name, hdr_fmt)

        # Overwrite the UID column with properly-typed values
        uid_col_idx = export.columns.get_loc('Unique Identification Number')
        num_fmt     = wb.add_format({'num_format': '0'})
        txt_fmt     = wb.add_format()

        for r, val in enumerate(aadhaar_converted, start=1):
            if isinstance(val, int):
                ws.write_number(r, uid_col_idx, val, num_fmt)
            else:
                ws.write(r, uid_col_idx, str(val), txt_fmt)

    output.seek(0)
    return output.read()


# ============================================================
#  NAVBAR
# ============================================================
st.markdown("""
<div class="navbar">
    <div class="navbar-brand">
        <div class="navbar-logo-box">K</div>
        <div>
            <div class="navbar-title">KKC &amp; Associates LLP</div>
            <div class="navbar-subtitle">Form 10BD Data Cleaner</div>
        </div>
    </div>
    <div class="navbar-badge">IT Tool v2.0</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
#  PAGE BODY
# ============================================================
st.markdown('<div class="page-body">', unsafe_allow_html=True)

st.markdown("""
<div class="section-label">Compliance Tool</div>
<div class="section-title">Form 10BD Data Cleaner</div>
<div class="section-desc">
    Upload your donor data Excel file. The tool validates all UIDs, corrects ID codes,
    strips every special character from every column, and exports a clean filing-ready sheet.
</div>
<div class="info-box">
    <strong>Cleaning rules applied to ALL columns:</strong> &nbsp;
    Only letters (A-Z), digits (0-9) and spaces are kept —
    commas, periods, hyphens, slashes, brackets, currency symbols and all other
    special characters are removed &nbsp;·&nbsp;
    Aadhaar / PAN / Passport / Driving Licence validated &nbsp;·&nbsp;
    Dates formatted DD-Mon-YYYY &nbsp;·&nbsp; Amounts converted to integers.
</div>
""", unsafe_allow_html=True)

# ---- Upload Row ----
col_up, col_info = st.columns([2, 1], gap="large")

with col_up:
    st.markdown('<div class="section-label">Step 1 — Upload File</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Drop your Form 10BD Excel file here",
        type=["xlsx"],
        label_visibility="collapsed"
    )

with col_info:
    st.markdown("""
    <div class="section-label">Expected Columns</div>
    <div class="col-info-box">
        ✦ &nbsp;<b>ID Code</b><br>
        ✦ &nbsp;<b>Unique Identification Number</b><br>
        ✦ &nbsp;Name of donor<br>
        ✦ &nbsp;Address of donor<br>
        ✦ &nbsp;Date of Issuance of Unique Registration Number<br>
        ✦ &nbsp;Amount of donation (Indian rupees)<br>
        ✦ &nbsp;Mode of receipt &nbsp;/&nbsp; Donation Type
    </div>
    """, unsafe_allow_html=True)

# ============================================================
#  MAIN LOGIC
# ============================================================
if uploaded_file is not None:
    try:
        raw_df     = pd.read_excel(uploaded_file)
        total_rows = len(raw_df)
        total_cols = len(raw_df.columns)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Step 2 — Preview &amp; Process</div>',
                    unsafe_allow_html=True)

        st.markdown(f"""
        <div class="stats-row">
            <div class="stat-card">
                <div class="stat-label">Total Rows</div>
                <div class="stat-value green">{total_rows:,}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Columns Detected</div>
                <div class="stat-value">{total_cols}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Uploaded File</div>
                <div class="stat-value"
                     style="font-size:13px;padding-top:6px;
                            font-family:'DM Sans',sans-serif;color:#7cb452;">
                    {uploaded_file.name}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_btn, _ = st.columns([1, 1], gap="large")
        with col_btn:
            process_clicked = st.button("⚙️  Process & Clean Data", use_container_width=True)

        if process_clicked:
            with st.spinner("Cleaning data — removing all special characters…"):
                processed_df = process_dataframe(raw_df)
            st.session_state["processed_df"] = processed_df
            st.session_state["file_name"]    = uploaded_file.name
            st.session_state["total_rows"]   = total_rows

        if ("processed_df" in st.session_state and
                st.session_state.get("file_name") == uploaded_file.name):

            processed_df = st.session_state["processed_df"]
            t_rows       = st.session_state["total_rows"]
            change_col   = 'Change Note' if 'Change Note' in processed_df.columns else None
            flagged      = int((processed_df[change_col] != '').sum()) if change_col else 0
            invalid      = int(processed_df[change_col]
                               .str.contains('Invalid', na=False).sum()) if change_col else 0
            clean_rows   = t_rows - flagged

            st.markdown(f"""
            <div class="stats-row">
                <div class="stat-card">
                    <div class="stat-label">Clean Records</div>
                    <div class="stat-value dgreen">{clean_rows:,}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Flagged / Corrected</div>
                    <div class="stat-value orange">{flagged:,}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Needs Manual Review</div>
                    <div class="stat-value red">{invalid:,}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Total Processed</div>
                    <div class="stat-value green">{t_rows:,}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.success(
                f"✅  {t_rows:,} records processed — "
                "all special characters removed from every column."
            )

            # ── Export ──
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Step 3 — Export</div>',
                        unsafe_allow_html=True)

            col_dl1, col_dl2 = st.columns([1, 1], gap="large")
            with col_dl1:
                excel_bytes = to_excel_bytes(processed_df)
                st.download_button(
                    label="📥  Download Cleaned Excel File",
                    data=excel_bytes,
                    file_name="Form10BD_Cleaned.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            with col_dl2:
                st.markdown("""
                <div class="export-box">
                    <b>What is inside the export:</b><br>
                    ✔ &nbsp;All special characters removed from every column<br>
                    ✔ &nbsp;Validated and corrected UID numbers<br>
                    ✔ &nbsp;Corrected ID code labels<br>
                    ✔ &nbsp;Dates formatted as DD-Mon-YYYY<br>
                    ✔ &nbsp;Change notes column for full audit trail
                </div>
                """, unsafe_allow_html=True)

            # ── Data Table ──
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="results-header">
                <div class="results-title">Cleaned Data Preview</div>
                <div class="results-count">{len(processed_df):,} records</div>
            </div>
            """, unsafe_allow_html=True)

            f_col, _ = st.columns([1, 3], gap="large")
            with f_col:
                show_filter = st.selectbox(
                    "Filter",
                    ["All Records", "Flagged / Corrected Only", "Needs Review Only"],
                    label_visibility="collapsed"
                )

            display_df = processed_df.copy()
            if show_filter == "Flagged / Corrected Only" and change_col:
                display_df = display_df[display_df[change_col] != '']
            elif show_filter == "Needs Review Only" and change_col:
                display_df = display_df[
                    display_df[change_col].str.contains('Invalid', na=False)
                ]

            st.dataframe(display_df, use_container_width=True, height=500)

    except Exception as e:
        st.error(f"❌  Error: {str(e)}")
        st.exception(e)

else:
    for k in ["processed_df", "file_name", "total_rows"]:
        st.session_state.pop(k, None)

    st.markdown("""
    <div class="upload-card">
        <div class="upload-icon">📂</div>
        <div class="upload-title">No file uploaded yet</div>
        <div class="upload-hint">
            Use the uploader above to select your Form 10BD Excel file (.xlsx)
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
#  FOOTER
# ============================================================
st.markdown("""
<div class="footer">
    <div class="footer-text">© 2025 KKC &amp; Associates LLP · All rights reserved</div>
    <div class="footer-brand">Designed by IT Team &nbsp;·&nbsp; Form 10BD Compliance Suite</div>
</div>
""", unsafe_allow_html=True)
