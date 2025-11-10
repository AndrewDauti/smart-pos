# Smart POS Mobile (Flutter)

## Quickstart
1. Create a Flutter project (so you have Android/iOS scaffolding):
   ```bash
   flutter create smart_pos
   ```
2. Replace the generated `lib/` and `pubspec.yaml` with files from this folder.
3. Run the backend, then run the app:
   ```bash
   flutter run
   ```
- The app points to `http://10.0.2.2:8000` by default (Android emulator to host). Adjust in `services/api.dart` if needed.

## Features
- Product list, basic cart with quantity controls
- Checkout computes totals on backend
- Invoice submission to backend
- Offline queue (shared_preferences) with retry stub
- Simple receipt screen
