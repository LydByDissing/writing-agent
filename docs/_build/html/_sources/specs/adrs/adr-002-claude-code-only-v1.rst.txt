ADR-002: Claude Code as the only supported platform in v1
==========================================================

.. adr:: Claude Code as the only supported platform in v1
   :id: ADR-002
   :status: accepted
   :c4_scope: letter_skill

   **Context**: The user asked whether the skill could work with ChatGPT as
   well. Claude Code skills are SKILL.md instruction sets that run inside
   Claude's agent framework. ChatGPT's plugin system uses OpenAPI specs and
   has a different architecture.

   **Decision**: v1 targets Claude Code only. The Python utility library
   (writing-agent src) is kept model-agnostic so a future adapter is possible.

   **Rationale**: Building for two agent frameworks simultaneously doubles
   the surface area without clear demand. The Python utilities (style rules,
   mailto: generation, clipboard) are reusable. Only the SKILL.md orchestration
   is Claude-specific.

   **Consequences**: Users must have Claude Code to use the skill. A future
   ADR-003 can address cross-platform support when there is concrete demand.

   **Alternatives considered**:

   - Dual-platform from day one — rejected: doubles testing and maintenance
     burden, and the two plugin systems are architecturally incompatible at
     the instruction layer.
