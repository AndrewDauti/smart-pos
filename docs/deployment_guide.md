# Deployment Guide

## Backend
1. `python -m venv .venv && source .venv/bin/activate`
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and set `MOCK_EINVOICE_URL` to your Postman Mock server URL.
4. `uvicorn app.main:app --host 0.0.0.0 --port 8000`

## Mobile
1. Install Flutter & SDKs.
2. Create project and replace `lib/` & `pubspec.yaml` with provided ones.
3. Ensure emulator/device can reach backend host; use `10.0.2.2` on Android emulator.

## Postman
1. Import `postman_collection.json`.
2. Set `{{base_url}}` to your backend URL.
