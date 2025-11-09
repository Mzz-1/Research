# Getting Started with TruthSeeker Research

## Quick Start Guide

This guide will help you get started with the TruthSeeker research project on AI-driven misinformation spread by bots vs humans.

## Prerequisites

- Python 3.8 or higher
- Git
- 10+ GB disk space for datasets
- (Optional) Jupyter Notebook environment

## Setup Instructions

### 1. Clone the Repository

If you haven't already:
```bash
git clone <repository-url>
cd Research
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download Datasets

Follow the instructions in `docs/data_acquisition.md` to download the required datasets:

```bash
# Create data directories if not exist
mkdir -p data/external

# Download FakeNewsNet
cd data/external
git clone https://github.com/KaiDMML/FakeNewsNet.git

# Download CoAID
git clone https://github.com/cuilimeng/CoAID.git

# Download TwiBot-22
# Visit https://twibot22.github.io/ for download instructions

cd ../..
```

### 5. Verify Setup

```bash
# Run a quick verification
python -c "import pandas as pd; import networkx as nx; import sklearn; print('Setup successful!')"
```

## Project Workflow

### Phase 1: Data Preparation

1. **Load datasets:**
   ```python
   from src.data_processing.load_data import DataLoader

   loader = DataLoader('data')
   datasets = loader.load_all()
   ```

2. **Integrate datasets:**
   ```python
   from src.data_processing.integrate_data import DataIntegrator

   integrator = DataIntegrator(datasets)
   unified_df = integrator.create_unified_dataset()
   integrator.save_integrated_data('data/processed/integrated_dataset.parquet')
   ```

3. **Explore data:**
   - Open `notebooks/01_data_exploration.ipynb`
   - Run through the cells to understand the data structure

### Phase 2: Research Question Analysis

#### RQ1: Spread Pattern Analysis
- Open `notebooks/02_rq1_spread_patterns.ipynb`
- Analyzes differences in spread speed, reach, and patterns

#### RQ2: Bot Detection (Coming Soon)
- Feature engineering
- ML model development
- Model evaluation

#### RQ3: Attribution Analysis (Coming Soon)
- Quantify bot vs human contribution
- Analyze seeding vs amplification roles

#### RQ4: Intervention Strategies (Coming Soon)
- Design intervention scenarios
- Simulate and evaluate impact

## Directory Structure

```
Research/
├── data/
│   ├── raw/              # Downloaded raw data
│   ├── processed/        # Cleaned, integrated data
│   └── external/         # External datasets (FakeNewsNet, CoAID, TwiBot-22)
├── notebooks/            # Jupyter notebooks
│   ├── 01_data_exploration.ipynb
│   └── 02_rq1_spread_patterns.ipynb
├── src/
│   ├── data_processing/  # Data loading and integration
│   ├── analysis/         # RQ-specific analysis scripts
│   ├── models/           # ML models
│   └── utils/            # Utility functions
├── results/
│   ├── figures/          # Generated visualizations
│   ├── tables/           # Results tables
│   └── models/           # Trained models
└── docs/                 # Documentation
```

## Common Tasks

### Load Integrated Dataset

```python
import pandas as pd

df = pd.read_parquet('data/processed/integrated_dataset.parquet')
```

### Run RQ1 Analysis

```python
from src.analysis.rq1_spread_patterns import RQ1Analyzer

analyzer = RQ1Analyzer(df)
results = analyzer.run_full_analysis()
```

### Generate Visualizations

```python
from src.utils.visualization import *

# Plot spread comparison
plot_spread_comparison(bot_data, human_data)

# Plot cascade size distribution
plot_cascade_size_distribution(bot_sizes, human_sizes)
```

### Calculate Metrics

```python
from src.utils.metrics import *

# Calculate spread velocity
velocity = calculate_spread_velocity(cascade_df)

# Calculate cascade metrics
metrics = calculate_cascade_metrics(cascade_df)
```

## Troubleshooting

### Issue: Dataset not found

**Solution:** Ensure you've downloaded all datasets to `data/external/` as per `docs/data_acquisition.md`

### Issue: Import errors

**Solution:** Make sure you've activated the virtual environment and installed all requirements:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: Memory errors with large datasets

**Solution:**
- Process data in chunks
- Use parquet format instead of CSV
- Consider using a machine with more RAM

### Issue: Missing timestamps or user IDs

**Solution:** Check the data integration script in `src/data_processing/integrate_data.py` and ensure proper column mapping

## Next Steps

1. **Complete data acquisition** - Download all required datasets
2. **Run data integration** - Create the unified analysis-ready dataset
3. **Exploratory analysis** - Use notebook 01 to understand the data
4. **RQ analysis** - Work through each research question systematically
5. **Document findings** - Update results and create visualizations

## Getting Help

- **Documentation:** See `docs/` directory for detailed guides
- **Code examples:** Check notebooks for working examples
- **Research plan:** See `docs/research_plan.md` for methodology details

## Contributing

When adding new analysis:
1. Create a new notebook in `notebooks/`
2. Add reusable functions to appropriate `src/` modules
3. Save visualizations to `results/figures/`
4. Document your approach in `docs/`

## License

[TBD]
