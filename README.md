# Secure Data Processing & Analytics Pipeline
**Master’s Degree in Data Science | Coursework Project**

## Abstract
This project implements a secure, PII-compliant data processing and analytics pipeline designed for restricted (air-gapped) environments. By integrating automated CI/CD methodologies with symmetric encryption standards, the system ensures Data-at-Rest security while providing rigorous system observability. The research focuses on the performance trade-offs between secure, isolated worker nodes and conventional host environments.



## System Architecture
The implementation utilizes a three-tier decoupled architecture to minimize the attack surface and ensure operational resilience:

1.  **Tier 1: Orchestration Layer (Local Host/Windows):** Manages code versioning, CI/CD pipeline triggers, and performance baseline logging.
2.  **Tier 2: Warehouse/Bastion Layer (Linux VirtualBox):** Acts as a dependency proxy, orchestrating the secure transfer of signed packages (wheels) to the production node, preventing the need for an external internet connection on the execution VM.
3.  **Tier 3: Execution Layer (OpenStack Worker VM):** A hardened, isolated node that performs in-memory processing of sensitive PII, ensuring raw, unencrypted data is never persisted.



## Key Features & Research Contributions
* **Automated Dependency Management:** Implements an offline "Warehouse" approach for dependency installation, simulating high-security enterprise network requirements.
* **Privacy-Preserving Analytics:** Utilizes `cryptography.fernet` (AES-128) to secure PII at the record level.
* **System Observability:** Built-in logging frameworks capture high-precision KPIs (processing duration, throughput, and memory consumption).
* **Configurable Benchmarking:** Provides a comparative framework to evaluate performance deltas between standard and hardened cloud environments.

## Technical Specifications
* **Core Logic:** Python 3.10+
* **Data Processing:** `pandas`
* **Encryption Standard:** `Fernet` (Symmetric Encryption)
* **Environment Management:** `.env` configuration-driven execution

### Dependency Matrix
| Component | Version | Purpose |
| :--- | :--- | :--- |
| `pandas` | >=2.2.0 | Dataframe manipulation |
| `cryptography` | >=42.0.0 | PII Encryption/Decryption |
| `python-dotenv` | >=1.0.0 | Environment configuration |

## Experimental Methodology
To evaluate the impact of infrastructure hardening on data processing performance, the following comparative framework is employed:

1.  **Baseline Generation:** Executes processing on the Local Host environment to establish throughput standards.
2.  **Hardened Execution:** Executes processing within the OpenStack-based, isolated environment.
3.  **Performance Analysis:** System logs (`.log`) are generated in both environments, providing empirical evidence regarding latency overhead introduced by virtualization and network isolation.

## Usage Guide
1. **Configuration:** Create a `.env` file to specify the target dataset (`DATA_FILE=large_dataset.csv`).
2. **Data Preparation:** Generate synthetic datasets using `generate_small_data.py` or `generate_large_data.py`.
3. **Execution:** Initiate the processing job:
   ```bash
   python secure_processor.py