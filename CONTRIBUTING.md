# Contributing to BioHealth AI

Thank you for your interest in contributing to **BioHealth AI**! We welcome contributions from developers, agronomists, physicians, data scientists, and healthcare AI researchers around the world.

---

## Code of Conduct

All contributors and participants are expected to adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please treat all community members with empathy, respect, and professionalism.

---

## Getting Started

### 1. Fork and Clone the Repository
```bash
git clone https://github.com/your-username/BioHealth-AI.git
cd BioHealth-AI
```

### 2. Set Up a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Configuration
1. Start MySQL (e.g. via XAMPP or Docker).
2. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
3. Initialize the database schema and seed default data:
   ```bash
   python init_db.py
   ```

### 5. Run the Automated Test Suite
Ensure that all integration and unit tests pass before making any changes:
```bash
python test_system.py
```

### 6. Start the Local Server
```bash
python run.py
```
Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

---

## Development Guidelines

1. **Branch Naming:** Use clear branch prefixes:
   * `feat/feature-name` for new capabilities
   * `fix/bug-description` for bug fixes
   * `docs/documentation-update` for documentation improvements
   * `model/retrained-weights` for ML model adjustments
2. **Coding Standards:** Follow PEP 8 guidelines for Python code. Maintain clean Jinja2 indentation and Bootstrap 5 responsive styling.
3. **Security Standards:**
   * Never commit `.env` or sensitive API keys.
   * Do not hardcode passwords or cryptographic secrets.
   * Use parameterized SQL queries (`cursor.execute(sql, (params,))`) to prevent SQL injection.
   * Protect all administrative routes with the `@admin_required` decorator.
4. **Testing Requirement:** Add corresponding unit tests in `test_system.py` for any new route, module, or API endpoint.

---

## Submitting a Pull Request (PR)

1. Commit your changes with concise, descriptive commit messages:
   ```bash
   git commit -m "feat(api): add batch prediction endpoint for crop leaves"
   ```
2. Push your branch to your forked repository:
   ```bash
   git push origin feat/your-feature
   ```
3. Open a Pull Request against the `main` branch.
4. Provide a clear summary of your changes, reference any related issues, and confirm that `python test_system.py` passes cleanly.

