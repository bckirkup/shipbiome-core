# bckirkup Repository Portfolio Overview

**As of:** 2026-08-16 (all repositories inspected on `main`, freshly pulled from `origin`).

This document describes the thirteen repository names supplied for review, grouped by
research programme. Every quantitative figure below was computed on the local clones
rather than copied from a README; where a README states a number that disagrees with the
measurement, both are shown and the disagreement is called out.

---

## Methodology and caveats

All figures are derived from **tracked files only** (`git ls-files`), so local virtual
environments, build directories, and `node_modules` never inflate a count. The exact
commands are listed in [Appendix A](#appendix-a--measurement-commands).

| Measure | How it was obtained | Known limitation |
|---|---|---|
| Lines of code | `cloc --list-file=<git ls-files>` | `cloc` counts committed JSON/Markdown as "code"; several repositories commit large JSON experiment outputs, so **total LOC and source LOC are reported separately**. |
| Python test files / functions | tracked paths matching `tests/`, `test_*.py`, `*_test.py`; functions matching `^\s*(async def\|def) test` | Misses `unittest` methods that are not named `test*`, and counts a parametrized function once. |
| Python tests *collected* | `pytest --collect-only -q` in each repo's own `.venv` where one exists | Reflects parametrization, so it is usually **higher** than the function count. Two repositories have local collection errors (noted inline) caused by missing optional dependencies in this workspace, not by broken tests. |
| TypeScript test cases | tracked `*.test.ts` files; cases matching `^\s*(it\|test)(\.each)?\(` | Source-pattern count, not a Vitest run. |
| C++ tests | tracked `tests/*.cpp` files, `void test_*()` functions, and `add_test(...)` registrations in `tests/CMakeLists.txt` | GutIBM uses hand-rolled `assert`-based mains, not GoogleTest, so "test functions" are counted syntactically. |
| Git activity | `git rev-list --count`, `git log` (commit dates, distinct author names, windowed counts) | Author identities include bot accounts (`devin-ai-integration[bot]`, `Cursor Agent`), which are reported as contributors because they author commits. |
| CI jobs | top-level keys under `jobs:` in each `.github/workflows/*.yml` | Job names, not step counts. |
| Maturity | packaging metadata (`version`, `Development Status` classifier), README status sections, CI breadth, and test density | Judgement call; the underlying signals are cited each time. |

Two caveats matter for reading the tables:

1. **JSON artefacts dominate three repositories.** Coral Key (242,714 JSON lines),
   Scrapiron (210,953) and Xylella (70,166) commit simulation baselines and grounded-access
   sweeps into the tree. Their "total LOC" is therefore an order of magnitude larger than
   the code a maintainer actually edits.
2. **One name is not a repository.** `bckirkup/TheKingAndI` is an old name that GitHub
   301-redirects to `bckirkup/TheKingsAndI`; see
   [the duplicate finding](#duplicate-finding-thekingandi-is-a-redirect-not-a-fork).
   Twelve distinct repositories back the thirteen requested names.

---

## Table of contents

- [Methodology and caveats](#methodology-and-caveats)
- [Executive summary](#executive-summary)
  - [Portfolio comparison table](#portfolio-comparison-table)
  - [Duplicate finding: TheKingAndI is a redirect, not a fork](#duplicate-finding-thekingandi-is-a-redirect-not-a-fork)
  - [What the numbers say about the portfolio](#what-the-numbers-say-about-the-portfolio)
- [1. The TattleTots ecosystem](#1-the-tattletots-ecosystem)
  - [1.1 TattleTots](#11-tattletots)
  - [1.2 domain-runner](#12-domain-runner)
  - [1.3 Scrapiron_and_the_Bear (FireEcology)](#13-scrapiron_and_the_bear-fireecology)
  - [1.4 Xylella_SPQR (GrainGuard)](#14-xylella_spqr-grainguard)
  - [1.5 Coral_Key_in_Three_Hour_Epochs (ReefWatch)](#15-coral_key_in_three_hour_epochs-reefwatch)
  - [1.6 Ecosystem-level observations](#16-ecosystem-level-observations)
- [2. Epidemiology and microbiome](#2-epidemiology-and-microbiome)
  - [2.1 Crusher_to_the_Bridge](#21-crusher_to_the_bridge)
  - [2.2 GutModelBacteriocins (GutIBM)](#22-gutmodelbacteriocins-gutibm)
  - [2.3 Garlic-Routed-Local-Area-Network-Domain (GARLAND)](#23-garlic-routed-local-area-network-domain-garland)
  - [2.4 shipbiome-core](#24-shipbiome-core)
- [3. Imaging and applications](#3-imaging-and-applications)
  - [3.1 Anaglyph](#31-anaglyph)
  - [3.2 Umkehrwalze_Cassel (revprint)](#32-umkehrwalze_cassel-revprint)
- [4. Games](#4-games)
  - [4.1 TheKingsAndI](#41-thekingsandi)
  - [4.2 TheKingAndI](#42-thekingandi)
- [5. Cross-portfolio observations](#5-cross-portfolio-observations)
- [6. Findings worth acting on](#6-findings-worth-acting-on)
- [Appendix A — measurement commands](#appendix-a--measurement-commands)
- [Appendix B — per-language line counts](#appendix-b--per-language-line-counts)
- [Appendix C — CI job inventory](#appendix-c--ci-job-inventory)

---

## Executive summary

The portfolio is a single research program expressed as twelve repositories. Its centre of
gravity is **agent-based simulation of information and disease ecologies**: one engine
(TattleTots) with a shared runner (domain-runner) and three interchangeable domain
adapters (fire, grain, reef); one large shipboard outbreak digital twin (Crusher to the
Bridge); one HPC C++/CUDA gut model (GutIBM); one privacy-preserving population
biosurveillance testbed (GARLAND); and one small Streamlit source-tracking app
(shipbiome-core). Two repositories are applied imaging tools (Anaglyph, revprint) and one
is a TypeScript game that reuses the same "psychology as measurable state" idea in a
leadership simulation (TheKingsAndI).

Engineering practice is unusually uniform for a solo-author portfolio: eleven of twelve
repositories run GitHub Actions, eleven register a SonarQube project, ten install
`pre-commit` with Ruff plus custom "sonar guard" hooks, eleven carry an `AGENTS.md`, and all
twelve carry a `.agents/skills/` directory of machine-readable operating procedures. The
measured test inventory across the portfolio is roughly **3,100 Python test functions plus 419
TypeScript cases plus 393 C++ test functions**, and Python collection in the repositories
that could be collected locally totals **1,512 + 523 + 443 + 229 + 209 + 146 + 97 + 86 + 3**
node IDs.

The clear outlier is the repository this document lives in: **shipbiome-core has no
README, no tests, no CI, and no lint configuration**, while carrying a Streamlit
application that other repositories in the portfolio would gate behind six CI jobs.

### Portfolio comparison table

LOC columns are `cloc` over tracked files. "Source LOC" is the primary-language figure;
"Total LOC" includes committed JSON data, Markdown, YAML, and shell. "Tests" is the
measured count (Python test functions / TypeScript cases / C++ test functions); the
parenthesised figure is `pytest --collect-only` where it could be run locally.

| # | Repository | Primary language | License (`LICENSE` file) | Source LOC | Total LOC | Tests | CI? | Maturity |
|---:|---|---|---|---:|---:|---|:--:|---|
| 1 | [TattleTots](#11-tattletots) | Python | Apache-2.0 | 18,947 | 41,160 | 381 (443 collected) | Yes — 7 jobs | Alpha, v0.1.0; engine with 3 live adapters |
| 2 | [domain-runner](#12-domain-runner) | Python | Apache-2.0 | 1,046 | 1,691 | 3 (3 collected) | Yes — 5 jobs | Alpha, v0.1.0; stable shared library |
| 3 | [Scrapiron_and_the_Bear](#13-scrapiron_and_the_bear-fireecology) | Python | Apache-2.0 | 7,450 | 220,146 | 222 (229 collected) | Yes — 6 jobs | Alpha, v0.1.0; measurement campaigns committed |
| 4 | [Xylella_SPQR](#14-xylella_spqr-grainguard) | Python | Apache-2.0 | 7,379 | 79,273 | 250 (209 collected, 3 local errors) | Yes — 6 jobs | Alpha, v0.1.0; strict-mypy domain |
| 5 | [Coral_Key_in_Three_Hour_Epochs](#15-coral_key_in_three_hour_epochs-reefwatch) | Python | Apache-2.0 (**pyproject says MIT**) | 5,816 | 250,240 | 137 (146 collected) | Yes — 6 jobs | Alpha, v0.1.0; newest domain adapter |
| 6 | [Crusher_to_the_Bridge](#21-crusher_to_the_bridge) | Python | MIT | 70,190 | 213,066 | 1,311 (1,512 collected) | Yes — 15 jobs / 2 workflows | Most mature; v0.1.0 but production-scale CI |
| 7 | [GutModelBacteriocins](#22-gutmodelbacteriocins-gutibm) | C++ (+CUDA, Python) | Apache-2.0 | 35,641 C++/CUDA/headers | 58,351 | 393 C++ fns / 86 CTest targets / 130 Python | Yes — 8 jobs | Explicit "research prototype", v0.1.0 |
| 8 | [GARLAND](#23-garlic-routed-local-area-network-domain-garland) | Python | Apache-2.0 | 18,394 | 22,595 | 501 (523 collected) | Yes — 3 workflows, 8 jobs | Alpha, v0.1.0; highest test density |
| 9 | [shipbiome-core](#24-shipbiome-core) | Python | MIT | 660 | 1,388 | **0** | **No** | Prototype; no README, no tests, no CI |
| 10 | [Anaglyph](#31-anaglyph) | Python | GPL-3.0-or-later | 3,604 | 4,715 | 97 (97 collected) | Yes — 5 jobs | Alpha, v0.1.0; hardware-dependent |
| 11 | [Umkehrwalze_Cassel](#32-umkehrwalze_cassel-revprint) | Python | Apache-2.0 | 8,119 | 11,113 | 86 (86 collected) | Yes — 5 jobs | Alpha, v0.1.0; 70% coverage gate |
| 12 | [TheKingsAndI](#41-thekingsandi) | TypeScript | AGPL-3.0 (dual: commercial) | 28,709 | 43,324 | 419 TS cases (44 files) | Yes — 3 + 3 nightly jobs | Milestones 1–6 "substantially landed"; `version 0.0.0` |
| 13 | [TheKingAndI](#42-thekingandi) | — | — | — | — | — | — | **Not a distinct repository — redirect to #12** |

Git activity, same as-of date:

| Repository | Commits | First commit | Latest commit | Distinct authors | Commits last 30d | Merge commits |
|---|---:|---|---|---:|---:|---:|
| Crusher_to_the_Bridge | 565 | 2026-05-23 | 2026-08-16 | 4 | 293 | 213 |
| GutModelBacteriocins | 631 | 2026-06-16 | 2026-08-16 | 4 | 343 | 236 |
| TheKingsAndI | 328 | 2026-07-26 | 2026-08-16 | 4 | 328 | 108 |
| TattleTots | 196 | 2026-06-06 | 2026-08-16 | 3 | 133 | 63 |
| GARLAND | 184 | 2026-06-16 | 2026-08-16 | 3 | 113 | 66 |
| Coral_Key_in_Three_Hour_Epochs | 100 | 2026-06-07 | 2026-08-16 | 3 | 57 | 32 |
| Xylella_SPQR | 90 | 2026-06-07 | 2026-08-16 | 2 | 51 | 33 |
| Scrapiron_and_the_Bear | 86 | 2026-06-06 | 2026-08-16 | 3 | 42 | 30 |
| Anaglyph | 40 | 2026-02-21 | 2026-08-15 | 2 | 12 | 15 |
| Umkehrwalze_Cassel | 35 | 2026-06-07 | 2026-08-15 | 2 | 14 | 12 |
| domain-runner | 22 | 2026-06-20 | 2026-08-15 | 1 | 11 | 8 |
| shipbiome-core | 10 | 2026-05-16 | 2026-08-12 | 2 | 2 | 3 |

*Source: `git rev-list --count HEAD`, `git log --reverse --format=%ad`, `git log -1`,
`git log --format=%aN | sort -u`, `git log --since='30 days ago'`, `git log --merges`.*

Every repository except shipbiome-core was touched within the last 24 hours to 10 days,
and eight of twelve were pushed on 2026-08-16. All twelve repositories were created between
2026-02-21 (Anaglyph) and 2026-07-26 (TheKingsAndI): this is a six-month-old portfolio
moving at 40–340 commits per month per active repository, with most commits arriving as
merges of `devin/*` and `cursor/*` agent branches.

### Duplicate finding: TheKingAndI is a redirect, not a fork

The task brief asked which of `TheKingsAndI` / `TheKingAndI` is canonical. The answer is
stronger than "one is canonical": **they are the same repository object on GitHub.**

| Check | `bckirkup/TheKingsAndI` | `bckirkup/TheKingAndI` |
|---|---|---|
| GitHub numeric repo id | `1313180573` | `1313180573` (identical) |
| `full_name` returned by API | `bckirkup/TheKingsAndI` | `bckirkup/TheKingsAndI` (API normalises the name) |
| `created_at` | 2026-07-26T21:39:03Z | 2026-07-26T21:39:03Z |
| `pushed_at` | 2026-08-16T19:16:02Z | 2026-08-16T19:16:02Z |
| HTTP status of `https://github.com/bckirkup/<name>` | 200 | **301 redirect** |
| `HEAD` in local clone | `d55bdf32d73f046986de2fee042e9a72da52e98c` | `d55bdf32d73f046986de2fee042e9a72da52e98c` |
| Commit count / branch list | 328 / 22 branches | 328 / identical 22 branches |
| Tracked LOC | 43,324 | 43,324 |
| `sonar.projectKey` | `bckirkup_TheKingsAndI` | `bckirkup_TheKingsAndI` |

*Source: `gh api repos/bckirkup/TheKingAndI --jq '{id,full_name,created_at}'` versus the
same call for `TheKingsAndI`; `curl -o /dev/null -w '%{http_code}'` against each web URL;
`git rev-parse HEAD` in both clones; `gh repo list bckirkup` (which lists `TheKingsAndI`
once and never lists `TheKingAndI`).*

**Canonical name: `bckirkup/TheKingsAndI`.** `TheKingAndI` is the repository's earlier
name, preserved by GitHub's rename redirect — which is why the READMEs are byte-identical:
there is only one README. The rename is documented inside the repository itself, in
[`docs/adr/0010-naming-the-king-and-i.md`](https://github.com/bckirkup/TheKingsAndI/blob/main/docs/adr/0010-naming-the-king-and-i.md).
A clone made from the old URL keeps the old remote string (`git remote -v` shows
`.../bckirkup/TheKingAndI`) and still fetches the canonical repository, so nothing breaks —
but any documentation, CI badge, or dependency pin using the old name should be updated,
because rename redirects stop working the moment someone else creates a repository at the
vacated name.

### What the numbers say about the portfolio

- **Two repositories carry most of the engineering mass.** Crusher to the Bridge (70,190
  Python lines, 1,512 collected tests, 15 CI jobs) and GutIBM (35,641 lines of
  C++/CUDA/headers, 86 CTest registrations, 8 CI jobs including GPU parity) are on a
  different scale from everything else.
- **Test density is consistent except at the edges.** Collected tests per 100 Python lines:
  GARLAND 2.8, Coral Key 2.5, Crusher 2.2, TattleTots 2.3, Anaglyph 2.7, Scrapiron 3.1,
  Xylella 2.8 — then Umkehrwalze 1.1, domain-runner 0.3, and shipbiome-core 0.
- **Committed simulation output is the single largest category of tracked lines** in the
  portfolio: over 650,000 JSON lines across Coral Key, Scrapiron, Xylella, Crusher and
  GutIBM. This is deliberate (grounded-access baselines and measurement records are meant
  to be reviewable in-tree) but it makes repository size a poor proxy for effort.
- **Licensing is intentional, not accidental** — Apache-2.0 for the research engines, MIT
  for the two ship-related applications, GPL-3.0-or-later for Anaglyph (which links
  PyQt6), and AGPL-3.0-with-commercial-option for the game. The one inconsistency is Coral
  Key, whose `LICENSE` file is Apache-2.0 while `pyproject.toml` and the README both say
  MIT.

---

## 1. The TattleTots ecosystem

Five repositories form a layered stack: a **runner** (`domain-runner`) that knows how to
step a simulation and batch it; an **engine** (`TattleTots`) that adds a dual-currency
agent ecology as an optional layer above the domain; and three **domain adapters**
(fire, grain, reef) that supply the physics and the human users being served.

```
domain-runner            ← layer-agnostic single/batch runners, no TattleTots dependency
      ↑
TattleTots               ← "tattletots" SimulationLayer: Tots, selection, dual currency
      ↑
Scrapiron / Xylella / Coral Key   ← domain physics, sensors, users, competing architectures
```
*Source: `domain-runner/README.md` §"Repository role"; each domain's `pyproject.toml`
depends on both `domain-runner` and `tattletots` as git dependencies.*

### 1.1 TattleTots

**Name and tagline.** "TattleTots — Domain-agnostic simulation engine for dual-currency
information ecologies." (`README.md`, title and subtitle.)

**Purpose.** The README states that TattleTots "models populations of
information-processing agents (\"Tots\") that compete in an evolutionary ecology with two
survival currencies: information (can you compress data?) and attention (do humans care
about your reports?)". The engine is deliberately domain-free: physics, sensors and human
users are supplied by an adapter, and the engine contributes selection, reproduction,
reporting economics and telemetry.

**Codebase.**

| Aspect | Detail | Source |
|---|---|---|
| Primary language | Python (18,947 tracked lines across 115 files) | `cloc` |
| Requires | Python ≥3.11 | `pyproject.toml` |
| Dependencies | `numpy`, `scipy`, `pydantic>=2`, `networkx`, `domain-runner` (git); optional `cupy-cuda12x` for GPU | `pyproject.toml` |
| Dev tooling | pytest, pytest-cov, ruff, mypy, pre-commit | `pyproject.toml` `[project.optional-dependencies].dev` |
| Package layout | `src/tattletots/{models,engine,interface,scenarios,telemetry}/`, `cli.py` | repository tree |
| Entry point | console script `tattletots = "tattletots.cli:main"` | `pyproject.toml` `[project.scripts]` |
| Reproducible install | `uv sync --locked --no-build …` then `uv run --no-sync tattletots …` (the README pins `uv` because two dependencies are git sources) | `README.md` Quick Start |

CLI examples from the README:

```bash
tattletots --scenario gaussian_shift --steps 400 --verbose
tattletots --config configs/gaussian_shift_default.json --verbose
```

**Documentation inventory.** 34 Markdown files. `AGENTS.md`, `CONTRIBUTING.md`,
`CHANGELOG.md`, `CODE_OF_CONDUCT.md`, a PR template, and a `docs/` directory that is
unusually measurement-oriented: `docs/theory.md`, `docs/architecture.md`,
`docs/domain_integration.md`, `docs/COORDINATION.md`, plus paired
measurement-report/measurement-data files (`docs/ceiling-measurement.md` +
`.json`, `docs/false-alarm-pricing.md` + `.json`, `docs/payoff-coupling.md` + `.json`,
`docs/threshold-calibration.md` + `.json`, `docs/heritability-measurement.md`,
`docs/reporting-opportunity-measurement.md`, `docs/currency-coupling-diagnosis.md`,
`docs/domain-richness-requirement.md`, `docs/cross-domain-grounding.md`,
`docs/initiation.md`). Root-level specifications: `ecology_dual_currency_model.md`,
`tattletots_plan.md`, `tattletots_requirements.md`. Five agent skills live in
`.agents/skills/` (`ci-test-design`, `dev-workflow`, `domain-adapter-guide`,
`download-deepwiki`, `sonar-quality`).

**Quality and maturity.**

| Metric | Value |
|---|---|
| Tracked LOC | Python 18,947; JSON 18,401; Markdown 3,484; YAML 192; TOML 118; shell 18 — **41,160 total** |
| Test files / functions | 38 / 381 |
| `pytest --collect-only` | **443 tests** |
| CI (`ci.yml`) | `lint`, `sonar-guard`, `typecheck`, `test`, `smoke`, `workflows`, `sonar` |
| Lint / types | Ruff + mypy (`pyproject.toml`), `.pre-commit-config.yaml`, `sonar-project.properties` |
| License | Apache-2.0 (`LICENSE`, and `license = "Apache-2.0"` in `pyproject.toml`) |
| Git | 196 commits, 2026-06-06 → 2026-08-16, 3 authors, 133 commits in the last 30 days |
| Version / status | `version = "0.1.0"`, classifier `Development Status :: 3 - Alpha` |

Maturity reading: **the most "finished-feeling" of the research engines below Crusher.**
Alpha by its own metadata, but it has a dedicated `smoke` CI job, a `sonar-guard` job that
runs before the analysis job, three independent domains consuming it, and a documentation
set organised around falsifiable measurements rather than feature descriptions.

### 1.2 domain-runner

**Name and tagline.** "domain-runner — Layer-agnostic **single** and **batch** simulation
runners shared by domain repositories (fire ecology, grain guard, reef watch, etc.)."
(`README.md`, first two lines.)

**Purpose.** The README defines a small contract: domains implement *hooks* (adapter
factory, metrics, config) and an optional *layer* sits above the adapter — `domain_only`
advances just the domain, `tattletots` is supplied by the engine package. The stated design
goal is that "future layers (new agent ecologies, human-in-the-loop stacks, etc.) implement
the same `SimulationLayer` protocol without changing domain physics code."

**Codebase.**

| Aspect | Detail | Source |
|---|---|---|
| Primary language | Python (1,046 tracked lines across 11 files) | `cloc` |
| Dependencies | **none** at runtime (`dependencies = []`); dev extra is pytest, pytest-cov, ruff | `pyproject.toml` |
| Layout | `src/domain_runner/` (`layer.py`, `single.py`, `batch`, `types.py`), `tests/`, `scripts/` | repository tree, README usage example |
| Entry point | library only — no `[project.scripts]`; consumers call `run_simulation(hooks, layer, run)` | `pyproject.toml`, README |
| Install as dependency | `"domain-runner @ git+https://github.com/bckirkup/domain-runner.git"` | README §Install |

**Documentation inventory.** 6 Markdown files: `README.md`, `AGENTS.md`, `LICENSE.md`, and
three agent skills (`domain-runner`, `download-deepwiki`, `sonar-quality`). No `docs/`
directory — appropriate for a 1,000-line library whose contract fits in one README.

**Quality and maturity.**

| Metric | Value |
|---|---|
| Tracked LOC | Python 1,046; Markdown 465; YAML 134; TOML 46 — **1,691 total** |
| Test files / functions | 2 / 3 (`tests/test_batch.py`, `tests/test_runner.py`); `pytest --collect-only` confirms **3** |
| CI (`ci.yml`) | `lint`, `test`, `guards`, `workflow-lint`, `sonar` |
| Lint / types | Ruff with `select = ["E","F","W","I","UP","B","SIM","ARG","C901","N"]` and `max-complexity = 10`; pre-commit; Sonar. **No mypy config** |
| License | Apache-2.0 — declared twice, in `LICENSE` and `LICENSE.md` |
| Git | 22 commits, 2026-06-20 → 2026-08-15, 1 author |
| Version / status | `0.1.0`, `Development Status :: 3 - Alpha` |

Maturity reading: **small, stable, and the least-tested link in the ecosystem.** Three
tests guard a component that all three domain repositories import; the same five-job CI
template as its siblings runs over it, but coverage is thin relative to its blast radius.

### 1.3 Scrapiron_and_the_Bear (FireEcology)

**Name and tagline.** "Scrapiron and the Bear — FireEcology Domain Simulation … A testbed
for TattleTots: autonomous fire-regime management with physical drone Tots." (`README.md`.)

**Purpose.** Wildfire-regime management as a TattleTots domain: active-fire detection,
dry-fuel monitoring, fire-weather indexing, controlled-burn monitoring, autonomous drone
suppression, human-response escalation, and an OPIR satellite backstop against which the
self-organising ecology is scored.

**Codebase.**

| Aspect | Detail | Source |
|---|---|---|
| Primary language | Python (7,450 tracked lines across 63 files) | `cloc` |
| Dependencies | numpy, pydantic, `domain-runner` and `tattletots` git dependencies; GPU extra | `pyproject.toml` |
| Layout | `src/fire_ecology/{environment,sensors,drones,users,architectures,adapter,metrics,scenarios}/`, `cli.py` | README §Architecture |
| Entry point | `fire-ecology = "fire_ecology.cli:main"` | `pyproject.toml` |

```bash
fire-ecology sim --layer domain_only --steps 200 --verbose
fire-ecology batch --config configs/batch_example.json
fire-ecology sim --layer tattletots --config configs/tattletots_integration.json
```
*Source: `README.md` Quick Start / Integrated Mode.*

**Documentation inventory.** 14 Markdown files plus a large committed measurement corpus:
`README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `baselines/README.md`,
`docs/COORDINATION.md`, `docs/designed_reporter_measurement.md` (+ `.json` and a
`docs/designed_reporter/` directory of four scenario JSONs),
`docs/fire_sensor_rebaseline.md` (+ `.json`), `docs/opir_ablation_grounded_access.md` with
a 31-file `docs/grounded_access/` sweep (three ground-truth-informed fractions × ablated /
assisted OPIR × five seeds, plus `summary.json`). Root specs:
`fire_tots_spec_v2.md`, `domain_master_plan_v2.md` (the cross-domain plan shared verbatim
with Xylella and Coral Key). Skills: `ci-test-design`, `download-deepwiki`, `fire-ecology`,
`sonar-quality`.

**Quality and maturity.**

| Metric | Value |
|---|---|
| Tracked LOC | **JSON 210,953**; Python 7,450; Markdown 1,497; YAML 158; TOML 88 — 220,146 total |
| Test files / functions | 19 / 222; `pytest --collect-only` → **229** |
| CI (`ci.yml`) | `lint`, `typecheck`, `test`, `guards`, `workflow-lint`, `sonar` |
| Lint / types | Ruff, mypy, pre-commit (ruff, ruff-format, mypy, sonar guards, zizmor), Sonar |
| License | Apache-2.0 (`LICENSE` + `pyproject.toml`) |
| Git | 86 commits, 2026-06-06 → 2026-08-16, 3 authors, 42 in the last 30 days |
| Version / status | `0.1.0`, `Development Status :: 3 - Alpha` |

Maturity reading: **alpha code, publication-grade experiment discipline.** The ratio of
committed measurement JSON (211k lines) to source (7.5k lines) is 28:1, which says the
repository's real product is the measurement record, not the library.

### 1.4 Xylella_SPQR (GrainGuard)

**Name and tagline.** "Xylella_SPQR (GrainGuard) — **Precision pest and weed management
domain simulation for TattleTots.**" (`README.md`.)

**Purpose.** The README states GrainGuard "tests whether a self-organizing drone/sensor
ecology (BMA) can manage crop pests and weeds more cost-effectively than centralized
precision agriculture platforms, by adapting to local heterogeneity, seasonal drift, and
co-evolutionary pest response faster than centralized systems." Its falsification test
(README §"Falsification Test (Spec §10)") is explicit: the ecology must match yield
protection with less pesticide **and** slower resistance evolution than a centralised
platform receiving the same sensor data.

Modelled features include a 1-locus resistance allele plus behavioural escape
(night-feeding, underside preference, edge refuge), three landscape variants
(monoculture → orchard → intercrop), five physical Tot body plans, six sensor types, and
an economic-injury-level model `EIL = C / (V × D × I × K)`. Five competing architectures
A0–A4 are scored against each other (human IPM, AI tractor, prescription drone,
centralised platform, and the TattleTots ecology).

**Codebase.**

| Aspect | Detail | Source |
|---|---|---|
| Primary language | Python (7,379 tracked lines across 67 files); requires ≥3.11 | `cloc`, `pyproject.toml` |
| Dependencies | numpy, pydantic, `domain-runner`, `tattletots`; `gpu` extra adds `cupy-cuda12x` | `pyproject.toml` |
| Layout | `src/grain_guard/{adapter,environment,sensors,equipment,users,architectures,metrics,scenarios}/`, `cli.py` | README §Architecture |
| Entry point | `grain-guard = "grain_guard.cli:main"` | `pyproject.toml` |

```bash
grain-guard sim --layer domain_only --steps 200 --verbose
grain-guard batch --config configs/batch_example.json
grain-guard sim --layer tattletots --config configs/tattletots_integration.json --output results.json --verbose
```

**Documentation inventory.** 15 Markdown files: `README.md`, `AGENTS.md`,
`CONTRIBUTING.md`, `baselines/README.md`, `docs/COORDINATION.md`,
`docs/designed_reporter_measurement.md` (+ `.json`), `docs/grain_detector_gradient.md`
with a six-file JSON gradient sweep, `docs/grain_instrument_rebaseline.md` (+ `.json`),
and the two root spec documents the README links as canonical:
`grain_tots_spec_v2.md` (full domain spec) and `domain_master_plan_v2.md` (cross-domain
comparison plan). Skills: `ci-test-design`, `download-deepwiki`, `grain-guard`,
`measurement-harness-testing`, `sonar-quality`.

**Quality and maturity.**

| Metric | Value |
|---|---|
| Tracked LOC | JSON 70,166; Python 7,379; Markdown 1,483; YAML 155; TOML 90 — 79,273 total |
| Test files / functions | 19 / 250 |
| `pytest --collect-only` | **209** collected with 3 collection errors in this workspace's `.venv` (missing optional imports locally); CI runs the suite plus a separate `-m smoke` step |
| CI (`ci.yml`) | `lint`, `typecheck`, `test` (with coverage upload + smoke step), `guards`, `workflow-lint`, `sonar` |
| Lint / types | Ruff (`max-complexity = 10`), **mypy `strict = true`**, pre-commit with a local mypy hook, Sonar (`sonar.sources=src,scripts,baselines`) |
| License | Apache-2.0 (`LICENSE`, `pyproject.toml`, README §License) |
| Git | 90 commits, 2026-06-07 → 2026-08-16, 2 authors, 51 in the last 30 days |
| Version / status | `0.1.0`, `Development Status :: 3 - Alpha` |

Maturity reading: **the most type-disciplined domain adapter** — strict mypy plus a
complexity ceiling of 10, with a `measurement-harness-testing` skill codifying how its
experiments are validated.

### 1.5 Coral_Key_in_Three_Hour_Epochs (ReefWatch)

**Name and tagline.** "ReefWatch — a fishery monitoring, IUU detection, and ocean sensor
ecology domain adapter for the TattleTots simulation engine." (`README.md`.)

**Purpose.** The README describes a marine protected area surrounded by legal fishing
grounds, used to test "whether a TattleTots information ecology can improve fishery
monitoring and IUU (Illegal, Unreported, Unregulated) detection in a mixed
ecological-adversarial domain." Model elements: Schaefer logistic stock dynamics, a mixed
legal/gaming/IUU fleet, six sensor modalities, adversarial AIS disabling and spoofing,
catch under-reporting, and three human user profiles. The three-hour epoch in the
repository name is the simulation tick.

**Codebase.**

| Aspect | Detail | Source |
|---|---|---|
| Primary language | Python (5,816 tracked lines across 51 files) | `cloc` |
| Dependencies | numpy, pydantic, `domain-runner`, `tattletots`; optional CuPy | `pyproject.toml` |
| Layout | `src/coral_key/{ocean,fleet,sensors,adversary}/` plus `adapter.py`, `config.py`, `users.py`, `metrics.py`, `cli.py` | repository tree |
| Entry point | `coral-key = "coral_key.cli:main"` | `pyproject.toml` |

```bash
coral-key sim --layer domain_only --epochs 200 --verbose
coral-key batch --config configs/batch_example.json
coral-key --config scenario.json --output results.json
```

**Documentation inventory.** 13 Markdown files: `README.md`, `AGENTS.md`,
`CONTRIBUTING.md`, `baselines/README.md`, `docs/COORDINATION.md`,
`docs/designed_reporter_measurement.md` (+ `.json`), a 16-file
`docs/grounded_access/` sweep keyed by ground-truth fraction and monitoring level
(`f0_m1_k3__*`, `f0_m3_k3__*`, `f0p34_m1_k3__*`, `f0p67_m1_k3__*` × ordinary / invasion /
oracle_upper_bound / all_designed_seed), root specs `ecology_reef_tots_spec_v2.md` and
`domain_master_plan_v2.md`. Skills: `ci-test-design`, `coral-key`, `download-deepwiki`,
`sonar-quality`, plus a legacy `.devin/skills/SKILL.md`.

**Quality and maturity.**

| Metric | Value |
|---|---|
| Tracked LOC | **JSON 242,714**; Python 5,816; Markdown 1,471; YAML 150; TOML 89 — 250,240 total (the largest tracked line count in the portfolio, 98% of it data) |
| Test files / functions | 25 / 137; `pytest --collect-only` → **146** |
| CI (`ci.yml`) | `lint`, `typecheck`, `test`, `guards`, `workflow-lint`, `sonar` |
| Lint / types | Ruff, mypy, pre-commit, Sonar |
| License | ⚠️ **inconsistent**: `LICENSE` is the Apache-2.0 text, while `pyproject.toml` says `license = "MIT"` with an MIT classifier and README §License says "MIT" |
| Git | 100 commits, 2026-06-07 → 2026-08-16, 3 authors, 57 in the last 30 days |
| Version / status | `0.1.0`, `Development Status :: 3 - Alpha` |

Maturity reading: **alpha, actively developed, with one packaging defect** — the licence
disagreement should be resolved before anyone consumes the package, since Apache-2.0 and
MIT differ in patent and notice obligations.

### 1.6 Ecosystem-level observations

- **The adapter template is real.** Scrapiron, Xylella and Coral Key share the same CI job
  list (`lint`, `typecheck`, `test`, `guards`, `workflow-lint`, `sonar`), the same
  pre-commit stack (ruff, ruff-format, optional mypy, `sonar-mechanical-guards`,
  `sonar-workflow-guards`, `zizmor`), the same `docs/COORDINATION.md` and
  `docs/designed_reporter_measurement.md` pattern, the same `baselines/README.md`, and a
  byte-shared `domain_master_plan_v2.md`.
- **Dependencies are git-pinned, not versioned.** All three domains depend on
  `domain-runner` and `tattletots` via `git+https://…` with no tag or commit pin
  (`pyproject.toml`, `[tool.hatch.metadata] allow-direct-references = true`), so a domain
  build resolves to whatever is on the engine's default branch at install time. TattleTots
  mitigates this for itself with a `uv.lock`-based install path in its README.
- **Test mass sits in the engine, not the runner.** 381 + 250 + 222 + 137 test functions in
  engine and domains versus 3 in the shared runner.

---

## 2. Epidemiology and microbiome

Four repositories about pathogens and microbial communities at four different scales: a
whole ship (Crusher), a mammalian gut lumen (GutIBM), a town of 250,000 people (GARLAND),
and a sequencing sample (shipbiome-core).

### 2.1 Crusher_to_the_Bridge

**Name and tagline.** "Crusher to the Bridge — An epidemiological testbed that bridges a
shipboard agent-based outbreak simulation with microbiome simulation and biosurveillance
diagnostics." (`README.md`, first paragraph.)

**Purpose.** The README describes a unified digital twin for maritime disease outbreaks
that integrates five external model traditions: **infection-dynamics** (the agent-based
model), **py-contam** (HVAC/airborne transport), **FRED-style behavioural compliance**,
**EMOD-style clinical progression**, and **GRUMB multi-kingdom microbiome** seeding. Above
the ship layer sit two further layers named in the README: `Picard_Framework` (ship-level
steppable simulation and cruise runs) and `Presidio` (fleet meta-simulation with
experience storage and Stackelberg utility export), plus a `decision_engine` implementing
threshold-belief policies.

**Codebase.**

| Aspect | Detail | Source |
|---|---|---|
| Primary language | Python (70,190 tracked lines across 319 files), Python ≥3.11 | `cloc`, README Quick Start |
| Dependency management | `requirements.txt` **and** `requirements.lock.txt` alongside `pyproject.toml` | repository root |
| Top-level packages | `engines/`, `crusher_labs/`, `picard_framework/`, `decision_engine/`, `presidio/`, `dashboard/`, `simulation_utils/`, `schemas/`, `data/`, `deploy/aws/`, `scripts/`, `tools/` | repository tree |
| Entry points | `orchestrator.py` (plus `orchestrator_{chronic,display,epoch,init,record,types}.py`), `presidio_runner.py`, `dashboard.py` (Streamlit LCARS dashboard), `tools/sanity_checker.py`, `run_campaign.sh` / `.bat` | repository tree |
| Console scripts | `crusher-orchestrator = "orchestrator:run"`, `crusher-presidio = "presidio_runner:main"` | `pyproject.toml` |
| Containerisation | root `Dockerfile` plus a second deploy image, AWS Batch campaign tooling under `deploy/aws/` | repository tree, `docker-campaign-smoke` CI job |

```bash
python3 tools/sanity_checker.py --from-config    # validate JSON + crusher_labs/config.yaml
python3 orchestrator.py                          # 24-epoch default run
python3 orchestrator.py --epochs 250
python3 -m streamlit run dashboard.py            # LCARS dashboard
python3 -m pytest tests/ -v --tb=short
```
*Source: `README.md` Quick Start. Simulation output lands in
`telemetry_buffer/simulation_history.json` and `telemetry_buffer/artificial_lab_notebook.json`,
which the README notes are gitignored runtime artefacts.*

**Documentation inventory.** By far the largest documentation set in the portfolio: **91
Markdown files (12,124 lines)**, plus LaTeX report sources and PDFs/DOCX review artefacts.
Highlights:

- Root governance: `README.md`, `AGENTS.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`,
  `SECURITY.md`, `citation.cff.txt`, issue and PR templates.
- `docs/README.md` is a documentation map (the README points to it explicitly).
- Operator manuals: `docs/OPERATORS_MANUAL.md`, `…_SHIP.md`, `…_GAME_THEORY.md`.
- Specifications: `docs/density_contact_spec.md`, `docs/medical_response_spec.md`,
  `docs/multi_pathogen_model_changes_spec.md`,
  `docs/preboarding_wearable_decision_model_spec.md`, `docs/instrument_parameterization.md`
  and `_v2`, `docs/tiered_escalation_spec.md` (linked from the README).
- Audits and reviews: `docs/MATHEMATICAL_FIDELITY_AUDIT.md`, `docs/CONTAM_PRJ_AUDIT.md`,
  `docs/clinical_dx_review.md`, `docs/WEARABLE_ANOMALY_REDESIGN.md`,
  `docs/SOP_CASCADE_RECONFIG.md`, `docs/boundary_aws_pipeline_lessons.md`.
- Manuscript pipeline: `docs/reports/*.tex` (architecture, VSP, interventions) with
  generated PDFs and reviewer DOCX files.
- Data-side READMEs: `data/templates/`, `data/contam_hobbyist/`, `deploy/aws/`,
  `_epoch_timing/`.
- **30 agent skills** in `.agents/skills/` — the largest such collection here — covering
  pathogen and platform authoring, AWS Batch campaigns, ContamX interop, diagnostic
  cascade, Stackelberg configuration, dashboard testing, schema validation and issue
  triage.

**Quality and maturity.**

| Metric | Value |
|---|---|
| Tracked LOC | Python 70,190; JSON 127,706; Markdown 12,124; YAML 1,153; TeX 673; PowerShell 481; shell 464; TOML 109; DOS batch 98; Dockerfile 59 — **213,066 total** across 651 files |
| Test files / functions | 104 / 1,311 |
| `pytest --collect-only` | **1,512 tests collected** (one module, `tests/test_download_boundary_results.py`, fails to collect in this workspace because an AWS-side optional dependency is absent) |
| README claim | "~900 tests" (Quick Start) and "~875 tests" (three further places). **Both are stale**: the measured suite is ~1.5k collected tests, 1.7× the documented figure |
| CI | `ci.yml` with 14 jobs: `lint`, `sonar-mechanical-guard`, `workflow-lint`, `sanity-checker`, `schema-validation`, `test`, `import-hygiene`, `presidio-smoke`, `sentinel-smoke`, `orchestrator-import-hygiene`, `dashboard-import`, `orchestrator-smoke`, `docker-campaign-smoke`, `sonar`; plus `picard-presidio.yml` (`framework`) |
| Lint / types | Ruff via pre-commit and a scoped CI invocation, custom `scripts/sonar_guard.py` (source and workflow modes), coverage via `pytest --cov`, SonarQube. **No mypy** |
| Notable | `AGENTS.md` records that `pre-commit run --all-files` is *not* a useful local gate because of a pre-existing C901 complexity backlog (measured max 117); new-code complexity is enforced by Sonar's new-code gate instead |
| License | MIT (`LICENSE`, `pyproject.toml` `license = {text = "MIT"}`) |
| Git | **565 commits**, 2026-05-23 → 2026-08-16, 4 authors, 293 commits in the last 30 days (92 in the last 7), 213 merges |
| Version / status | `0.1.0` in packaging metadata, which badly understates the artefact |

Maturity reading: **the most mature repository in the portfolio by every measure except its
version string.** It has the widest CI surface (smoke tests for the orchestrator, the
dashboard import, Presidio, the sentinel, and a Docker campaign), the largest test suite,
schema validation as a gate, a security policy, a citation file, cloud deployment tooling,
and a manuscript pipeline. The main documentation debt is the repeated stale test count.

### 2.2 GutModelBacteriocins (GutIBM)

**Name and tagline.** "GutIBM — 3D Individual-based Model for Enterobacteriaceae Gut
Dynamics … A massively parallel, 3D Individual-based Model (IbM) built to solve the
*Enterobacteriaceae* 'diversity paradox' in the mammalian gut." (`README.md`.)

**Purpose.** The README frames a specific scientific puzzle: spatial fragmentation in the
gut should support high diversity, yet empirical data show limited coexistence and
monochromatic strain clustering. GutIBM integrates mucus fluid dynamics, bacteriocin
diffusion, and metabolic trade-offs governed by TonB-dependent transporters, synthesising
two named theoretical frameworks — **EARI** (Eco-Advective Receptor Interference) and
**VADI** (Viscous Advective-Diffusion Interference), each with its own root-level blueprint
document.

Architecturally it follows **NUFEB-2**'s LAMMPS-inspired modular `Fix` philosophy, with
four deliberate departures documented in the README's design-decision table: QSSA +
Green's-function diffusion kernels instead of explicit FTCS (no CFL constraint), a
Viscoelastic Background Field continuum instead of discrete background flora, decoupled
timescales (biology 60 s → instantaneous QSSA chemistry → physics 60 s), and spatial
hashing for O(N) neighbour queries.

**Codebase.**

| Aspect | Detail | Source |
|---|---|---|
| Primary language | C++ (30,286 lines / 127 files) with C/C++ headers (3,813 / 70) and CUDA (1,542 / 10); Python (6,238 / 40) for analysis and tooling; shell (3,461 / 25) for campaign scripts | `cloc` |
| Build system | CMake (`CMakeLists.txt`, 337 lines of CMake); options `GUTIBM_USE_MPI`, `GUTIBM_USE_HDF5`, `GUTIBM_USE_OPENMP`, CUDA | root `CMakeLists.txt` |
| Parallelism | MPI domain decomposition, optional OpenMP, optional CUDA GPU kernels (`src/gpu/`) | README, `src/` tree, CI `gpu-parity`/`cuda-compile` jobs |
| Layout | `src/{core,diffusion,fields,fixes,genome,gpu,io}/` + `main.cpp`; `python/gut_ibm_tools/` (installable via `python/setup.py`); `tests/`; `examples/`; `experiments/`; `scripts/`; `deploy/aws/`; `sonar/` | repository tree |
| Entry point | `gut_ibm <config.json>` binary (`add_executable(gut_ibm src/main.cpp …)`), e.g. `./build/gut_ibm examples/single_colony/input.json`; plus a Python batch runner and analysis CLI in `python/gut_ibm_tools/` | `CMakeLists.txt`, `examples/*/README.md` |
| Typical build | `cmake -S . -B build -DGUTIBM_USE_MPI=ON -DGUTIBM_USE_HDF5=ON && cmake --build build -j`, then `ctest --test-dir build` | README / `AGENTS.md` |

**Documentation inventory.** 50 Markdown files (8,878 lines), organised as a real
handbook:

- Root: `README.md`, `AGENTS.md` (developer/agent guidelines, CI map, "known landmines"),
  `EARI.md`, `VADI.md`, and **five numbered specification documents** —
  `GutIBM Spec 1_ Chemical Environment.md`, `Spec 2_ Bacteriocin Induction.md`,
  `Spec 3_ Cell Biology.md`, `Spec 4 v2_ Mechanistic Gaps + Output Schedule.md`,
  `Spec 5_ Species Wiring Fixes.md`.
- `docs/`: `CONFIG_FORMAT.md`, `PARAMETERS.md`, `API.md`, `MECHANISMS.md`, `SCALING.md`,
  `BATCH_RUNNER.md`, `AWS_BATCH.md`, `AWS_CALIBRATION_6H.md`,
  `BRANCHING_FROM_CHECKPOINTS.md`, `CARBON_BUDGET.md`, `COHERENCE_DIAGNOSIS.md`,
  `COLONY_OBSERVABLES.md`, `MULTI_SCALE_EXPERIMENTATION.md`, `OPERATING_ENVELOPE.md`,
  `PRE_SUBMISSION_CHECKLIST.md`, `PROJECT_BOARD.md`,
  `RECEPTOR_LIGAND_PARAMETERIZATION.md`, `SONARQUBE_PLAN.md`, `T2_COLONY_CHALLENGE.md`,
  `TOXIN_SENTINEL.md`, `UNITS_AUDIT.md`, `WIRING_AUDIT.md`, `WSL2_SETUP.md`.
- Per-example READMEs for six runnable examples (`single_colony`, `diversity_paradox`,
  `cell_biology`, `batch_scan`, `eari_vadi_validation`, `immigration_fork`) plus
  `experiments/` and `experiments/diversity_campaign/`.
- Eight agent skills, including `gut-ibm`, `testing-gutibm`, `gutibm-campaign-ops`, and
  three SonarQube-specific ones (`sonarqube-cpp`, `sonarqube-python`, `sonarqube-gutibm`).

**Quality and maturity.**

| Metric | Value |
|---|---|
| Tracked LOC | C++ 30,286; Markdown 8,878; Python 6,238; headers 3,813; shell 3,461; JSON 3,268; CUDA 1,542; CMake 337; PowerShell 298; YAML 177; Dockerfile 53 — **58,351 total** across 408 files |
| C++ tests | 78 tracked `tests/*.cpp` files containing **393 `void test_*()` functions**; **86 `add_test(...)` registrations** in `tests/CMakeLists.txt`. The suite is hand-rolled (`<cassert>` + `int main`), not GoogleTest — a `TEST`/`TEST_F` grep returns zero matches |
| Python tests | 18 files / 130 functions under `python/tests/` (local `pytest` collection needs `h5py`, absent in this workspace) |
| Shell tests | `tests/test_aws_capacity_script.sh`, `tests/test_checkpoint_retention.sh` |
| CI (`ci.yml`) | 8 jobs: `unit-tests`, `serial-build`, `integration-tests`, `openmp-parity`, `gpu-parity`, `cuda-compile`, `eari-vadi-validation`, `python-lint` — i.e. numerical **parity** checks between serial/OpenMP and CPU/GPU paths are gates, not afterthoughts |
| Lint / types | Ruff for `python/`; compiler warnings (`-Wall -Wextra`) as the C++ lint gate; `sonar-project.properties` plus a `sonar/` directory and `docs/SONARQUBE_PLAN.md`. No pre-commit config |
| License | Apache-2.0 (`LICENSE`); README §License defers to the file |
| Git | **631 commits** (the most in the portfolio), 2026-06-16 → 2026-08-16, 4 authors, 343 in the last 30 days, 275 in the last 7 |
| Version / status | "**Version:** 0.1.0 (research prototype — see AGENTS.md for HPC/MPI scaling notes)" |

Maturity reading: **the highest-velocity repository and the most demanding to operate.**
It is self-labelled a research prototype, but it has HPC-grade CI (multi-rank MPI, OpenMP
and GPU parity), a documented operating envelope, checkpoint-branching support, and AWS
campaign tooling with a carbon budget document. Its main fragility is environmental rather
than logical: MPI/CUDA/HDF5 build permutations mean local runs need specific toolchain
combinations.

### 2.3 Garlic-Routed-Local-Area-Network-Domain (GARLAND)

**Name and tagline.** "GARLAND — The Privacy-Protecting Body Area Network Based Public
Health Reference Architecture." (`README.md` title.)

**Purpose.** The README describes "a high-performance, privacy-preserving Epidemiological
Security Testbed simulation built on Mesa ABM, custom NumPy biometric synthesis (inspired
by NeuroKit2 statistical principles), and OpenWearables data schema conventions."
Scale is a stated design target: **a town of 250,000 agents at 5-minute resolution.** Four
layers are modelled — the `CitizenAgent` edge device, a hazard engine with SEIR and
Gaussian plume models, a decentralised privacy protocol, and an attack simulation that
tries to re-identify or degrade it.

**Codebase.**

| Aspect | Detail | Source |
|---|---|---|
| Primary language | Python (18,394 tracked lines across 67 files) | `cloc` |
| Dependencies | Mesa, NetworkX, NumPy, Pandas, Matplotlib, PyYAML, H3; optional NeuroKit2 and SciPy | `pyproject.toml` |
| Reproducibility | `uv.lock` committed | repository root |
| Layout | flat, module-per-concern `src/garland/`: `agents.py`, `app.py`, `simulation.py`, `hazards.py`, `pathogens.py`, `biometric_synthesis.py`, `biometric_profiles.py`, `biometrics.py`, `modality_signatures.py`, `devices.py`, `device_lifecycle.py`, `channels.py`, `privacy.py`, `attacks.py`, `detection.py`, `disambiguation.py`, `thresholds.py`, `confounders.py`, `perturbations.py`, `adoption.py`, `venues.py`, `spatial.py`, `metrics.py`, `experiment.py`, `benchmark.py`, `openwearables.py`, `config.py`, `constants.py`, `paths.py`, `data/` | repository tree |
| Entry point | `garland = "garland.app:main"` | `pyproject.toml` `[project.scripts]` |

**Documentation inventory.** 29 Markdown files: `README.md`, `AGENTS.md`,
`CONTRIBUTING.md`, `CHANGELOG.md`, `examples/README.md`, and a domain-reference `docs/`
set — `docs/BIOMETRICS.md`, `docs/EPIDEMIOLOGY.md`, `docs/EVENT_CATALOGUE.md`,
`docs/OPERATIONAL_DETECTION.md`, `docs/SENSOR_MODALITIES.md`, `docs/SCALING.md`. Nine
agent skills in `.agents/skills/` (`garland-architecture`, `garland-development`,
`garland-testing`, `garland-privacy-protocol`, `garland-code-review`, `garland-issues`,
`ci-test-design`, `download-deepwiki`, `sonar-quality`), mirrored in a `.cursor/skills/`
tree that additionally carries `references/feature-backlog.md` and
`references/resolved-issues.md` — the closest thing in the portfolio to a wiki.

**Quality and maturity.**

| Metric | Value |
|---|---|
| Tracked LOC | Python 18,394; Markdown 2,889; YAML 1,070; JSON 164; TOML 78 — **22,595 total** |
| Test files / functions | 34 / 501 |
| `pytest --collect-only` | **523 collected** (1 deselected) — the highest test-to-source density in the portfolio (~2.8 tests per 100 Python lines) |
| CI | three workflows: `tests.yml` (`lint`, `typecheck`, `test`, `guards`, `workflow-lint`, `sonar`), `benchmark.yml` (`benchmark`), `stationarity.yml` (`stationarity`) |
| Lint / types | Ruff, mypy, pytest + coverage, pre-commit, SonarQube |
| Notable | The dedicated `benchmark` and `stationarity` workflows make performance-at-scale and statistical stationarity **continuous gates** rather than one-off studies |
| License | Apache-2.0 (`LICENSE`, `pyproject.toml`) |
| Git | 184 commits, 2026-06-16 → 2026-08-16, 3 authors, 113 in the last 30 days |
| Version / status | `0.1.0`, `Development Status :: 3 - Alpha` |

Maturity reading: **best-tested repository per line of code**, with the most interesting CI
idea in the portfolio (stationarity as a build gate). Alpha metadata, but the engineering is
closer to Crusher than to the domain adapters.

### 2.4 shipbiome-core

**shipbiome-core has no `README.md`** (confirmed via `git ls-files`: the only Markdown files
tracked are `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and `.agents/skills/ci-test-design/SKILL.md`).
The description below is therefore derived from module docstrings, `CONTRIBUTING.md`, and
the tracked file inventory, and every claim names its origin.

**Name and tagline.** "Shipbiome — Streamlit UI for exploring shipboard microbiome
simulation and source tracking" (module docstring, `shipbiome_app.py`), over a
"Shipboard Microbiome Study Design Simulator" (module docstring, `shipbiome_design.py`).

**Purpose.** From the `shipbiome_design.py` docstring: the module "provides a generative
data model to simulate shipboard microbiome data using a Dirichlet-Multinomial model. The
simulator generates synthetic microbiome samples by mixing evidence-based source profiles
representing different microbial environments relevant to shipboard settings." The same
docstring enumerates the four base source profiles and their provenance:

| Profile | Provenance (docstring) | Composition highlights |
|---|---|---|
| Human skin | public 16S rRNA, MGnify study `MGYS00001295` | 34 genera; *Propionibacterium* 64%, *Staphylococcus* 15% |
| Seawater | public 16S rRNA, MGnify study `MGYS00002552` | 74 genera; *Flavobacterium* 10%, Thermoplasmata 9% |
| Urban surfaces | public 16S rRNA, MGnify study `MGYS00005612` | 106 genera; *Pseudomonas* 8%, *Streptococcus* 7%, *Acinetobacter* 6% |
| Industrial | synthesised from industrial-microbiome literature | 6 genera: *Pseudomonas* 40%, *Methylobacterium* 20%, *Desulfovibrio* 10%, *Acinetobacter* 10%, *Sphingomonas* 10%, *Pelobacter* 10% |

The docstring also names the three public classes: `SourceProfiles` (manages the
evidence-based profiles), `DirichletMultinomialSimulator` (generates synthetic samples),
and `FEASTEstimator` (estimates source proportions from mixed samples). The purpose of the
package is therefore **study design**: generate realistic sink mixtures, then check whether
source-tracking can recover the mixing proportions you designed for.

`validate_expanded_profiles.py`'s docstring documents the extended profile set: it "loads
all 9 source profiles (bacteria, fungi, virome), verifies normalization and kingdom
representation, and generates Dirichlet-Multinomial samples using various mixtures to
confirm no index or alpha errors occur" — i.e. the repository has already moved from four
bacterial profiles to nine multi-kingdom ones.

**Contribution culture.** `CONTRIBUTING.md` is four lines long and worth quoting because it
explains the repository's shape: "The Prime Directive: Fix it, improve it, have fun. We
don't do 'processes.' We do engineering. … Rule 0: If you find a bug, don't just report
it—patch it. Run CI tests. Rule 1: Documentation is a courtesy and brevity is valuable."
Note that Rule 0 tells contributors to "run CI tests" in a repository that has **no CI and
no tests**.

**Codebase.**

| Aspect | Detail | Source |
|---|---|---|
| Primary language | Python — 3 tracked modules, 660 code lines (+246 comment lines, an unusually high 27% comment ratio) | `cloc` |
| Frameworks | `streamlit>=1.28.0`, `numpy>=1.24.0`, `plotly>=5.18.0`, `pypdf>=4.0.0` | `requirements.txt` (there is **no** `pyproject.toml` or `setup.py`) |
| Modules | `shipbiome_design.py` (model: profiles, Dirichlet-Multinomial sampler, FEAST estimator), `shipbiome_app.py` (Streamlit UI, Plotly figures, PDF ingestion via `pypdf`), `validate_expanded_profiles.py` (profile validation script) | module docstrings, imports |
| Data assets | `expanded_maritime_profiles.json` and `public_source_profiles.json` (528 JSON lines total), `Gleaves Crew.txt`, `RG19_ALPHA_Gleaves_DD423_02.jpg`, `kosmos_Maritime_Biodefense_Microbiome_Research_Framework.pdf` (loaded by the app as `FRAMEWORK_PDF`) | `git ls-files`, `shipbiome_app.py` |
| Entry points | `streamlit run shipbiome_app.py` (stated in the app docstring: "Run from this folder"); `python shipbiome_design.py` exercises the model directly; `python validate_expanded_profiles.py` validates profiles | module docstrings |
| Hygiene issue | `__pycache__/shipbiome_app.cpython-312.pyc` and `__pycache__/shipbiome_design.cpython-312.pyc` are **tracked in git** | `git ls-files` |

**Documentation inventory.** `CONTRIBUTING.md` (4 lines), `CODE_OF_CONDUCT.md`, and one
agent skill, `.agents/skills/ci-test-design/SKILL.md` — the same shared skill that eight
other repositories carry, describing how to write graded-sensitivity and
bounds/invariant tests. No `README.md`, no `docs/`, no `AGENTS.md`, no ADRs.

**Quality and maturity.**

| Metric | Value |
|---|---|
| Tracked LOC | Python 660; JSON 528; Markdown 200 — **1,388 total** across 8 files |
| Tests | **0** test files, 0 test functions |
| CI | **none** — `.github/` does not exist |
| Lint / types / Sonar / pre-commit | **none** — no `pyproject.toml`, no ruff/mypy config, no `.pre-commit-config.yaml`, no `sonar-project.properties` |
| License | MIT (`LICENSE`) |
| Git | 10 commits, 2026-05-16 → 2026-08-12, 2 authors, 2 commits in the last 30 days — the least active repository |
| Version / status | no version declared anywhere; effectively an **early prototype / demo app** |

Maturity reading: **the portfolio's outlier.** The science content is well documented inside
the code (provenance-cited source profiles, a stated model, a validation script), but every
engineering guardrail the other eleven repositories share is missing here, and committed
`.pyc` files suggest the repository was seeded by copying a working directory. The cheapest
high-value work in the whole portfolio is here: add a README derived from the existing
docstrings, add a `pyproject.toml`, port the sibling `ci.yml` template, and turn
`validate_expanded_profiles.py` into `tests/` using the `ci-test-design` skill that is
already checked in.

---

## 3. Imaging and applications

### 3.1 Anaglyph

**Name and tagline.** "Anaglyph — Live 3D red-cyan anaglyph compositing from dual-camera
stereoscopes." (`README.md`.)

**Purpose.** The README describes software that "manages two AmScope MD500L cameras
(left/right stereo pair) and an optional AmScope MU503 (top-down USB 3.0 camera) attached
to a trinocular stereoscope", composites the stereo pair into a live red-cyan anaglyph, and
supports calibration and recording. It is the only repository in the portfolio whose
primary function is driving physical hardware.

**Codebase.**

| Aspect | Detail | Source |
|---|---|---|
| Primary language | Python (3,604 tracked lines across 16 files) | `cloc` |
| Dependencies | `opencv-python`, `numpy`, `PyQt6` | `pyproject.toml` |
| Modules | `main.py` (CLI), `camera_manager.py`, `gui.py`, `compositor.py`, `video_recorder.py`, `calibration.py`, `tests/` | repository tree, README |
| Entry points | `python main.py --verify` (hardware check), `python main.py --gui`; console script `anaglyph = "main:main"` | README, `pyproject.toml` |

**Documentation inventory.** 11 Markdown files: `README.md`, `AGENTS.md`,
`CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and a four-document `docs/` set —
`docs/architecture.md`, `docs/development_plan.md`, `docs/hardware_guide.md`,
`docs/calibration_guide.md`. The hardware guide matters more here than elsewhere: the
software is unusable without the specific camera models. Three agent skills: `anaglyph`,
`ci-test-design`, `sonar-quality`. The README carries a `## Roadmap` section, the only
explicit roadmap heading among the Python repositories.

**Quality and maturity.**

| Metric | Value |
|---|---|
| Tracked LOC | Python 3,604; Markdown 921; YAML 124; TOML 66 — **4,715 total** across 30 files |
| Test files / functions | 10 / 97; `pytest --collect-only` → **97** (all pass collection locally; the suite mocks the cameras) |
| CI (`ci.yml`) | `lint`, `test`, `guards`, `workflow-lint`, `sonar` |
| Lint / types | Ruff + mypy + pytest config in `pyproject.toml`; `.pre-commit-config.yaml`; `sonar-project.properties`; `requirements.txt` alongside `pyproject.toml` |
| License | **GPL-3.0-or-later** (`LICENSE` is the GPLv3 text; `pyproject.toml` declares `license = "GPL-3.0-or-later"`) — the strictest copyleft in the portfolio, consistent with PyQt6's licensing |
| Git | 40 commits, **2026-02-21** (oldest repository in the portfolio) → 2026-08-15, 2 authors, 12 in the last 30 days |
| Version / status | `0.1.0`; README §Roadmap tracks remaining work |

Maturity reading: **small, tidy, and appropriately tested for a hardware app** — 97 tests
over 3.6k lines with the camera layer mocked, plus a `--verify` mode that is the real
acceptance test when hardware is attached.

### 3.2 Umkehrwalze_Cassel (revprint)

**Name and tagline.** "revprint — Image processing pipeline for historical manuscript
digitisation. Transforms raw archival scans (JPEG) into clean ink-on-white reproductions
suitable for fresh printing or OCR." (`README.md`.)

**Purpose.** The README names the corpus precisely: "18th-century English/German cursive
ledgers from the Hessisches Staatsarchiv Marburg (item 4 h Nr. 4156, Hessian field hospital
records, 1777–1778)", and the specific degradations handled — binding curvature, ink
bleed-through from facing pages, librarian stamps, spine shadows, ragged edges, staining.

**Codebase.**

| Aspect | Detail | Source |
|---|---|---|
| Primary language | Python (8,119 tracked lines across 81 files), Python ≥3.10 | `cloc`, `pyproject.toml` |
| Dependencies | flask, joblib, numpy, opencv-python-headless, pillow, pydantic-settings, rapidfuzz, reportlab, scikit-image, scikit-learn, scipy, tifffile, tqdm; `[gpu]` extra adds torch + kornia; `[ocr]` extra adds pytesseract | `pyproject.toml` |
| Layout | `src/revprint/` with one module per pipeline stage (`cli.py`, `batch_pipeline.py`, `adaptive_clean.py`, `line_dewarp.py`, `ghost_cross_page.py`, `spine_flatten.py`, `corpus_stats.py`, `page_model.py`, `stamp_suppress.py`, `proof.py`, `image_processing.py`, `ghost_suppression.py`, `pdf_export.py`, `web.py`, `config.py`), plus `inputs/`, `scripts/`, `tests/` | README §Project structure |
| Entry point | `revprint = "revprint.cli:main"` | `pyproject.toml` |
| Configuration | env vars or `.env` via pydantic-settings: `RPK_INPUT_ROOT`, `RPK_JOB_STORE`, `RPK_PROJECT_STORE`, `RPK_PROCESSING_PROFILE`, plus optional Google Translate / Gemini keys | README §Configuration |
| Persistence | two SQLite stores (job tracking, project/volume organisation) | README §Configuration |

The CLI is the broadest in the portfolio — `scan`, `process-proof`, `batch`, `init-jobs`,
`status`, `project init|list`, `volume add|list`, `review add|list|export|rubric`,
`htr scaffold`, and `gui` (a Flask review UI) — and the README documents the eight-phase
batch pipeline (page model → corpus stats → stamp suppression → spine flattening →
adaptive Sauvola binarisation → line dewarping → cross-page ghost subtraction → QA
metrics) as well as four named processing profiles (`quick`, `balanced`, `forensic`,
`training`).

**Documentation inventory.** 10 Markdown files: `README.md` (itself a substantial manual
with pipeline and profile tables), `AGENTS.md`, `CONTRIBUTING.md`,
`docs/cloud_offload_contract.md`, `docs/model_dataset_spec.md`, `docs/samples/README.md`.
Four agent skills: `revprint`, `ci-test-design`, `download-deepwiki`, `sonar-quality`.

**Quality and maturity.**

| Metric | Value |
|---|---|
| Tracked LOC | Python 8,119; JSON 2,039 (an archive metadata export); Markdown 775; YAML 118; TOML 62 — **11,113 total** |
| Test files / functions | 35 / 86; `pytest --collect-only` → **86** |
| Coverage gate | `--cov-fail-under=70` in `pyproject.toml` `addopts` — the only hard coverage threshold in the portfolio. Locally the collected-but-unrun suite reports 21% because collection alone executes no tests; CI runs the suite for real |
| CI (`ci.yml`) | `lint`, `test`, `guards`, `workflow-lint`, `sonar` |
| Lint / types | Ruff with `select = ["E","F","I","ARG","C90"]`; pre-commit (ruff, ruff-format, sonar guards, zizmor); Sonar (`sonar.sources=src/revprint`). **No mypy** |
| Technical-debt honesty | `[tool.ruff.lint.mccabe] max-complexity = 65` with the comment "Measured current maximum; ratchet this ceiling down only", plus per-file `C901`/`ARG001` ignores each annotated with the measured complexity (e.g. `web.py: create_app (65) and index (34)`) | `pyproject.toml` |
| License | Apache-2.0 (`LICENSE`; README §Licence: "Apache 2.0 — see `LICENSE`") |
| Git | 35 commits, 2026-06-07 → 2026-08-15, 2 authors, 14 in the last 30 days |
| Version / status | `0.1.0`; description "Manuscript image pipeline: scan discovery, job tracking, print outputs" |

Maturity reading: **working tool with acknowledged internal debt.** It is the only
repository that both enforces a coverage floor and records its complexity ceiling as a
number to ratchet down, which is a healthier position than an unmeasured "we should
refactor this" note.

---

## 4. Games

### 4.1 TheKingsAndI

**Name and tagline.** "The Kings and I: Sacrifice and Command — **A chess game of sacrifice
and command.**" (`README.md`. The README notes the internal codename *Living Chess*.)

**Purpose.** From the README: "The pieces under your command are not wooden automata. They
remember every match you have played together. They trust you, or they do not. Rooks hold
Pawns in contempt until a Pawn dies to save one. Push a piece too far and it will obey
badly, refuse outright, or walk off the board — and once one walks, the rest can follow in a
matter of moves." The design thesis is stated as "You can be the better chess player and
still lose, because being right is not the same as being followed." Mechanically it "layers
a persistent multi-agent psychology model over standard chess rules, and reuses the same
telemetry as a leadership-dynamics simulation: a post-match audit of how you led, and a
campaign debrief of the culture you built."

**Codebase.**

| Aspect | Detail | Source |
|---|---|---|
| Primary language | TypeScript, strict mode (28,709 tracked lines across 170 files) | `cloc`, `tsconfig.json` |
| Stack | React 18 + Vite + pnpm; Vitest; Zustand state; `chessground` board; `chess.js` rules; `stockfish.wasm` and a bundled Lozza engine; Dexie (IndexedDB) persistence; ESLint + Prettier; SonarQube Cloud | `package.json`, README |
| Layout | `src/{app,chess,core,engine,narrative,orchestration,persistence,psychology,ui}/`, plus `sim/` (headless harness), `tests/`, `scripts/`, `vendor/`, `deploy/` | repository tree |
| Entry points / scripts | `pnpm dev` (Vite), `pnpm build` (`tsc --noEmit && vite build`), `pnpm lint` (`eslint . && prettier --check .`), `pnpm typecheck`, `pnpm test` (Vitest, excluding three heavy suites), `pnpm test:heavy`, `pnpm test:coverage`, `pnpm sim` (`tsx sim/cli.ts`), `pnpm season`, `pnpm sim:aggregate`, `pnpm sim:sweep` | `package.json` `scripts` |
| Determinism rules | seeded RNG, banned transcendentals, enforced layer boundaries (documented in the `typescript-toolchain` skill and ADR 0034 "deterministic query barrier") | `.agents/skills/typescript-toolchain/SKILL.md`, `docs/adr/` |

```bash
pnpm install
pnpm lint && pnpm typecheck && pnpm test
pnpm sim --matches=20 --leader=tyrannical   # Lozza default; --engine=fake in CI
```
*Source: `README.md` §Status.*

**Documentation inventory.** The richest documentation set in the portfolio by structure:
**104 Markdown files (10,212 lines)**, including

- **55 ADRs** in `docs/adr/` (`0000-adr-process` through `0054-the-seminar-pool-and-what-a-player-knows`),
  plus `docs/adr/IMPLEMENTATION_STATUS.md` tracking which decisions are wired into code.
  ADR 0010 records the rename that produced the duplicate-name confusion; ADRs 0006/0020
  cover licensing; 0032–0036 cover toolchain, static analysis, the deterministic query
  barrier, three-channel credence, and the separate engine audit stream.
- Design references: `docs/architecture.md`, `docs/psychology_engine.md`,
  `docs/belief_model.md`, `docs/trust_dynamics.md`, `docs/desertion_model.md`,
  `docs/design_decisions.md` (the README calls this the authority on "what is decided, and
  what is still open"), and a normative
  `docs/spec/psychology-engine.reference.ts` carrying equations and default coefficients.
- **A dated calibration journal** in `docs/calibration/` (ten entries from
  `2026-08-10-state-of-play.md` to `2026-08-19-piece-quality-and-the-bench.md`, including
  `blocked-on-measurement`, `cross-style-table`, `desertion-gradient`,
  `exit-cost-asymmetry`, `exit-permanence-sweep`, `pawn-hope-sweep`) — effectively a lab
  notebook for game balance.
- Governance: `AGENTS.md`, `CONTRIBUTING.md` (DCO sign-off required), `LICENSING.md`,
  `deploy/aws/README.md`.
- Seven agent skills: `living-chess`, `psychology-engine`, `narrative-llm`,
  `balance-simulation`, `typescript-toolchain`, `sonarqube-quality-gate`,
  `ci-test-design`.

**Quality and maturity.**

| Metric | Value |
|---|---|
| Tracked LOC | TypeScript 28,709; Markdown 10,212; YAML 2,905; JSON 555; CSS 411; shell 354; JavaScript 139; Dockerfile 27; HTML 12 — **43,324 total** across 296 files |
| Tests | 44 tracked `*.test.ts` files containing **419** `it(`/`test(` cases; three heavy suites (`sim.trajectory`, `sim.sweep`, `chess.board.fuzz`) are excluded from `pnpm test` and run via `pnpm test:heavy` / the nightly workflow |
| CI | `ci.yml` (`hygiene`, `app`, `sonar`) and `nightly.yml` (`lozza-calibration`, `vitest-heavy`, `stockfish-spot`) — long-running engine work is deliberately moved off the PR path |
| Lint / types | ESLint (`eslint.config.js`) + Prettier, `tsc --noEmit` strict typecheck, Vitest coverage → `coverage/lcov.info` for Sonar, `.pre-commit-config.yaml`, `sonar-project.properties` (`sonar.projectKey=bckirkup_TheKingsAndI`) |
| License | **AGPL-3.0** (`LICENSE` is the AGPLv3 text; `package.json` `"license": "AGPL-3.0"`), dual-licensed with commercial terms per the README and `LICENSING.md` (ADR 0006, ADR 0020) |
| Git | 328 commits, 2026-07-26 → 2026-08-16, 4 authors, all 328 commits within the last 30 days (159 in the last 7), 108 merges, 22 branches on the remote, 104 pull requests to date |
| Version / status | `package.json` `"version": "0.0.0"`, but README §Status says "**Milestones 1–6 substantially landed**" — chess substrate, Stockfish 1.3 pool + shared-search broker, psychology with live cascade/witness/sacrifice/costly-signal wiring, headless harness with coefficient sweeps, playable UI slice, campaign/persistence spine, and authored narration are in tree. Still open: supportive-desertion calibration, Milestone 5b (seminar/cohort), and wiring decisions **D49/D50** (ADRs 0035/0036) into live credence state and the engine audit stream |

Maturity reading: **the fastest-moving repository and the most rigorously specified.** 55
ADRs with an implementation-status tracker, a dated calibration journal, a nightly workflow
for expensive engine runs, and a dual licence with commercial terms — an unusual amount of
governance for a three-week-old codebase. The `0.0.0` version is a placeholder, not a
statement about completeness.

### 4.2 TheKingAndI

**This name does not identify a separate repository.** `bckirkup/TheKingAndI` is the former
name of `bckirkup/TheKingsAndI`; GitHub resolves it through a rename redirect to the same
repository object (identical numeric id `1313180573`, identical `created_at`/`pushed_at`,
identical `HEAD` `d55bdf32…`, identical 22 branches, identical 43,324 tracked lines,
identical `sonar.projectKey`). `gh repo list bckirkup` lists the repository once, under
`TheKingsAndI`. See
[the duplicate finding](#duplicate-finding-thekingandi-is-a-redirect-not-a-fork) for the
full evidence table, and [§4.1](#41-thekingsandi) for the content description.

Consequences worth noting:

- There is nothing to merge, reconcile, or archive — no divergent history exists.
- Local clones created from the old URL keep a stale remote (`git remote -v` shows
  `…/bckirkup/TheKingAndI`) and continue to work only while the redirect stands. Repointing
  them is a one-line fix: `git remote set-url origin https://github.com/bckirkup/TheKingsAndI`.
- The name change itself is documented in
  `docs/adr/0010-naming-the-king-and-i.md`, so the two names appearing in inventories is a
  cataloguing artefact rather than a code-management problem.

---

## 5. Cross-portfolio observations

**A shared engineering template exists and is followed.** Nine repositories carry the shared
`sonar-quality` skill (GutIBM has three Sonar-specific ones of its own), eleven register a
SonarQube project, ten install
`pre-commit` with the same core hooks (`ruff`, `ruff-format`, local `sonar-mechanical-guards`
and `sonar-workflow-guards`, and `zizmor` for GitHub Actions security linting), and eight
Python repositories run the same five-or-six-job workflow shape
(`lint` → `typecheck` → `test` → `guards` → `workflow-lint` → `sonar`). Two repositories
opt out: GutIBM replaces it with an HPC-specific 8-job pipeline, and shipbiome-core has no
CI at all.

**Agent-facing documentation is a first-class artefact.** Eleven repositories carry
`AGENTS.md`, and all twelve carry `.agents/skills/*/SKILL.md` — 83 skill documents in total,
from 1 (shipbiome-core) to 30 (Crusher). Several skills recur verbatim across repositories
(`ci-test-design` in eleven, `sonar-quality` in nine, `download-deepwiki` in nine), which is
effectively a copied shared library of procedures. GARLAND additionally mirrors its skills
into `.cursor/skills/` with a feature backlog and resolved-issues reference, and Coral Key
still carries a legacy `.devin/skills/SKILL.md`.

**Measurement is treated as an output.** Six repositories commit measurement records
next to code: `docs/*-measurement.md` + `.json` pairs (TattleTots, Scrapiron, Xylella,
Coral Key), `docs/grounded_access/` sweep corpora (Scrapiron 31 files, Coral Key 16),
GutIBM's `experiments/` and validation examples, and TheKingsAndI's dated
`docs/calibration/` journal. This is why total tracked LOC correlates so poorly with
source size.

**Development is agent-driven and merge-based.** Distinct commit authors are
`Benjamin Kirkup`, `devin-ai-integration[bot]`, `Cursor Agent`, `Devin AI` and `cursor[bot]`;
branch names on TheKingsAndI's remote are almost all `devin/<timestamp>-<topic>` or
`cursor/<topic>`. Merge commits are 30–40% of history in the active repositories
(Crusher 213/565, GutIBM 236/631, TheKingsAndI 108/328), i.e. work lands through PRs
rather than direct pushes.

**Cross-repository coupling is by git URL.** The three domain adapters depend on
`domain-runner` and `tattletots` as unpinned `git+https` references, and Crusher's README
names `infection-dynamics`, `py-contam`, `FRED` and `EMOD-Generic` — all of which exist as
separate repositories under the same account. Nothing in the portfolio is published to
PyPI or npm, so integration is source-level.

**Type checking is inconsistent.** mypy is configured in TattleTots, Scrapiron, Xylella
(strict), Coral Key, GARLAND and Anaglyph; it is absent from Crusher (the largest Python
codebase), domain-runner, revprint and shipbiome-core. TheKingsAndI compensates with strict
`tsc`.

---

## 6. Findings worth acting on

Ordered by cost-to-benefit, each with the evidence that produced it:

1. **Coral Key's licence disagrees with itself.** `LICENSE` is Apache-2.0; `pyproject.toml`
   declares `license = "MIT"` with an MIT classifier, and README §License says MIT. Pick one
   before the package is consumed.
2. **shipbiome-core has no README, tests, CI, or lint config** (`git ls-files`), yet its
   `CONTRIBUTING.md` instructs contributors to "Run CI tests". The four sibling artefacts it
   needs — README, `pyproject.toml`, `ci.yml`, and `tests/` derived from
   `validate_expanded_profiles.py` — all exist in template form elsewhere in the portfolio.
3. **Crusher's README understates its test suite by ~40%** — "~900 tests" / "~875 tests" in
   four places versus 1,512 collected. Since the number is quoted as a quality signal, it is
   worth regenerating (or replacing with a coverage badge).
4. **Tracked build artefacts in shipbiome-core.** Two `__pycache__/*.pyc` files are tracked;
   they should be removed and `.gitignore`d.
5. **domain-runner is under-tested for its blast radius** — 3 tests guard the runner that
   TattleTots and three domain repositories all execute through.
6. **Unpinned git dependencies** across the three domain adapters mean a reproducible build
   depends on branch state. TattleTots' `uv.lock` approach, or tag/commit pins, would fix it.
7. **Repoint clones and references from `TheKingAndI` to `TheKingsAndI`** while the rename
   redirect still exists.

---

## Appendix A — measurement commands

Every number in this document is reproducible with the following commands, run inside each
clone on `main` (as of 2026-08-16):

```bash
# Tracked-source line counts (excludes venvs, node_modules, build output by construction)
git ls-files > /tmp/f.txt
cloc --quiet --list-file=/tmp/f.txt --md .

# Python test files and test functions (tracked, path-anchored)
git ls-files \
  | grep -E '(^|/)tests?/.*\.py$|(^|/)test_[^/]*\.py$|(^|/)[^/]*_test\.py$' \
  | grep -E 'test' | sort -u
# ... piped into: xargs grep -hcE '^[[:space:]]*(async def|def) test'

# Python tests actually collected (uses each repo's own .venv when present)
python -m pytest --collect-only -q

# TypeScript test files and cases
git ls-files | grep -E '\.(test|spec)\.(ts|tsx|js)$'
# ... piped into: xargs grep -hcE '^[[:space:]]*(it|test)(\.each)?\('

# C++ tests (GutIBM)
ls tests/*.cpp | wc -l
grep -rhE '^[[:space:]]*(static )?void test_[A-Za-z0-9_]+\(' tests/*.cpp | wc -l
grep -c 'add_test' tests/CMakeLists.txt

# Git activity
git rev-list --count HEAD
git log --reverse --format=%ad --date=short | head -1
git log -1 --format=%ad --date=short
git log --format='%aN' | sort -u
git log --since='30 days ago' --oneline | wc -l
git log --merges --oneline | wc -l

# CI job names
# top-level keys under `jobs:` in each .github/workflows/*.yml

# Duplicate-repository determination
gh api repos/bckirkup/TheKingAndI  --jq '{id,full_name,created_at,pushed_at}'
gh api repos/bckirkup/TheKingsAndI --jq '{id,full_name,created_at,pushed_at}'
curl -s -o /dev/null -w '%{http_code}\n' https://github.com/bckirkup/TheKingAndI   # 301
git rev-parse HEAD   # in both clones
gh repo list bckirkup --limit 100
```

Definitions used throughout:

- **Source LOC** — `cloc` "code" lines for the repository's primary language(s) only.
- **Total LOC** — `cloc` "code" lines summed over all tracked languages, including committed
  JSON data and Markdown.
- **Test function** — a syntactic match, not a collected node; **collected** figures come
  from pytest itself.
- **Contributor** — a distinct `%aN` author name in `git log`, bots included.
- **CI present** — at least one file under `.github/workflows/`.

---

## Appendix B — per-language line counts

`cloc` code lines over tracked files, 2026-08-16.

| Repository | Files | Primary language (lines) | Other notable languages (lines) | Total |
|---|---:|---|---|---:|
| TattleTots | 169 | Python 18,947 | JSON 18,401; Markdown 3,484; YAML 192; TOML 118; shell 18 | 41,160 |
| domain-runner | 20 | Python 1,046 | Markdown 465; YAML 134; TOML 46 | 1,691 |
| Scrapiron_and_the_Bear | 120 | Python 7,450 | JSON 210,953; Markdown 1,497; YAML 158; TOML 88 | 220,146 |
| Xylella_SPQR | 95 | Python 7,379 | JSON 70,166; Markdown 1,483; YAML 155; TOML 90 | 79,273 |
| Coral_Key_in_Three_Hour_Epochs | 87 | Python 5,816 | JSON 242,714; Markdown 1,471; YAML 150; TOML 89 | 250,240 |
| Crusher_to_the_Bridge | 651 | Python 70,190 | JSON 127,706; Markdown 12,124; YAML 1,153; TeX 673; PowerShell 481; shell 464; TOML 109; batch 98; Dockerfile 59; SVG 9 | 213,066 |
| GutModelBacteriocins | 408 | C++ 30,286 | Markdown 8,878; Python 6,238; headers 3,813; shell 3,461; JSON 3,268; CUDA 1,542; CMake 337; PowerShell 298; YAML 177; Dockerfile 53 | 58,351 |
| GARLAND | 120 | Python 18,394 | Markdown 2,889; YAML 1,070; JSON 164; TOML 78 | 22,595 |
| shipbiome-core | 8 | Python 660 | JSON 528; Markdown 200 | 1,388 |
| Anaglyph | 30 | Python 3,604 | Markdown 921; YAML 124; TOML 66 | 4,715 |
| Umkehrwalze_Cassel | 95 | Python 8,119 | JSON 2,039; Markdown 775; YAML 118; TOML 62 | 11,113 |
| TheKingsAndI | 296 | TypeScript 28,709 | Markdown 10,212; YAML 2,905; JSON 555; CSS 411; shell 354; JavaScript 139; Dockerfile 27; HTML 12 | 43,324 |

## Appendix C — CI job inventory

| Repository | Workflow | Jobs |
|---|---|---|
| TattleTots | `ci.yml` | `lint`, `sonar-guard`, `typecheck`, `test`, `smoke`, `workflows`, `sonar` |
| domain-runner | `ci.yml` | `lint`, `test`, `guards`, `workflow-lint`, `sonar` |
| Scrapiron_and_the_Bear | `ci.yml` | `lint`, `typecheck`, `test`, `guards`, `workflow-lint`, `sonar` |
| Xylella_SPQR | `ci.yml` | `lint`, `typecheck`, `test`, `guards`, `workflow-lint`, `sonar` |
| Coral_Key_in_Three_Hour_Epochs | `ci.yml` | `lint`, `typecheck`, `test`, `guards`, `workflow-lint`, `sonar` |
| Crusher_to_the_Bridge | `ci.yml` | `lint`, `sonar-mechanical-guard`, `workflow-lint`, `sanity-checker`, `schema-validation`, `test`, `import-hygiene`, `presidio-smoke`, `sentinel-smoke`, `orchestrator-import-hygiene`, `dashboard-import`, `orchestrator-smoke`, `docker-campaign-smoke`, `sonar` |
| Crusher_to_the_Bridge | `picard-presidio.yml` | `framework` |
| GutModelBacteriocins | `ci.yml` | `unit-tests`, `serial-build`, `integration-tests`, `openmp-parity`, `gpu-parity`, `cuda-compile`, `eari-vadi-validation`, `python-lint` |
| GARLAND | `tests.yml` | `lint`, `typecheck`, `test`, `guards`, `workflow-lint`, `sonar` |
| GARLAND | `benchmark.yml` | `benchmark` |
| GARLAND | `stationarity.yml` | `stationarity` |
| Anaglyph | `ci.yml` | `lint`, `test`, `guards`, `workflow-lint`, `sonar` |
| Umkehrwalze_Cassel | `ci.yml` | `lint`, `test`, `guards`, `workflow-lint`, `sonar` |
| TheKingsAndI | `ci.yml` | `hygiene`, `app`, `sonar` |
| TheKingsAndI | `nightly.yml` | `lozza-calibration`, `vitest-heavy`, `stockfish-spot` |
| shipbiome-core | — | **no workflows** |
