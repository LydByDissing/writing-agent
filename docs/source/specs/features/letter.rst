Multilingual Business Email Writer
====================================

.. feat:: Multilingual Business Email Writer
   :id: FEAT-LETTER
   :status: approved

   A Claude Code skill (``/letter``) that helps a Danish-speaking business
   professional write emails in any target language. The user describes their
   intent in Danish; the skill interviews them, drafts in Danish, gets approval,
   then spawns a Cultural Translator and a Language Expert to produce a
   polished, human-sounding business email ready to send.

Requirements
------------

.. req:: Intent capture interview
   :id: REQ-LETTER-001
   :links: FEAT-LETTER
   :status: approved
   :rationale: All writing quality depends on capturing full intent before any text is produced. Incomplete intent leads to wrong tone, missing points, and revision loops.
   :acceptance: Given the user invokes /letter, when the interview completes, then all nine fields (purpose, recipient, relationship, key points, target language, call to action, subject hook, cultural context, constraints) are non-empty and confirmed by the user before DanishWriter is called.
   :non_goal: Does not capture GDPR opt-out language or legal disclaimers.
   :c4_component: Interviewer
   :c4_container: letter_skill

   The system shall conduct a conversational interview in Danish, asking one or
   two questions at a time, confirming each answer before proceeding, and
   refusing to advance to the writing phase until all nine required fields are
   captured.

.. req:: Cold-canvas strict mode
   :id: REQ-LETTER-002
   :links: FEAT-LETTER
   :status: approved
   :rationale: Cold outreach has the lowest tolerance for weak subject lines or unclear openers. A bad cold email is deleted in under two seconds.
   :acceptance: Given relationship = cold-canvas, when the subject line is captured, then the Interviewer applies strict review (≤8 words, no question marks, reason-to-open test) and pushes back at least once if the subject does not pass. Given the final email, when the LanguageExpert reviews it, then it checks the opening sentence does not start with "I" and contains a clear reason to keep reading.
   :non_goal: Does not check GDPR/CASL compliance.
   :c4_component: Interviewer
   :c4_container: letter_skill

   The system shall apply stricter subject line and opening-sentence rules when
   the relationship type is ``cold-canvas``.

.. req:: Danish draft with approval gate
   :id: REQ-LETTER-003
   :links: FEAT-LETTER
   :status: approved
   :rationale: Danish is the user's strongest language. Approving content in Danish before translation ensures the message is correct before cultural adaptation introduces variation.
   :acceptance: Given the interview is complete, when DanishWriter produces the draft, then the system presents subject_da and body_da to the user and waits for explicit approval or change request before spawning any sub-agent.
   :non_goal: Does not write in any language other than Danish at this stage.
   :c4_component: DanishWriter
   :c4_container: letter_skill

   The system shall write the email in Danish first and present it to the user
   for approval before any translation work begins.

.. req:: Human-tone writing rules
   :id: REQ-LETTER-004
   :links: FEAT-LETTER
   :status: approved
   :rationale: LLM-generated text is recognisable and undermines trust in business contexts. The output must read as written by a human professional.
   :acceptance: Given any generated email body (Danish or translated), when the LanguageExpert scans it, then zero em-dashes, zero bullet lists in body, zero hedging openers, zero filler closings, and no consecutive sentences starting with the same word are present in the final delivered email.
   :non_goal: Does not enforce a specific reading-level score.
   :c4_component: DanishWriter
   :c4_container: letter_skill

   The system shall enforce human-tone rules on all generated content: no
   em-dashes, no bullet lists in body, no hedging openers, no filler closings,
   varied sentence length, no consecutive sentences starting with the same word,
   at most one exclamation mark per email.

.. req:: Cultural translation with adaptation notes
   :id: REQ-LETTER-005
   :links: FEAT-LETTER
   :status: approved
   :rationale: A literal translation is often inappropriate across business cultures. The tone, register, and structure that work in Denmark may not work in Germany, Japan, or the USA. Cultural adaptation is the core value of this skill.
   :acceptance: Given an approved Danish draft and a target language + cultural context, when CulturalTranslator runs, then the output includes subject_tl, body_tl, and adaptation_notes listing what was changed and why. The register matches the relationship type (cold-canvas = maximum formality; known = semi-formal).
   :non_goal: Does not translate to more than one target language per session.
   :c4_component: CulturalTranslator
   :c4_container: letter_skill

   The system shall translate the Danish draft into the target language while
   applying business cultural norms appropriate to the recipient's country and
   the relationship type, and shall report what was culturally adapted.

