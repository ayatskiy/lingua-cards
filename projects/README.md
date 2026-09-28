# projects/

Project folders group card sets without adding provenance to canonical cards.

```text
projects/
  <project-slug>/
    sets/
      <set-name>.json
```

Examples:

```text
projects/deutsch-uebungen/sets/2026-09-29.json
projects/travel-german/sets/lesson-12.json
projects/general/sets/2026-09-29.json
```

A set manifest contains only `schema_version` and ordered canonical card IDs.
