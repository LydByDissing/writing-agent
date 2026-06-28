# [origin ref=wr-73j req=REQ-LETTER-004 c4=writing_agent_src/StyleRules]
#   [intent]Unit tests for style_rules.py (LLM marker detection)[/intent]
# [/origin]
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.style_rules import check


class TestStyleRulesCheckEmDash:
    """Tests for em-dash detection in check() function."""

    def test_check_em_dash_present_returns_marker(self):
        """Arrange/Act/Assert: check() returns em-dash when em-dash present"""
        # Arrange
        body = "This is a test — with an em-dash"

        # Act
        result = check(body=body)

        # Assert
        assert 'em-dash' in result

    def test_check_em_dash_not_present_no_marker(self):
        """Arrange/Act/Assert: check() does not return em-dash without em-dash"""
        # Arrange
        body = "This is a test with no special dashes"

        # Act
        result = check(body=body)

        # Assert
        assert 'em-dash' not in result

    def test_check_en_dash_also_detected(self):
        """Arrange/Act/Assert: check() detects en-dash (–) as well"""
        # Arrange
        body = "This is a test – with an en-dash"

        # Act
        result = check(body=body)

        # Assert
        assert 'em-dash' in result

    def test_check_double_hyphen_em_dash_detected(self):
        """Arrange/Act/Assert: check() detects -- (double-hyphen) as LLM em-dash marker"""
        # Arrange
        body = "This is a test -- with a double hyphen"

        # Act
        result = check(body=body)

        # Assert
        assert 'em-dash' in result


class TestStyleRulesCheckCleanText:
    """Tests for clean text returning empty list."""

    def test_check_clean_text_returns_empty_list(self):
        """Arrange/Act/Assert: check() returns empty list on clean text"""
        # Arrange
        body = "This is clean text without any markers."
        subject = "Clean Subject"

        # Act
        result = check(body=body, subject=subject)

        # Assert
        assert result == []

    def test_check_empty_text_returns_empty_list(self):
        """Arrange/Act/Assert: check() returns empty list for empty input"""
        # Arrange
        body = ""
        subject = ""

        # Act
        result = check(body=body, subject=subject)

        # Assert
        assert result == []


class TestStyleRulesCheckHedgingOpeners:
    """Tests for hedging opener detection."""

    def test_check_hedging_opener_it_seems_detected(self):
        """Arrange/Act/Assert: check() detects 'it seems' as hedging opener"""
        # Arrange
        body = "It seems like this is a good idea."

        # Act
        result = check(body=body)

        # Assert
        assert 'hedging-opener' in result

    def test_check_hedging_opener_perhaps_detected(self):
        """Arrange/Act/Assert: check() detects 'perhaps' as hedging opener"""
        # Arrange
        body = "Perhaps we should try this approach."

        # Act
        result = check(body=body)

        # Assert
        assert 'hedging-opener' in result

    def test_check_hedging_opener_maybe_detected(self):
        """Arrange/Act/Assert: check() detects 'maybe' as hedging opener"""
        # Arrange
        body = "Maybe this will work."

        # Act
        result = check(body=body)

        # Assert
        assert 'hedging-opener' in result

    def test_check_hedging_opener_i_think_detected(self):
        """Arrange/Act/Assert: check() detects 'i think' as hedging opener"""
        # Arrange
        body = "I think we should proceed with caution."

        # Act
        result = check(body=body)

        # Assert
        assert 'hedging-opener' in result

    def test_check_hedging_opener_case_insensitive(self):
        """Arrange/Act/Assert: check() detects hedging openers case-insensitively"""
        # Arrange
        body = "PERHAPS we should try. Maybe not."

        # Act
        result = check(body=body)

        # Assert
        assert 'hedging-opener' in result

    def test_check_hedging_opener_after_period(self):
        """Arrange/Act/Assert: check() detects hedging opener in second sentence"""
        # Arrange
        body = "First sentence here. Perhaps we could try this."

        # Act
        result = check(body=body)

        # Assert
        assert 'hedging-opener' in result


class TestStyleRulesCheckFillerClosings:
    """Tests for filler-closing detection."""

    def test_check_filler_closing_looking_forward_detected(self):
        """Arrange/Act/Assert: check() detects 'looking forward to hearing from you'"""
        # Arrange
        body = "Please review the proposal. Looking forward to hearing from you."

        # Act
        result = check(body=body)

        # Assert
        assert 'filler-closing' in result

    def test_check_filler_closing_let_me_know_detected(self):
        """Arrange/Act/Assert: check() detects 'let me know if you have any questions'"""
        # Arrange
        body = "Attached is the document. Let me know if you have any questions."

        # Act
        result = check(body=body)

        # Assert
        assert 'filler-closing' in result

    def test_check_filler_closing_feel_free_detected(self):
        """Arrange/Act/Assert: check() detects 'feel free to reach out'"""
        # Arrange
        body = "I hope this helps. Feel free to reach out."

        # Act
        result = check(body=body)

        # Assert
        assert 'filler-closing' in result

    def test_check_no_filler_closing_returns_no_marker(self):
        """Arrange/Act/Assert: check() does not flag clean business closing"""
        # Arrange
        body = "I look forward to your response. We can discuss the details on Thursday."

        # Act
        result = check(body=body)

        # Assert
        assert 'filler-closing' not in result


