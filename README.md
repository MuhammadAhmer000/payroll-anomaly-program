# Payroll Anomaly Detection System
A machine learning-based system that detects anomalies in employee payroll data.
Flags irregular payment records and displays results through a web interface.
 
**Status:** In active development — ML pipeline complete, frontend integration in progress.
 
---
 
## Features
- Detects anomalous payroll records using machine learning (z-score based)
- Configurable detection parameters via YAML config files
- Web-based interface for uploading data and viewing flagged results
- REST API backend built with FastAPI
- User authentication and data storage via Supabase
- Fully containerized — runs anywhere with Docker
---
 
## Tech Stack
- **Language:** Python
- **Backend:** FastAPI
- **Frontend:** React (Vite)
- **ML:** scikit-learn, scipy
- **Data Processing:** pandas, numpy
- **Database/Auth:** PostgreSQL, Supabase
- **Containerization:** Docker, Docker Compose
---
 
## Project Structure
```
src/          # Core ML logic, API routes, and processing modules
frontend/     # React web interface
config/       # YAML configuration and thresholds
data/         # Sample datasets
```
 
---
 
## Running with Docker (Recommended)
Requires Docker Desktop installed.
 
1. Clone the repo
```bash
git clone https://github.com/MuhammadAhmer000/payroll-anomaly-program
cd payroll-anomaly-program
```
 
2. Add your `.env` file to the root directory with the required credentials (contact for access)
3. Run
```bash
docker compose up
```
 
Frontend: http://localhost:5173  
Backend API: http://localhost:8000/docs
 
---
 
## Running Locally (Development)
```bash
git clone https://github.com/MuhammadAhmer000/payroll-anomaly-program
cd payroll-anomaly-program
```
 
**Backend**
```bash
pip install -r requirements.txt
fastapi run src/main.py
```
 
**Frontend**
```bash
cd frontend
npm install
npm run dev
```
 
> Requires a `.env` file with Supabase and database credentials. Contact for demo access.
 
---
 
## Author
Muhammad Ahmer — [LinkedIn](https://www.linkedin.com/in/muhammad-ahmer-/) · [GitHub](https://github.com/MuhammadAhmer000)
