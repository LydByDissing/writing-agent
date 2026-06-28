# [origin ref=wr-zfo req=REQ-LETTER-001 c4=letter_skill/Interviewer,DanishWriter,CulturalTranslator,LanguageExpert]
#   [intent]Structural tests verifying SKILL.md contains all required sections, interview fields, rules, and persona specs[/intent]
# [/origin]

import pytest
from pathlib import Path


def read_skill_file():
    """Read the SKILL.md file and return content."""
    skill_path = Path(__file__).parent.parent / "skills" / "letter" / "SKILL.md"
    with open(skill_path, "r", encoding="utf-8") as f:
        return f.read()


class TestInterviewFieldsPresent:
    """Tests verify all 9 interview fields are documented."""

    def test_purpose_field_documented_in_table(self):
        """Arrange: Read SKILL.md
        Act: Search for 'purpose' in the interview fields table
        Assert: Field is present in the table"""
        content = read_skill_file()
        assert "| 1 | `purpose`" in content

    def test_recipient_field_documented_in_table(self):
        """Arrange: Read SKILL.md
        Act: Search for 'recipient' in the interview fields table
        Assert: Field is present in the table"""
        content = read_skill_file()
        assert "| 2 | `recipient`" in content

    def test_relationship_field_documented_in_table(self):
        """Arrange: Read SKILL.md
        Act: Search for 'relationship' in the interview fields table
        Assert: Field is present in the table"""
        content = read_skill_file()
        assert "| 3 | `relationship`" in content

    def test_key_points_field_documented_in_table(self):
        """Arrange: Read SKILL.md
        Act: Search for key_points as row 4 in interview fields table
        Assert: Field is present in the table row"""
        content = read_skill_file()
        assert "| 4 | `key_points`" in content

    def test_target_language_field_documented_in_table(self):
        """Arrange: Read SKILL.md
        Act: Search for target_language as row 5 in interview fields table
        Assert: Field is present in the table row"""
        content = read_skill_file()
        assert "| 5 | `target_language`" in content

    def test_call_to_action_field_documented_in_table(self):
        """Arrange: Read SKILL.md
        Act: Search for call_to_action as row 6 in interview fields table
        Assert: Field is present in the table row"""
        content = read_skill_file()
        assert "| 6 | `call_to_action`" in content

    def test_subject_hook_field_documented_in_table(self):
        """Arrange: Read SKILL.md
        Act: Search for subject_hook as row 7 in interview fields table
        Assert: Field is present in the table row"""
        content = read_skill_file()
        assert "| 7 | `subject_hook`" in content

    def test_cultural_context_field_documented_in_table(self):
        """Arrange: Read SKILL.md
        Act: Search for cultural_context as row 8 in interview fields table
        Assert: Field is present in the table row"""
        content = read_skill_file()
        assert "| 8 | `cultural_context`" in content

    def test_constraints_field_documented_in_table(self):
        """Arrange: Read SKILL.md
        Act: Search for constraints as row 9 in interview fields table
        Assert: Field is present in the table row"""
        content = read_skill_file()
        assert "| 9 | `constraints`" in content

    def test_cold_canvas_opener_note_in_intent_object(self):
        """Arrange: Read SKILL.md
        Act: Search for cold_canvas_opener_note in intent object definition
        Assert: Field is documented in the intent object"""
        content = read_skill_file()
        assert "cold_canvas_opener_note" in content


class TestColdCanvasSection:
    """Tests verify cold-canvas section exists and is properly documented."""

    def test_cold_canvas_strict_mode_section_exists(self):
        """Arrange: Read SKILL.md
        Act: Search for cold-canvas strict mode section header
        Assert: Section header is present"""
        content = read_skill_file()
        assert "### Cold-canvas strict mode" in content

    def test_cold_canvas_relationship_value_documented(self):
        """Arrange: Read SKILL.md
        Act: Search for cold-canvas as a relationship value
        Assert: cold-canvas is documented as valid relationship value"""
        content = read_skill_file()
        assert "cold-canvas" in content

    def test_cold_canvas_subject_stress_test_documented(self):
        """Arrange: Read SKILL.md
        Act: Search for cold-canvas subject stress-test instruction
        Assert: Step 1 mentions stress-testing the subject"""
        content = read_skill_file()
        assert "Step 1 — Subject stress-test" in content

    def test_cold_canvas_opening_sentence_note_documented(self):
        """Arrange: Read SKILL.md
        Act: Search for cold-canvas opening-sentence instruction
        Assert: Step 2 mentions opening-sentence note"""
        content = read_skill_file()
        assert "Step 2 — Opening-sentence note" in content


