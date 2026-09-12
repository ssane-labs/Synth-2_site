# /learn — the reading list

`index.html` is **generated**. Do not edit it by hand; edit the data and rebuild.

```
links/part1.json   sections 01–07   foundations → pretraining
links/part2.json   sections 08–14   fine-tuning → RAG
links/part3.json   sections 15–20   prompting → free compute
build.py           writes index.html from those three files
check_links.py     requests every URL and reports what broke
```

## Updating the list

1. Edit the relevant `links/partN.json`. One entry looks like:

   ```json
   {"t":"Title", "by":"Author or organisation", "u":"https://…",
    "k":"course", "m":"one line: what it is, how long, what licence"}
   ```

   `k` is one of `course video book docs code notebook paper article interactive
   reference blog tool` — anything else still renders, but gets no filter chip
   unless you add it to `KINDS` in `build.py`.

2. Check nothing is dead:

   ```
   python learn/check_links.py
   ```

   Note: `kaggle.com` answers 404 and `huggingface.co` answers 429 to scripted
   requests when hit in parallel. Both are false alarms — confirm in a browser
   before deleting an entry.

3. Rebuild and commit both files:

   ```
   python learn/build.py
   ```

## The rules this page keeps

- **Every row links to the original.** Nothing is mirrored, copied or summarised
  at length here; the one-line notes are ours, the material is theirs.
- **Free means free to read or watch**, without a trial or a card. Courses that
  only charge for a certificate are fine — say so in the note.
- **No affiliate links, ever.**
- The footer date comes from `datetime.date.today()` at build time, so it is
  honest only if you actually ran `check_links.py` that day.
