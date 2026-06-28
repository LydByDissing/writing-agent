FEAT-LETTER Design Session — run 9f8536a6
==========================================

:Date: 2026-06-27
:Feature: FEAT-LETTER
:Run: 9f8536a6
:c4_elements: Interviewer DanishWriter CulturalTranslator LanguageExpert OutputFormatter letter_skill writing_agent_src
:Requirements: FEAT-LETTER REQ-LETTER-001 REQ-LETTER-002 REQ-LETTER-003 REQ-LETTER-004 REQ-LETTER-005 REQ-LETTER-006 REQ-LETTER-007 REQ-LETTER-008 REQ-LETTER-009 REQ-LETTER-010

Interview Transcript
--------------------

**Agent**: Is this a Claude Code plugin/skill (same pattern as agent-project), or a standalone CLI tool?

**User**: Yes, let's implement a Claude skill. Can we make it work with ChatGPT as well?

**Agent**: Claude Code skills are Claude-specific. We'll build for Claude Code v1 and keep the Python utilities model-agnostic. Where should the output go — terminal/clipboard, file, or email client?

**User**: b (file) with a prompt to activate c (email client). Correction: a+c — terminal/clipboard plus prompt to open email client.

**Agent**: Should `letter` handle both letters and emails, or two separate skills? Should it support any target language or a predefined set?

**User**: Letters in 2026 is always an email. Default to email. Any language, but favor large EU languages + Danish. If agent isn't 100% confident, prompt the user for action.

**Agent**: Here is a draft intent capture checklist — does it look right? What should the email client integration actually do?

**User**: Let's primarily target business relationships across cultures. Output: c — copy + show a mailto: link with subject pre-filled.

**Agent**: Should cultural translation also apply country-level business norms? If the user wants changes after translation, go back to Danish draft or edit the translation?

**User**: Cultural adaptation yes, weighted by existing relationship. Revision: restart the loop (back to Danish draft). Important: subject line must be sharp and short — it's the hook. Anti-LLM writing rules are required (no em-dashes everywhere, etc.). How does the user know the final email is good?

**Agent**: Should the quality gate be done by the same translation agent, or a separate "language expert" agent?

**User**: A new "language teacher" agent that is expert in the set language. Cold canvas: more strict (no GDPR, but stricter subject line and opening).
