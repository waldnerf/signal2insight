---
title: "PepsiCo revenue growth management, LinkedIn carousel"
type: carousel
status: draft
source: ArxivWiki/summaries/2606.17941.md
arxiv_id: "2606.17941"
depth_pattern: spec-cards
slides: 14
revision: 0
---

# PepsiCo revenue growth management · 14-slide carousel

Slide-by-slide text export. Structured Situation, Complication, Resolution, Impact.
The two charts are noted as figures; the drawings live only in the HTML artifact.
Deep-dive slides carry a section tracker tag (Base pricing / Trade promotion); the active section is shown in [brackets] and renders as a two-part progress tracker.

Source: arXiv 2606.17941 · INFORMS Journal on Applied Analytics

---

## Slide 1 · Trade promotion is the second largest line on a CPG P&L, after cost of goods sold.

It also holds one of the largest remaining opportunities for systematic optimization.

PepsiCo built two production systems to capture it. Here's how

*Llenas et al. · PepsiCo Deploys AI-Driven Pricing and Promotion Optimization at Scale · arXiv 2606.17941* · June 16th 2026

---

## Slide 2 · In a margin-sensitive industry, price and promotion decide who wins

Consumer packaged goods is a high-volume, low-margin business where pricing and promotion move revenue, profit and share most directly. PepsiCo runs it at scale: a portfolio over €78 billion a year across many markets and channels, every call shaped by shifting demand, retailers, seasons and competitors.

Revenue management rests on two interrelated levers, base pricing and trade promotion, and they run on different clocks.

---

## Slide 3 · Two levers set revenue in CPG, and they play by different rules


|   | Base pricing | Trade promotion |
|---|---|---|
| **What** | Everyday shelf price | Temporary deal (buy one get one, 2 for €5) |
| **Cadence** | Reset once or twice a year | Calendar per quarter or year |
| **Hard part** | Elasticity and portfolio spillovers | Scheduling under slotting, spacing, seasonality |
| **Goal** | Hit targets without a price war | Maximise lift without eroding margin |
| **As a problem** | Identification: prices rarely move | Combinatorial: a huge feasible space |

*Handwritten labels beneath the columns: "PricingAI" under Base pricing, "PromoAI" under Trade promotion.*

---

## Slide 4 · PepsiCo built one architecture that automates manual pricing and promotion decisions across markets

PricingAI sets the base shelf prices across the portfolio. PromoAI builds the promotional calendars commercial teams take into retailer negotiations.


Both run the same five stage pipeline on one cloud data platform:

1. **Harmonized history** · sales, prices, promotions and costs, cleaned to one standard
2. **Demand model** · learns how volume responds to price and promotion
3. **Market rules** · each market keeps its commercial rules outside the code
4. **Optimizer** · picks the best plan those rules allow
5. **Planner screen** · review, override, commit

> Keeping the stages separate lets one team run both systems across dozens of markets. Refreshing a model leaves the optimizer untouched.

---

## Slide 5 · PricingAI: from sparse price history to a portfolio price vector

Tracker · [Base pricing] · Trade promotion

Top to bottom flow: Inputs → Model → Calibration → Outputs.

- **Inputs** · Sales, prices, volumes and distribution by item, retailer and week; costs and sell-in prices; conjoint priors where available; all keyed to a product master (brand, size, taste, price line).
- **Model** · Two stages: a Bayesian hierarchical model estimates own and cross price elasticities as full distributions, then a differential-evolution search finds the best prices.
- **Calibration** · Up to ten seeded runs, each posterior seeding the next.
- **Outputs** · One price vector across 40 or more product groups, respecting price ladders and thresholds, with predicted volume, revenue and margin including cross price effects.

---

## Slide 6 · Shared product traits let rare price moves still display price sensitivity

Tracker · [Base pricing] · Trade promotion

Estimating a separate price sensitivity for every product and retailer combination asks more than the data can answer, because shelf prices rarely move. The model instead breaks sensitivity into a few traits that products share, and estimates those together.

**Price sensitivity, before and after**

- **a separate figure for every product and retailer** (shown as a dense grid of individual figures)
- **five shared traits that add up:** category baseline, brand, pack size, flavour, retailer

Each estimate comes back as a range rather than a single number, so the uncertainty travels with it. One cycle's results become the starting point for the next.

> Price sensitivities hold steady between cycles, so a recommendation stays defensible in front of a retailer.

---

## Slide 7 · The portfolio has to be priced as one because every move ripples

Tracker · [Base pricing] · Trade promotion

