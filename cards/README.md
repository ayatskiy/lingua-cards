# cards/

Global canonical card store with deterministic content-derived identity.

For:

`canonical_key = verb:sich erinnern`

compute SHA-256, then store:

`cards/by-key/<first-two-hash-chars>/CARD-<full-sha256>.json`

There is **no global index file**.

The deterministic path is the duplicate lookup. Card files contain learning content only.
