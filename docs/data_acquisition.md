# Data Acquisition Guide

## TruthSeeker Dataset Components

### 1. FakeNewsNet
**Description**: A repository for fake news dataset containing news content, social context, and spatiotemporal information.

**Components**:
- News articles (real and fake)
- Social media posts sharing these articles
- User engagement data (likes, retweets, comments)
- Temporal information

**Sources**:
- PolitiFact fact-checking
- GossipCop entertainment fact-checking

**Download**:
```bash
# Clone FakeNewsNet repository
git clone https://github.com/KaiDMML/FakeNewsNet.git data/external/FakeNewsNet
```

**References**:
- Paper: "FakeNewsNet: A Data Repository with News Content, Social Context and Spatiotemporal Information for Studying Fake News on Social Media"
- Link: https://github.com/KaiDMML/FakeNewsNet

### 2. CoAID
**Description**: COVID-19 Healthcare Misinformation Dataset

**Components**:
- COVID-19 related news articles
- Social media posts
- Claims and fact-checks
- Multi-modal data (text, images)

**Download**:
```bash
# Clone CoAID repository
git clone https://github.com/cuilimeng/CoAID.git data/external/CoAID
```

**References**:
- Paper: "CoAID: COVID-19 Healthcare Misinformation Dataset"
- Link: https://github.com/cuilimeng/CoAID

### 3. TwiBot-22
**Description**: Twitter Bot Detection Benchmark with comprehensive bot/human labels

**Components**:
- User profiles (bot and human)
- Tweet content
- User network information
- Bot labels (binary classification)

**Download**:
```bash
# Download from official source
# Visit: https://twibot22.github.io/
# Or use direct download link
wget https://zenodo.org/record/XXX/files/Twibot-22.zip -O data/external/Twibot-22.zip
unzip data/external/Twibot-22.zip -d data/external/TwiBot-22/
```

**References**:
- Paper: "TwiBot-22: Towards Graph-Based Twitter Bot Detection"
- Link: https://github.com/LuoUndergradXJTU/TwiBot-22

### 4. Additional Datasets (if needed)

#### Botometer Scores
- Real-time bot detection scores
- API access required
- Link: https://botometer.osome.iu.edu/

#### Twitter API Data
- Historical tweets
- User information
- Network relationships
- Requires Twitter API access

## Data Organization

After downloading, organize data as follows:

```
data/
├── raw/
│   ├── fakenewsnet/
│   │   ├── politifact/
│   │   └── gossipcop/
│   ├── coaid/
│   │   ├── news/
│   │   └── social_media/
│   └── twibot22/
│       ├── users/
│       ├── tweets/
│       └── labels/
├── processed/
│   ├── integrated_posts.csv
│   ├── bot_labels.csv
│   ├── propagation_networks.gpickle
│   └── analysis_ready.parquet
└── external/
    └── (raw downloads)
```

## Data Integration Steps

### Step 1: Load Individual Datasets
```python
# Load FakeNewsNet
import pandas as pd
fakenews_data = pd.read_csv('data/raw/fakenewsnet/...')

# Load CoAID
coaid_data = pd.read_csv('data/raw/coaid/...')

# Load TwiBot-22
twibot_data = pd.read_csv('data/raw/twibot22/...')
```

### Step 2: Match Posts to User Labels
- Extract user IDs from social media posts
- Match with TwiBot-22 bot/human labels
- Handle missing labels (classify or exclude)

### Step 3: Create Unified Dataset
- Combine FakeNewsNet and CoAID posts
- Add bot/human labels
- Include temporal information
- Add network/propagation data

### Step 4: Quality Control
- Check for missing values
- Validate label consistency
- Remove duplicates
- Verify temporal ordering

## Data Access Considerations

### Privacy and Ethics
- Ensure compliance with platform terms of service
- Respect user privacy
- Follow research ethics guidelines
- Anonymize user information when possible

### Data Availability
- Some datasets may require registration
- Twitter data subject to API restrictions
- Check license requirements for each dataset

## Next Steps

1. Download datasets listed above
2. Run data validation scripts (`src/data_processing/validate_data.py`)
3. Execute integration pipeline (`src/data_processing/integrate_data.py`)
4. Generate data quality report
5. Proceed to exploratory analysis
