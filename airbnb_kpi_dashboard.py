"""
Streamlit dashboard: fundamental KPIs for NYC Airbnb listings (Excel export).
Looks for airbnb.xlsx or airbnd.xlsx in ~/Downloads by default.
"""

from __future__ import annotations

from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st


def _default_excel_paths() -> list[Path]:
    d = Path.home() / "Downloads"
    return [d / "airbnb.xlsx", d / "airbnd.xlsx"]


@st.cache_data(show_spinner=False)
def load_listings(path_str: str) -> pd.DataFrame:
    df = pd.read_excel(path_str, sheet_name=0, engine="openpyxl")
    df.columns = df.columns.astype(str).str.strip()
    return df


def main() -> None:
    st.set_page_config(page_title="Airbnb NYC KPIs", layout="wide")
    st.title("Airbnb NYC — KPI dashboard")
    st.caption("Data from your Excel export (`airbnb.xlsx` / `airbnd.xlsx` in Downloads).")

    with st.sidebar:
        st.header("Data source")
        candidates = _default_excel_paths()
        found = [p for p in candidates if p.is_file()]
        custom = st.text_input(
            "Or path to .xlsx",
            value=str(found[0]) if found else "",
            help="Full path if the file is not in Downloads or uses another name.",
        )
        path = Path(custom.strip()).expanduser() if custom.strip() else None
        if path is None or not path.is_file():
            for p in found:
                path = p
                break

        if path is None or not path.is_file():
            st.error("No workbook found. Set the path above or place `airbnb.xlsx` in Downloads.")
            st.stop()

        st.success(f"Using: `{path}`")

        st.header("Filters")
        load_btn = st.button("Reload data", help="Clear cache and re-read the file.")

    if load_btn:
        st.cache_data.clear()
        st.rerun()

    try:
        df = load_listings(str(path))
    except Exception as e:
        st.error(f"Could not read workbook: {e}")
        st.stop()

    # Expected columns from Airbnb_NYC sheet
    nb_col = "Neighbourhood" if "Neighbourhood" in df.columns else None
    room_col = "Room Type" if "Room Type" in df.columns else None

    with st.sidebar:
        boroughs = sorted(df[nb_col].dropna().unique().tolist()) if nb_col else []
        selected_boroughs = (
            st.multiselect("Borough", boroughs, default=boroughs) if boroughs else []
        )
        rooms = sorted(df[room_col].dropna().unique().tolist()) if room_col else []
        selected_rooms = st.multiselect("Room type", rooms, default=rooms) if rooms else []

    filtered = df
    if nb_col and selected_boroughs:
        filtered = filtered[filtered[nb_col].isin(selected_boroughs)]
    if room_col and selected_rooms:
        filtered = filtered[filtered[room_col].isin(selected_rooms)]

    n = len(filtered)
    if n == 0:
        st.warning("No rows match the current filters.")
        st.stop()

    price = filtered["Price"] if "Price" in filtered.columns else pd.Series(dtype=float)
    reviews = (
        filtered["Number Of Reviews"]
        if "Number Of Reviews" in filtered.columns
        else pd.Series(dtype=int)
    )
    score = (
        filtered["Review Scores Rating"]
        if "Review Scores Rating" in filtered.columns
        else pd.Series(dtype=float)
    )
    beds = filtered["Beds"] if "Beds" in filtered.columns else pd.Series(dtype=float)
    host_col = "Host Id" if "Host Id" in filtered.columns else None

    median_p = float(price.median()) if len(price) else float("nan")
    mean_p = float(price.mean()) if len(price) else float("nan")
    total_reviews = int(reviews.sum()) if len(reviews) else 0
    avg_reviews = float(reviews.mean()) if len(reviews) else float("nan")
    scored = score.dropna()
    avg_score = float(scored.mean()) if len(scored) else float("nan")
    pct_scored = 100.0 * len(scored) / n if n else 0.0
    unique_hosts = int(filtered[host_col].nunique()) if host_col else None
    avg_beds = float(beds.dropna().mean()) if len(beds.dropna()) else float("nan")

    st.subheader("Key metrics")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Listings", f"{n:,}")
    c2.metric("Median price / night", f"${median_p:,.0f}" if median_p == median_p else "—")
    c3.metric("Mean price / night", f"${mean_p:,.0f}" if mean_p == mean_p else "—")
    c4.metric("Total reviews", f"{total_reviews:,}")
    c5.metric("Avg reviews / listing", f"{avg_reviews:.1f}" if avg_reviews == avg_reviews else "—")

    c6, c7, c8, c9 = st.columns(4)
    c6.metric("Avg review score", f"{avg_score:.1f}" if avg_score == avg_score else "—")
    c7.metric("Listings with score", f"{pct_scored:.0f}%")
    if unique_hosts is not None:
        c8.metric("Unique hosts", f"{unique_hosts:,}")
    else:
        c8.metric("Unique hosts", "—")
    c9.metric("Avg beds (where known)", f"{avg_beds:.2f}" if avg_beds == avg_beds else "—")

    st.subheader("Breakdowns")
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("**Listings by borough**")
        if nb_col:
            b = (
                filtered.groupby(nb_col, dropna=False)
                .size()
                .reset_index(name="listings")
                .sort_values("listings", ascending=False)
            )
            chart_b = (
                alt.Chart(b)
                .mark_bar()
                .encode(
                    x=alt.X("listings:Q", title="Listings"),
                    y=alt.Y(f"{nb_col}:N", sort="-x", title=None),
                    tooltip=[nb_col, "listings"],
                )
                .properties(height=220)
            )
            st.altair_chart(chart_b, use_container_width=True)
        else:
            st.info("No borough column found.")

    with col_b:
        st.markdown("**Listings by room type**")
        if room_col:
            r = (
                filtered.groupby(room_col, dropna=False)
                .size()
                .reset_index(name="listings")
                .sort_values("listings", ascending=False)
            )
            chart_r = (
                alt.Chart(r)
                .mark_arc(innerRadius=50)
                .encode(
                    theta=alt.Theta("listings:Q", title="Listings"),
                    color=alt.Color(f"{room_col}:N", title="Room type"),
                    tooltip=[room_col, "listings"],
                )
                .properties(height=260)
            )
            st.altair_chart(chart_r, use_container_width=True)
        else:
            st.info("No room type column found.")

    st.markdown("**Median price by borough**")
    if nb_col and len(price):
        med_by = (
            filtered.assign(_price=price)
            .groupby(nb_col, dropna=False)["_price"]
            .median()
            .reset_index(name="median_price")
            .sort_values("median_price", ascending=False)
        )
        chart_m = (
            alt.Chart(med_by)
            .mark_bar()
            .encode(
                x=alt.X("median_price:Q", title="Median price ($)"),
                y=alt.Y(f"{nb_col}:N", sort="-x", title=None),
                tooltip=[nb_col, alt.Tooltip("median_price:Q", format=",.0f", title="Median $")],
            )
            .properties(height=220)
        )
        st.altair_chart(chart_m, use_container_width=True)

    with st.expander("Sample rows"):
        st.dataframe(filtered.head(50), use_container_width=True)


if __name__ == "__main__":
    main()
