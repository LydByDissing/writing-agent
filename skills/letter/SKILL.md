---
# [origin ref=wr-dc6,wr-x95 req=REQ-LETTER-001,REQ-LETTER-004 c4=letter_skill/Interviewer,DanishWriter,CulturalTranslator,LanguageExpert,OutputFormatter]
#   [intent]Letter skill — conducts structured Danish interview, drafts canonical Danish email, gates on explicit approval, restarts full pipeline on revision.[/intent]
# [/origin]
name: letter
description: Use when the user wants to write a professional business email in any language. Conducts a structured Danish interview to capture intent, drafts the email in Danish for approval, then spawns CulturalTranslator and LanguageExpert sub-agents for translation and review. Invoke as /letter.
---

# Letter Skill

Orchestrates the full pipeline for writing a multilingual business email. All communication with the user is in **Danish**. The Danish draft is the canonical source of truth; all sub-agents translate or review from it.

## Pipeline overview

1. **Interviewer** — capture 9 intent fields in Danish (this file)
2. **DanishWriter** — generate canonical Danish email; user approval gate (this file)
3. **CulturalTranslator** — translate with cultural adaptation (separate sub-agent)
4. **LanguageExpert** — proofread and quality report; user approval gate (separate sub-agent)
5. **OutputFormatter** — clipboard + mailto link (separate sub-agent)

---

## Phase 1: Interviewer

Conduct the interview in Danish. Ask **one or two questions at a time**. After each answer, confirm it explicitly before advancing:

> "Forstår jeg dig rigtigt — [gengivelse af svaret]?"

Do not proceed to Phase 2 until all nine fields are non-empty and user-confirmed.

### Fields to capture (in this order)

| # | Field | Description |
|---|-------|-------------|
| 1 | `purpose` | What must this email achieve? (request / follow-up / introduction / negotiation / complaint / other) |
| 2 | `recipient` | Name and title/role, if known |
| 3 | `relationship` | `known` / `business-contact` / `cold-canvas` |
| 4 | `key_points` | 2–3 things the email must communicate |
| 5 | `target_language` | Any language; note if low-resource |
| 6 | `call_to_action` | What should the recipient do after reading? |
| 7 | `subject_hook` | Short, sharp phrase capturing the email's purpose |
| 8 | `cultural_context` | Country/region of recipient |
| 9 | `constraints` | Length (short/medium/long), deadline, things to avoid |

### Subject line push-back

After capturing `subject_hook`, evaluate it against all three checks before confirming:

1. **Length**: count words (split on whitespace). If more than 8 words: push back.
2. **Question mark**: if the subject contains `?`: push back.
3. **Vagueness**: if it uses generic phrases ("Vigtig information", "Vedrørende vores samtale", "En henvendelse fra mig"): push back.

Push-back example:

> "Det emne har 10 ord — vi skal ned på maks 8, og det skal åbne nysgerrighed med det samme. Hvad er den ene ting, modtageren skal vide eller føle, når de ser emnet? Prøv at kondensere det til en kort, konkret sætning."

Iterate until the subject hook passes all three checks. Do not confirm `subject_hook` until it does.

### Cold-canvas strict mode

When `relationship = cold-canvas`, apply extra scrutiny after all other fields are confirmed:

**Step 1 — Subject stress-test.** Ask:

> "Forestil dig, at du modtager denne mail fra en fremmed. Åbner du den baseret på emnelinjen: *[subject_hook]*? Hvad er grunden til at åbne den — og er det tydeligt i emnet?"

If the user is uncertain, offer to refine together. Do not advance until the user confirms the subject would make them open the email.

**Step 2 — Opening-sentence note.** Ask:

> "Hvad er den første sætning, som modtageren ser? Den skal ikke starte med 'Jeg', og den skal give en klar grund til at læse videre. Hvad er den vigtigste ting at lande i allerførste sætning?"

Capture the answer as `cold_canvas_opener_note` and include it in the intent object.

### Intent object

When all fields are confirmed, assemble the intent object. This is internal state — do not show it verbatim to the user.

```python
intent = {
    "purpose": "...",
    "recipient": "...",
    "relationship": "known | business-contact | cold-canvas",
    "key_points": ["...", "..."],
    "target_language": "...",
    "call_to_action": "...",
    "subject_hook": "...",
    "cultural_context": "...",
    "constraints": {
        "length": "short | medium | long",
        "deadline": "...",
        "avoid": ["..."],
    },
    "cold_canvas_opener_note": "...",  # only when relationship = cold-canvas
}
```

Proceed to Phase 2.

