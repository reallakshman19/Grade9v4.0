# Schema versioning

- Records currently require `schema_version: "1.0.0"`.
- Additive optional fields may use a minor version after a tested reader upgrade.
- Breaking required-field, semantics, or status changes require a major version and migration.
- Reject unknown major versions; never silently reinterpret old records.
- Schemas validate shapes and required fields, not physical truth, reviewer identity or cognitive sufficiency.
- Each collection is a JSON array; each member validates against the correspondingly named schema file. `bundle.json` is one object.
