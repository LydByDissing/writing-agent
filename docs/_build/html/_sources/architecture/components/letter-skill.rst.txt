letter skill — Components
=========================

The ``letter`` skill container contains five logical components that run in
sequence. Each component maps to a distinct agent persona or utility module.

.. image:: ../diagrams/components_letter_skill.svg
   :alt: Component Diagram — letter skill
   :align: center
   :width: 100%

Components
----------

Interviewer
~~~~~~~~~~~

**Responsibility**: Conduct a structured intent-capture interview with the user
in Danish. Collect all required fields before any writing begins.

**Pattern**: Conversational state machine — one or two questions at a time,
confirms each answer before advancing.

**Fields captured** (all required before advancing):

1. Purpose — what the email must achieve (request, follow-up, introduction, negotiation, complaint, etc.)
2. Recipient — name and title/role if known
3. Relationship — ``known`` / ``business-contact`` / ``cold-canvas``
4. Key points — 2–3 things the email must communicate
5. Target language — any language; prefer EU + Danish; confidence check on low-resource languages
6. Call to action — what the recipient should do after reading
7. Subject line hook — a sharp, short phrase capturing the email's purpose; the Interviewer pushes back if it is vague or long
8. Cultural context — country/region of recipient (informs Cultural Translator)
9. Constraints — length (short/medium/long), deadline, things to avoid

**Cold-canvas extra**: when relationship = ``cold-canvas``, the Interviewer
applies stricter subject line review ("would this subject make you open an
email from a stranger?") and checks that the purpose is clear within the
first sentence.

**Does NOT**: write any content. Owns only the intent capture state.

**Interfaces**: outputs a structured ``intent`` object passed to DanishWriter.

---

DanishWriter
~~~~~~~~~~~~

**Responsibility**: Write the email body and subject line in Danish, based on
the ``intent`` object. This is the canonical version; all subsequent agents
translate or review from this.

**Pattern**: Single-shot generation with self-review against the intent checklist.

**Human-tone rules** (enforced at generation time):

- No em-dashes (— or --)
- No bullet lists inside the email body
- No hedging openers ("Certainly!", "Of course!", "As an AI")
- No filler closings ("In conclusion", "I hope this finds you well")
- Sentence length varies — mix short and long
- Do not start consecutive sentences with the same word
- No more than one exclamation mark in the entire email
- Subject line: ≤8 words, no question marks, no "Re:" unless it is a genuine reply

**Does NOT**: translate. Does not apply cultural adaptations.

**Interfaces**: outputs ``{subject_da, body_da}`` for the user approval gate.

**Gate**: presents the Danish draft to the user. Does not advance until the
user explicitly approves or requests changes.

---

CulturalTranslator
~~~~~~~~~~~~~~~~~~

**Responsibility**: Translate the approved Danish email into the target language,
applying business cultural norms for the recipient's country and relationship type.

**Pattern**: Spawned as a sub-agent with full context (intent object + Danish draft).
Specialised persona: "senior business correspondent fluent in [target language]
writing for a [country] business context."

**Cultural adaptation logic**:

- ``cold-canvas``: maximum formality, conservative opening, clear value proposition in first sentence
- ``business-contact``: formality calibrated to cultural norm (e.g. DE/JP high; US/AU lower)
- ``known``: semi-formal; can reference shared context if captured in intent

**Language confidence check**: before translating, the agent self-assesses
confidence (high / medium / low). If medium or low, it surfaces this to the
user with a prompt: "My [language] confidence is [level]. Proceed, switch language, or find a native reviewer?"

**Human-tone rules**: same rules as DanishWriter, applied in target language.

**Does NOT**: quality-check its own output. Does not own the approval gate.

**Interfaces**: outputs ``{subject_tl, body_tl, adaptation_notes}`` to LanguageExpert.

---

LanguageExpert
~~~~~~~~~~~~~~

**Responsibility**: Review the translated email as a native-speaker proofreader.
Catch language errors, LLM markers, tone mismatches, and cultural slip-ups.

**Pattern**: Spawned as a sub-agent. Persona: "native [target language] speaker
and business writing coach." Receives the full intent object, the Danish original,
and the translation.

**Review checklist**:

- Grammar and spelling
- Register: does the formality match the relationship + cultural norm?
- LLM marker scan: em-dashes, bullet lists in body, hedging openers, filler closings, robotic sentence rhythm
- Subject line: ≤8 words, compelling, no question marks
- Call to action: present and unambiguous
- Cold-canvas check (if applicable): does the opening give a reason to keep reading without starting with "I"?

**Output**: the reviewed email (with corrections applied) + a quality report:

.. code-block:: text

   Subject: [final subject]

   [final email body]

   ---
   Quality report:
   ✓ Purpose: [restated]
   ✓ Cultural register: [what was adapted and why]
   ✓ Call to action: confirmed present
   ✓ Human tone: [any LLM markers found and fixed, or "none detected"]
   ⚠ [any warnings or items user should verify]

**Does NOT**: rewrite content or change the message. Fixes language only.
If a content change is needed (missing key point, wrong call to action), it
flags it and asks the user to go back to the Danish draft.

**Interfaces**: outputs ``{subject_final, body_final, quality_report}`` to OutputFormatter.

**Gate**: presents quality report to user. Does not advance until user approves
or requests revision (→ restart from DanishWriter).

---

OutputFormatter
~~~~~~~~~~~~~~~

**Responsibility**: Deliver the finished email to the user.

**Steps**:

1. Copy ``body_final`` to clipboard via ``pyperclip``.
2. Generate a ``mailto:`` link: ``mailto:[recipient_email if captured]?subject=[url-encoded subject_final]&body=[url-encoded body_final]``
3. Print to terminal:

.. code-block:: text

   ✓ Email copied to clipboard.

   Open in email client:
   mailto:[recipient]?subject=[subject]&body=[...]

   (Click the link above, or paste from clipboard.)

**Does NOT**: send the email. Does not store the email.

**Interfaces**: terminal output only. No return value.
