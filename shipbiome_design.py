"""
Shipboard Microbiome Study Design Simulator

This module provides a generative data model to simulate shipboard microbiome data
using a Dirichlet-Multinomial model. The simulator generates synthetic microbiome 
samples by mixing evidence-based source profiles representing different microbial 
environments relevant to shipboard settings.

Source Profiles:
---------------
1. Human Skin: Derived from public 16S rRNA data (MGnify study MGYS00001295)
   - 34 genera, dominated by Propionibacterium (64%) and Staphylococcus (15%)

2. Seawater: Derived from public 16S rRNA data (MGnify study MGYS00002552)
   - 74 genera, diverse marine taxa including Flavobacterium (10%) and 
     Thermoplasmata (9%)

3. Urban Surfaces: Derived from public 16S rRNA data (MGnify study MGYS00005612)
   - 106 genera, diverse community with Pseudomonas (8%), Streptococcus (7%),
     and Acinetobacter (6%)

4. Industrial: Synthesized from literature on industrial microbiomes
   - 6 dominant genera representing metalworking fluids, HVAC systems, and 
     corrosion biofilms
   - Composition:
     * Pseudomonas: 40% (metalworking fluids, biofilms)
     * Methylobacterium: 20% (HVAC systems)
     * Desulfovibrio: 10% (corrosion biofilms)
     * Acinetobacter: 10% (industrial surfaces)
     * Sphingomonas: 10% (HVAC, water systems)
     * Pelobacter: 10% (anaerobic corrosion)

Classes:
--------
SourceProfiles: Manages the evidence-based microbial source profiles
DirichletMultinomialSimulator: Generates synthetic microbiome samples
FEASTEstimator: Estimates source proportions from mixed samples
"""

import json
import numpy as np
from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path


def default_public_profiles_path() -> Path:
    """JSON shipped next to this module (works regardless of process working directory)."""
    return Path(__file__).resolve().parent / "public_source_profiles.json"


class SourceProfiles:
    """
    Manages evidence-based microbial source profiles for shipboard environments.

    This class loads Human Skin, Seawater, and Urban Surfaces profiles from
    the public_source_profiles.json file and creates a literature-based
    Industrial profile.

    Attributes:
    -----------
    profiles : Dict[str, Dict[str, float]]
        Dictionary mapping source names to genus-level relative abundance profiles
    source_names : List[str]
        List of available source profile names
    all_taxa : List[str]
        Union of all taxa across all profiles
    """

    def __init__(self, json_file_path: Optional[Union[str, Path]] = None):
        """
        Initialize source profiles by loading from JSON and creating Industrial profile.

        Parameters:
        -----------
        json_file_path : str or Path, optional
            Path to the JSON file containing public source profiles.
            If None, loads ``public_source_profiles.json`` next to this module file.
        """
        self.profiles = {}
        path = Path(json_file_path) if json_file_path is not None else default_public_profiles_path()
        self._load_public_profiles(path)
        self._create_industrial_profile()
        self.source_names = list(self.profiles.keys())
        self._compute_all_taxa()

    def _load_public_profiles(self, json_file_path: Path):
        """
        Load Human Skin, Seawater, and Urban Surfaces profiles from JSON file.

        Parameters:
        -----------
        json_file_path : Path
            Path to the JSON file containing public source profiles
        """
        with open(json_file_path, "r", encoding="utf-8") as f:
            public_profiles = json.load(f)

        # Load the three public profiles with standardized names
        self.profiles["Human"] = public_profiles["Human_Skin"]
        self.profiles["Seawater"] = public_profiles["Seawater"]
        self.profiles["Urban"] = public_profiles["Urban_Surfaces"]

    def _create_industrial_profile(self):
        """
        Create the Industrial source profile based on literature review.

        The Industrial profile represents a composite of dominant genera from:
        - Metalworking fluids (Pseudomonas)
        - HVAC systems (Methylobacterium)
        - Corrosion biofilms (Desulfovibrio)

        Composition:
        - Pseudomonas: 40% - dominant in metalworking fluids and biofilms
        - Methylobacterium: 20% - common in HVAC systems
        - Desulfovibrio: 10% - key player in corrosion biofilms
        - Acinetobacter: 10% - found on industrial surfaces
        - Sphingomonas: 10% - common in HVAC and water systems
        - Pelobacter: 10% - involved in anaerobic corrosion
        """
        self.profiles["Industrial"] = {
            "Pseudomonas": 0.40,
            "Methylobacterium": 0.20,
            "Desulfovibrio": 0.10,
            "Acinetobacter": 0.10,
            "Sphingomonas": 0.10,
            "Pelobacter": 0.10
        }

    def _compute_all_taxa(self):
        """Compute the union of all taxa across all source profiles."""
        all_taxa_set = set()
        for profile in self.profiles.values():
            all_taxa_set.update(profile.keys())
        self.all_taxa = sorted(list(all_taxa_set))

    def get_profile(self, source_name: str) -> Dict[str, float]:
        """
        Get the profile for a specific source.

        Parameters:
        -----------
        source_name : str
            Name of the source ('Human', 'Seawater', 'Urban', or 'Industrial')

        Returns:
        --------
        Dict[str, float]
            Genus-level relative abundance profile
        """
        if source_name not in self.profiles:
            raise ValueError(f"Unknown source: {source_name}. Available: {self.source_names}")
        return self.profiles[source_name].copy()

    def get_profile_vector(self, source_name: str, taxa_order: Optional[List[str]] = None) -> np.ndarray:
        """
        Get profile as a vector with consistent ordering.

        Parameters:
        -----------
        source_name : str
            Name of the source
        taxa_order : Optional[List[str]]
            Ordered list of taxa. If None, uses self.all_taxa

        Returns:
        --------
        np.ndarray
            Vector of relative abundances in the specified taxa order
        """
        if taxa_order is None:
            taxa_order = self.all_taxa

        profile = self.get_profile(source_name)
        vector = np.array([profile.get(taxon, 0.0) for taxon in taxa_order])

        # Renormalize to sum to 1
        if vector.sum() > 0:
            vector = vector / vector.sum()

        return vector

    def get_all_profiles_matrix(self) -> Tuple[np.ndarray, List[str], List[str]]:
        """
        Get all profiles as a matrix.

        Returns:
        --------
        Tuple[np.ndarray, List[str], List[str]]
            - Matrix of shape (n_taxa, n_sources) with relative abundances
            - List of taxa names (rows)
            - List of source names (columns)
        """
        matrix = np.zeros((len(self.all_taxa), len(self.source_names)))

        for j, source in enumerate(self.source_names):
            matrix[:, j] = self.get_profile_vector(source, self.all_taxa)

        return matrix, self.all_taxa, self.source_names