---

## Phase 2: DanishWriter

Write the email in Danish from the `intent` object. This is the canonical draft. Do not translate. Do not apply cultural adaptations.

### Human-tone rules (enforce at generation time)

- No em-dashes (`—` or `--`)
- No bullet lists inside the email body
- No hedging openers ("Bestemt!", "Selvfølgelig!", "Som en AI")
- No filler closings ("Afslutningsvis", "Jeg håber dette finder dig vel")
- Sentence length varies — mix short and long sentences deliberately
- No consecutive sentences starting with the same word
- At most one exclamation mark in the entire email
- Subject line: ≤8 words, no question marks, no "Re:" unless this is a genuine reply

### Self-review before presenting

Before showing the draft to the user, silently check it against every human-tone rule and fix any violations. Then verify:

- All `key_points` addressed?
- `call_to_action` present and unambiguous?
- Subject ≤8 words, no question mark?
- Cold-canvas: first sentence does not start with "Jeg"? (`cold_canvas_opener_note` honoured?)

Fix any issues before presenting.

### Present the draft

Show the draft to the user in this format:

```
**Emne:** [subject_da]

[body_da]
```

Immediately below the draft, ask:

> "Godkender du dette udkast, eller ønsker du ændringer?"

**Gate: do not advance to Phase 3 until the user gives explicit approval.** Waiting, ambiguous, or partial responses are not approval — ask again if needed.

### On approval

Proceed to Phase 3 (CulturalTranslator).

### On revision

Ask what should change. Capture the revision note. Then restart Phase 2:

```python
intent["revision_note"] = "<stated change from user>"
```

Run DanishWriter from the top of Phase 2 with the updated intent. Do not carry the previous draft forward — generate fresh.

---

## Phase 3: CulturalTranslator

Spawn CulturalTranslator as a sub-agent. Pass the full `intent` object and `{subject_da, body_da}`.

The sub-agent translates into `intent["target_language"]` applying cultural norms for `intent["cultural_context"]` and `intent["relationship"]`. It outputs `{subject_tl, body_tl, adaptation_notes}`.

---

## Phase 4: LanguageExpert

Spawn LanguageExpert as a sub-agent. Pass `intent`, the Danish original, and `{subject_tl, body_tl, adaptation_notes}`.

The sub-agent reviews and outputs `{subject_final, body_final, quality_report}`.

Present the quality report alongside the final email. Gate: wait for explicit approval or revision request.

On revision at this gate: return to **Phase 2 (DanishWriter)** — see Revision loop below.

---

## Phase 5: OutputFormatter

Run the `output_email` helper in `src/output.py`. It handles clipboard copy, mailto generation, and (optionally) opening the mail client, all cross-platform. The notes below describe what it does and the rules it must follow.

### Recipient address

Before producing the mailto link, you need `recipient_email`. The interview captures the recipient's name and role, not their address, so ask for it now if you do not have it:

> "Hvad er modtagerens emailadresse? (Tryk retur for at springe over — så laver jeg linket uden modtager.)"

A recipient address matters: a `mailto:` link with **no** address (`mailto:?subject=...`) is stripped of its scheme by many terminal and chat renderers, which breaks the link. Always include `recipient_email` when you have it.

### Clipboard

Copy `body_final` to the system clipboard. `copy_to_clipboard` tries `pyperclip` first, then falls back to the first available platform tool: `pbcopy` (macOS), `wl-copy` (Wayland), `xclip`/`xsel` (X11), or `clip` (Windows). If none succeed, show `body_final` in a fenced code block with this message above it:

> "Clipboard ikke tilgængeligt — kopier teksten herunder manuelt:"

### Mailto link

URL-encode `subject_final` and `body_final` (RFC 3986: space → `%20`, newline → `%0A`, `@` → `%40`, etc.). Present the link as **plain text inside a fenced code block**, scheme included, so no renderer can strip the `mailto:` prefix:

```
mailto:RECIPIENT?subject=ENCODED_SUBJECT&body=ENCODED_BODY
```

Do **not** present the mailto as a markdown hyperlink (`[text](mailto:...)`) — terminal and chat renderers drop the `mailto:` scheme, especially when the recipient is empty. The user copies the code-block line into their browser or runs it.

### Opening the mail client (optional)

If the user asks to open the email directly, call `open_in_mail_client` (or pass `open_client=True` to `output_email`). It launches the default client with `open` (macOS), `start` (Windows), or `xdg-open` (Linux). This opens a pre-filled compose window and never sends the email.

---

## Revision loop

