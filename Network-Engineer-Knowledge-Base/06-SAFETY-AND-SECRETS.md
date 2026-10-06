# Safety and Secrets

## Sensitive material found by category

The repository includes file types that commonly expose sensitive information:

- `.env` files and testbeds with credentials
- YAML inventories with usernames or passwords
- router configuration backups
- HAR files with headers, cookies, tokens, and URLs
- PCAP files with addresses, names, and traffic metadata
- JSON/notebook output containing command results
- local databases and generated logs

The generated catalog marks likely sensitive files and leaves them in their
original locations.

## Rules

1. Never commit active credentials.
2. Use `.env.example` only for variable names and placeholders.
3. Prefer environment variables or an approved secret manager.
4. Replace real IPs, hostnames, serials, usernames, and secrets before sharing.
5. Treat device backups, HAR, and PCAP as confidential.
6. Rotate a credential if it was committed or shared, even after deleting it.
7. Add generated outputs, caches, and active `.env` files to `.gitignore`.

## Safe credential pattern

```python
import os

username = os.environ["NET_USER"]
password = os.environ["NET_PASS"]
```

Fail clearly when required variables are missing. Do not silently substitute a
default password.

## Before publishing a project

- Search the full Git history, not only the working tree.
- Remove or sanitize packet captures and device output.
- Replace inventories with documentation-safe examples.
- Verify that notebooks have no sensitive cell output.
- Confirm licenses for copied external material.
- Run a secret scanner and review every result.
