# Decision-Making Models

Models for making better choices under uncertainty and complexity.

## Expected Value

**Principle**: The average outcome if a decision is repeated many times, weighted by probability.

**When to Use**:
- Quantifiable risks and rewards
- Repeated decisions
- Portfolio optimization

**Questions**:
- What are all possible outcomes and their probabilities?
- What's the value of each outcome?
- What's the expected value: EV = Σ(probability × outcome)?

**Example**: Insurance (negative EV but valuable risk transfer), poker decisions, A/B testing.

**Pitfalls**:
- Ignores variance and tail risk
- Assumes utility is linear (it's not)
- Single events may not average out

---

## Minimax

**Principle**: Minimize the maximum possible loss - focus on worst-case scenarios.

**When to Use**:
- High-stakes decisions
- Risk-averse contexts
- Adversarial situations

**Questions**:
- What's the worst that could happen with each option?
- Which option has the least terrible worst-case?
- Can I afford the worst-case outcome?

**Example**: Nuclear deterrence, legal strategy, disaster preparedness.

**Pitfalls**:
- Can be overly pessimistic
- May sacrifice upside for safety
- Assumes rational adversary

---

## Satisficing

**Principle**: Choose the first option that meets your criteria rather than optimizing for the absolute best.

**When to Use**:
- Information gathering is costly
- "Good enough" exists
- Time constraints

**Questions**:
- What are my minimum acceptable criteria?
- What's the cost of continued search?
- Is optimization worth the effort?

**Example**: Job search (accept good offer vs endless searching), apartment hunting, restaurant choice.

**Pitfalls**:
- Criteria may be poorly defined
- May settle too quickly
- Can miss significantly better options

---

## Reversibility

**Principle**: Favor decisions that can be easily reversed over those that can't.

**When to Use**:
- Uncertainty about outcomes
- Learning opportunities
- Experimentation

**Questions**:
- How hard is it to undo this decision?
- What's locked in vs what's flexible?
- Can I try before committing?

**Example**: Two-way vs one-way doors (Bezos), renting vs buying, dating vs marriage.

**Pitfalls**:
- Some irreversible decisions are necessary
- Reversibility may have hidden costs
- Can lead to commitment avoidance

---

## Optionality

**Principle**: Preserve multiple future choices rather than committing prematurely.

**When to Use**:
- High uncertainty environments
- Learning contexts
- Strategic positioning

**Questions**:
- What options does this preserve or eliminate?
- What's the value of waiting for information?
- Am I paying too much to keep options open?

**Example**: Financial options, modular architecture, career breadth before specialization.

**Pitfalls**:
- Options have costs (time, money, attention)
- Can lead to analysis paralysis
- Some opportunities require commitment

---

## Decision Fatigue

**Principle**: Decision quality degrades with the number of decisions made, especially trivial ones.

**When to Use**:
- Decision sequencing
- Routine automation
- Energy management

**Questions**:
- How many decisions have I made today?
- Can I automate/eliminate this decision?
- Is this the right time for important decisions?

**Example**: Why CEOs wear same outfit, meal planning, decision timing.

**Pitfalls**:
- Not all decisions are equally draining
- Individual variation in susceptibility
- Can justify avoiding decisions

---

## Paradox of Choice

**Principle**: Too many options can decrease satisfaction and increase anxiety.

**When to Use**:
- Product design
- Menu creation
- Self-imposed constraints

**Questions**:
- Are more options actually helping?
- What's the optimal number of choices?
- Can I constrain the choice set productively?

**Example**: Jam study (24 options vs 6), restaurant menus, streaming content paralysis.

**Pitfalls**:
- Optimal number varies by context
- Some complexity is necessary
- Can justify limiting options too much

---

## Regret Minimization

**Principle**: Make decisions based on minimizing future regret rather than maximizing current utility.

**When to Use**:
- Major life decisions
- Long-term choices
- Value alignment

**Questions**:
- What will I regret not trying?
- Which choice will I defend more easily to future self?
- What matters in the long run?

**Example**: Career changes, starting businesses, relationships (Bezos regret minimization framework).

**Pitfalls**:
- Future self's values may differ
- Can lead to risk-seeking
- Regret is hard to predict

---

## Multi-Criteria Decision Analysis

**Principle**: Break complex decisions into multiple weighted criteria for systematic evaluation.

**When to Use**:
- Complex tradeoffs
- Team decisions
- Objective comparison needed

**Questions**:
- What are all the relevant criteria?
- How important is each criterion (weight)?
- How does each option score on each criterion?

**Example**: Hiring decisions (skills × culture fit × experience), vendor selection, real estate.

**Pitfalls**:
- Weights are subjective
- May miss intangible factors
- Can become mechanistic

---

## Elimination by Aspects

**Principle**: Sequentially eliminate options that don't meet progressively refined criteria.

**When to Use**:
- Large option sets
- Clear must-haves
- Efficient filtering

**Questions**:
- What's my most important criterion?
- Which options fail this criterion?
- What's the next most important criterion?

**Example**: Job applications (location → salary → role → culture), car shopping, college selection.

**Pitfalls**:
- Order of criteria matters
- May eliminate compensatory options
- Assumes criteria independence

---

## VDS Framework (Variable-Delta-Strategy)

**Principle**: Rapid problem analysis through root variable identification, differential advantage, and concrete strategy derivation. Paired with a 5-step problem clarification process (Output→Input→Constraint→Dilemma→Role).

**When to Use**:
- Quick direction decisions (30 min)
- Problem clarification before deep analysis
- Cross-domain problem analysis
- "I have a vague feeling but can't articulate the problem"

**Questions**:
- V: What 2-3 factors are irreplaceable? (If removed, everything else falls apart?)
- D: What makes my situation different from the standard path? Can this difference be inverted into an advantage?
- S: What one-sentence action follows from V+D? Is it executable and falsifiable?

**Example**: Hearing-impaired girl doing livestream → V: quality+trust+traffic → D: hearing impairment (invertible) → S: target deaf community with sign language, expand globally.

**Pitfalls**:
- V trap: listing 10 "important factors" instead of 2-3 irreplaceable ones
- D trap: equating disadvantage with difference (difference must be invertible)
- S trap: abstract strategy ("work harder") instead of concrete action
- Static trap: V/D/S change over time — re-calibrate quarterly

**详见**: [vds-framework.md](vds-framework.md)

---

## Integration with Other Models

**Combines well with**:
- Probability Models → Quantifying uncertainty in decisions
- Cognitive Biases → Recognizing decision traps
- Expected Value + Regret Minimization → Balanced framework
- Systems Thinking → Understanding decision consequences

**Conflicts with**:
- Pure intuition
- Analysis paralysis
- Decision avoidance