class TestSubjectLengthRule:
    """Tests verify subject ≤8 words rule is documented."""

    def test_subject_line_max_8_words_in_phase_2(self):
        """Arrange: Read SKILL.md
        Act: Search for ≤8 words constraint in Phase 2 rules
        Assert: Rule is documented in Phase 2"""
        content = read_skill_file()
        assert "more than 8 words" in content

    def test_subject_line_max_8_words_in_phase_2_checks(self):
        """Arrange: Read SKILL.md
        Act: Search for length check mentioning 8 words before confirming
        Assert: Rule documented in push-back section"""
        content = read_skill_file()
        assert "count words" in content and "more than 8" in content

    def test_subject_line_8_word_limit_in_cultural_translator(self):
        """Arrange: Read SKILL.md
        Act: Search for ≤8 words rule inside CulturalTranslator section specifically
        Assert: Rule is present in the CulturalTranslator sub-agent section"""
        content = read_skill_file()
        ct_start = content.find("## Sub-agent: CulturalTranslator")
        ct_end = content.find("## Sub-agent: LanguageExpert")
        assert ct_start != -1 and ct_end != -1
        ct_section = content[ct_start:ct_end]
        assert "8 words" in ct_section

    def test_subject_no_question_marks_rule(self):
        """Arrange: Read SKILL.md
        Act: Search for question mark prohibition in subject line
        Assert: Rule is documented"""
        content = read_skill_file()
        assert "no question marks" in content.lower()


class TestLLMMarkerProhibitions:
    """Tests verify all LLM marker prohibitions are documented."""

    def test_em_dash_prohibition_in_phase_2(self):
        """Arrange: Read SKILL.md
        Act: Search for em-dash prohibition in Phase 2
        Assert: Prohibition is documented"""
        content = read_skill_file()
        assert "No em-dashes" in content

    def test_em_dash_prohibition_in_cultural_translator(self):
        """Arrange: Read SKILL.md
        Act: Extract CulturalTranslator section and search for em-dash prohibition
        Assert: Prohibition is documented in CulturalTranslator human-tone rules"""
        content = read_skill_file()
        ct_start = content.find("## Sub-agent: CulturalTranslator")
        ct_end = content.find("## Sub-agent: LanguageExpert")
        ct_section = content[ct_start:ct_end]
        assert "No em-dashes" in ct_section

    def test_body_bullet_prohibition_in_phase_2(self):
        """Arrange: Read SKILL.md
        Act: Search for bullet list prohibition in Phase 2
        Assert: Prohibition is documented"""
        content = read_skill_file()
        assert "No bullet lists inside the email body" in content

    def test_body_bullet_prohibition_in_cultural_translator(self):
        """Arrange: Read SKILL.md
        Act: Extract CulturalTranslator section and search for bullet list prohibition
        Assert: Prohibition is documented in CulturalTranslator human-tone rules"""
        content = read_skill_file()
        ct_start = content.find("## Sub-agent: CulturalTranslator")
        ct_end = content.find("## Sub-agent: LanguageExpert")
        ct_section = content[ct_start:ct_end]
        assert "No bullet lists inside the email body" in ct_section

    def test_hedging_openers_prohibition_in_phase_2(self):
        """Arrange: Read SKILL.md
        Act: Search for hedging openers prohibition in Phase 2
        Assert: Prohibition is documented with examples"""
        content = read_skill_file()
        assert "No hedging openers" in content

    def test_hedging_openers_prohibition_in_cultural_translator(self):
        """Arrange: Read SKILL.md
        Act: Extract CulturalTranslator section and search for hedging openers prohibition
        Assert: Prohibition is documented in CulturalTranslator human-tone rules"""
        content = read_skill_file()
        ct_start = content.find("## Sub-agent: CulturalTranslator")
        ct_end = content.find("## Sub-agent: LanguageExpert")
        ct_section = content[ct_start:ct_end]
        assert "No hedging openers" in ct_section

    def test_filler_closings_prohibition_in_phase_2(self):
        """Arrange: Read SKILL.md
        Act: Search for filler closings prohibition in Phase 2
        Assert: Prohibition is documented with examples"""
        content = read_skill_file()
        assert "No filler closings" in content

    def test_filler_closings_prohibition_in_cultural_translator(self):
        """Arrange: Read SKILL.md
        Act: Extract CulturalTranslator section and search for filler closings prohibition
        Assert: Prohibition is documented in CulturalTranslator human-tone rules"""
        content = read_skill_file()
        ct_start = content.find("## Sub-agent: CulturalTranslator")
        ct_end = content.find("## Sub-agent: LanguageExpert")
        ct_section = content[ct_start:ct_end]
        assert "No filler closings" in ct_section

    def test_all_llm_markers_in_language_expert_scan(self):
        """Arrange: Read SKILL.md
        Act: Search for LanguageExpert LLM marker scan checklist within that section
        Assert: All LLM markers and subject-line rules documented in LanguageExpert section"""
        content = read_skill_file()
        le_start = content.find("## Sub-agent: LanguageExpert")
        assert le_start != -1
        le_section = content[le_start:]
        assert "LLM marker scan" in le_section
        assert "Em-dashes" in le_section
        assert "Bullet lists" in le_section
        assert "Hedging openers" in le_section
        assert "Filler closings" in le_section
        assert "exclamation mark" in le_section
        assert "8 words" in le_section
        assert "question marks" in le_section


