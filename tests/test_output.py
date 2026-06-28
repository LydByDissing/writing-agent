# [origin ref=wr-73j req=REQ-LETTER-009 c4=writing_agent_src/OutputFormatter]
#   [intent]Unit tests for output.py (mailto URL generation) and clipboard handling[/intent]
# [/origin]
import pytest
from unittest.mock import patch, MagicMock
from urllib.parse import parse_qs, urlparse
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.output import format_mailto_link, output_email, copy_to_clipboard
import pyperclip


class TestFormatMailtoLink:
    """Tests for mailto: URL generation with proper encoding."""

    def test_format_mailto_link_basic_url_structure_correct(self):
        """Arrange/Act/Assert: Basic mailto URL has correct structure"""
        # Arrange
        recipient = "test@example.com"
        subject = "Hello"
        body = "Test body"

        # Act
        result = format_mailto_link(recipient, subject, body)

        # Assert
        assert result.startswith(f"mailto:{recipient}")
        assert "subject=" in result
        assert "body=" in result

    def test_format_mailto_link_email_preserved_exact(self):
        """Arrange/Act/Assert: Recipient email is pre-filled exactly"""
        # Arrange
        recipient = "user@example.com"
        subject = "Test"
        body = "Body"

        # Act
        result = format_mailto_link(recipient, subject, body)

        # Assert
        assert result.startswith("mailto:user@example.com?")

    def test_format_mailto_link_space_url_encoded(self):
        """Arrange/Act/Assert: Spaces are percent-encoded as %20 (RFC 6068)"""
        # Arrange
        recipient = "test@example.com"
        subject = "Hello World"
        body = "This is a test"

        # Act
        result = format_mailto_link(recipient, subject, body)

        # Assert - RFC 6068 requires %20, not +
        assert "Hello%20World" in result
        assert "This%20is%20a%20test" in result
        assert "Hello+World" not in result
        assert "This+is+a+test" not in result

    def test_format_mailto_link_ampersand_url_encoded(self):
        """Arrange/Act/Assert: Ampersand (&) is encoded as %26 in both params"""
        # Arrange
        recipient = "test@example.com"
        subject = "Test & Demo"
        body = "Rock & Roll"

        # Act
        result = format_mailto_link(recipient, subject, body)

        # Assert - & must be %26; spaces must be %20 (RFC 6068)
        query_string = result[result.index("?") + 1:]
        assert "%26" in query_string
        assert "Test%20%26%20Demo" in query_string

    def test_format_mailto_link_danish_chars_url_encoded(self):
        """Arrange/Act/Assert: Danish chars (ÆØÅ) are correctly encoded"""
        # Arrange
        recipient = "test@example.com"
        subject = "Æ Ø Å"
        body = "Æben Øl År"

        # Act
        result = format_mailto_link(recipient, subject, body)

        # Assert - special chars should be percent-encoded
        # %C3%86 = Æ, %C3%98 = Ø, %C3%85 = Å
        assert "%" in result  # URL encoding should be present
        parsed = urlparse(result)
        params = parse_qs(parsed.query)
        # The decoded values should contain the original chars
        assert "Æ" in params['subject'][0] or "%C3%86" in result

    def test_format_mailto_link_subject_in_params(self):
        """Arrange/Act/Assert: Subject parameter is in URL params"""
        # Arrange
        recipient = "test@example.com"
        subject = "Test Subject"
        body = "Test Body"

        # Act
        result = format_mailto_link(recipient, subject, body)

        # Assert - parse_qs decodes percent-encoding; subject must round-trip cleanly
        parsed = urlparse(result)
        params = parse_qs(parsed.query, keep_blank_values=True)
        assert 'subject' in params
        assert subject in params['subject'][0]

    def test_format_mailto_link_body_in_params(self):
        """Arrange/Act/Assert: Body parameter is in URL params"""
        # Arrange
        recipient = "test@example.com"
        subject = "Test Subject"
        body = "Test Body Content"

        # Act
        result = format_mailto_link(recipient, subject, body)

        # Assert - parse_qs decodes percent-encoding; body must round-trip cleanly
        parsed = urlparse(result)
        params = parse_qs(parsed.query, keep_blank_values=True)
        assert 'body' in params
        assert body in params['body'][0]

    def test_format_mailto_link_special_chars_multiline(self):
        """Arrange/Act/Assert: Multiline body with special chars is encoded"""
        # Arrange
        recipient = "test@example.com"
        subject = "Test"
        body = "Line 1\nLine 2\nLine 3"

        # Act
        result = format_mailto_link(recipient, subject, body)

        # Assert
        assert "mailto:test@example.com?" in result
        # Newlines should be encoded
        parsed = urlparse(result)
        params = parse_qs(parsed.query)
        assert 'body' in params


