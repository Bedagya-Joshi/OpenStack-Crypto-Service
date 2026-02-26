# OpenStack-Crypto-Service

## Project Overview
This project implements a **Secure Data Processing Service** deployed on a private OpenStack cloud. It demonstrates the integration of **Symmetric Cryptography** (using the `cryptography` library) with modern **DevOps practices**.

## Key Features
* **Symmetric Encryption:** Uses Fernet (AES-128) to secure sensitive CSV datasets.
* **Automated Deployment:** Features a CI/CD pipeline using **GitHub Actions** to automatically deploy code changes to an OpenStack Virtual Machine.
* **Performance Benchmarking:** Includes built-in KPI logging to compare encryption throughput between Local environments and Cloud infrastructure.
* **Data Generation:** Custom script to generate unique 100MB+ datasets for stress testing.

## Technology Stack
* **Language:** Python 3.9+
* **Cloud Platform:** OpenStack (Nova Compute, Cinder Storage)
* **CI/CD:** GitHub Actions
* **Libraries:** `cryptography`, `pandas`

## How to Run
1.  **Generate Data:** `python generate_data.py`
2.  **Run Encryption:** `python secure_processor.py`
3.  **Check Logs:** View `app_troubleshooting.log` for performance metrics.
