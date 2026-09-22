# Risk taxonomy

| Code | Category | What it covers |
|---|---|---|
| DATA | Data integrity | Validation, duplicates, encoding, time zones and DST, rounding, data migration, large or empty inputs |
| PERM | Permissions | Which roles can see or do what, privilege escalation, leakage between accounts |
| FLOW | Workflow and state | Job state transitions, undo and reversal, cancellations and reschedules, concurrent edits |
| INTG | Integrations | Third-party failures, retries, auth expiry, rate limits, sync direction, duplicate events |
| PRIV | Privacy and security | PII exposure, consent, data retention, audit trails, injection, sensitive content in files or messages |
| PLAT | Platform and environment | Offline mode, mobile vs. web differences, device and OS versions, network conditions |
| PERF | Performance and scale | Large accounts, bulk operations, file sizes, timeouts |
| A11Y | Accessibility | Screen readers, keyboard access, color contrast, alternatives to motor-heavy interactions |
| REGR | Regression | Impact on existing features, reports, and user habits |
| REL | Release and rollout | Feature flags, migration of existing data, rollback, customer communication, support readiness |

## Overlapping categories
Some risks fit more than one category (e.g., leakage between accounts is both
PERM and PRIV). Each answer-key risk has one `primary` code and optional
`alternates`. A catch filed under any listed code counts as a match.
Per-category reporting uses the primary code.
