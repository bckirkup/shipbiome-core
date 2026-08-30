---
name: searching-literature-evidence
description: Search the peer-reviewed literature with the Consensus MCP server to source a shipbiome source profile or simulator parameter — taxon relative abundances for skin, seawater, urban-surface, gut and industrial sources, compositional variability, and source-tracking performance — including query construction, filter discipline, and how a hit becomes a docstring citation with an evidence grade. Use whenever a source profile needs a citation, or when asked what the literature says about a community's composition.
---

# Searching the Literature (Consensus MCP)

The `consensus` MCP server has one tool, `search`, over ~220M papers
(Semantic Scholar, PubMed, Scopus, ArXiv). It returns title, authors, year,
journal, citation count, DOI, a Consensus URL, and the abstract.

```
mcp_tool(command="call_tool", server="consensus", tool_name="search",
         tool_args='{"query": "metalworking fluid microbial community 16S Pseudomonas relative abundance"}')
```

Run `mcp_tool(command="list_tools", server="consensus")` for the current
parameter list before using an unfamiliar filter.

## What actually needs sourcing here

This is an educational simulator: the numbers that matter scientifically are the
**source profiles** — the per-taxon relative abundances that define what "skin",
"seawater", "urban surface" or "industrial" looks like. Everything else is
design.

Source-profile numbers, e.g. in `shipbiome_design.py`:

```python
"Pseudomonas": 0.40,
"Methylobacterium": 0.20,
"Desulfovibrio": 0.10,
```

These are empirical claims about a real community and must cite where they came
from. The module docstrings name the source domains (metalworking fluids, HVAC
systems, corrosion biofilms) and some MGnify studies (`MGYS00001295` skin,
`MGYS00002552` seawater, `MGYS00005612` urban surfaces), but the numbers at the
definition have no paper or accession attached. Closing that gap is the point of
this skill.

**Not** measurements, and not to be dressed up with citations:

- `concentration_param=100.0` in `DirichletMultinomialSimulator` — a dispersion
  choice controlling how tightly samples cluster around the profile. It is a
  design knob. If you want it defensible, source the *observed* variability
  (e.g. between-sample Bray-Curtis dissimilarity or a fitted Dirichlet
  precision) and record the mapping as a derivation, clearly labelled as such.
- `total_reads=10000` — simulated sequencing depth. A study-design convention,
  not a biological constant.

## Query construction

Query in the vocabulary of the paper you want:

- Good: `built environment surface microbiome 16S rRNA relative abundance genus level mass transit`
- Weak: `what bacteria live on surfaces`

Searches this repo needs:

- Skin — `human skin microbiome`, `sebaceous/moist/dry site`,
  `Cutibacterium Staphylococcus relative abundance`.
- Seawater — `marine bacterioplankton community composition`,
  `coastal surface water 16S`, `SAR11 Rhodobacteraceae`.
- Built environment — `built environment microbiome`, `mass transit surfaces`,
  `MetaSUB`, `sink P-trap biofilm`, `shower head`, `HVAC condensate`,
  `indoor air microbial source tracking`.
- Industrial — `metalworking fluid microbial contamination`,
  `microbiologically influenced corrosion biofilm`,
  `sulfate-reducing bacteria ballast/bilge`, `marine fuel tank microbiome`.
- Shipboard specifically — `ship microbiome`, `submarine/spacecraft
  built-environment microbiome`, `ISS surface microbiome` (closest analogue for
  a confined, mechanically ventilated, human-dominated habitat).
- Method — `FEAST source tracking`, `SourceTracker accuracy`,
  `unknown source proportion`, `rarefaction depth effect on beta diversity`.

Search for the community, then separately for a paper that reports **genus-level
relative abundances**, which is what a profile needs. A review describing which
taxa dominate is not the same as a table you can normalise.

## Filter discipline

Default to **no filters**; every filter silently removes evidence.

- `human=true` will discard the seawater, surface and industrial literature —
  most of what this repo needs. Only reasonable for skin or gut profiles, and
  even then it drops relevant *in vitro* work.
- `medical_mode=true` is wrong for environmental and industrial microbiology.
- `domain="bio,env,eng"` is the useful narrowing.
- `year_min` is defensible here, unlike in most repos: pre-2010 culture-based
  surveys report a very different picture from amplicon and shotgun studies, and
  a profile mixing the two is incoherent. If you filter, say so in the citation
  and prefer filtering by **method** in the query (`16S rRNA amplicon`,
  `shotgun metagenomic`) over filtering by year.
- `sjr_max=1` gives Q1 only; never reach for `sjr_min`, which *excludes* the top
  tiers.

Filters reorder as well as remove. Re-run a promising query without filters
before calling any value *the* measurement.

## Result handling

- Default page returns 20 papers; `page_size` narrows it (5 works). `page=1`
  returns a genuinely different set on this organisation's plan, so paginate
  when the first page is all reviews.
- Twenty abstracts overflow the tool result. The output is truncated and the
  full text written to a file named in the truncation notice — **read that
  file**. Items 15-20 are frequently the primary surveys, because reviews rank
  higher.
- Abundances are in tables and supplementary files, essentially never in the
  abstract. Open the DOI, and prefer papers with a public accession so the
  profile can be regenerated.

## Turning a survey into a profile

Record the citation where the profile is defined, not only in the module
docstring:

```python
INDUSTRIAL_PROFILE = {
    # Genus-level mean relative abundance, 16S V4 amplicon, n=<N> in-service
    # metalworking-fluid sumps. <Author> et al. <year>, <journal>, Table <n>
    # (DOI: <doi>) / MGnify <accession>. Renormalised over the six genera this
    # simulator tracks; the remaining <x>% of the original community is dropped.
    # Grade B: industrial sumps standing in for shipboard machinery spaces.
    "Pseudomonas": 0.40,
```

Two things must be stated because both change the numbers:

- **Renormalisation.** Restricting a real community to six genera and rescaling
  to 1.0 inflates every one of them. Say what fraction of the original community
  the retained taxa covered.
- **Taxonomic level and pipeline.** Genus-level abundances depend on the
  classifier and reference database; a genus in one pipeline can be split or
  absent in another.

Grades:

- **A** — direct measurement of this community in this setting (a shipboard
  survey for a shipboard profile).
- **B** — an analogous habitat: industrial sumps for machinery spaces, mass
  transit for cabin surfaces, coastal water for ballast.
- **C** — inferred, estimated, or a declared assumption.

Most profiles here will honestly be Grade B, and that is fine — being an
educational tool makes labelling the analogy *more* important, not less, since
students will read the profile as a fact about ships.

If no source exists, say so explicitly rather than inventing a plausible number.
A declared Grade C is honest; a fabricated citation or accession is not.

## What this search must never be used for

Do not adjust a profile — or pick among candidate papers — because it makes the
FEAST-style estimator recover the mixing proportions more accurately. The
estimator's recovery is the thing being demonstrated; tuning the sources to it
makes the demonstration circular and teaches the wrong lesson.

Fix the query and the filters from the definition of the community first. Where
sources are genuinely hard to distinguish because they share taxa, that is a real
property of source tracking worth surfacing, not a bug to source your way out
of. And never modify tests to make them pass.
