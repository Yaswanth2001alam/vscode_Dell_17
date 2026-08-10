# Azure DevOps idle pipeline email monitor

This checks the Azure DevOps REST API every 30 minutes and emails you when the
`SWAN` project changes from **active** to **idle**. Active means at least one
build is `inProgress`, `notStarted`, or `postponed`.

## 1. Create credentials

1. In Azure DevOps, create a token with the minimum **Build: Read** (`vso.build`)
   permission. Your company may require an approved PAT; if PAT creation is
   restricted, ask your administrator for an Entra/service identity instead.
2. For Gmail, enable two-step verification and create an **App Password**.
   Do not use your normal Gmail password.
3. Never paste either secret into the Python file or commit the `.env` file.

## 2. Install and configure

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item pipeline-monitor.env.example .env
notepad .env
```

Load the variables in PowerShell:

```powershell
Get-Content .env | ForEach-Object {
    if ($_ -match '^\s*([^#][^=]*)=(.*)$') {
        [Environment]::SetEnvironmentVariable($matches[1].Trim(), $matches[2].Trim(), 'Process')
    }
}
```

Test the API without sending an email:

```powershell
python azure_pipeline_idle_monitor.py --once --dry-run
```

Test one real check (it emails only if the project is idle):

```powershell
python azure_pipeline_idle_monitor.py --once
```

Run continuously every 30 minutes:

```powershell
python azure_pipeline_idle_monitor.py
```

Keep the process running in a Windows Task Scheduler task, server, container,
or Azure Function. A laptop-only process stops checking when the laptop sleeps.

## Alert behavior

- One email is sent when the project first becomes idle.
- Further idle checks do not send duplicates.
- After a pipeline becomes active, the next idle period can send a new alert.
- Set `SEND_RECOVERY_EMAIL=true` to also receive a recovery email.
- API/email errors are logged and are never treated as "no pipelines running."

## Recommended production design

For a company environment, run this as an Azure Function with a 30-minute timer
and use managed identity or a service principal plus Key Vault. That avoids a
long-lived personal token and Gmail password on a workstation. An alternative
is an Azure DevOps scheduled YAML pipeline, but that pipeline itself may count
as active while performing the check, so exclude its definition ID if using
that design.
