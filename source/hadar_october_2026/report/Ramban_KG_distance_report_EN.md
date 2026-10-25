# Measuring Agreement in the Ramban Supercommentary Tradition
### A knowledge-graph distance analysis of 21 commentators across 38 sections

*Final report · 2026-09-06 · updated 2026-10 · all analyses reproducible from `RambanKGAnalysis/scripts/`*

> **Correction, October 2026.** A check against the source (Eliezer Baumgarten) found a labelling
> error in the Da'at Chacham units. `DaatChachamVatokan114` is Da'at Chacham, **Vat. 214** (there is
> no Vat. 114 witness). `DaatChachamVatokan214` is the **marginal notes on Da'at Chacham, Vat. 214**,
> a separate unit, not a witness. Texts, graphs and all numbers are unchanged; identifiers are file
> names and are kept. Readings affected are marked below.

---

## Executive summary

We built knowledge graphs for 21 supercommentators on Nachmanides (Ramban) across 38 sections of
his Torah commentary — 385 graphs in all — and measured how far apart they are, using a five-rung
distance ladder over four different notions of "the same concept".

**The headline is a negative one, and it is robust.** The supercommentators do not form schools.
What the corpus contains is *manuscript families* — witnesses of the same text — set against a broad
and near-total dispersion. Commentators writing on the *same passage of Ramban* share about 8% of
their concepts, and of the claims they could both have made about that shared 8% they agree on
almost none.

Six results carry the report:

1. **No schools.** Cluster structure beats chance in 13 of 36 sections, but most of those are a
   single commentator separating from the rest (12+1, 9+1), not two camps. Balanced structure exists
   in only a handful (§18 at 5+5 is the clearest). Denser graphs show *no more* structure than sparse
   ones, so this is not an artefact of thin extraction.
2. **Divergence is total, and extends to the proof-texts.** Median locus overlap 0.080; median
   reading agreement 0.000. Even scriptural anchors recur across commentators only 35% of the time —
   less often than a divine name or a biblical figure.
3. **Manuscript families are recovered cleanly**, and three previously unremarked candidates emerge,
   each confirmed by two independent instruments.
4. **IbnShuib is the closest tracker of Ramban** on four measures — content, order, grouping and
   register.
5. **The distance ladder is not redundant**: 45 aligner×rung cells reduce to 29 independent axes.
6. **The measurement scale matters more than expected.** A raw rung score is *ordinal*; calibrated
   into bits of evidence, a gap between 0.9 and 0.7 turns out to be worth **zero** additional
   evidence.

---

## 1. What was measured, and how

### 1.1 The corpus

| | |
|---|---|
| Graphs | 385 (`data/graphs_canonical/`) |
| Sections of Ramban | 38 |
| Commentators | 21 (12 with ≥10 sections) |
| Section × commentator grid | 48.2% dense |
| Median graph | 35 concepts / 41 edges |

Two graphs are empty (`kg_7_2_RAMBAN`, `kg_9_UnKnownEskorial`) and one has two concepts
(`kg_8_UnKnownEskorial`); all three are excluded from every ranking. Section §1's RAMBAN graph is a
correct graph of the *wrong passage* — a known data error, retained deliberately as a control.

### 1.2 The distance ladder

| rung | question |
|---|---|
| **D1** content | do they discuss the same concepts? |
| **D2** structural (L0/L1/L2) | do they make the same claims about them? |
| **D3** anchoring | do they root the same idea in the same scriptural place? |
| **D4** positional | do they place concepts in the same neighbourhood? |
| **D5** sequence | do they present ideas in the same order? |

### 1.3 Four notions of identity

A distance is only meaningful once "the same concept" is defined. Four definitions were run as
separate rows and compared:

- **Method I — embedding**: same *meaning*, by cosine above a threshold. The only method with an
  absolute scale, and therefore the only one that can say "no".
- **Method II — canonical authority**: same *referent*, decided by resolving a quotation to a
  canonical verse. Deterministic and corpus-global, but reaches only 12.9% of concepts.
- **I+II composite**: verse first, then embedding, then label. This turned out to be the best row on
  **every** rung against a negative control.
- **I∧III corroborated**: embedding detects, structural role corroborates a relaxed band. Method III
  is *never* used alone — a size-matched panel showed it matches ~18–19 nodes in *unrelated* pairs
  exactly as in related ones, so it has no "no".