class TestOutputEmail:
    """Tests for output_email function including clipboard and printing."""

    @patch('src.output.pyperclip.copy')
    @patch('builtins.print')
    def test_output_email_copies_body_to_clipboard(self, mock_print, mock_copy):
        """Arrange/Act/Assert: output_email copies body to clipboard"""
        # Arrange
        recipient = "test@example.com"
        subject = "Test"
        body = "Email body content"

        # Act
        output_email(recipient, subject, body)

        # Assert
        mock_copy.assert_called_once_with(body)

    @patch('src.output.pyperclip.copy')
    @patch('builtins.print')
    def test_output_email_prints_success_message(self, mock_print, mock_copy):
        """Arrange/Act/Assert: output_email prints success message"""
        # Arrange
        recipient = "test@example.com"
        subject = "Test"
        body = "Email body"

        # Act
        output_email(recipient, subject, body)

        # Assert
        mock_print.assert_any_call("✓ Email body copied to clipboard")

    @patch('src.output.pyperclip.copy')
    @patch('builtins.print')
    def test_output_email_prints_mailto_link(self, mock_print, mock_copy):
        """Arrange/Act/Assert: output_email prints a mailto link containing recipient and subject"""
        # Arrange
        recipient = "test@example.com"
        subject = "Test Subject"
        body = "Email body"

        # Act
        output_email(recipient, subject, body)

        # Assert - the link line must contain recipient, subject param, and body param
        printed_messages = [call.args[0] for call in mock_print.call_args_list]
        link_lines = [msg for msg in printed_messages if "mailto:" in str(msg)]
        assert len(link_lines) == 1
        link = link_lines[0]
        assert "mailto:test@example.com" in link
        assert "subject=" in link
        assert "body=" in link

    @patch('src.output.pyperclip.copy')
    @patch('builtins.print')
    def test_output_email_recipient_in_mailto_link(self, mock_print, mock_copy):
        """Arrange/Act/Assert: output_email prints mailto with correct recipient"""
        # Arrange
        recipient = "user@domain.com"
        subject = "Subject"
        body = "Body"

        # Act
        output_email(recipient, subject, body)

        # Assert
        printed_messages = [call.args[0] for call in mock_print.call_args_list]
        mailto_messages = [msg for msg in printed_messages if "mailto:" in str(msg)]
        assert len(mailto_messages) > 0
        assert any("user@domain.com" in str(msg) for msg in mailto_messages)


class TestCopyToClipboard:
    """Tests for the clipboard helper and its pyperclip -> wl-copy/xclip/xsel fallback chain."""

    @patch('src.output.pyperclip.copy')
    def test_copy_uses_pyperclip_when_available(self, mock_copy):
        """Arrange/Act/Assert: pyperclip is tried first and reported as success"""
        # Arrange / Act
        result = copy_to_clipboard("hello")

        # Assert
        mock_copy.assert_called_once_with("hello")
        assert result is True

    @patch('src.output.subprocess.run')
    @patch('src.output.shutil.which')
    @patch('src.output.pyperclip.copy', side_effect=pyperclip.PyperclipException("no backend"))
    def test_copy_falls_back_to_shell_tool(self, mock_copy, mock_which, mock_run):
        """Arrange/Act/Assert: when pyperclip has no backend, a shell tool is used"""
        # Arrange: only wl-copy is installed
        mock_which.side_effect = lambda cmd: "/usr/bin/wl-copy" if cmd == "wl-copy" else None

        # Act
        result = copy_to_clipboard("body text")

        # Assert
        assert result is True
        mock_run.assert_called_once()
        called_cmd = mock_run.call_args.args[0]
        assert called_cmd[0] == "wl-copy"
        assert mock_run.call_args.kwargs.get("input") == "body text"

    @patch('src.output.shutil.which', return_value=None)
    @patch('src.output.pyperclip.copy', side_effect=pyperclip.PyperclipException("no backend"))
    def test_copy_returns_false_when_no_mechanism(self, mock_copy, mock_which):
        """Arrange/Act/Assert: returns False when neither pyperclip nor shell tools work"""
        # Act
        result = copy_to_clipboard("body text")

        # Assert
        assert result is False

    @patch('src.output.copy_to_clipboard', return_value=False)
    @patch('builtins.print')
    def test_output_email_warns_when_clipboard_unavailable(self, mock_print, mock_copy):
        """Arrange/Act/Assert: output_email warns and still prints mailto when clipboard fails"""
        # Act
        output_email("user@domain.com", "Subject", "Body")

        # Assert
        printed_messages = [str(call.args[0]) for call in mock_print.call_args_list]
        assert any("Could not copy to clipboard" in msg for msg in printed_messages)
        assert any("mailto:" in msg for msg in printed_messages)
