# PII Detector – Shivam Raj

## Overview
This project implements a **PII (Personally Identifiable Information) Detector** in Python.  
It processes CSV files containing JSON data, detects sensitive fields (e.g., phone numbers, Aadhaar, email, UPI, passport), and redacts them to protect user privacy.  

The project is divided into two parts:  
1. **Detector Code** → Python script (`detector_shivam_raj.py`) for identifying and masking PII.  
2. **Deployment Strategy** → Markdown document (`deployment_strategy.md`) describing how to deploy the tool locally, on servers, or in the cloud.  

---

## Features
- Detects common PII fields:
  - Phone numbers  
  - Aadhaar numbers  
  - Email addresses  
  - UPI IDs  
  - Passport numbers  
- Redacts detected values with `REDACTED_<PII_TYPE>`.  
- Works directly on JSON stored inside CSV columns.  
- Lightweight (uses only Python standard library).  


