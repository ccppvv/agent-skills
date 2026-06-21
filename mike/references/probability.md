# Probability and Statistics Models

Reasoning under uncertainty and making better predictions.

## Bayesian Thinking

**Principle**: Update beliefs based on new evidence; combine prior probability with new data.

**Formula**: P(H|E) = P(E|H) × P(H) / P(E)
- P(H|E): Posterior probability (belief after evidence)
- P(E|H): Likelihood (how likely evidence if hypothesis true)
- P(H): Prior probability (belief before evidence)
- P(E): Probability of evidence

**When to Use**:
- Updating beliefs with new information
- Medical diagnosis
- Evaluating claims and evidence

**Questions**:
- What was my prior belief?
- How strong is this new evidence?
- What's my updated belief?

**Example**:
- Prior: 1% chance you have disease
- Test 90% accurate (90% true positive, 10% false positive)
- Test positive → Only ~8.3% chance you actually have disease
- (Most people would guess much higher!)

**Pitfalls**:
- Ignoring base rates (prior probability)
- Overweighting new evidence
- Forgetting to update continuously

---

## Base Rate Neglect

**Principle**: Tendency to ignore population-level statistics in favor of specific case information.

**When to Use**:
- Risk assessment
- Prediction and forecasting
- Evaluating unique cases

**Questions**:
- What's the base rate for this type of situation?
- Am I being swayed by specific details over statistical reality?
- How common is this generally?

**Example**:
- "This startup has a great team" (specific)
- vs. "90% of startups fail" (base rate)
- Optimal prediction weighs both

**Mitigation**:
- Always look up base rates first
- Use base rate as starting point
- Only deviate with strong evidence

---

## Regression to the Mean

**Principle**: Extreme values tend to be followed by more moderate values.

**When to Use**:
- Evaluating performance
- Making predictions
- Understanding fluctuations

**Questions**:
- Is this extreme performance likely to continue?
- How much is luck vs. skill?
- What's the typical range?

**Examples**:
- Rookie of the year often "sophomore slump"
- Stock picking: Hot fund performance often cools
- Sports: Exceptional season followed by average one

**Pitfalls**:
- Attributing mean reversion to your intervention
- Creating false narratives for natural variation
- Over-correcting for regression

---

## Expected Value

**Principle**: Average outcome when accounting for probabilities: E(V) = Σ(probability × outcome)

**When to Use**:
- Decision-making under uncertainty
- Comparing risky options
- Portfolio optimization

**Questions**:
- What are all possible outcomes?
- What's the probability of each?
- What's the weighted average?

**Example**:
- 70% chance of $100, 30% chance of $0
- Expected Value = (0.7 × $100) + (0.3 × $0) = $70

**Considerations**:
- Doesn't account for risk tolerance
- Single expected value masks distribution
- May not apply to one-time decisions
- Consider utility, not just money

---

## Black Swan

**Principle**: Rare, high-impact events that are unpredictable but rationalized in hindsight.

**Characteristics**:
- **Rarity**: Outside normal expectations
- **Extreme impact**: Massive consequences
- **Retrospective predictability**: Seems obvious after the fact

**When to Use**:
- Risk management
- Strategy planning
- Understanding history

**Questions**:
- What low-probability, high-impact events could occur?
- How fragile am I to tail risks?
- Am I confusing hindsight with foresight?

**Examples**:
- 2008 Financial Crisis
- COVID-19 Pandemic
- Internet revolution
- 9/11 attacks

**Responses**:
- Build antifragility (benefit from volatility)
- Avoid catastrophic risks
- Keep optionality
- Don't over-rely on models

---

## Sample Size and Statistical Significance

**Principle**: Small samples produce unreliable results; need adequate size for valid conclusions.

**When to Use**:
- Evaluating research/data
- A/B testing
- Making decisions from evidence

**Questions**:
- How large is the sample?
- Is this result statistically significant?
- Could this be random chance?

**Key Concepts**:
- **Statistical significance**: Unlikely to be due to chance
- **Effect size**: Magnitude of difference
- **Confidence interval**: Range of likely values
- **p-value**: Probability of result if no real effect

**Pitfalls**:
- "Statistically significant" ≠ "important"
- Multiple comparisons increase false positives
- p-hacking and publication bias

---

## Law of Large Numbers

**Principle**: As sample size increases, sample average converges to expected value.

**When to Use**:
- Understanding variance
- Portfolio construction
- Insurance and risk pooling

**Questions**:
- Do I have enough trials for reliable averages?
- What's the variance around the mean?
- How many samples until convergence?

**Examples**:
- Casino profits: Reliable over many bets, uncertain per bet
- Insurance: Predictable claims across many policyholders
- Quality control: Test batches, not individual items

