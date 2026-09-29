# dedupe/

Technical cross-deck duplicate registry.

There is no single global index.

For each `canonical_key`:
1. compute SHA-256;
2. use first two hex characters as shard filename;
3. look up key in `dedupe/<shard>.json`.

Example:

`noun:entscheidung -> SHA-256 starts with 31 -> dedupe/31.json`

Each shard maps canonical key to the deck path where it was first introduced.

Only non-empty shards need to exist.
