# Safe Content Administration

## Direction

Keep the existing Flask API, Vue frontend, and SQLite database. Add a separate Django admin application that reads and writes the existing `tour_dates` and `shoutouts` tables. This gives authenticated editing and moderation without moving data or changing the public API contract. Keep new shoutouts immediately visible; admin users can edit or delete them.

## Implementation steps

1. Add Django admin models mapped to the existing SQLite tables and register useful list, search, and filtering controls.
2. Configure admin credentials, allowed hosts, CSRF, sessions, and database location using environment variables.
3. Keep the existing Flask routes and frontend response formats unchanged; run Django as a separate admin service.
4. Make date seeding non-destructive and prevent reset commands from targeting a configured production database.
5. Document local/admin startup, production routing, SQLite backup and restore, and rollback. Coordinate Pi systemd and nginx changes in the external homelab repository.

## Verification

- Confirm admin authentication is required and tour-date changes persist to the existing tables.
- Confirm shoutouts remain immediately public and can be edited or deleted by an admin.
- Verify the Flask API still serves the same responses and behavior from the shared database.
- Back up and restore a copy of the database; verify both tables and record counts before production rollout.
- Validate Django configuration and run targeted backend tests. Smoke-test HTTPS admin access and rollback on the Raspberry Pi before switching production traffic.

## Scope constraints

- Keep SQLite; splitting databases or migrating the public API to Django is not part of this implementation.
- Do not add vendor/agent branding, references, or agent-specific instruction files.