**Pitfalls**:
- "Gambler's fallacy": Thinking past results affect future independent events
- Assuming all distributions converge quickly
- Ignoring tail risks

---

## Antifragility

**Principle**: Systems that gain from disorder, volatility, and stress (beyond robust or resilient).

**Spectrum**:
- **Fragile**: Harmed by volatility
- **Robust**: Unaffected by volatility
- **Antifragile**: Benefits from volatility

**When to Use**:
- Risk management
- System design
- Personal development

**Questions**:
- Does this get stronger or weaker under stress?
- How can I benefit from volatility?
- What's my exposure to tail events?

**Examples**:
- Fragile: Egg, fixed schedule, large corporation
- Robust: Rock, flexible schedule, regulations
- Antifragile: Immune system, trial and error, evolution

**Strategies**:
- Build in redundancy
- Keep optionality
- Use barbell strategy (safe + speculative, avoid medium risk)
- Have "skin in the game"

---

## Fat Tails and Power Laws

**Principle**: Some distributions have "fat tails" - extreme events are more common than normal distribution predicts.

**Normal vs. Fat-Tailed**:
- **Normal**: Most variation near mean, rare extremes (height, test scores)
- **Fat-Tailed**: Extremes more common, dominated by outliers (wealth, book sales, city size)

**When to Use**:
- Risk assessment
- Resource allocation
- Understanding inequality

**Questions**:
- Is this normally distributed or fat-tailed?
- How important are extreme outcomes?
- Am I underestimating tail risk?

