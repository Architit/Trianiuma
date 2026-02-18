# Gateway Access Contract

## Scope
This contract defines mandatory gateway interfaces for:
- GitHub (source control sync)
- OneDrive (external file exchange)
- Google Workspace (external docs/data exchange)

## Required Environment Variables
- `GATEWAY_GITHUB_REMOTE` (default: `origin`)
- `GATEWAY_ONEDRIVE_ROOT` (example: `/mnt/c/Users/<user>/OneDrive`)
- `GATEWAY_GWORKSPACE_ROOT` (example: `/mnt/c/Users/<user>/GoogleDrive` or mounted workspace path)
- `GATEWAY_EXPORT_DIR` (default: `<repo>/.gateway/export`)
- `GATEWAY_IMPORT_DIR` (default: `<repo>/.gateway/import`)

## Mandatory Operations
1. Verify GitHub gateway reachability by validating configured git remote.
2. Verify OneDrive gateway by checking configured directory path.
3. Verify Google Workspace gateway by checking configured directory path.
4. Export repository package to gateway export directory.
5. Import package from gateway import directory into a staged location.

## Safety Rules
- No destructive overwrite during import.
- Imports must go to `./.gateway/import_staging` first.
- Export/import operations must emit explicit logs and non-zero exits on failure.

## Implementation
- Script: `scripts/gateway_io.sh`
- Verification mode: `scripts/gateway_io.sh verify`
- Export mode: `scripts/gateway_io.sh export`
- Import mode: `scripts/gateway_io.sh import <archive>`
