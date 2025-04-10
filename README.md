# 🛡️ IoT Vulnerability Auditor

A Python-based tool that detects publicly exposed WattBox devices, tests for default credentials, and optionally checks for known CVEs using Shodan's CVEDB.

## 🚀 Features
- Searches Shodan for devices on port 80 with "wattbox" in banner
- Attempts login using Basic Auth (`wattbox:wattbox`)
- Detects hardware model
- (Optional) Uses CVEDB API to look for CVEs via CPE
- Exports results to CSV

## ⚙️ Requirements
- Python 3.10+
- requests
- pandas

## 🔐 Setup
Install dependencies:

```bash
pip install -r requirements.txt
```

Set your Shodan API key:

```bash
export SHODAN_API_KEY="your_api_key_here"
```

## 🧪 Run the script

```bash
python Wattbox_vulnerability_comentado.py
```

## 📦 Output
If vulnerabilities are found, they're saved to `wattbox_vulnerables.csv`.

## 🔐 Disclaimer
This tool is for educational and ethical security research purposes only. Do not use it without explicit permission.

## 👨‍💻 Author
[Sergio Mazo](https://github.com/SergioMazo)