class TestStyleRulesCheckBulletList:
    """Tests for bullet list detection."""

    def test_check_bullet_list_dash_detected(self):
        """Arrange/Act/Assert: check() detects bullet list with dashes"""
        # Arrange
        body = "Items:\n- Item 1\n- Item 2"

        # Act
        result = check(body=body)

        # Assert
        assert 'bullet-list' in result

    def test_check_bullet_list_asterisk_detected(self):
        """Arrange/Act/Assert: check() detects bullet list with asterisks"""
        # Arrange
        body = "Items:\n* Item 1\n* Item 2"

        # Act
        result = check(body=body)

        # Assert
        assert 'bullet-list' in result

    def test_check_bullet_list_dot_detected(self):
        """Arrange/Act/Assert: check() detects bullet list with bullet points"""
        # Arrange
        body = "Items:\n• Item 1\n• Item 2"

        # Act
        result = check(body=body)

        # Assert
        assert 'bullet-list' in result

    def test_check_no_bullet_list_no_marker(self):
        """Arrange/Act/Assert: check() does not detect bullet list without bullets"""
        # Arrange
        body = "Item 1\nItem 2"

        # Act
        result = check(body=body)

        # Assert
        assert 'bullet-list' not in result


class TestStyleRulesCheckExclamationMarks:
    """Tests for multiple exclamation mark detection."""

    def test_check_multiple_exclamation_marks_detected(self):
        """Arrange/Act/Assert: check() detects >1 exclamation marks"""
        # Arrange
        body = "This is great! I love it!"

        # Act
        result = check(body=body)

        # Assert
        assert 'multiple-exclamation-marks' in result

    def test_check_single_exclamation_mark_not_detected(self):
        """Arrange/Act/Assert: check() allows single exclamation mark"""
        # Arrange
        body = "This is great!"

        # Act
        result = check(body=body)

        # Assert
        assert 'multiple-exclamation-marks' not in result

    def test_check_no_exclamation_marks_not_detected(self):
        """Arrange/Act/Assert: check() allows no exclamation marks"""
        # Arrange
        body = "This is great"

        # Act
        result = check(body=body)

        # Assert
        assert 'multiple-exclamation-marks' not in result

    def test_check_three_exclamation_marks_detected(self):
        """Arrange/Act/Assert: check() detects 3 exclamation marks"""
        # Arrange
        body = "Great! Excellent! Fantastic!"

        # Act
        result = check(body=body)

        # Assert
        assert 'multiple-exclamation-marks' in result


class TestStyleRulesCheckSubjectLength:
    """Tests for subject word count detection."""

    def test_check_subject_too_long_9_words_detected(self):
        """Arrange/Act/Assert: check() detects subject with 9 words (>8)"""
        # Arrange
        subject = "This is a very long subject line that exceeds eight words"

        # Act
        result = check(subject=subject)

        # Assert
        assert 'subject-too-long' in result

    def test_check_subject_exactly_8_words_not_detected(self):
        """Arrange/Act/Assert: check() allows subject with exactly 8 words"""
        # Arrange
        subject = "This is a subject line with exactly eight"

        # Act
        result = check(subject=subject)

        # Assert
        assert 'subject-too-long' not in result

    def test_check_subject_7_words_not_detected(self):
        """Arrange/Act/Assert: check() allows subject with 7 words"""
        # Arrange
        subject = "This is a subject with only seven words"

        # Act
        result = check(subject=subject)

        # Assert
        assert 'subject-too-long' not in result

    def test_check_subject_10_words_detected(self):
        """Arrange/Act/Assert: check() detects subject with 10 words"""
        # Arrange
        subject = "This is a very long subject line that clearly exceeds the maximum"

        # Act
        result = check(subject=subject)

        # Assert
        assert 'subject-too-long' in result


class TestStyleRulesCheckMultipleMarkers:
    """Tests for detecting multiple markers in same text."""

    def test_check_multiple_markers_detected_together(self):
        """Arrange/Act/Assert: check() returns multiple markers when present"""
        # Arrange
        body = "Perhaps we should try this! Excellent! This is great!"
        subject = "This is a very long subject line that exceeds eight words"

        # Act
        result = check(body=body, subject=subject)

        # Assert
        assert 'hedging-opener' in result
        assert 'multiple-exclamation-marks' in result
        assert 'subject-too-long' in result

    def test_check_em_dash_and_bullet_list(self):
        """Arrange/Act/Assert: check() detects both em-dash and bullet list"""
        # Arrange
        body = "Here are items — key points:\n- Item 1\n- Item 2"

        # Act
        result = check(body=body)

        # Assert
        assert 'em-dash' in result
        assert 'bullet-list' in result


class TestStyleRulesCheckSubjectQuestionMark:
    """Tests for question mark in subject detection."""

    def test_check_question_mark_in_subject_detected(self):
        """Arrange/Act/Assert: check() detects question mark in subject"""
        # Arrange
        subject = "Can we discuss this?"

        # Act
        result = check(subject=subject)

        # Assert
        assert 'question-mark-in-subject' in result

    def test_check_no_question_mark_in_subject_not_detected(self):
        """Arrange/Act/Assert: check() does not detect question mark without one"""
        # Arrange
        subject = "Let us discuss this"

        # Act
        result = check(subject=subject)

        # Assert
        assert 'question-mark-in-subject' not in result