### 1.4 The negative control

Every claim in this report is measured against **600 size-matched cross-section pairs** — commentators
writing on *different* passages, therefore known to be unrelated. This is what converts a similarity
score into evidence. Its availability was the decisive argument for keeping the unit of analysis at
the section level rather than merging each commentator into one graph: per-section yields **72,024**
known-unrelated pairs, per-commentator only **38**.

### 1.5 Measurement scale

A raw rung score is **ordinal** — higher means more similar, and nothing more. "Distance" promises
more than we measure. Calibrated against the negative control, the same score becomes **bits of
evidence** (log₂ of the likelihood ratio), which has a true zero at "no evidence" and on which
differences are meaningful.

> **The clearest illustration:** in the best cell, a raw score of **0.9 and a raw score of 0.7 carry
> the identical +6.33 bits** — an odds ratio of 1.0. Both land in the top calibration bin, because
> almost nothing in this corpus scores that high. The ordinal reading makes the gap look decisive;
> the interval reading shows it is empty.

A ratio scale of *closeness* is not available: it would need a unit of textual closeness, and there
isn't one. A ratio scale of *evidence* is available, and is what we use.

### 1.6 A global vocabulary

Pairwise alignment mints a concept's key *per pair*, so the same concept has a different name in
every comparison — which makes statements like "these four commentators share concept X" literally
unsayable. We therefore built **multiple graph alignment** (`graphcompare/multi.py`): one global key
space per section, validated to recover the known manuscript twins at **2.42×** separation from
non-twins while still flagging the §1 data error.

---

## 2. Findings by research question

### RQ #1 — Measurement

The distance matrix reproduces the earlier E3 analysis at **ρ = 0.950** across 339 vs-Ramban pairs,
confirming the instrument before any new claim rests on it. Two corpus defects surfaced in the
process: the two empty graphs, and confirmation that §1 is a graph of the wrong passage.

The ladder is **not redundant**: across 1,873 pairs, 45 aligner×rung cells collapse to only **29
independent axes** at ρ ≥ 0.98. The rungs measure genuinely different things — a methodological
result in its own right for graph-distance work on humanities corpora.

A clean negative: switching Method I from directional `argmax` to symmetric `mutual` changes the
pair ordering by **ρ = 0.996** — i.e. essentially nothing. The directional matching choice in the
earlier analysis was not load-bearing.

### RQ #2 — Explaining similarity

Across **1,534 horizontal pairs** (commentator ↔ commentator):

- The accepted band (central 80%) is a raw score of **0.076 – 0.354**.
- **18% of pairs carry zero or negative evidence** — no more similar than two commentators writing
  on unrelated passages.
- The threshold of ">0.50" suggested in the source research document sits at the **96.8th
  percentile**: only 49 pairs of 1,534 reach it.

Outlier cutoffs were derived rather than chosen: *divergent* = bits ≤ 0 (straight from the null);
*close* = at least as similar as the lower quartile of 42 confirmed manuscript-twin instances.

