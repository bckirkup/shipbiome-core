"""
Shipbiome — Streamlit UI for exploring shipboard microbiome simulation and source tracking.

Run from this folder:
    streamlit run shipbiome_app.py
"""

from __future__ import annotations

import csv
import io
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pypdf import PdfReader

from shipbiome_design import (
    DirichletMultinomialSimulator,
    FEASTEstimator,
    SourceProfiles,
    default_public_profiles_path,
)

APP_DIR = Path(__file__).resolve().parent
FRAMEWORK_PDF = APP_DIR / "kosmos_Maritime_Biodefense_Microbiome_Research_Framework.pdf"
SOURCE_LABELS = {
    "Human": "Human (skin-associated)",
    "Seawater": "Seawater",
    "Urban": "Urban surfaces",
    "Industrial": "Industrial / ship systems",
}


@st.cache_resource
def get_profiles() -> SourceProfiles:
    return SourceProfiles()


@st.cache_resource
def get_simulator() -> DirichletMultinomialSimulator:
    return DirichletMultinomialSimulator(get_profiles())


@st.cache_resource
def get_feast() -> FEASTEstimator:
    return FEASTEstimator(get_profiles())


def read_framework_pdf_bytes() -> Optional[bytes]:
    if not FRAMEWORK_PDF.is_file():
        return None
    return FRAMEWORK_PDF.read_bytes()


def extract_framework_text(max_pages: int = 8, max_chars: int = 12000) -> str:
    if not FRAMEWORK_PDF.is_file():
        return ""
    reader = PdfReader(str(FRAMEWORK_PDF))
    parts: List[str] = []
    for i, page in enumerate(reader.pages[:max_pages]):
        t = page.extract_text() or ""
        parts.append(f"--- Page {i + 1} ---\n{t}")
    text = "\n\n".join(parts)
    if len(text) > max_chars:
        text = text[:max_chars] + "\n\n… (truncated)"
    return text


def guess_framework_headings(text: str, limit: int = 12) -> List[str]:
    """Heuristic lines that look like PDF headings (for sidebar context)."""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    candidates: List[str] = []
    for ln in lines:
        if len(ln) > 80:
            continue
        if re.match(r"^\d+[\.)]\s+\S", ln):
            candidates.append(ln)
            continue
        letters = sum(c.isalpha() for c in ln)
        if letters >= 4 and letters / max(len(ln), 1) > 0.55 and ln.upper() == ln and not ln.isdigit():
            candidates.append(ln)
    seen = set()
    out: List[str] = []
    for c in candidates:
        key = c.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(c)
        if len(out) >= limit:
            break
    return out


def normalized_proportions(
    weights: Dict[str, float], source_order: List[str]
) -> Dict[str, float]:
    raw = {s: max(0.0, float(weights.get(s, 0.0))) for s in source_order}
    total = sum(raw.values())
    if total <= 0:
        return {s: 1.0 / len(source_order) for s in source_order}
    return {s: raw[s] / total for s in source_order}


def init_session() -> None:
    defaults = {
        "w_human": 40,
        "w_seawater": 25,
        "w_urban": 20,
        "w_industrial": 15,
        "total_reads": 10000,
        "seed": 42,
        "concentration": 100.0,
        "sample": None,
        "true_props": None,
        "estimated": None,
        "include_unknown": True,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def counts_to_csv(sample: Dict[str, int]) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["taxon", "reads"])
    for taxon in sorted(sample.keys()):
        w.writerow([taxon, sample[taxon]])
    return buf.getvalue()


def proportions_to_csv(rows: List[Tuple[str, float, float]]) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["source", "true_proportion", "estimated_proportion"])
    for name, true_p, est_p in rows:
        w.writerow([name, f"{true_p:.6f}", f"{est_p:.6f}"])
    return buf.getvalue()


