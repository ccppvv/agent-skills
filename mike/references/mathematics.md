# Mathematics & Logic Models

Fundamental mathematical and logical reasoning frameworks for structured thinking.

## Occam's Razor

**Principle**: Among competing explanations, the simplest one is usually correct (entities should not be multiplied beyond necessity).

**When to Use**:
- Choosing between theories
- Debugging and troubleshooting
- Hypothesis selection
- Model building

**Questions**:
- What's the simplest explanation?
- Am I adding unnecessary complexity?
- Which theory requires fewer assumptions?

**Example**: Hearing hoofbeats, think horses not zebras. Software bug is more likely configuration error than compiler bug.

**Pitfalls**:
- Oversimplification
- "Simplest" can be subjective
- Sometimes reality is complex
- Can miss valid complex explanations

---

## Inductive Reasoning

**Principle**: Drawing general conclusions from specific observations.

**When to Use**:
- Pattern recognition
- Hypothesis generation
- Learning from experience
- Scientific discovery

**Process**:
1. Observe specific instances
2. Identify patterns
3. Formulate general principle
4. Test with new instances

**Example**: Observing that the sun has risen every day leads to conclusion "the sun rises every day."

**Pitfalls**:
- Hasty generalization from few cases
- Sampling bias
- Black swan events
- Induction problem (Hume)

---

## Deductive Reasoning

**Principle**: Drawing specific conclusions from general principles.

**When to Use**:
- Logical proof
- Applying rules to cases
- Mathematical reasoning
- Legal reasoning

**Structure**:
- Major premise: All A are B
- Minor premise: C is A
- Conclusion: Therefore C is B

**Example**: All mammals are warm-blooded. Whales are mammals. Therefore whales are warm-blooded.

**Pitfalls**:
- Invalid premises lead to invalid conclusions
- Formal validity ≠ truth
- Requires correct application of rules

---

## Proof by Contradiction

**Principle**: Prove a statement by assuming its negation and deriving a contradiction.

**When to Use**:
- Mathematical proofs
- Logical arguments
- Showing impossibility
- Refuting claims

**Process**:
1. Assume the opposite of what you want to prove
2. Follow logical implications
3. Arrive at contradiction
4. Conclude original statement must be true

**Example**: Proving √2 is irrational by assuming it's rational and deriving a contradiction.

**Pitfalls**:
- Must ensure contradiction is genuine
- Requires careful logical steps
- Can be confusing to follow

---

## Mathematical Induction

**Principle**: Prove a statement for all natural numbers by proving base case and inductive step.

**When to Use**:
- Proving properties of sequences
- Algorithm correctness
- Recursive structures
- General formulas

**Process**:
1. Base case: Prove for n=1 (or n=0)
2. Inductive hypothesis: Assume true for n=k
3. Inductive step: Prove true for n=k+1
4. Conclude: True for all n

**Example**: Proving sum formula: 1+2+...+n = n(n+1)/2

**Pitfalls**:
- Must prove both base case and inductive step
- Inductive step must be valid
- Only works for well-ordered sets

---

## Permutations and Combinations

**Principle**: Methods for counting arrangements (order matters) and selections (order doesn't matter).

**When to Use**:
- Probability calculations
- Planning and scheduling
- Resource allocation
- Possibility analysis

**Formulas**:
- **Permutations**: P(n,r) = n!/(n-r)! (order matters)
- **Combinations**: C(n,r) = n!/[r!(n-r)!] (order doesn't matter)

**Example**: 
- Permutations: Number of ways to arrange 3 books from 5: P(5,3) = 60
- Combinations: Number of ways to choose 3 books from 5: C(5,3) = 10

**Pitfalls**:
- Confusing permutations with combinations
- Overcounting due to symmetry
- Underestimating large factorials

---

## Graph Theory

**Principle**: Mathematical study of networks, nodes, and edges.

**When to Use**:
- Network analysis
- Relationship mapping
- Path optimization
- Dependency analysis

**Key Concepts**:
- **Nodes/Vertices**: Objects
- **Edges**: Connections
- **Directed vs Undirected**: One-way vs two-way
- **Weighted**: Edges have values
- **Path**: Sequence of edges
- **Cycle**: Path that returns to start

**Applications**:
- Social networks
- Transportation routes
- Computer networks
- Project dependencies

**Pitfalls**:
- Can become computationally complex
- May miss important context
- Assumes static structure

---

## Set Theory

**Principle**: Mathematics of collections and their relationships.

**When to Use**:
- Categorization
- Logic and proofs
- Database design
- Understanding overlap

**Operations**:
- **Union (A ∪ B)**: Elements in A or B
- **Intersection (A ∩ B)**: Elements in both
- **Difference (A - B)**: Elements in A but not B
- **Complement**: Elements not in set
- **Subset**: A ⊆ B if all A elements are in B

**Example**: Venn diagrams showing customer segments: new customers, repeat customers, high-value customers, and their overlaps.

**Pitfalls**:
- Set paradoxes (Russell's paradox)
- Ambiguous set definitions
- Confusing element vs. subset

---

## Zero-Sum Game

**Principle**: One player's gain equals another's loss; total gains and losses sum to zero.

**When to Use**:
- Competitive strategy
- Negotiation analysis
- Understanding conflict
- Resource allocation

**Characteristics**:
- Fixed pie
- Pure competition
- No mutual gains possible
- Adversarial

**Examples**:
- Poker
- Futures contracts
- Sports matches
- Market share (approximately)

**Pitfalls**:
- Many situations are non-zero-sum but treated as zero-sum
- Creates adversarial mindset
- Misses cooperation opportunities

---

## Non-Zero-Sum Game

**Principle**: Total gains and losses don't sum to zero; mutual benefit or harm possible.

**When to Use**:
- Cooperation strategy
- Trade negotiations
- Partnership formation
- Win-win thinking

**Characteristics**:
- Variable pie
- Cooperation can benefit both
- Integration possible
- Potential for mutual gain

**Examples**:
- Trade
- Business partnerships
- Environmental cooperation
- Innovation

**Implications**:
- Cooperation can create value
- Trust becomes important
- Long-term relationships matter
- Reputation effects

**Pitfalls**:
- Can be exploited by defectors
- Requires trust
- Coordination challenges
