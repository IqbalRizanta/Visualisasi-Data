# Security Policy

## Reporting Vulnerabilities

If you discover a security vulnerability, please open a private issue or contact the maintainers directly.

## Security Audit Summary

### Findings (scanned 2024)

| # | Category | Severity | Status |
|---|----------|----------|--------|
| 1 | ReDoS via unvalidated search input | **Critical** | Fixed |
| 2 | Missing CORS/XSRF server configuration | **High** | Fixed |
| 3 | No authentication layer | Medium | Documented |
| 4 | `unsafe_allow_html=True` usage | Low | Documented |
| 5 | Hardcoded API keys / secrets | None | Clean |
| 6 | SQL injection | N/A | No database used |
| 7 | Exposed debug endpoints | Low | Fixed (toolbar set to minimal) |

### Details

#### 1. ReDoS — Regular Expression Denial of Service (FIXED)

The search input in the Beranda page was passed directly to `pandas.Series.str.contains()` which interprets strings as regex by default. A crafted regex pattern (e.g., `(a+)+$`) could cause catastrophic backtracking and hang the server.

**Fix:** Added `regex=False` and input length cap (200 chars).

#### 2. Missing Server Security Configuration (FIXED)

No `.streamlit/config.toml` existed. Default Streamlit settings may leave CORS open and XSRF protection disabled depending on version.

**Fix:** Added `.streamlit/config.toml` with:
- `enableXsrfProtection = true`
- `enableCORS = false`
- `fileWatcherType = "none"`
- `toolbarMode = "minimal"`

#### 3. No Authentication (DOCUMENTED)

The app has no authentication. Anyone with the URL can access the dashboard. For production deployments, consider:
- Streamlit's built-in authentication (`[server] enableAuth = true`)
- A reverse proxy with authentication (nginx + OAuth2 Proxy, Cloudflare Access, etc.)
- Streamlit Community Cloud's built-in viewer authentication

#### 4. `unsafe_allow_html=True` (DOCUMENTED)

Used 15+ times for custom styling. Currently safe because all rendered data originates from a static CSV controlled by the developers. However, if the data source is ever changed to accept user-uploaded CSVs or external APIs, this becomes an XSS vector.

**Recommendation:** If accepting user-uploaded data in the future, sanitize all values before rendering in HTML templates (e.g., use `html.escape()`).

## Dependency Security

Run periodic audits:

```bash
pip install pip-audit
pip-audit -r requirements.txt
```