def main() -> None:
    st.set_page_config(
        page_title="Shipbiome explorer",
        page_icon=None,
        layout="wide",
    )
    init_session()

    profiles = get_profiles()
    simulator = get_simulator()
    feast = get_feast()
    source_order = list(profiles.source_names)

    st.title("Shipbiome explorer")
    st.markdown(
        "Explore **synthetic shipboard microbiome mixtures** built from published source profiles, "
        "then see how **source tracking** estimates which environments contributed. "
        "This is an educational simulator—not a clinical or operational decision tool."
    )

    with st.sidebar:
        st.header("Research framework")
        pdf_bytes = read_framework_pdf_bytes()
        if pdf_bytes:
            st.download_button(
                label="Download framework (PDF)",
                data=pdf_bytes,
                file_name=FRAMEWORK_PDF.name,
                mime="application/pdf",
            )
        else:
            st.warning(
                f"Framework PDF not found at:\n`{FRAMEWORK_PDF}`"
            )

        excerpt = extract_framework_text()
        if excerpt:
            headings = guess_framework_headings(excerpt)
            if headings:
                st.subheader("Topics detected in the PDF (preview)")
                for h in headings[:8]:
                    st.caption(h)
            with st.expander("Framework text preview (first pages)"):
                st.text(excerpt)

        st.divider()
        st.checkbox(
            "Include “Unknown” source in estimates",
            key="include_unknown",
        )

    tab_sim, tab_track, tab_export = st.tabs(
        ["1. Simulate a mixture", "2. Source tracking", "3. Export results"]
    )

    with tab_sim:
        st.markdown(
            "Set **relative weights** for each environment; they are scaled to sum to 100% when you generate a sample."
        )
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.slider(
                SOURCE_LABELS["Human"], 0, 100, key="w_human"
            )
        with c2:
            st.slider(
                SOURCE_LABELS["Seawater"], 0, 100, key="w_seawater"
            )
        with c3:
            st.slider(
                SOURCE_LABELS["Urban"], 0, 100, key="w_urban"
            )
        with c4:
            st.slider(
                SOURCE_LABELS["Industrial"], 0, 100, key="w_industrial"
            )

        r1, r2, r3 = st.columns(3)
        with r1:
            st.number_input(
                "Total simulated reads",
                min_value=1000,
                max_value=500_000,
                step=1000,
                key="total_reads",
            )
        with r2:
            st.number_input(
                "Random seed",
                min_value=0,
                max_value=2_147_483_647,
                step=1,
                key="seed",
            )
        with r3:
            st.number_input(
                "Dirichlet concentration (dispersion)",
                min_value=1.0,
                max_value=5000.0,
                step=10.0,
                key="concentration",
                help="Higher values = less random spread around the mixture.",
            )

        weights = {
            "Human": st.session_state["w_human"],
            "Seawater": st.session_state["w_seawater"],
            "Urban": st.session_state["w_urban"],
            "Industrial": st.session_state["w_industrial"],
        }
        props = normalized_proportions(weights, source_order)
        st.caption(
            "Normalized mixture: "
            + ", ".join(f"{SOURCE_LABELS.get(s, s)}={props[s]*100:.1f}%" for s in source_order)
        )

        if st.button("Generate sample", type="primary"):
            simulator.concentration_param = float(st.session_state["concentration"])
            sample = simulator.generate_sample(
                props,
                total_reads=int(st.session_state["total_reads"]),
                random_state=int(st.session_state["seed"]),
            )
            st.session_state["sample"] = sample
            st.session_state["true_props"] = props.copy()
            st.session_state["estimated"] = None
            st.success(
                f"Generated {len(sample)} taxa, {sum(sample.values()):,} reads (seed={st.session_state['seed']})."
            )

        sample = st.session_state.get("sample")
        if sample:
            top_n = st.slider("Show top taxa by reads", 5, 40, 15, key="topn")
            sorted_taxa = sorted(sample.items(), key=lambda x: x[1], reverse=True)[:top_n]
            taxa_names = [t for t, _ in sorted_taxa]
            counts = [c for _, c in sorted_taxa]
            fig = px.bar(
                x=taxa_names,
                y=counts,
                labels={"x": "Genus / taxon", "y": "Read count"},
                title=f"Top {top_n} taxa in the latest sample",
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Generate a sample to see read counts by taxon.")

    with tab_track:
        st.markdown(
            "Run a simplified **FEAST-style** estimate of how much each source contributed to the current sample. "
            "Estimates are **uncertain** and meant for **exploration**, not diagnosis."
        )
        sample = st.session_state.get("sample")
        true_props = st.session_state.get("true_props")
        if not sample or not true_props:
            st.warning("Go to **Simulate a mixture** and generate a sample first.")
        else:
            if st.button("Run source estimate", type="primary"):
                est = feast.estimate_proportions(
                    sample,
                    include_unknown=bool(st.session_state["include_unknown"]),
                )
                st.session_state["estimated"] = est
            estimated = st.session_state.get("estimated")
            if estimated:
                labels: List[str] = []
                true_vals: List[float] = []
                est_vals: List[float] = []
                for s in source_order:
                    labels.append(SOURCE_LABELS.get(s, s))
                    true_vals.append(true_props.get(s, 0.0))
                    est_vals.append(estimated.get(s, 0.0))
                if "Unknown" in estimated:
                    labels.append("Unknown")
                    true_vals.append(0.0)
                    est_vals.append(estimated["Unknown"])

                fig = go.Figure(
                    data=[
                        go.Bar(name="True (simulator)", x=labels, y=true_vals),
                        go.Bar(name="Estimated", x=labels, y=est_vals),
                    ]
                )
                fig.update_layout(
                    barmode="group",
                    yaxis_title="Proportion",
                    title="True mixing proportions vs estimated source contributions",
                    legend_title="",
                    yaxis_tickformat=".0%",
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info('Click **Run source estimate** to compute proportions.')

    with tab_export:
        sample = st.session_state.get("sample")
        true_props = st.session_state.get("true_props")
        estimated = st.session_state.get("estimated")
        if not sample:
            st.warning("Nothing to export yet. Generate a sample on tab 1.")
        else:
            st.download_button(
                label="Download read counts (CSV)",
                data=counts_to_csv(sample),
                file_name="shipbiome_sample_counts.csv",
                mime="text/csv",
            )
            if true_props and estimated:
                rows: List[Tuple[str, float, float]] = []
                for s in source_order:
                    rows.append(
                        (s, true_props.get(s, 0.0), estimated.get(s, 0.0))
                    )
                if "Unknown" in estimated:
                    rows.append(("Unknown", 0.0, estimated["Unknown"]))
                st.download_button(
                    label="Download true vs estimated proportions (CSV)",
                    data=proportions_to_csv(rows),
                    file_name="shipbiome_source_proportions.csv",
                    mime="text/csv",
                )
            else:
                st.caption(
                    "Run **Source tracking** to enable the proportions CSV download."
                )

    st.divider()
    st.caption(
        f"Profiles JSON: `{default_public_profiles_path()}` · "
        f"Framework: `{FRAMEWORK_PDF.name}`"
    )


if __name__ == "__main__":
    main()
