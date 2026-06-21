# Data Science Models

Mental models for data analysis, machine learning, and statistical modeling.

## Curse of Dimensionality

**Principle**: As dimensions increase, data becomes sparse and distance metrics lose meaning.

**When to Use**:
- Feature selection
- Model design
- Understanding ML limitations
- Data requirements estimation

**Problems**:
- Exponential data requirements
- Distance concentration
- Overfitting risk
- Computational complexity

**Questions**:
- How many features do I really need?
- Do I have enough data for these dimensions?
- Can I reduce dimensionality?

**Example**: With 10 binary features, need data for 2^10 = 1024 combinations. 100 features = 2^100 combinations (impossible).

**Pitfalls**:
- Adding features seems helpful but can hurt
- Intuition from 2D/3D doesn't apply
- More data may not solve the problem

---

## Bias-Variance Tradeoff

**Principle**: Models face tension between underfitting (high bias) and overfitting (high variance).

**When to Use**:
- Model selection
- Hyperparameter tuning
- Understanding errors
- Balancing complexity

**Concepts**:
- **Bias**: Error from wrong assumptions (underfitting)
- **Variance**: Error from sensitivity to training data (overfitting)
- **Sweet spot**: Minimize total error

**Questions**:
- Is my model too simple or too complex?
- Am I underfitting or overfitting?
- What's the right complexity level?

**Example**: Linear model (high bias, low variance); Deep neural net (low bias, high variance). Need balance.

**Pitfalls**:
- Can't eliminate both
- Tradeoff point depends on data
- Regularization helps but doesn't eliminate

---

## Feature Engineering

**Principle**: Creating and selecting informative variables is often more important than choice of algorithm.

**When to Use**:
- Improving model performance
- Domain knowledge application
- Data transformation
- Creating predictive signals

**Techniques**:
- Domain transformations
- Interaction features
- Aggregations
- Encoding categorical variables
- Temporal features
- Feature crosses

**Questions**:
- What domain knowledge can inform features?
- What interactions matter?
- Are there hidden patterns to extract?

**Example**: From date, create: day_of_week, is_weekend, is_holiday. From transaction: frequency, recency, monetary value (RFM).

**Pitfalls**:
- Can create too many features (curse of dimensionality)
- Overfitting to training data
- Leakage from target variable

---

## Cross-Validation

**Principle**: Test model on held-out data to estimate generalization performance.

**When to Use**:
- Model evaluation
- Hyperparameter tuning
- Preventing overfitting
- Comparing models

**Types**:
- **K-fold**: Split data into K parts, train on K-1, test on 1
- **Stratified**: Preserve class distribution
- **Time-series**: Respect temporal order
- **Leave-one-out**: Extreme case of K-fold

**Questions**:
- How well will this generalize?
- Am I overfitting?
- Which model is truly better?

**Example**: 5-fold CV gives better estimate than single train/test split. Prevents lucky/unlucky splits.

**Pitfalls**:
- Computationally expensive
- Still uses same dataset
- Can leak information if done wrong

---

## Ensemble Methods

**Principle**: Combine multiple models to improve predictions beyond any single model.

**When to Use**:
- Boosting performance
- Reducing variance
- Robust predictions
- Kaggle competitions

**Types**:
- **Bagging**: Train on bootstrap samples (Random Forest)
- **Boosting**: Sequential training on errors (XGBoost)
- **Stacking**: Meta-model on base models
- **Voting**: Combine predictions

**Questions**:
- Can diverse models complement each other?
- What's the right combination strategy?
- Am I overfitting the ensemble?

**Example**: Random Forest combines many decision trees; Netflix Prize won by ensemble; bagging reduces variance.

**Pitfalls**:
- Increased complexity
- Harder to interpret
- Diminishing returns
- Computational cost

---

## Gradient Descent

**Principle**: Iteratively move in direction of steepest descent to find optimal parameters.

**When to Use**:
- Training neural networks
- Optimizing loss functions
- Parameter estimation
- Continuous optimization

**Variants**:
- **Batch**: Full dataset per update
- **Stochastic (SGD)**: Single sample per update
- **Mini-batch**: Subset per update
- **Adaptive**: Adam, RMSprop

**Questions**:
- What learning rate?
- Converging or oscillating?
- Stuck in local minimum?

**Example**: Neural network training; logistic regression; any differentiable optimization problem.

**Pitfalls**:
- Learning rate critical
- Local minima
- Vanishing/exploding gradients
- Requires differentiable functions

---

## Regularization

**Principle**: Add penalty for complexity to prevent overfitting.

**When to Use**:
- Preventing overfitting
- Feature selection
- Improving generalization
- Handling multicollinearity

**Types**:
- **L1 (Lasso)**: Sparse solutions, feature selection
- **L2 (Ridge)**: Shrinks coefficients smoothly
- **Elastic Net**: Combines L1 and L2
- **Dropout**: Random neuron deactivation

**Questions**:
- How much to penalize complexity?
- Which regularization type?
- Am I underfitting due to too much regularization?

**Example**: Ridge regression shrinks coefficients; Lasso can zero out features; dropout in neural networks.

**Pitfalls**:
- Need to tune regularization strength
- May hurt if model too simple
- Different types have different effects

---

## Dimensionality Reduction

**Principle**: Reduce number of variables while preserving important information.

**When to Use**:
- Visualization
- Noise reduction
- Computational efficiency
- Addressing curse of dimensionality

**Techniques**:
- **PCA**: Linear combinations capturing variance
- **t-SNE**: Nonlinear, good for visualization
- **Autoencoders**: Neural network compression
- **Feature selection**: Remove redundant features

**Questions**:
- How much information can I afford to lose?
- Linear or nonlinear reduction?
- What's the intrinsic dimensionality?

**Example**: Compress 100 features to 10 principal components; visualize high-D data in 2D with t-SNE.

**Pitfalls**:
- Loss of information
- Interpretability reduced
- May remove important signals
- Computational cost

---

## Anomaly Detection

**Principle**: Identify unusual patterns that don't conform to expected behavior.

**When to Use**:
- Fraud detection
- Quality control
- System monitoring
- Rare event identification

**Approaches**:
- **Statistical**: Beyond N standard deviations
- **Isolation Forest**: Isolate outliers
- **One-class SVM**: Learn normal boundary
- **Autoencoders**: Reconstruction error

**Questions**:
- What's normal vs abnormal?
- How rare are anomalies?
- What's cost of false positives/negatives?

**Example**: Credit card fraud; manufacturing defects; network intrusion; sensor failures.

**Pitfalls**:
- Defining "normal" is hard
- Rare events = limited training data
- Anomalies evolve over time
- High false positive rates

---

## A/B Testing

**Principle**: Randomly assign users to variants and measure differences to establish causation.

**When to Use**:
- Feature validation
- Optimization
- Decision-making
- Causal inference

**Requirements**:
- Random assignment
- Sufficient sample size
- Clear metrics
- Statistical significance

**Questions**:
- What's the minimum detectable effect?
- How long to run?
- Is difference statistically significant?
- Are results practically significant?

**Example**: Test new UI design; pricing experiments; email subject lines; algorithm changes.

**Pitfalls**:
- Multiple testing problem
- Network effects
- Novelty effects
- Ethical concerns
- Sample ratio mismatch
