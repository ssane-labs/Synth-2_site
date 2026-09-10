# sanelabs.org

The Sane Labs site. Two pages, no build step.

- `/` — the lab: the model line from Sane-47M through Synth-2, and Sane Studio.
- `/synth-2/` — **Synth-2**, a 1.23B-parameter language model (≈330M active per token)
  trained from scratch. What it is for, and the real state of the pretraining run.

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

## Updating the run log

### The fast way — Supabase (no deploy)

Open the project's SQL editor and insert the new measurement. The site picks it up on the
next page load; nothing needs to be committed or rebuilt.

```sql
insert into public.run_log (step, loss, recorded_on, note)
values (86000, 2.0290, '2026-09-12', 'first session after the router_bias fix')
on conflict (step) do update
  set loss = excluded.loss,
      recorded_on = excluded.recorded_on,
      note = excluded.note;
```

Optional columns: `trend_per_1k` and `trend_note` for a measured slope, `lr_event` for a
labelled vertical marker on the chart (for example `'LR / 3'`).

Headline figures that are not per-step live in `run_meta`:

```sql
update public.run_meta
   set expert_share = 24.1,   -- share of FFN output from routed experts
       mfu = 6.4,
       stage = 'B',
       updated_at = now()
 where id = 'run';
```

### The offline way — the JSON file

Keeps the fallback in step with the database, and is worth doing every few sessions:

```bash
python append_run_point.py --step 86000 --loss 2.0290 --note "first session after the router_bias fix"
git add run-log.json && git commit -m "run log: step 86,000" && git push
```

The script sorts the points, replaces a measurement at the same step instead of duplicating
it, and prints what it did.

## Running it locally

No build step, no dependencies — it is one HTML file.

```bash
python -m http.server 8000
```

Then open `http://127.0.0.1:8000`. Opening a page straight from the filesystem also works,
except that the `run-log.json` fallback cannot be fetched from a `file://` page.

## Deployment

GitHub Pages, from the default branch, root folder, served at **sanelabs.org**
(the `CNAME` file claims the domain).

## Layout

```
index.html             the lab page
synth-2/index.html     the Synth-2 page
run-log.json           the fallback copy of the training log
append_run_point.py    appends one measurement to run-log.json
CNAME                  the custom domain
```

Each page is one file — markup, styles and scripts together — and they share no assets,
so either can be changed without touching the other.

Third-party code is loaded from a CDN and pinned: GSAP with ScrollTrigger for the
scroll-driven animation, Lenis for smooth scrolling, and Fraunces / Inter / IBM Plex Mono
from Google Fonts. The page degrades to a plain, fully readable document if any of them
fails to load, and all animation is switched off under `prefers-reduced-motion`.

## Contact

ssanelabs@gmail.com — corrections to the numbers are especially welcome; every measurement
on the page is reproducible.
