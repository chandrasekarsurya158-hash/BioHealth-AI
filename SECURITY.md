# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.0.x   | :white_check_mark: |
| < 2.0   | :x:                |

---

## Reporting a Vulnerability

The security and privacy of healthcare and patient information in **BioHealth AI** is of the highest priority. If you discover a security vulnerability, we appreciate your help in responsibly disclosing it to us.

### Please Do Not:
* Open a public GitHub Issue describing the security flaw.
* Disclose details publicly before a fix has been validated and released.

### How to Report:
1. Email your vulnerability report to: `security@biohealth.local` (or through GitHub's Private Security Advisory feature).
2. Please include:
   * A clear description of the vulnerability.
   * Step-by-step reproduction instructions or a minimal Proof of Concept (PoC).
   * Potential impact on user data or model inference integrity.
3. You will receive an initial response within 48 hours acknowledging receipt.
4. We will coordinate remediation and publish an acknowledgment once patched.

---

## Security Best Practices for Self-Hosters

* **Secret Key:** Always set a strong, unique `SECRET_KEY` in your `.env` file before exposing the server publicly:
  ```bash
  python -c "import secrets; print(secrets.token_hex(32))"
  ```
* **Database Isolation:** Restrict MySQL database user privileges to `SELECT`, `INSERT`, `UPDATE`, and `DELETE`. Do not use `root` with empty passwords in production deployments.
* **HTTPS / SSL:** Always serve BioHealth AI behind a reverse proxy (e.g., Nginx, Caddy, or Cloudflare) with active TLS/SSL certificates.

