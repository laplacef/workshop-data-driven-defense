# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| latest  | Yes       |

Only the latest release receives security patches.

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

To report a vulnerability, use [GitHub's private vulnerability reporting](https://github.com/laplacef/workshop-data-driven-defense/security/advisories/new). You can expect an initial response within 72 hours.

Please include:
- A description of the vulnerability
- Steps to reproduce the issue
- Potential impact assessment

## Scope

The following are considered security issues:
- Arbitrary code execution through model loading or deserialization of pickled artifacts
- Credential exposure through notebook output or committed configuration
- Dependency vulnerabilities in direct dependencies

## Out of Scope

The following are **not** security issues:
- Accuracy, bias, or performance of the trained models
- Integrity or licensing of the Edge-IIoTset dataset
- Availability of upstream dataset hosts
