# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in Strand SDK, please do **not** open a public issue. Instead, please email the maintainers privately to report the issue.

### Responsible Disclosure

We follow responsible disclosure practices:

1. **Report privately** — Send details to the maintainers via email
2. **Allow time for a fix** — We will work to address the issue promptly
3. **Coordinate disclosure** — We will work with you on timing for public disclosure
4. **Credit** — We will acknowledge your contribution if you wish

## Supported Versions

| Version | Status | Security Updates |
|---------|--------|------------------|
| 0.x.x   | Beta   | Until v1.0.0     |
| 1.x.x   | Current | Active support   |

## Known Security Considerations

- **Reproducibility**: Strand SDK captures experimental configurations in manifests. Ensure sensitive parameters (API keys, credentials) are never included in manifests.
- **Dependencies**: Regularly update dependencies for security patches. Run `pip install --upgrade -r requirements.txt`
- **Model Files**: When downloading pre-trained models (ESMFold, BioBERT, ProtBERT), verify integrity and use only from official sources.

## Security Best Practices

1. Keep Strand SDK updated to the latest version
2. Use virtual environments to isolate dependencies
3. Review manifests before sharing experiments publicly
4. Report security issues responsibly
5. Monitor dependency security advisories

## Acknowledgments

We appreciate the security research community and thank anyone who has reported vulnerabilities responsibly.

