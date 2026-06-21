# Network Science Models

Models for understanding connected systems, from social networks to infrastructure.

## Small-World Networks

**Principle**: Networks with high local clustering but short average path lengths between any two nodes.

**When to Use**:
- Social network analysis
- Information diffusion
- System connectivity

**Questions**:
- What's the average path length?
- How clustered are local connections?
- What shortcuts connect distant parts?

**Example**: Six degrees of separation, brain neural networks, power grids.

**Pitfalls**:
- Not all networks are small-world
- Requires specific topology
- Can be disrupted easily

---

## Preferential Attachment

**Principle**: "Rich get richer" - nodes with more connections are more likely to gain new connections.

**When to Use**:
- Growth dynamics
- Inequality understanding
- Network evolution

**Questions**:
- Do hubs attract more connections?
- How does this create power-law distribution?
- Can we break preferential attachment?

**Example**: Social media followers, citation networks, wealth accumulation, airport hubs.

**Pitfalls**:
- Can create winner-take-all dynamics
- Not always desirable
- Can be amplified or dampened

---

## Network Effects

**Principle**: Value of a network increases with the number of users (Metcalfe's Law: value ∝ n²).

**When to Use**:
- Platform strategy
- Growth planning
- Competitive moats

**Questions**:
- Does adding users add value for existing users?
- What's the minimum viable network size?
- Are there negative network effects?

**Example**: Social networks, marketplaces, telephones, programming languages.

**Pitfalls**:
- Can be negative (congestion, spam)
- Cold start problem
- May not be quadratic

---

## Betweenness Centrality

**Principle**: Importance of nodes as bridges - how often they lie on shortest paths between others.

**When to Use**:
- Identifying key connectors
- Bottleneck analysis
- Influence mapping

**Questions**:
- Which nodes connect different clusters?
- What happens if bridges fail?
- Who controls information flow?

**Example**: Diplomats between nations, translators between communities, routers in networks.

**Pitfalls**:
- Computationally expensive
- May not equal influence
- Can create single points of failure

---

## Community Detection

**Principle**: Identifying densely connected subgroups within larger networks.

**When to Use**:
- Organizational structure
- Market segmentation
- Social group analysis

**Questions**:
- What natural clusters exist?
- How isolated are communities?
- What connects communities?

**Example**: Friend groups in social networks, product categories, research communities.

**Pitfalls**:
- Many algorithms, different results
- Communities overlap
- May be hierarchical

---

## Network Resilience

**Principle**: Ability of networks to maintain function despite node/edge failures.

**When to Use**:
- System design
- Risk assessment
- Redundancy planning

**Questions**:
- How does the network fail?
- Are failures correlated?
- What's the critical threshold?

**Example**: Internet routing (resilient), power grids (less resilient), supply chains.

**Pitfalls**:
- Targeted vs random attacks differ
- Resilience costs efficiency
- Cascading failures possible

---

## Information Diffusion

**Principle**: How information/behavior spreads through network topology and dynamics.

**When to Use**:
- Viral marketing
- Rumor control
- Innovation adoption

**Questions**:
- What's the transmission probability?
- Who are the super-spreaders?
- How fast does this diffuse?

**Example**: Viral videos, disease spread, technology adoption, memes.

**Pitfalls**:
- Prediction is hard
- Timing matters
- Content affects diffusion rate

---

## Clustering Coefficient

**Principle**: Measure of how much nodes cluster together - "friend of friend is also friend."

**When to Use**:
- Network structure analysis
- Trust assessment
- Redundancy evaluation

**Questions**:
- How tight-knit are local connections?
- Is this more clustered than random?
- What does clustering enable/prevent?

**Example**: High clustering in social networks, low in power grids, variable in biological networks.

**Pitfalls**:
- Local vs global clustering
- Doesn't capture all structure
- May miss weak ties

---

## Degree Distribution

**Principle**: The pattern of how connections are distributed across nodes - normal, power-law, or other.

**When to Use**:
- Network type identification
- Vulnerability assessment
- Growth prediction

**Questions**:
- Is distribution normal or power-law?
- Are there super-nodes (hubs)?
- How does this affect resilience?

**Example**: Power-law: social networks, WWW. Normal: power grids, roads.

**Pitfalls**:
- Distribution type affects everything
- Can be misleading if wrong
- May change over time

---

## Viral Coefficient

**Principle**: Average number of new users each existing user brings (k-factor).

**When to Use**:
- Growth modeling
- Product strategy
- Marketing planning

**Questions**:
- What's our viral coefficient (k)?
- Is k > 1 (exponential) or k < 1 (dying)?
- How can we increase k?

**Example**: k=1.2 means each user brings 1.2 others (exponential growth); k=0.8 means decline.

**Pitfalls**:
- Averages hide distribution
- Changes over time
- Requires sustainability

---

## Integration with Other Models

**Combines well with**:
- Systems Thinking → Network as system
- Complexity Science → Emergent network behavior
- Game Theory → Strategic network formation
- Epidemiology → Diffusion dynamics

**Conflicts with**:
- Atomistic analysis
- Linear models
- Ignoring structure
