# sanelabs.org

The Sane Labs site. Two pages, no build step.

- `/` — the lab: the model line from Sane-47M through Synth-2, and Sane Studio.
- `/synth-2/` — **Synth-2**, a 1.23B-parameter language model (≈330M active per token)
  trained from scratch. What it is for, and the real state of the pretraining run.
- `/notes/` — working notes: what was measured this week and what it changed.

The models themselves live on the Hub, and the training code in a separate repository.
This one is only the site.

## What is on the Synth-2 page

- a hand-written mock-up of the output format (per-token uncertainty `u` drawn on an answer);
- the target configuration, taken from the model's `ARCHITECTURE.md`;
- **the run log** — held-out loss against training step, read live, not hard-coded;
- acceptance criteria that have not been measured yet, stated as targets;
- a support block and a contact address.

Nothing on the page claims a measurement that has not been taken. The demo answer is
labelled as a mock-up, because the model is still in pretraining and is not served anywhere.

## Where the numbers come from

`synth-2/index.html` resolves the run log from three sources, in order, and uses the first
that answers:

1. **Supabase** — tables `run_log` and `run_meta`, read through the REST API with the
   project's *publishable* key. Row-level security allows `SELECT` only; a write with that
   key is refused with `401`. This is why the key is safe to keep in a public file.
2. **`run-log.json`** — the same data as a file at the site root. Used when Supabase is
   unreachable, and it keeps the site working with no external dependency at all.
3. the page's own artifact store — only relevant inside a Claude preview, where `fetch`
   is blocked by the sandbox.

Whichever source answers is named in the panel header, so it is always visible which one
you are looking at.

## Notes

`notes/index.html` is generated from the lab page's stylesheet so the two cannot drift
apart, but it is committed as a finished file — there is still no build step. To add an
entry, copy the last `<article class="lognote">` block and write the new note above it;
the numbering runs downwards, newest first. A note is worth adding when a measurement
changed what happened next, including when it killed an explanation.

Keep to the rule the rest of the site follows: no figure that was not measured.

## The view counter

`beacon.js` writes one row per page view into the `hit` table of the same Supabase
project. There is no cookie, no `localStorage`, no visitor identifier, no IP and no user
agent — only the path, the referring host, a `?src=` campaign tag, the window width and
whether the reader arrived from outside the site. Do Not Track and Global Privacy Control
are honoured, and every failure is swallowed so the counter can never break a page.

Row-level security lets the publishable key `INSERT` and nothing else; the table has no
`SELECT` policy, so the log cannot be read back from a browser. Read it in the SQL editor:

```sql
select * from public.hit_daily where day > current_date - 14;
```

Tag a link when posting it somewhere, and the source shows up by name rather than as a
referrer that may or may not survive the trip:

```
https://sanelabs.org/synth-2/?src=hn
```

Because anyone holding the publishable key can insert, the table is a counter and not an
audit log — treat a sudden flat spike as noise rather than as readers.

## Sharing cards

`og.png` and `synth-2/og.png` are 1200×630 and are referenced absolutely, which is what
the crawlers require. They are drawn by a script kept out of this repository; if the
figures on them go stale, redraw rather than edit, and keep the file names — a changed
`og:image` URL is re-fetched, a changed image behind the same URL often is not.

## Contact

ssanelabs@gmail.com — corrections to the numbers are especially welcome; every measurement
on the page is reproducible.
