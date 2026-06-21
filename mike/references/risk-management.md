# Risk Management Models

Models for identifying, assessing, and mitigating risks systematically.

## Risk Matrix

**Principle**: Assess risks on two dimensions - probability of occurrence and potential impact.

**When to Use**:
- Risk prioritization
- Resource allocation
- Portfolio management

**Questions**:
- What's the likelihood of this risk?
- What's the potential impact?
- Which quadrant: high/low probability × high/low impact?

**Example**: 2×2 matrix with High Probability/High Impact (urgent), Low/Low (ignore), etc.

**Pitfalls**:
- Oversimplifies complex risks
- Probability/impact often correlated
- Categorical boundaries are arbitrary

---

## Diversification

**Principle**: Spreading exposure across uncorrelated assets/options reduces overall risk.

**When to Use**:
- Portfolio construction
- Strategy design
- Capability building

**Questions**:
- Are these truly uncorrelated?
- What's the optimal diversification level?
- Am I over-diversified (diworsification)?

**Example**: Stock portfolios, skill sets, customer base, supplier networks.

**Pitfalls**:
- Correlation increases in crises
- Over-diversification dilutes returns
- Some bets should be concentrated

---

## Stress Testing

**Principle**: Test system performance under extreme but plausible scenarios.

**When to Use**:
- Robustness assessment
- Contingency planning
- Capacity evaluation

**Questions**:
- What extreme scenarios are plausible?
- How does the system perform under stress?
- Where are the breaking points?

**Example**: Bank capital adequacy tests, infrastructure load testing, supply chain scenarios.

**Pitfalls**:
- Hard to imagine all scenarios
- May pass tests but fail in reality
- Can create false confidence

---

## Value at Risk (VaR)

**Principle**: Maximum expected loss over a time period at a given confidence level.

**When to Use**:
- Financial risk quantification
- Position sizing
- Risk budgeting

**Questions**:
- What's the worst loss at X% confidence?
- Over what time horizon?
- What's beyond VaR (tail risk)?

**Example**: "95% confidence of losing no more than $1M in a day" = $1M VaR at 95%.

**Pitfalls**:
- Ignores tail risk beyond VaR
- Assumes normal distribution (often wrong)
- Can be gamed

---

## Tail Risk

**Principle**: Extreme events in distribution tails - rare but catastrophic losses.

**When to Use**:
- Black swan preparation
- Portfolio insurance
- Existential risk assessment

**Questions**:
- What's the worst-case scenario?
- How would we survive tail events?
- What's our exposure to fat tails?

**Example**: Market crashes, pandemics, natural disasters, system failures.

**Pitfalls**:
- Low probability creates complacency
- Hard to estimate probabilities
- May overprepare for unlikely events

---

## Contingency Planning

**Principle**: Prepare backup plans for identified risks before they materialize.

**When to Use**:
- Project planning
- Crisis preparation
- Business continuity

**Questions**:
- What could go wrong?
- What's our response plan?
- Do we have resources allocated?

**Example**: Backup systems, emergency funds, succession plans, disaster recovery.

**Pitfalls**:
- Can't plan for everything
- Plans may become obsolete
- Resources tied up in contingencies

---

## Risk Appetite

**Principle**: The amount and type of risk an entity is willing to accept in pursuit of objectives.

**When to Use**:
- Strategy alignment
- Decision frameworks
- Risk culture

**Questions**:
- What level of risk is acceptable?
- What types of risk are we willing to take?
- How does this align with objectives?

**Example**: Startup (high risk appetite) vs utility (low risk appetite), geographic expansion vs core market.

**Pitfalls**:
- Often poorly defined
- May not match actual behavior
- Changes with circumstances

---

## Hedging Strategies

**Principle**: Offsetting potential losses through inverse positions or insurance.

**When to Use**:
- Risk transfer
- Downside protection
- Exposure management

**Questions**:
- What am I hedging against?
- What's the cost of hedging?
- Is this a pure hedge or speculation?

**Example**: Currency hedging, options, insurance, diversification, fixed-price contracts.

**Pitfalls**:
- Hedges cost money (reduce upside)
- Imperfect hedges (basis risk)
- May eliminate good volatility too

---

## Black Swan Protection

**Principle**: Strategies specifically for extreme, unpredictable events with massive impact.

**When to Use**:
- Catastrophic risk mitigation
- Anti-fragile positioning
- Asymmetric payoff seeking

**Questions**:
- What unthinkable event would destroy us?
- How can we benefit from extreme volatility?
- Where are convex exposures?

**Example**: Options strategies, barbell portfolio (safe + highly speculative), redundancy, optionality.

**Pitfalls**:
- Expensive to maintain
- May never pay off
- Can't protect against all swans

---

## Risk Register

**Principle**: Systematic documentation of identified risks, assessment, mitigation, and ownership.

**When to Use**:
- Project management
- Enterprise risk management
- Compliance

**Questions**:
- What risks have we identified?
- Who owns each risk?
- What's the mitigation plan and status?

**Example**: Project risk logs, corporate risk registers, operational risk tracking.

**Pitfalls**:
- Can become bureaucratic
- May not capture unknown unknowns
- Requires maintenance

---

## Risk Appetite

**Principle**: Organization's willingness to accept risk in pursuit of objectives; defines acceptable risk-taking boundaries.

**When to Use**:
- Strategic planning
- Policy setting
- Decision frameworks
- Culture definition

**Questions**:
- How much risk are we willing to take?
- What risks are we never willing to accept?
- Does our behavior match our stated appetite?

**Example**: Startup (high risk appetite) vs bank (low); innovation vs safety culture; aggressive vs conservative investment strategies.

**Pitfalls**:
- Stated vs actual appetite differ
- Can shift in crises
- One size doesn't fit all activities

---

## Contingency Planning

**Principle**: Prepare backup plans for when primary plans fail; anticipate failure modes and have ready alternatives.

**When to Use**:
- Critical operations
- High-uncertainty environments
- Disaster recovery
- Strategic planning

**Questions**:
- What could go wrong?
- What's Plan B, C, D?
- How quickly can we switch plans?

**Example**: Emergency funds, backup suppliers, redundant systems, evacuation plans, business continuity planning.

**Pitfalls**:
- Can't plan for everything
- Maintenance burden
- May reduce commitment to Plan A

---

## Tail Risk

**Principle**: Risk of extreme events in distribution tails; rare but catastrophic outcomes beyond normal risk calculations.

**When to Use**:
- Extreme event planning
- Portfolio protection
- Systemic risk assessment
- Black swan preparation

**Questions**:
- What's the worst case?
- What if the unlikely happens?
- Can we survive tail events?

**Example**: Market crashes, pandemics, natural disasters, cyber attacks; 2008 financial crisis, COVID-19.

**Pitfalls**:
- Hard to quantify
- Can lead to over-preparation
- VaR misses tail risk

---

## Integration with Other Models

**Combines well with**:
- Probability Models → Quantifying risk
- Complexity Science → Understanding cascading risks
- Decision-Making → Risk-adjusted decisions
- Black Swan + Antifragility → Extreme event preparation

**Conflicts with**:
- Pure optimization (ignores risk)
- Risk-neutral assumptions
- Certainty illusions