class TestApprovalGates:
    """Tests verify both approval gate blocks are documented."""

    def test_phase_2_danish_writer_approval_gate_exists(self):
        """Arrange: Read SKILL.md
        Act: Search for Phase 2 approval gate after DanishWriter draft
        Assert: Gate documentation is present"""
        content = read_skill_file()
        assert "Gate: do not advance to Phase 3 until the user gives explicit approval" in content

    def test_phase_2_gate_requires_explicit_approval(self):
        """Arrange: Read SKILL.md
        Act: Search for explicit approval requirement in Phase 2 gate
        Assert: Documentation states waiting/ambiguous responses are not approval"""
        content = read_skill_file()
        assert "Waiting, ambiguous, or partial responses are not approval" in content

    def test_phase_4_language_expert_approval_gate_exists(self):
        """Arrange: Read SKILL.md
        Act: Search for Phase 4 approval gate after LanguageExpert review
        Assert: Gate documentation is present"""
        content = read_skill_file()
        assert "Do not advance to OutputFormatter until the user gives explicit approval" in content

    def test_phase_4_gate_requests_explicit_approval(self):
        """Arrange: Read SKILL.md
        Act: Search for explicit approval request in Phase 4 gate
        Assert: Documentation states user must give explicit approval"""
        content = read_skill_file()
        # Search for the gate instruction in Phase 4
        assert "Godkender du dette, eller ønsker du ændringer?" in content


class TestRevisionRestartInstruction:
    """Tests verify revision-restart instructions are documented."""

    def test_revision_loop_section_exists(self):
        """Arrange: Read SKILL.md
        Act: Search for Revision loop section header
        Assert: Section header is present"""
        content = read_skill_file()
        assert "## Revision loop" in content

    def test_revision_restarts_from_phase_2(self):
        """Arrange: Read SKILL.md
        Act: Search for revision restart instruction
        Assert: Documentation states restart from Phase 2"""
        content = read_skill_file()
        assert "**Restart from Phase 2 (DanishWriter).**" in content

    def test_revision_loop_full_pipeline_description(self):
        """Arrange: Read SKILL.md
        Act: Search for full pipeline description in revision loop
        Assert: Documentation describes full pipeline from Phase 2 onward"""
        content = read_skill_file()
        assert "DanishWriter → CulturalTranslator → LanguageExpert → OutputFormatter" in content

    def test_revision_note_captured_in_intent(self):
        """Arrange: Read SKILL.md
        Act: Search for revision_note in intent object documentation
        Assert: revision_note field is documented"""
        content = read_skill_file()
        assert 'revision_note' in content


class TestCulturalTranslatorSubAgent:
    """Tests verify CulturalTranslator sub-agent section with required specs."""

    def test_cultural_translator_section_exists(self):
        """Arrange: Read SKILL.md
        Act: Search for CulturalTranslator sub-agent section header
        Assert: Section header is present"""
        content = read_skill_file()
        assert "## Sub-agent: CulturalTranslator" in content

    def test_cultural_translator_persona_documented(self):
        """Arrange: Read SKILL.md
        Act: Search for CulturalTranslator persona definition
        Assert: Persona is documented"""
        content = read_skill_file()
        assert '"You are a senior business correspondent fluent in [target_language]' in content

    def test_cultural_translator_confidence_gate_exists(self):
        """Arrange: Read SKILL.md
        Act: Search for confidence gate section in CulturalTranslator
        Assert: Confidence gate is documented"""
        content = read_skill_file()
        assert "### Confidence gate" in content

    def test_cultural_translator_adaptation_by_relationship(self):
        """Arrange: Read SKILL.md
        Act: Search for relationship-based formality adaptation in CulturalTranslator
        Assert: Adaptation rules are documented"""
        content = read_skill_file()
        assert "Apply formality calibrated to `intent[\"relationship\"]`" in content

    def test_cultural_translator_output_format_documented(self):
        """Arrange: Read SKILL.md
        Act: Search for CulturalTranslator output format
        Assert: Output format with subject_tl, body_tl, adaptation_notes is documented"""
        content = read_skill_file()
        assert '"subject_tl"' in content
        assert '"body_tl"' in content
        assert '"adaptation_notes"' in content