Changing one price shifts demand across every other product, so across a large portfolio the trade-off surface turns bumpy, with many false peaks.

> **[Figure]** A rugged non-convex objective landscape with ten independent search runs settling on three different peaks, four of them on the global optimum.
>
>

- Up to ten searches run in parallel, each from a different starting point.

> Every search is seeded, so the same inputs always return the same prices and a planner asking why a price moved gets the same answer twice. A typical run finishes inside thirty minutes.

---

## Slide 8 · PromoAI: from harmonized history to a signed calendar

Tracker · Base pricing · [Trade promotion]

Top to bottom flow: Inputs → Model → Calibration → Outputs.

- **Inputs** · Weekly sales, prices, promotions, shelf placement, trade spend and cost, grouped into product groups.
- **Model** · One global demand model (LightGBM); its curve is linearised into a mixed-integer program that picks one promotional option per product per week.
- **Calibration** · Solved in Gurobi to a 1 to 5% optimality gap, backtested against legacy forecasts, retrained quarterly.
- **Outputs** · Promotional calendars over an 8 to 52 week horizon under different revenue-versus-margin objectives, each with revenue, margin, volume and frequency for what-if simulation.

---

## Slide 9 · One demand model covers the portfolio, so thin history still forecasts well

Tracker · Base pricing · [Trade promotion]

One machine learning model covers every product group at once, in place of a separate model per product. Groups with little sales history borrow patterns from similar ones, while the model still learns its own baseline for each. It is tuned on percentage error, which keeps accuracy comparable across products selling in wildly different volumes.

**What drives demand, in order of influence**

- **Which product** · product group · ranked first
- **Timing** · year, holiday, week of year, quarter
- **Promotion** · offer type, shelf price, price paid, discount depth, month

> Brand strength dominates demand, seasonality comes next, and the promotion levers a planner actually controls rank third. That ordering sets a realistic ceiling on what any promotion can move.

---

## Slide 10 · Simplifying the demand curve is what makes the calendar solvable

Tracker · Base pricing · [Trade promotion]

The optimizer works in straight segments, and the demand model produces a curve. The system samples that curve across the range of competitor discounting, then replaces it with a few straight segments.

> **[Figure]** A nonlinear demand response curve with a three segment piecewise linear approximation and two interior breakpoints.
>
> Legend: demand model | straight line stand-in | ● joins

An automated fitting step places the joins where they matter most, and stops adding segments once further ones stop earning the solver time they cost. Two to four segments suffice everywhere.

> This is the seam between prediction and decision. Skip it and an accurate forecast stays a slide, rather than a signed calendar.

---

## Slide 11 · A new market goes live by editing a rules file, rather than the code

Tracker · Base pricing · [Trade promotion]

The optimizer picks exactly one promotional option per product per week. The design separates the mathematics that holds everywhere from the commercial rules that vary market to market.

- **Fixed · the same in every market** One offer per week for each product. Competitor pressure carries what rival formats are discounting into the forecast. The simplified demand curve keeps the whole problem solvable.
- **Configurable · each market keeps its own rules in a plain text file** Financial: revenue targets, trade spend limits, margin preservation, market share. Calendar: seasonal rules, holiday alignment, frequency bounds, spacing. Execution: competitor lockout, ad block linking, retail price restrictions, front page exposure.

> **"This configuration approach dramatically reduces the technical effort required for market expansion."**

---

## Slide 12 · Nothing reaches a planner until it clears accuracy, economic sanity and a full business-rule run

**Checks cleared before release, and again at every refresh**

- 01 Accuracy. Tested on periods held back from training, and against the forecasts it replaced.
- 02 Economic sense. Price sensitivities have to land in ranges a commercial team recognizes.
- 03 Full run through. Every business rule verified on past and simulated plans.

---

## Slide 13 · Planners execute the recommendations, and cycle times fell from weeks to minutes

- Commercial teams accept and execute the large majority of optimized recommendations, which is the point at which the value becomes real.
- Markets absorbed more retailers and categories within their existing planning headcount, and planning meetings moved from spreadsheet review to scenario analysis.
- Scope grew from a single pilot market to deployment across several continents.

> **"The single most important factor in driving adoption was giving users meaningful control."**

> Senior management confirmed improvements in revenue and margin, while the underlying figures remain commercially sensitive.

---

## Slide 14 · Where in your planning stack does a human still reconcile the model output by hand?

Pick one planning process you own. Trace it from the forecast through to the committed decision, and mark the point where a person still balances the model output against the constraints by hand.

That reconciliation is your optimization layer, waiting to be built.

Name it in the comments.

---
