"""
Validation script for expanded_maritime_profiles.json

Loads all 9 source profiles, verifies normalization, and generates
Dirichlet-Multinomial samples using various mixtures to confirm no
index or alpha errors occur.
"""

import json
import sys
import numpy as np
from pathlib import Path
from shipbiome_design import SourceProfiles, DirichletMultinomialSimulator, FEASTEstimator


class ExpandedSourceProfiles(SourceProfiles):
    """Loads all 9 profiles from expanded_maritime_profiles.json directly."""

    def __init__(self, json_file_path=None):
        # Skip the parent __init__ — we load differently
        self.profiles = {}
        path = Path(json_file_path) if json_file_path else (
            Path(__file__).resolve().parent / "expanded_maritime_profiles.json"
        )
        with open(path, "r", encoding="utf-8") as f:
            self.profiles = json.load(f)
        self.source_names = list(self.profiles.keys())
        self._compute_all_taxa()


def main():
    print("=" * 70)
    print("VALIDATION: expanded_maritime_profiles.json")
    print("=" * 70)

    # --- Step 1: Load and verify profiles ---
    print("\n[1] Loading expanded profiles...")
    profiles = ExpandedSourceProfiles()

    print(f"    Loaded {len(profiles.source_names)} source profiles")
    print(f"    Total unique taxa: {len(profiles.all_taxa)}")

    expected_profiles = [
        "Human_Gut_Healthy",
        "Human_Respiratory_Healthy",
        "Human_Skin",
        "Sink_P_Traps",
        "Showers",
        "Toilets",
        "Outdoor_Air",
        "Human_Gut_Infected",
        "Human_Respiratory_Infected",
    ]

    errors = 0

    for name in expected_profiles:
        if name not in profiles.source_names:
            print(f"    ERROR: Missing profile '{name}'")
            errors += 1

    if errors > 0:
        print(f"\n    FAILED: {errors} missing profiles")
        sys.exit(1)

    print("    All 9 expected profiles present.")

    # --- Step 2: Verify normalization ---
    print("\n[2] Verifying profile normalization...")
    for name in profiles.source_names:
        profile = profiles.get_profile(name)
        total = sum(profile.values())
        n_taxa = len(profile)
        status = "OK" if np.isclose(total, 1.0, atol=1e-6) else "FAIL"
        if status == "FAIL":
            errors += 1
        print(f"    {name:35s}: {n_taxa:3d} taxa, sum={total:.8f} [{status}]")

    if errors > 0:
        print(f"\n    FAILED: {errors} profiles not normalized")
        sys.exit(1)
    print("    All profiles sum to 1.0.")

    # --- Step 3: Verify infected profiles contain pathogens ---
    print("\n[3] Verifying pathogen spikes in infected profiles...")
    gut_infected = profiles.get_profile("Human_Gut_Infected")
    resp_infected = profiles.get_profile("Human_Respiratory_Infected")

    if "Clostridioides_difficile" in gut_infected:
        cdiff_pct = gut_infected["Clostridioides_difficile"] * 100
        print(f"    Human_Gut_Infected: Clostridioides_difficile = {cdiff_pct:.1f}%  [OK]")
    else:
        print("    ERROR: Clostridioides_difficile not found in Human_Gut_Infected")
        errors += 1

    if "Legionella_pneumophila" in resp_infected:
        leg_pct = resp_infected["Legionella_pneumophila"] * 100
        print(f"    Human_Respiratory_Infected: Legionella_pneumophila = {leg_pct:.1f}%  [OK]")
    else:
        print("    ERROR: Legionella_pneumophila not found in Human_Respiratory_Infected")
        errors += 1

    # --- Step 4: Test single-source samples ---
    print("\n[4] Generating single-source samples (one profile at 100%)...")
    simulator = DirichletMultinomialSimulator(profiles, concentration_param=100.0)

    for name in profiles.source_names:
        proportions = {s: (1.0 if s == name else 0.0) for s in profiles.source_names}
        try:
            sample = simulator.generate_sample(proportions, total_reads=5000, random_state=42)
            print(f"    {name:35s}: {len(sample):3d} taxa, {sum(sample.values()):5d} reads  [OK]")
        except Exception as e:
            print(f"    {name:35s}: ERROR - {e}")
            errors += 1

    # --- Step 5: Test mixed-source samples ---
    print("\n[5] Generating mixed-source samples...")
    mix_scenarios = [
        ("Cabin (Gut+Skin+Respiratory)", {
            "Human_Gut_Healthy": 0.4, "Human_Skin": 0.35, "Human_Respiratory_Healthy": 0.25,
        }),
        ("Bathroom (Toilets+Showers+Skin)", {
            "Toilets": 0.45, "Showers": 0.35, "Human_Skin": 0.20,
        }),
        ("Galley (Sinks+Outdoor_Air+Gut)", {
            "Sink_P_Traps": 0.40, "Outdoor_Air": 0.30, "Human_Gut_Healthy": 0.30,
        }),
        ("Infected Cabin (GutInfected+Skin+Toilets)", {
            "Human_Gut_Infected": 0.50, "Human_Skin": 0.30, "Toilets": 0.20,
        }),
        ("All 9 sources equal", {
            s: 1.0 / 9.0 for s in profiles.source_names
        }),
    ]

    for label, proportions in mix_scenarios:
        # Ensure all sources are in the dict (zero for missing)
        full_props = {s: proportions.get(s, 0.0) for s in profiles.source_names}
        # Renormalize to handle floating-point drift
        total = sum(full_props.values())
        full_props = {s: v / total for s, v in full_props.items()}
        try:
            sample = simulator.generate_sample(full_props, total_reads=10000, random_state=123)
            print(f"    {label:45s}: {len(sample):3d} taxa, {sum(sample.values()):5d} reads  [OK]")
        except Exception as e:
            print(f"    {label:45s}: ERROR - {e}")
            errors += 1

    # --- Step 6: Test FEAST estimation on a mixed sample ---
    print("\n[6] Testing FEAST estimation on infected-cabin mixture...")
    feast = FEASTEstimator(profiles)
    infected_props = {s: 0.0 for s in profiles.source_names}
    infected_props["Human_Gut_Infected"] = 0.50
    infected_props["Human_Skin"] = 0.30
    infected_props["Toilets"] = 0.20

    sample = simulator.generate_sample(infected_props, total_reads=10000, random_state=99)
    estimated = feast.estimate_proportions(sample, include_unknown=True)

    print(f"    {'Source':35s}  {'True':>8s}  {'Estimated':>10s}")
    print(f"    {'-'*57}")
    for source in profiles.source_names:
        true_val = infected_props.get(source, 0.0)
        est_val = estimated.get(source, 0.0)
        marker = " <--" if true_val > 0.05 else ""
        print(f"    {source:35s}  {true_val:8.3f}  {est_val:10.3f}{marker}")
    if "Unknown" in estimated:
        print(f"    {'Unknown':35s}  {'---':>8s}  {estimated['Unknown']:10.3f}")

    # --- Summary ---
    print("\n" + "=" * 70)
    if errors == 0:
        print("VALIDATION PASSED: All 9 profiles loaded, normalized, and usable.")
        print("DirichletMultinomialSimulator generates samples without errors.")
        print("FEAST estimation runs successfully on expanded profile set.")
    else:
        print(f"VALIDATION FAILED: {errors} error(s) encountered.")
    print("=" * 70)

    sys.exit(0 if errors == 0 else 1)


if __name__ == "__main__":
    main()
