# Project Management Models

Mental models for effective project planning, execution, and delivery.

## Critical Path Method

**Principle**: Identify the sequence of dependent tasks that determines minimum project duration.

**When to Use**:
- Project scheduling
- Deadline management
- Resource prioritization
- Identifying bottlenecks

**Components**:
- **Critical path**: Longest sequence of tasks
- **Float/slack**: How much tasks can slip
- **Dependencies**: Task relationships
- **Critical tasks**: No slack, delays impact completion

**Questions**:
- What's the longest path?
- Which tasks have no slack?
- What happens if this task delays?
- Can we parallel anything?

**Example**: Software release requires: code (10d) → testing (5d) → deployment (2d) = 17d critical path. Documentation (3d) can happen in parallel.

**Pitfalls**:
- Assumes fixed task durations
- Dependencies may be unclear
- Resource constraints not captured
- Can become outdated quickly

---

## Scope Creep

**Principle**: Uncontrolled expansion of project scope without adjustments to time, cost, or resources.

**When to Use**:
- Change management
- Requirement control
- Stakeholder management
- Risk identification

**Causes**:
- Vague requirements
- Poor change control
- Stakeholder pressure
- Gold-plating
- Incomplete planning

**Questions**:
- Is this in original scope?
- What's the impact on timeline/budget?
- Can we defer to next phase?
- Is this a nice-to-have or must-have?

**Example**: "While we're at it, let's add..." requests; feature creep in software; expanding renovations.

**Pitfalls**:
- Hard to say no
- Seems small at the time
- Compounds over time
- Kills projects

**Solutions**:
- Clear scope documentation
- Change control process
- Firm but flexible boundaries
- Backlog for future items

---

## Milestone Tracking

**Principle**: Break projects into measurable checkpoints to track progress and maintain momentum.

**When to Use**:
- Progress monitoring
- Stakeholder communication
- Team motivation
- Risk early detection

**Characteristics**:
- Specific and measurable
- Time-bound
- Significant achievements
- Clear completion criteria
- Regular intervals

**Questions**:
- Are we on track?
- What's blocking the next milestone?
- Do milestones align with goals?
- Are they meaningful or arbitrary?

**Example**: Sprint demos; phase gates; product launches; regulatory approvals; alpha/beta releases.

**Pitfalls**:
- Too many = overhead
- Too few = late surprises
- Vanity milestones
- Moving goalposts

---

## Resource Leveling

**Principle**: Optimize resource allocation to avoid overloading and maintain steady utilization.

**When to Use**:
- Capacity planning
- Preventing burnout
- Schedule optimization
- Multi-project management

**Techniques**:
- Delay non-critical tasks
- Split assignments
- Adjust task durations
- Add resources strategically

**Questions**:
- Who's overloaded?
- What can be deferred?
- Can tasks be redistributed?
- What's the impact on timeline?

**Example**: Developer working on 3 projects simultaneously. Level by: moving non-urgent work, bringing in help, or extending deadlines.

**Pitfalls**:
- May extend project duration
- Context switching costs
- Can be complex to optimize
- People aren't fungible

---

## Stakeholder Mapping

**Principle**: Identify and analyze stakeholders by influence and interest to guide engagement strategy.

**When to Use**:
- Project initiation
- Communication planning
- Change management
- Risk management

**Matrix**:
- **High Power, High Interest**: Manage closely
- **High Power, Low Interest**: Keep satisfied
- **Low Power, High Interest**: Keep informed
- **Low Power, Low Interest**: Monitor

**Questions**:
- Who cares about this?
- Who can block or enable?
- What do they need?
- How often to engage?

**Example**: CEO (high power/interest); end users (low power/high interest); adjacent teams (varies).

**Pitfalls**:
- Stakeholders change
- Hidden stakeholders
- Underestimating influence
- Over/under-communicating

---

## Work Breakdown Structure (WBS)

**Principle**: Decompose project into hierarchical, manageable components.

**When to Use**:
- Project planning
- Estimation
- Assignment clarity
- Progress tracking

**Structure**:
- Level 1: Project
- Level 2: Major deliverables
- Level 3: Work packages
- Level 4: Tasks

**Questions**:
- What are all the pieces?
- How do they relate?
- What's the right granularity?
- Who owns each piece?

**Example**: Website project → Design → Wireframes, Mockups, User testing. Development → Frontend, Backend, Integration.

**Pitfalls**:
- Too detailed = overhead
- Too high-level = ambiguity
- Forgetting dependencies
- Incomplete decomposition

---

## Earned Value Management (EVM)

**Principle**: Integrate scope, schedule, and cost to measure project performance.

**When to Use**:
- Performance measurement
- Forecasting
- Variance analysis
- Executive reporting

**Key Metrics**:
- **PV (Planned Value)**: Budgeted cost for work scheduled
- **EV (Earned Value)**: Budgeted cost for work completed
- **AC (Actual Cost)**: Actual cost of work completed
- **SPI** = EV/PV (schedule performance)
- **CPI** = EV/AC (cost performance)

**Questions**:
- Are we ahead or behind schedule?
- Over or under budget?
- What's the forecast at completion?

**Example**: Planned to complete 50% ($500K) by now. Actually completed 40% ($450K). Behind schedule but under budget.

**Pitfalls**:
- Complex to set up
- Requires disciplined tracking
- Can be gamed
- Overhead for small projects

---

## Buffer Management (Critical Chain)

**Principle**: Aggregate safety margins into project and feeding buffers rather than padding individual tasks.

**When to Use**:
- Uncertainty management
- Preventing Parkinson's Law
- Schedule compression
- Critical Chain Method

**Approach**:
- Remove task padding
- Add project buffer (end)
- Add feeding buffers (non-critical to critical)
- Monitor buffer consumption

**Questions**:
- Where's the real uncertainty?
- How much buffer do we need?
- Is buffer consumption accelerating?

**Example**: Instead of every task +20%, aggressive estimates + 30% buffer at end. 100d tasks → 80d + 20d buffer.

**Pitfalls**:
- Team may not trust
- Requires culture change
- Buffer sizing is art
- Can still run out

---

## Retrospective Meetings

**Principle**: Regular reflection on what worked, what didn't, and how to improve.

**When to Use**:
- End of sprint/phase/project
- After incidents
- Continuous improvement
- Team learning

**Format**:
- **What went well**: Celebrate successes
- **What didn't**: Identify problems
- **What to improve**: Action items
- **Appreciate**: Thank team members

**Questions**:
- What should we keep doing?
- What should we stop?
- What should we try?
- What did we learn?

**Example**: Sprint retro: "Stand-ups too long" → Action: Timeboxed to 15min. "Good: Pairing on complex bugs" → Continue.

**Pitfalls**:
- Becoming routine/boring
- No psychological safety
- No follow-through
- Blaming individuals
- Skipping when busy
