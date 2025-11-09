# AI in Misinformation Spread: Bots vs Humans

## Research Overview

This research project investigates the role of AI and automated bots in spreading misinformation on social media, comparing bot-driven propagation patterns with organic human sharing. We use the TruthSeeker dataset and related sources to analyze, detect, and understand misinformation dynamics.

## Research Questions

### RQ1: Spread Pattern Differences
**What are the differences in how misinformation spreads on social media when driven by bots compared to when driven by human users?**

Key aspects to investigate:
- Speed of spread (temporal dynamics)
- Audience reach and size
- Network structure of propagation
- Cascading patterns and virality metrics

### RQ2: Detection Techniques
**How can AI techniques be used to detect or distinguish misinformation that is being propagated by bots versus by humans?**

Focus areas:
- Account-level features (profile characteristics, posting patterns)
- Content-level features (linguistic patterns, sentiment, topics)
- Network-level features (follower graphs, interaction patterns)
- Machine learning model development and evaluation

### RQ3: Attribution and Quantification
**What proportion of misinformation dissemination can be attributed to automated bot activity relative to organic human activity?**

Analysis goals:
- Quantify bot vs. human contribution to misinformation spread
- Identify whether bots seed false news or amplify existing content
- Measure relative impact on information cascades

### RQ4: Intervention Strategies
**What interventions would be effective in reducing the spread of misinformation by bots without impeding legitimate human discourse?**

Intervention evaluation:
- Bot account removal strategies
- Algorithmic down-ranking approaches
- Impact on legitimate information flow
- Cost-benefit analysis of different interventions

## Project Structure

```
.
├── data/
│   ├── raw/              # Original, immutable data
│   ├── processed/        # Cleaned, transformed data
│   └── external/         # External datasets and references
├── notebooks/            # Jupyter notebooks for exploration and analysis
├── src/
│   ├── data_processing/  # Data loading, cleaning, integration scripts
│   ├── analysis/         # Analysis scripts
│   ├── models/           # ML model implementations
│   └── utils/            # Utility functions
├── results/
│   ├── figures/          # Generated plots and visualizations
│   ├── tables/           # Results tables and statistics
│   └── models/           # Trained model artifacts
├── docs/                 # Documentation and research notes
└── README.md
```

## Dataset

### TruthSeeker Dataset
The primary dataset includes:
- **FakeNewsNet**: Social media posts with veracity labels
- **CoAID**: COVID-19 related misinformation dataset
- **TwiBot-22**: Twitter bot detection dataset with bot/human labels
- Additional sources for network and propagation data

### Data Integration Tasks
1. Link social media posts to bot/human labels
2. Match posts from FakeNewsNet/CoAID with user identities from TwiBot-22
3. Construct propagation networks and cascades
4. Integrate temporal information for spread analysis

## Methodology

### Phase 1: Data Preparation
- [ ] Download and organize TruthSeeker dataset components
- [ ] Clean and validate data quality
- [ ] Integrate bot labels with misinformation posts
- [ ] Construct propagation networks
- [ ] Create analysis-ready datasets

### Phase 2: Exploratory Analysis
- [ ] Descriptive statistics of bot vs. human accounts
- [ ] Temporal analysis of misinformation spread
- [ ] Network structure analysis
- [ ] Preliminary visualizations

### Phase 3: Detection and Classification
- [ ] Feature engineering (account, content, network features)
- [ ] ML model development for bot vs. human detection
- [ ] Model evaluation and interpretation
- [ ] Feature importance analysis

### Phase 4: Impact Quantification
- [ ] Measure bot contribution to misinformation spread
- [ ] Analyze cascades initiated by bots vs. humans
- [ ] Quantify reach and influence metrics
- [ ] Statistical testing and validation

### Phase 5: Intervention Analysis
- [ ] Simulate intervention strategies
- [ ] Measure impact on misinformation spread
- [ ] Assess impact on legitimate discourse
- [ ] Develop recommendations

## Key Metrics

### Spread Metrics
- Cascade size and depth
- Spread velocity and acceleration
- Temporal decay patterns
- Network centrality measures
- Audience reach and engagement

### Detection Metrics
- Classification accuracy, precision, recall, F1-score
- ROC-AUC and PR-AUC
- Feature importance scores
- Model interpretability measures

### Impact Metrics
- Bot vs. human contribution ratio
- Seeds vs. amplification role
- Intervention effectiveness scores

## Dependencies

See `requirements.txt` for Python package dependencies.

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Download TruthSeeker dataset (see `docs/data_acquisition.md`)
4. Run initial data exploration: `notebooks/01_data_exploration.ipynb`

## Contributors

Research Team

## License

TBD
