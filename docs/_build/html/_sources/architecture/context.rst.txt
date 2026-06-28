System Context
==============

The writing-agent is a Claude Code skill that helps a Danish-speaking business
professional write emails in foreign languages. The user writes intent in Danish;
the system interviews, drafts, translates, and quality-checks before outputting
a ready-to-send email.

.. image:: diagrams/context.svg
   :alt: System Context Diagram
   :align: center
   :width: 100%

Elements
--------

.. list-table::
   :header-rows: 1
   :widths: 20 15 65

   * - Name
     - Type
     - Purpose
   * - Business Professional
     - Person
     - Danish-speaking user who needs to send business emails in other languages
   * - writing-agent
     - System
     - Claude Code skill that interviews, drafts, translates, and quality-checks emails
   * - Claude AI
     - External System
     - Powers all agent personas (interviewer, writer, translator, language expert)
   * - Email Client
     - External System
     - Receives the finished email via mailto: link; opened on user request

Key Relationships
-----------------

- The Business Professional invokes the ``letter`` skill inside Claude Code.
- The skill uses Claude AI to run four agent personas in sequence.
- The finished email is delivered to the user's clipboard and optionally opens their Email Client via a pre-filled mailto: link (subject + recipient pre-filled).

Assumptions & Open Questions
-----------------------------

* The user's mother tongue is Danish; all intent capture is in Danish.
* Cross-platform email client support (ChatGPT, etc.) is out of scope for v1 — see ADR-002.
* Language confidence: if Claude is not confident in a low-resource language, it prompts the user before proceeding.