.. req:: Language confidence gate
   :id: REQ-LETTER-006
   :links: FEAT-LETTER
   :status: approved
   :rationale: Claude's language quality varies significantly across languages. Producing a poor-quality email in a language where the user cannot verify it is worse than surfacing uncertainty.
   :acceptance: Given a target language, when CulturalTranslator self-assesses its confidence as medium or low, then it presents the confidence level to the user and offers three options (proceed / switch language / note to find native reviewer) before generating output.
   :non_goal: Does not block high-confidence languages (large EU languages + Danish).
   :c4_component: CulturalTranslator
   :c4_container: letter_skill

   The system shall self-assess language confidence before translating and
   surface a user prompt if confidence is medium or low.

.. req:: Language expert quality review
   :id: REQ-LETTER-007
   :links: FEAT-LETTER
   :status: approved
   :rationale: The Cultural Translator optimises for cultural fit. A separate Language Expert persona catches grammar errors, LLM markers, and tone mismatches that the translator may introduce.
   :acceptance: Given a translated email, when LanguageExpert completes its review, then the output includes a quality report with: purpose restated, cultural register noted, call to action confirmed, human-tone scan result, and any warnings. The report is presented alongside the final email before the user approval gate.
   :non_goal: Does not rewrite content — content changes must go back to the Danish draft.
   :c4_component: LanguageExpert
   :c4_container: letter_skill

   The system shall spawn a Language Expert sub-agent to proofread the
   translated email and produce a quality report before delivery.

.. req:: Sharp subject line
   :id: REQ-LETTER-008
   :links: FEAT-LETTER
   :status: approved
   :rationale: The subject line is the hook that determines whether the email is opened. In business cold outreach especially, a vague or long subject line means the email is ignored.
   :acceptance: Given any generated email, when OutputFormatter delivers it, then subject_final is ≤8 words, contains no question marks, and was reviewed by LanguageExpert for compellingness. The Interviewer must have challenged the user if the initial hook was vague or exceeded 8 words.
   :non_goal: Does not A/B test subject lines.
   :c4_component: Interviewer
   :c4_container: letter_skill

   The system shall enforce a ≤8-word subject line that was validated by both
   the Interviewer (intent stage) and the LanguageExpert (review stage).

.. req:: Clipboard output and mailto link
   :id: REQ-LETTER-009
   :links: FEAT-LETTER
   :status: approved
   :rationale: The user needs to get the finished email into their email client with minimum friction. Clipboard + mailto: covers all clients without requiring integration.
   :acceptance: Given user approval of the final email, when OutputFormatter runs, then body_final is copied to clipboard via pyperclip AND a mailto: link with url-encoded subject_final and body_final is printed as a clickable terminal link.
   :non_goal: Does not send the email programmatically. Does not integrate with specific email clients (Gmail API, Outlook, etc.).
   :c4_component: OutputFormatter
   :c4_container: letter_skill

   The system shall copy the final email body to the clipboard and print a
   pre-filled mailto: link (subject + body url-encoded) to the terminal.

.. req:: Revision loop restart
   :id: REQ-LETTER-010
   :links: FEAT-LETTER
   :status: approved
   :rationale: If the user wants changes after seeing the translated version, going back to the Danish canonical draft ensures all agents re-run with consistent intent rather than patching a translation mid-stream.
   :acceptance: Given the user requests a change at any approval gate after the Danish draft, when the revision is requested, then the system returns to DanishWriter with the original intent object plus the stated change, and the full pipeline (DanishWriter → CulturalTranslator → LanguageExpert) re-runs from that point.
   :non_goal: Does not allow partial re-runs (e.g. re-running only LanguageExpert with a manual edit).
   :c4_component: DanishWriter
   :c4_container: letter_skill

   The system shall restart the pipeline from the Danish draft stage whenever
   the user requests a revision after the Danish approval gate.
