# ProprioSuite

## Overview

**ProprioSuite** is an open-source analysis pipeline designed for two proprioceptive testing paradigms: the pointing task and the weight discrimination task. The pointing task measures proprioception, while the weight discrimination task measures whether we can discriminate between different weights. This project aims to provide a standardized pipeline for the intricate data analysis following these tests, especially in scenarios where others may conduct the same tests and require analysis.

For instructions on how the tasks are performed, see their documentation:

[Pointing Task]()

[Weight Discrimination Task]()

### Features

- Modular statistical analysis for raw data from the tests.
- Publicly available database for subjects without a known neurological condition.
- Comparison baseline for others to analyze their data and compare subjects to the normal range.
- Performance report generation.
- Modules: `PointingTask` and `WeightDiscrimination`.

### Application in Industry

This project is primarily targeted at healthcare and somatosensory research.

## Technical Details

- **Programming Language**: R
- **Dependencies**: List of packages (to be updated later)
- **Architecture**: The package consists of two modules - `PointingTask` and `WeightDiscrimination`. Each module contains analyses, figures, comparison tools, and a performance report generator specific to its task.

## Getting Started

### Prerequisites

- R
- Ensure you have the devtools package installed. If not, you can install it using:

```R
install.packages("devtools")
```

### Installation

You can install the package with `devtools`:

```R
library(devtools)
install_github("yurisugano/ProprioSuite")
library(ProprioSuite)
```

### Usage

Install the package and refer to the modules available in the documentation.

## Project Status

The codebase is complete, but the project is in the process of being organized into a package for publication. All analyses can currently be performed using the scripts locally.

### Milestones

- Raw data analysis
- Feature extraction
- Comparison to normal range
- Performance reports

### Collaboration

Open to collaborations. If interested in using the package for tests and analysis, please reach out for a smooth integration and direct bug resolution.

## Additional Information

- Publicly available, unidentifable data on 60 subjects without a known neurological condition.
- Raw data details:
  - PointingTask: Finger position across time database with time intervals (typically 1/30 s for 30fps recordings), x and y position.
  - WeightDiscrimination: See the [sample data]()

For more information, questions, or collaborations, visit [my home page](#).

