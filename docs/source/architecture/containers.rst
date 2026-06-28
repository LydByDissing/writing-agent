Containers
==========

The writing-agent has two containers: the ``letter`` skill (Claude Code agent
orchestrator) and a Python utility library that handles style rules, mailto:
generation, and clipboard output.

.. image:: diagrams/containers.svg
   :alt: Container Diagram
   :align: center
   :width: 100%

Elements
--------

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 40

   * - Name
     - Type
     - Technology
     - Purpose
   * - letter skill
     - Claude Code Skill
     - SKILL.md + Claude agent framework
     - Orchestrates the four-agent pipeline; manages interview, approval gates, and sub-agent spawning
   * - writing-agent src
     - Python library
     - Python 3.12
     - Style rule enforcement, mailto: link generation, clipboard copy, language confidence heuristics

Key Relationships
-----------------

- The ``letter`` skill is invoked by the user inside Claude Code via ``/letter``.
- The skill spawns sub-agents (Cultural Translator, Language Expert) using Claude's agent framework.
- The skill calls ``writing-agent src`` utilities to apply style rules, generate mailto: links, and copy to clipboard.
- The skill passes the finished email body + subject back to the user in the terminal.

Assumptions & Open Questions
-----------------------------

* No persistent storage — session state lives in the conversation context only.
* Clipboard access uses ``pyperclip`` (cross-platform: Linux xclip/xsel, macOS pbcopy, Windows clip).
* mailto: link is printed as a clickable terminal hyperlink where supported.