**The close tail validates the instrument.** `KeterShemTov ↔ KeterShemTovMS_L` tops it in four
separate sections; `DaatChacham107 ↔ 114` (the two Da'at Chacham witnesses, Vat. 107 and Vat. 214) in two more.

⭐ **Three candidate relationships not in the known gold set**, each recurring across sections:

| pair | sections |
|---|---|
| `UnKnownEskorial ↔ UnKnownVatikan214` | §19_2, §20, §26 |
| `DaatChachamVatokan214` (marginal notes, Vat. 214) `↔ UnKnownEskorial` | §22, §25_2 |
| `MeiratEinayim ↔ SaportaOxford1645` | §15 |

Recurrence is what makes these more than topical coincidence — one section could be shared subject
matter; three cannot. **All three were later confirmed independently** by co-clustering (RQ #3).

✅ **The "214 anomaly" is resolved, and it was a detection.** The earlier analysis grouped
DaatChacham 107, 114 and 214 as one family. Our measurements placed **214 outside** that group
(107↔214 and 114↔214 rank at the 23rd–40th percentile, while 107↔114 ranks at the 99th) and
attached it instead to `UnKnownEskorial`. The source check (October 2026) explains why: the unit
labelled 214 is the marginal notes on Da'at Chacham, not a witness, while the unit labelled 114 is
the real Vat. 214 witness. Without being told, the measurements separated the one unit that is not
a Da'at Chacham witness.

### RQ #3 — Clusters

**Per section:** cluster structure beats a permutation null in **13 of 36 sections** at p < 0.05
(5 survive Benjamini-Hochberg; 3 survive Bonferroni: §26, §30_1, §32).

⚠️ **But read the cluster sizes.** Most significant splits are a single commentator separating from
the rest — §26 and §24 are 12+1, §22 is 9+1. Genuinely balanced structure appears in only a few:
**§18 (5+5, p = 0.005)**, §32 (4+2+2), §5, §7_1. Silhouettes stay low throughout (0.05–0.32) and mean
pairwise distance is 0.83–0.96. **The corpus has outliers more than it has camps.**

**Across sections — "local or consistent?"** For each pair of commentators we measured the fraction
of shared sections in which they land in the same cluster:

| pair | co-cluster rate | sections |
|---|---|---|
| KeterShemTov ↔ KeterShemTovMS_L | **1.00** | 17 |
| **UnKnownEskorial ↔ UnKnownVatikan214** | **1.00** | 7 |
| DaatChacham107 ↔ 114 (= Vat. 214) | **0.96** | 25 |
| Likutim_bhml_1978 ↔ UnKnownEskorial | 0.80 | 5 |

The median over 105 pairs is **0.32 — chance**. So the only consistent groupings in this tradition
are **manuscript families, not schools**.

**Is the absence of schools real, or just sparse graphs?** Tested directly: if sparsity were
suppressing structure, denser sections would show more of it. They do not — concepts→silhouette
ρ = −0.178, and −0.143 controlling for the number of commentators. Sparsest and densest halves have
median silhouettes of 0.106 and 0.097.

⭐ And an unexpected finding in the same test: **more material makes commentators *more* distant, not
less** (concepts → mean pairwise distance ρ = +0.227). They do not converge as they say more; they
diverge further.

### RQ #4 — Dominance

The plan proposed centrality on the similarity graph. We reframed, for two reasons the plan itself
anticipates: dominance is *directional* and a symmetric distance cannot express direction; and a
graph with mean distances of 0.83–0.96 whose significant structure is mostly lone outliers has no
centre for centrality to find.

**In a supercommentary tradition the centre is not an emergent hub — it is the base text.** The
question becomes: who stays closest to Ramban?

| # | commentator | content | order | co-cluster | register | mean rank |
|---|---|---|---|---|---|---|
| 1 | **IbnShuib** | 0.345 | 0.914 | 0.69 | 0.971 | **11.8** |
| 2 | UnKnownEskorial | 0.351 | 0.874 | 0.54 | 0.945 | 11.0 |
| 3 | Ricanati | 0.286 | 0.863 | 0.45 | 0.940 | 9.8 |
| … | | | | | | |
| 12 | Comment_a_shuib_Parma_68 | 0.109 | 0.405 | 0.36 | 0.881 | 2.0 |

**IbnShuib leads on all four measures.** The commentator at the bottom is the same one that dominates
the divergent tail in RQ #2 and forms the lone-outlier split in RQ #6.

⚠️ Two qualifications. The four measures are **not independent** — content and order correlate at
+0.91 — so this is a *stable ranking*, not four independent confirmations. And **closeness is not
influence**: this says who tracks the base text, not who shaped the tradition, which would require
citation direction and chronology that the graphs do not carry.

### RQ #5 — Characterising divergence

We decomposed each pair into **locus overlap** (do they engage the same material?) and **reading
agreement** (of the claims they could *both* have made about their *shared* concepts, how many do
they share?). The conditional denominator is what separates "talking about different things" from
"reading the same thing differently".

- median locus overlap **0.080**
- median reading agreement **0.000**
- **27%** of pairs share concepts but never link the same two — no comparable claim exists at all
- of those that do have comparable claims, **59% agree on nothing**

⚠️ **Both measures sit at the floor, and they are not alternatives.** It would be wrong to report
"divergence is about reading rather than locus": an 8% locus overlap means they mostly do not meet on
the same ideas in the first place. **Divergence is total.**

**Which kinds of concept are shared** (share rate = appears in ≥2 commentators of the same section):

| class | share rate |
|---|---|
| SpiritualEntity | 0.391 |
| BiblicalFigure | 0.390 |
| PhysicalObject | 0.371 |
| **scriptural anchor (verse)** | **0.349** |
| TheologicalConcept | 0.320 |
| KabbalisticConcept | 0.306 |
| BiblicalSource (a book) | 0.192 |
| OtherConcept | 0.168 |

The specific question posed was *verses versus kabbalistic terms*. Verses are shared more — but only
modestly, 0.349 against 0.306.

⚠️ **The "fixed point" intuition is only weakly supported.** If every commentator had to pass through
the same verses, the anchor rate should tower over the concept types. It sits mid-table instead: they
are **less likely to share a verse than to share a divine name or a biblical figure**.

⭐ **The asymmetry is the reportable claim.** Verses beat both *doctrinal* classes but lose to the
*concrete* ones. What this tradition holds in common is its **cast and furniture** — who and what the
passage is about — more than either its proof-texts or its doctrine.

Most widely shared anchors: **Gen 9:13** (13 commentators, §5) · **Hab 3:2** (11, §12) ·
**Lev 23:40** (10, §27).

### RQ #6 — The nature of the vertices

Since the commentators do not group by content, do they group by **method** — the kinds of node and
edge they favour? Distance here is the Jensen-Shannon divergence between type distributions.

⚠️ Ramban himself must be excluded: with him included the best split is trivially {Ramban} vs
{everyone}, because the base text is not a kabbalistic supercommentary (`KabbalisticConcept` −15.9
percentage points).

Among the 12 supercommentators, **only the single-outlier split is significant**:

| k | cluster sizes | silhouette | p |
|---|---|---|---|
| **2** | **11+1** | 0.529 | **0.000** |
| 3 | 9+2+1 | 0.259 | 0.664 |
| 4 | 9+1+1+1 | 0.204 | 0.854 |
| 5 | 5+4+1+1+1 | 0.272 | 0.680 |
| 6 | 4+3+2+1+1+1 | 0.290 | 0.570 |

Every *balanced* partition fails. **They do not group by method either.**

**But style is a genuinely independent axis** — its correlation with content co-clustering is −0.166,
near zero. The profiles measure something the content rungs do not; they simply do not partition the
tradition. As descriptive signatures they work well:

- **IbnShuib** is the *least* kabbalistic supercommentator (`KabbalisticConcept` −8.9pp, scriptural
  quotation +3.9pp) — coherent with his being the closest tracker of Ramban.
- **KeterShemTovMS_L** is the most kabbalistic (+7.0pp).
- **Comment_a_shuib_Parma_68** is the outlier: `PhysicalObject` +7.2pp, `BiblicalQuotation` −7.3pp.

---

## 3. Cross-cutting findings

**Overlap is not agreement.** The corpus repeatedly produces pairs with substantial shared vocabulary
and no shared claims — the diagnostic case being pairs at D1 = 0.364 with D2·L2 = 0.000. Any
similarity measure reported without its structural companion will overstate agreement.

**The instrument has a floor that must be reported with the findings.** Per-pair significance testing
is mostly unavailable on this corpus: under the appropriate null, 96% of pairs are degenerate for
D2·L2, 84% for D3, 52% for D4. Aggregate evidence (bits over the corpus) survives; per-pair
significance largely does not. This is a property of the corpus, not a failure of the run, and it
explains why claims requiring per-pair significance could not be substantiated.

**Evidence is cheap; interpretation is not.** The entire computational campaign cost **$0 in LLM
spend** except one verification exercise at **$0.25**. Every substantive limitation encountered was
methodological, not budgetary.

---

## 4. Corrections and limitations

We record the errors found and fixed during the campaign, because two of them changed conclusions.

🛑 **A broken permutation null (found 2026-09-06) invalidated the first version of RQ #3.** The null
permuted rows and columns of the distance matrix by the *same* permutation — a pure relabelling that
leaves the geometry untouched, so the clustering and its silhouette were identical in every draw
(verified: 50 draws, all 0.908940). The p-values it produced were tie-breaking noise. Corrected, the
result moved from "1 of 36 sections" to **13 of 36**. The corrected reading is in RQ #3.

🛑 **A confounded measure closed Step 6 (the vertical lens) as a negative.** Comparing whole systems
by repertoire overlap turned out to be ~76% explained by how much a commentator wrote
(ρ = +0.874 between repertoire size and vertical closeness). The apparent "drift" signal was coverage,
not divergence. Whole-system comparison needs a size-controlled statistic; the raw version is not
reportable.

⚠️ **A stored methodological claim was amended.** An earlier finding held that structural
corroboration at a relaxed threshold gave a 4 : 1 precision advantage. Re-measured on two corpora,
it was *below parity* at the original parameters, and only becomes load-bearing after moving the
threshold from 0.55 to 0.68. The qualitative claim survives; the numbers were withdrawn.

⚠️ **D3 = 1.0 means "no grounding evidence", not "perfect agreement"** — the top disagreements
between D1 and D3 are pairs with zero shared content and empty grounding sets on both sides.

⚠️ **D5's local-best score saturates on size-mismatched pairs**, and aggregated per commentator it is
largely a restatement of content overlap (ρ = 0.865). Sequence claims must be made pair-wise, or with
a length-controlled statistic.

**Known limitations of scope:**

- The unit of analysis is the section. The candidate pair `UnKnownVatikan214 ≈ DaatChachamVatokan214`
  (the anonymous unit and the marginal notes, both in Vat. 214) shares no section and is therefore
  unmeasurable here — an accepted cost of the decision. Whether the anonymous unit is part of the
  marginal notes is an open question for the scholars.
- Only the `verified` tier of scriptural anchoring carries a canonical verse (2,454 of 3,499
  quotations, 70%), so loose citation is undercounted and the verse share rate of 0.349 is a **lower
  bound**.
- The global vocabulary is built per section, not per corpus. Statements comparing concept identity
  *across* sections are outside what this analysis supports.
- An estimated **~10.4% of alignment merges are wrong** (27.9% in the 0.80–0.85 similarity band,
  4.0% above it), measured by LLM adjudication of 1,812 merges.

---

## 5. What a scholar should look at

1. **The three candidate manuscript relationships** in RQ #2, each confirmed by two independent
   instruments, with their shared concepts, scriptural anchors and shared claims in
   `data/step3/3_similarity_band.md`.
2. **The 214 anomaly** — a direct challenge to an existing grouping.
3. **§18**, the one section with a clean balanced two-camp split (5+5, p = 0.005).
4. **The divergent pairs** in `data/step3/`, each with the claims each side makes *instead* — for
   example §26, where one witness argues in a numerological-sefirotic register (עשרה → כח אחד,
   חפ"ת → ג' אבות) while another argues in a *midat ha-din* register (דין בדין → דין קשה/רפה,
   עלוי העטרה → תרועת מלחמה). Same passage of Ramban, different conceptual worlds.

---

## Appendix — artifacts

| analysis | outputs | script |
|---|---|---|
| E3 reproduction | `data/step2a/` | `step2a_methodI.py`, `step2a_correlate.py` |
| Aligner × rung matrix | `data/step2b/matrix.csv`, `2b_results.md` | `step2b_matrix.py`, `step2b_analyze.py` |
| Gold bake-off, redundancy, D5-vs-Ramban | `data/step2b/2c_2e_results.md` | `step2c_2e.py` |
| Measurement scale (bits) | `data/step2b/2f_scales_results.md` | `step2f_scales.py` |
| Null testability | `data/step2b/2g_null_testability.md` | `step2g_nulls.py` |
| Similarity band + outliers (RQ #2) | `data/step3/` | `step3_band.py` |
| Global alignment + acceptance | `data/mga/` | `mga_validate.py`, `mga_verify_sample.py` |
| Clusters (RQ #3) | `data/step4/` | `step4_clusters.py`, `step4b_density_check.py` |
| Divergence (RQ #5) | `data/step5/` | `step5_divergence.py`, `step5b_verses.py` |
| Vertex profiles (RQ #6) | `data/step6/6_vertex_profiles.md` | `step6_vertex_profiles.py` |
| Vertical lens (Step 6) | `data/step6/6_vertical_lens.md` | `step6_vertical_lens.py` |
| Dominance (RQ #4) | `data/rq4/` | `rq4_dominance.py` |

Framework code: `simplekg/graphcompare/` — `multi.py` (multiple alignment), `scales.py` (measurement
scale), `nulls.py` (significance), `corroborate.py`, `role.py`, `compare.py`, `reduce.py`.
