# Financial Engineering Models

Advanced financial concepts for risk management, pricing, and portfolio optimization.

## Portfolio Theory (Modern Portfolio Theory)

**Principle**: Diversification reduces risk without sacrificing expected return; optimal portfolios balance risk and return on the efficient frontier.

**When to Use**:
- Investment allocation
- Risk management
- Asset diversification
- Strategic resource allocation

**Questions**:
- How correlated are these assets?
- What's the optimal risk-return tradeoff?
- Am I diversified or just scattered?

**Example**: Don't put all eggs in one basket; combine uncorrelated assets (stocks + bonds + real estate) to reduce portfolio volatility.

**Pitfalls**:
- Assumes normal distributions (ignores fat tails)
- Correlations increase in crises
- Past correlations don't predict future

---

## Value at Risk (VaR)

**Principle**: Maximum expected loss over a given time period at a specific confidence level (e.g., 95% confident won't lose more than $X).

**When to Use**:
- Risk assessment
- Capital allocation
- Regulatory compliance
- Stress testing

**Questions**:
- What's my maximum loss at X% confidence?
- How much capital should I reserve?
- What's the tail risk beyond VaR?

**Example**: "We're 99% confident we won't lose more than $1M in a day." Used by banks for capital requirements.

**Pitfalls**:
- Ignores tail events (the 1%)
- Doesn't tell you how bad the tail can be
- Can create false sense of security

---

## Hedging Strategies

**Principle**: Take offsetting positions to reduce exposure to adverse price movements; insurance against downside.

**When to Use**:
- Risk mitigation
- Protecting gains
- Reducing volatility
- Currency/commodity exposure

**Questions**:
- What risk am I most exposed to?
- What's the cost of the hedge?
- Am I hedging or speculating?

**Example**: Airline hedges fuel costs with futures; exporter hedges currency risk; farmer locks in crop prices.

**Pitfalls**:
- Hedging costs money (reduces upside)
- Basis risk (hedge doesn't perfectly match)
- Over-hedging can create new risks

---

## Delta Hedging

**Principle**: Continuously adjust positions to maintain risk neutrality with respect to underlying asset price changes.

**When to Use**:
- Options market making
- Risk-neutral pricing
- Dynamic hedging
- Volatility trading

**Questions**:
- How sensitive is my position to price changes?
- How often should I rebalance?
- What are transaction costs?

**Example**: Options dealer buys/sells underlying stock to offset delta exposure from options sold to customers.

**Pitfalls**:
- Requires continuous rebalancing (costly)
- Gamma risk (delta changes)
- Assumes continuous markets

---

## Volatility Arbitrage

**Principle**: Profit from difference between implied volatility (option prices) and realized volatility (actual market moves).

**When to Use**:
- Options trading
- Market inefficiency exploitation
- Statistical arbitrage
- Risk-neutral strategies

**Questions**:
- Is implied volatility too high or low?
- What's my forecast of realized volatility?
- How will I hedge directional risk?

**Example**: Sell options when implied vol > expected realized vol; buy when implied vol < expected realized vol.

**Pitfalls**:
- Requires accurate volatility forecasting
- Jump risk (sudden moves)
- Model risk

---

## Convexity

**Principle**: Non-linear relationship between price and yield; positive convexity means gains from yield drops exceed losses from yield increases.

**When to Use**:
- Bond portfolio management
- Options valuation
- Risk assessment
- Strategic positioning

**Questions**:
- How does my position behave in extreme moves?
- Do I benefit from volatility?
- What's the cost of convexity?

**Example**: Bonds have positive convexity (benefit from rate volatility); short options have negative convexity (hurt by big moves).

**Pitfalls**:
- Positive convexity costs money (lower yield)
- Convexity changes with conditions
- Can be complex to calculate

---

## Margin of Safety (in Finance)

**Principle**: Buy assets well below intrinsic value to provide cushion against errors in valuation or adverse events.

**When to Use**:
- Value investing
- Risk management
- Capital preservation
- Conservative analysis

**Questions**:
- What's the intrinsic value?
- How large a margin do I need?
- What could I be wrong about?

**Example**: Warren Buffett - buy $1 of value for $0.50; provides protection against valuation errors and downside risk.

**Pitfalls**:
- Hard to determine intrinsic value
- Market can stay "wrong" longer than you can stay solvent
- Opportunity cost of waiting

---

## Liquidity Premium

**Principle**: Less liquid assets must offer higher expected returns to compensate for difficulty of selling quickly without price impact.

**When to Use**:
- Asset valuation
- Investment decisions
- Risk pricing
- Portfolio construction

**Questions**:
- How quickly can I exit this position?
- What's the bid-ask spread?
- How much return compensates for illiquidity?

**Example**: Private equity demands higher returns than public stocks; corporate bonds vs Treasury bonds.

**Pitfalls**:
- Liquidity evaporates in crises
- Hard to quantify liquidity premium
- Can trap capital

---

## Duration

**Principle**: Measure of bond price sensitivity to interest rate changes; approximates percentage price change for 1% rate move.

**When to Use**:
- Bond portfolio management
- Interest rate risk assessment
- Asset-liability matching
- Immunization strategies

**Questions**:
- How sensitive am I to rate changes?
- What's my duration exposure?
- How do I match assets and liabilities?

**Example**: Bond with duration of 5 years loses ~5% value if rates rise 1%; duration gap analysis for banks.

**Pitfalls**:
- Linear approximation (convexity matters)
- Assumes parallel yield curve shifts
- Reinvestment risk

---

## Leverage (Financial)

**Principle**: Using borrowed capital to amplify returns (and losses); magnifies both gains and risks.

**When to Use**:
- Return enhancement
- Capital efficiency
- Arbitrage strategies
- Real estate investing

**Questions**:
- What's my debt-to-equity ratio?
- Can I service debt in downturns?
- What's the cost of leverage vs expected return?

**Example**: Buying house with 20% down (5:1 leverage); hedge funds using margin; corporate debt for acquisitions.

**Pitfalls**:
- Magnifies losses equally
- Forced liquidation in drawdowns
- Interest costs compound
- Can lead to bankruptcy

---

## Integration with Other Models

**Combines well with**:
- Probability & Statistics → Risk quantification
- Game Theory → Market dynamics
- Optionality → Strategic flexibility
- Antifragility → Benefiting from volatility

**Conflicts with**:
- Overconfidence in models
- Ignoring tail risks
- Assuming normal distributions