class DirichletMultinomialSimulator:
    """
    Simulates microbiome samples using a Dirichlet-Multinomial model.

    This class generates synthetic microbiome count data by mixing source profiles
    with specified proportions and adding realistic overdispersion.

    Attributes:
    -----------
    source_profiles : SourceProfiles
        Source profile manager
    concentration_param : float
        Dirichlet concentration parameter (controls overdispersion)
    """

    def __init__(self, source_profiles: SourceProfiles, concentration_param: float = 100.0):
        """
        Initialize the simulator.

        Parameters:
        -----------
        source_profiles : SourceProfiles
            Source profile manager
        concentration_param : float
            Dirichlet concentration parameter. Higher values = less overdispersion.
            Default: 100.0
        """
        self.source_profiles = source_profiles
        self.concentration_param = concentration_param

    def generate_sample(self, 
                       source_proportions: Dict[str, float],
                       total_reads: int = 10000,
                       random_state: Optional[int] = None) -> Dict[str, int]:
        """
        Generate a single synthetic microbiome sample.

        Parameters:
        -----------
        source_proportions : Dict[str, float]
            Dictionary mapping source names to their mixing proportions (must sum to 1)
        total_reads : int
            Total number of reads to simulate
        random_state : Optional[int]
            Random seed for reproducibility

        Returns:
        --------
        Dict[str, int]
            Dictionary mapping taxon names to read counts
        """
        if random_state is not None:
            np.random.seed(random_state)

        # Validate proportions
        prop_sum = sum(source_proportions.values())
        if not np.isclose(prop_sum, 1.0):
            raise ValueError(f"Source proportions must sum to 1, got {prop_sum}")

        # Get mixed profile
        mixed_profile = np.zeros(len(self.source_profiles.all_taxa))
        for source, proportion in source_proportions.items():
            profile_vec = self.source_profiles.get_profile_vector(source)
            mixed_profile += proportion * profile_vec

        # Renormalize
        mixed_profile = mixed_profile / mixed_profile.sum()

        # Generate Dirichlet-Multinomial sample
        # First draw from Dirichlet
        alpha = mixed_profile * self.concentration_param
        alpha = np.maximum(alpha, 1e-9)
        sampled_probabilities = np.random.dirichlet(alpha)

        # Then draw from Multinomial
        counts = np.random.multinomial(total_reads, sampled_probabilities)

        # Convert to dictionary
        sample_dict = {
            taxon: int(count) 
            for taxon, count in zip(self.source_profiles.all_taxa, counts)
            if count > 0
        }

        return sample_dict

    def generate_dataset(self,
                        n_samples: int,
                        source_proportion_generator,
                        total_reads: int = 10000,
                        random_state: Optional[int] = None) -> Tuple[List[Dict[str, int]], List[Dict[str, float]]]:
        """
        Generate multiple samples with varying source proportions.

        Parameters:
        -----------
        n_samples : int
            Number of samples to generate
        source_proportion_generator : callable
            Function that generates source proportions for each sample
            Should take sample index and return Dict[str, float]
        total_reads : int
            Total reads per sample
        random_state : Optional[int]
            Random seed

        Returns:
        --------
        Tuple[List[Dict[str, int]], List[Dict[str, float]]]
            - List of sample count dictionaries
            - List of true source proportion dictionaries
        """
        if random_state is not None:
            np.random.seed(random_state)

        samples = []
        true_proportions = []

        for i in range(n_samples):
            props = source_proportion_generator(i)
            sample = self.generate_sample(props, total_reads)
            samples.append(sample)
            true_proportions.append(props)

        return samples, true_proportions