class TestLanguageExpertSubAgent:
    """Tests verify LanguageExpert sub-agent section with quality report format."""

    def test_language_expert_section_exists(self):
        """Arrange: Read SKILL.md
        Act: Search for LanguageExpert sub-agent section header
        Assert: Section header is present"""
        content = read_skill_file()
        assert "## Sub-agent: LanguageExpert" in content

    def test_language_expert_persona_documented(self):
        """Arrange: Read SKILL.md
        Act: Search for LanguageExpert persona definition
        Assert: Persona is documented"""
        content = read_skill_file()
        assert '"You are a native [target_language] speaker and business writing coach."' in content

    def test_language_expert_review_checklist_exists(self):
        """Arrange: Read SKILL.md
        Act: Search for LanguageExpert review checklist
        Assert: Checklist section is documented"""
        content = read_skill_file()
        assert "### Review checklist" in content

    def test_language_expert_quality_report_format_documented(self):
        """Arrange: Read SKILL.md
        Act: Search for quality report format in LanguageExpert
        Assert: Quality report format section exists"""
        content = read_skill_file()
        assert "### Quality report format" in content

    def test_quality_report_has_purpose_field(self):
        """Arrange: Read SKILL.md
        Act: Search for Purpose field in quality report format
        Assert: Purpose field is documented with checkmark"""
        content = read_skill_file()
        assert "✓ Purpose:" in content

    def test_quality_report_has_cultural_register_field(self):
        """Arrange: Read SKILL.md
        Act: Search for Cultural register field in quality report format
        Assert: Cultural register field is documented with checkmark"""
        content = read_skill_file()
        assert "✓ Cultural register:" in content

    def test_quality_report_has_call_to_action_field(self):
        """Arrange: Read SKILL.md
        Act: Search for Call to action field in quality report format
        Assert: Call to action field is documented with checkmark"""
        content = read_skill_file()
        assert "✓ Call to action:" in content

    def test_quality_report_has_human_tone_field(self):
        """Arrange: Read SKILL.md
        Act: Search for Human tone field in quality report format
        Assert: Human tone field is documented with checkmark"""
        content = read_skill_file()
        assert "✓ Human tone:" in content

    def test_quality_report_has_warnings_section(self):
        """Arrange: Read SKILL.md
        Act: Search for warnings section in quality report format
        Assert: Warnings section with ⚠ symbol is documented"""
        content = read_skill_file()
        assert "⚠" in content

    def test_quality_report_all_four_checkmark_fields_required(self):
        """Arrange: Read SKILL.md
        Act: Search for requirement that all four ✓ fields are required
        Assert: Requirement is documented"""
        content = read_skill_file()
        assert "All four `✓` fields are required in every report" in content

    def test_language_expert_output_format_documented(self):
        """Arrange: Read SKILL.md
        Act: Search for LanguageExpert output format with quality_report
        Assert: Output format is documented"""
        content = read_skill_file()
        assert '"subject_final"' in content
        assert '"body_final"' in content
        assert '"quality_report"' in content


class TestOutputFormatterPhase:
    """Tests verify Phase 5 / OutputFormatter section documents clipboard and mailto."""

    def _phase5_section(self) -> str:
        content = read_skill_file()
        start = content.find("## Phase 5: OutputFormatter")
        assert start != -1, "Phase 5: OutputFormatter section not found in SKILL.md"
        end = content.find("\n## ", start + 1)
        return content[start:] if end == -1 else content[start:end]

    def test_phase5_section_exists(self):
        """Arrange: Read SKILL.md
        Act: Search for Phase 5 OutputFormatter section header
        Assert: Section header is present"""
        content = read_skill_file()
        assert "## Phase 5: OutputFormatter" in content

    def test_phase5_documents_clipboard_copy(self):
        """Arrange: Read SKILL.md
        Act: Extract Phase 5 section and search for clipboard copy instruction
        Assert: pyperclip clipboard copy is documented"""
        section = self._phase5_section()
        assert "clipboard" in section.lower()
        assert "pyperclip" in section

    def test_phase5_documents_mailto_link(self):
        """Arrange: Read SKILL.md
        Act: Extract Phase 5 section and search for mailto link instruction
        Assert: mailto: link output is documented"""
        section = self._phase5_section()
        assert "mailto:" in section

    def test_phase5_documents_url_encoding(self):
        """Arrange: Read SKILL.md
        Act: Extract Phase 5 section and check for url-encoded requirement
        Assert: url-encoding of subject and body is documented"""
        section = self._phase5_section()
        assert "url-encoded" in section or "url_encoded" in section or "urlencode" in section.lower()