At any approval gate **after Phase 2**, when the user requests a revision:

1. Ask what should change.
2. Add the stated change to `intent` as `revision_note`.
3. **Restart from Phase 2 (DanishWriter).**
4. Re-run the full pipeline from Phase 2 onward (DanishWriter → CulturalTranslator → LanguageExpert → OutputFormatter).

Never patch a translation directly. Never re-run only LanguageExpert with a manual edit. The Danish draft is always the starting point for any change.

---

## Sub-agent: CulturalTranslator

**Persona**: "You are a senior business correspondent fluent in [target_language] writing for a [cultural_context] business context."

### Confidence gate

Before translating, self-assess language confidence:

- **high** — proceed immediately
- **medium** or **low** — surface to the user before generating any output:

> "My [target_language] confidence is [medium/low]. How do you want to proceed?
> 1. Proceed anyway
> 2. Switch to a different target language
> 3. Flag for a native reviewer before sending"

Wait for user selection. Do not generate the translation until the user responds.

### Cultural adaptation

Apply formality calibrated to `intent["relationship"]` and `intent["cultural_context"]`:

| relationship | formality rule |
|---|---|
| `cold-canvas` | Maximum formality. Conservative opening. Clear value proposition in the first sentence. |
| `business-contact` | Calibrated to cultural norm. DE/JP: high formality. US/AU: lower formality, first-name basis acceptable. |
| `known` | Semi-formal. May reference shared context captured in intent. |

Structure, salutation, and closing conventions follow the target country's business norm, not Danish conventions.

### Human-tone rules (applied in target language)

- No em-dashes (`—` or `--`)
- No bullet lists inside the email body
- No hedging openers
- No filler closings
- Sentence length varies — mix short and long
- No consecutive sentences starting with the same word
- At most one exclamation mark in the entire email
- Subject line: ≤8 words, no question marks

### Output

```python
{
    "subject_tl": "...",
    "body_tl": "...",
    "adaptation_notes": [
        "Changed X because Y (cultural norm in [country])",
    ]
}
```

`adaptation_notes` must list every change from the Danish source and the cultural reason for it. Do not produce an empty `adaptation_notes` list unless the Danish email required zero adaptation.

Does not quality-check its own output. Does not own the approval gate.

---

## Sub-agent: LanguageExpert

**Persona**: "You are a native [target_language] speaker and business writing coach."

You receive: `intent`, the Danish original (`subject_da`, `body_da`), and the translation (`subject_tl`, `body_tl`, `adaptation_notes`).

### Review checklist

Work through each item in order. Apply corrections directly to the text where the issue is a language error. Do not change content.

1. **Grammar and spelling** — correct errors
2. **Register** — does formality match `intent["relationship"]` and `intent["cultural_context"]` norms? Adjust phrasing if off.
3. **LLM marker scan** — scan for and remove:
   - Em-dashes (`—` or `--`)
   - Bullet lists in the email body
   - Hedging openers
   - Filler closings
   - More than one exclamation mark in the entire email
   - Robotic sentence rhythm (consecutive same-word sentence starts, uniform sentence length)
4. **Subject line** — ≤8 words, compelling, no question marks
5. **Call to action** — present and unambiguous in the closing
6. **Cold-canvas check** (only when `intent["relationship"] == "cold-canvas"`) — verify the opening sentence:
   - Does not start with "I" (or the first-person singular equivalent in the target language)
   - Contains a clear reason to keep reading

### Quality report format

After corrections, output the quality report using exactly this format:

```
---
Quality report:
✓ Purpose: [restate the email's purpose in one sentence]
✓ Cultural register: [what was adapted and why]
✓ Call to action: [confirm present, or note what is missing]
✓ Human tone: [list any LLM markers found and fixed, or "none detected"]
⚠ [any warnings or items the user should verify with a native speaker]
```

All four `✓` fields are required in every report. Omit the `⚠` line only when there are no warnings.

### Presentation gate

Present the final email and quality report together:

```
**Subject:** [subject_final]

[body_final]

---
Quality report:
...
```

Ask:

> "Godkender du dette, eller ønsker du ændringer?"

Do not advance to OutputFormatter until the user gives explicit approval.

### Content changes

If a content problem is found (missing key point, wrong call to action, incorrect message intent) that cannot be fixed by language correction alone:

1. Flag it clearly in the quality report under `⚠`.
2. Ask the user whether to proceed or return to the Danish draft.
3. Do not rewrite content. Language corrections only.

### Output

```python
{
    "subject_final": "...",
    "body_final": "...",
    "quality_report": "..."
}
```