**Examples of Power Laws**:
- Wealth distribution (Pareto)
- City sizes (Zipf's law)
- Book/movie sales
- Earthquake magnitudes

**Implications**:
- Can't use normal distribution statistics
- Extremes matter more than average
- Winner-take-all dynamics
- Black swans more likely

---

## Regression to the Mean

**Principle**: Extreme values tend to be followed by more moderate values closer to the average.

**When to Use**:
- Performance evaluation
- Avoiding overreaction to outliers
- Understanding natural variation

**Questions**:
- Is this extreme result likely to persist?
- How much of this is luck vs. skill?
- What's the baseline average?

**Example**: A student who scores exceptionally high on one test will likely score closer to their average on the next test. Sports teams with extreme seasons tend toward average the following year.

**Pitfalls**:
- Mistaking regression for intervention effects
- Can lead to complacency
- Doesn't mean no real change occurred

---

## Sample Size Effects

**Principle**: Small samples produce more extreme results and less reliable estimates than large samples.

**When to Use**:
- Evaluating statistics and studies
- A/B testing
- Quality assessment

**Questions**:
- How large is the sample?
- Is this result statistically significant?
- Could this be random variation?

**Example**: Small schools appear in both "best" and "worst" lists more often than large schools, not due to quality but due to higher variance in small samples.

**Pitfalls**:
- Law of small numbers bias
- Overconfidence in small samples
- Ignoring confidence intervals

---

## Base Rate Neglect

**Principle**: The tendency to ignore base rates (prior probabilities) in favor of specific information.

**When to Use**:
- Diagnosis and prediction
- Risk assessment
- Avoiding false positives

**Questions**:
- What's the base rate in the population?
- How rare is this condition/event?
- Am I weighing the prior probability properly?

**Example**: If a disease affects 1% of population and test is 95% accurate, a positive result means only ~16% chance of having disease (not 95%).

**Pitfalls**:
- Focusing on specific case details
- Ignoring prevalence
- Overweighting anecdotes

---

## Central Limit Theorem

**Principle**: Distribution of sample means approaches normal distribution as sample size increases, regardless of original distribution.

**When to Use**:
- Statistical inference
- Understanding why normal distribution appears often
- Justifying parametric tests

**Questions**:
- Is my sample size large enough?
- Can I assume normality of means?
- What's the underlying distribution?

**Example**: Heights are normally distributed partly because they're the sum of many genetic and environmental factors.

**Pitfalls**:
- Requires sufficient sample size
- Doesn't apply to medians or other statistics
- Original distribution still matters for small samples

---

## Monte Carlo Simulation

**Principle**: Use random sampling to model complex systems and estimate probabilities.

**When to Use**:
- Complex probability problems
- Risk analysis
- When analytical solutions are intractable

**Questions**:
- What are the key uncertainties?
- What probability distributions apply?
- How many simulations do I need?

**Example**: Estimate project completion time by simulating thousands of scenarios with random task durations.

**Pitfalls**:
- Garbage in, garbage out
- Can create false precision
- Computationally intensive

---

## Confidence Intervals

**Principle**: A range of values that likely contains the true parameter with specified probability.

**When to Use**:
- Reporting estimates with uncertainty
- Comparing groups
- Decision-making under uncertainty

**Questions**:
- What's the confidence level (typically 95%)?
- How wide is the interval?
- Does it include practically significant values?

**Example**: "Sales will increase by 5% (95% CI: 2%-8%)" means we're 95% confident the true increase is between 2-8%.

**Pitfalls**:
- Misinterpreting as probability of truth
- Ignoring width of interval
- Multiple comparison problems

---

## Correlation vs. Causation

**Principle**: Variables may be correlated without one causing the other.

**When to Use**:
- Interpreting research findings
- Avoiding false conclusions
- Designing interventions

**Questions**:
- Could there be a common cause?
- Could causation run the opposite direction?
- Is this just coincidence?
- What's the mechanism?

**Example**: Ice cream sales correlate with drownings (both caused by hot weather), but ice cream doesn't cause drownings.

**Pitfalls**:
- Confounding variables
- Reverse causation
- Selection bias
- Spurious correlations

---

## Statistical Significance

**Principle**: A result is statistically significant if it's unlikely to have occurred by chance alone.

**When to Use**:
- Hypothesis testing
- Evaluating research
- A/B testing

**Questions**:
- What's the p-value?
- Is the effect size meaningful?
- Could this be due to multiple testing?

**Example**: p < 0.05 means less than 5% chance of observing this result if null hypothesis is true.

**Pitfalls**:
- Confusing significance with importance
- P-hacking and multiple testing
- Ignoring effect size
- Publication bias

---

## Probability Distributions

**Principle**: Mathematical functions describing likelihood of different outcomes.

**When to Use**:
- Modeling uncertainty
- Risk analysis
- Understanding data patterns

**Common Distributions**:
- **Normal**: Symmetric bell curve (height, errors)
- **Exponential**: Time until event (wait times)
- **Poisson**: Count of rare events (calls per hour)
- **Power Law**: Fat-tailed (wealth, city sizes)

**Questions**:
- What distribution fits this process?
- What are the parameters?
- Are assumptions met?

**Pitfalls**:
- Wrong distribution choice
- Fat tails in assumed normal distributions
- Ignoring tail dependencies

---

## Conditional Probability

**Principle**: Probability of event A given that event B has occurred: P(A|B).

**When to Use**:
- Sequential decision-making
- Bayesian reasoning
- Understanding dependencies

**Questions**:
- How does new information change probabilities?
- Are these events independent?
- What's P(A|B) vs. P(B|A)?

**Example**: P(rain|clouds) ≠ P(clouds|rain). Probability of rain given clouds is lower than probability of clouds given rain.

**Pitfalls**:
- Confusing P(A|B) with P(B|A)
- Ignoring base rates
- Assuming independence

---

## Gambler's Fallacy

**Principle**: Mistaken belief that past independent events affect future probabilities.

**When to Use**:
- Understanding randomness
- Avoiding betting fallacies
- Teaching probability

**Questions**:
- Are these events truly independent?
- Am I expecting "balance" in randomness?
- Is there memory in the system?

**Example**: After 5 coin flips showing heads, probability of next flip being tails is still 50%, not higher.

**Pitfalls**:
- Seeing patterns in randomness
- Hot hand fallacy (opposite error)
- Applies only to independent events

---

## Law of Small Numbers

**Principle**: Mistaken belief that small samples reflect population characteristics as well as large samples.

**When to Use**:
- Interpreting research
- A/B testing
- Avoiding premature conclusions

**Questions**:
- Is this sample large enough?
- Could this be random variation?
- What would a larger sample show?

**Example**: Seeing 3 successes in 5 trials and assuming 60% success rate, when true rate might be very different.

**Pitfalls**:
- Overconfidence in small samples
- Premature stopping of experiments
- Mistaking noise for signal

---

## Posterior Probability

**Principle**: Updated probability after observing evidence (Bayesian updating).

**When to Use**:
- Updating beliefs with new evidence
- Medical diagnosis
- Incremental learning

**Formula**: P(A|B) = P(B|A) × P(A) / P(B)

**Questions**:
- What was my prior belief?
- How strong is this evidence?
- What's my updated probability?

**Example**: Starting with 1% probability of disease, positive test (90% accuracy) updates to ~8% probability.

**Pitfalls**:
- Ignoring base rates
- Overweighting single pieces of evidence
- Confirmation bias in evidence selection

---

## Prior Probability

**Principle**: Initial probability before observing new evidence.

**When to Use**:
- Bayesian analysis
- Setting baselines
- Avoiding base rate neglect

**Questions**:
- What's the base rate?
- What do I know before seeing this evidence?
- Is my prior reasonable?

**Example**: Before testing for rare disease, prior probability is its prevalence in population (~1%), not 50%.

**Pitfalls**:
- Choosing uninformative priors poorly
- Ignoring available prior information
- Overconfident priors resistant to evidence