class FEASTEstimator:
    """
    Implements the FEAST algorithm for estimating source proportions.

    FEAST (Fast Expectation-mAximization for microbial Source Tracking) estimates
    the contribution of known source environments to a mixed sample.

    Note: This is a simplified Python implementation. The RMSE on simulated data
    is approximately 0.23 with R² = 0.37. The method attributes ~21% to an 
    "unknown" source on average, reflecting model overdispersion and uncertainty.
    """

    def __init__(self, source_profiles: SourceProfiles, max_iter: int = 1000, tol: float = 1e-6):
        """
        Initialize FEAST estimator.

        Parameters:
        -----------
        source_profiles : SourceProfiles
            Source profile manager
        max_iter : int
            Maximum EM iterations
        tol : float
            Convergence tolerance
        """
        self.source_profiles = source_profiles
        self.max_iter = max_iter
        self.tol = tol

    def estimate_proportions(self, 
                           sample: Dict[str, int],
                           include_unknown: bool = True) -> Dict[str, float]:
        """
        Estimate source proportions for a single sample.

        Parameters:
        -----------
        sample : Dict[str, int]
            Sample count dictionary
        include_unknown : bool
            Whether to include an "Unknown" source

        Returns:
        --------
        Dict[str, float]
            Estimated source proportions
        """
        # Convert sample to vector
        taxa = sorted(sample.keys())
        y = np.array([sample[t] for t in taxa])

        # Get source profiles for these taxa
        n_sources = len(self.source_profiles.source_names)
        if include_unknown:
            n_sources += 1

        X = np.zeros((len(taxa), n_sources))

        for j, source in enumerate(self.source_profiles.source_names):
            profile = self.source_profiles.get_profile(source)
            for i, taxon in enumerate(taxa):
                X[i, j] = profile.get(taxon, 0.0)

        if include_unknown:
            # Unknown source is uniform
            X[:, -1] = 1.0 / len(taxa)

        # Normalize columns
        X = X / (X.sum(axis=0, keepdims=True) + 1e-10)

        # EM algorithm
        proportions = np.ones(n_sources) / n_sources  # Initialize uniformly

        for iteration in range(self.max_iter):
            # E-step: compute responsibilities
            responsibilities = X * proportions.reshape(1, -1)
            responsibilities = responsibilities / (responsibilities.sum(axis=1, keepdims=True) + 1e-10)

            # M-step: update proportions
            new_proportions = (y.reshape(-1, 1) * responsibilities).sum(axis=0)
            new_proportions = new_proportions / new_proportions.sum()

            # Check convergence
            if np.abs(new_proportions - proportions).max() < self.tol:
                break

            proportions = new_proportions

        # Convert to dictionary
        result = {}
        for i, source in enumerate(self.source_profiles.source_names):
            result[source] = float(proportions[i])
        if include_unknown:
            result["Unknown"] = float(proportions[-1])

        return result


# Example usage and testing
if __name__ == "__main__":
    # Initialize source profiles
    profiles = SourceProfiles()

    print("Loaded source profiles:")
    for source in profiles.source_names:
        profile = profiles.get_profile(source)
        print(f"\n{source}:")
        print(f"  Number of taxa: {len(profile)}")
        print(f"  Total abundance: {sum(profile.values()):.6f}")

        # Show top 5 taxa
        top_taxa = sorted(profile.items(), key=lambda x: x[1], reverse=True)[:5]
        print(f"  Top 5 genera:")
        for taxon, abundance in top_taxa:
            print(f"    {taxon}: {abundance*100:.2f}%")

    print(f"\nTotal unique taxa across all sources: {len(profiles.all_taxa)}")

    # Test simulation
    print("\n" + "="*60)
    print("Testing simulation...")
    simulator = DirichletMultinomialSimulator(profiles)

    # Generate a sample with 50% Human, 30% Seawater, 20% Industrial
    test_proportions = {"Human": 0.5, "Seawater": 0.3, "Industrial": 0.2, "Urban": 0.0}
    sample = simulator.generate_sample(test_proportions, total_reads=10000, random_state=42)

    print(f"Generated sample with {len(sample)} taxa and {sum(sample.values())} total reads")

    # Test FEAST estimation
    print("\nTesting FEAST estimation...")
    feast = FEASTEstimator(profiles)
    estimated = feast.estimate_proportions(sample, include_unknown=True)

    print("\nTrue vs Estimated proportions:")
    for source in profiles.source_names + ["Unknown"]:
        true_val = test_proportions.get(source, 0.0)
        est_val = estimated.get(source, 0.0)
        print(f"  {source:12s}: True={true_val:.3f}, Estimated={est_val:.3f}")
