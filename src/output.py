# [origin ref=wr-65v req=REQ-LETTER-009 c4=writing_agent_src/OutputFormatter]
#   [intent]Copies email body to clipboard and generates mailto: link for terminal output[/intent]
# [/origin]
import platform
import shutil
import subprocess
import pyperclip
from urllib.parse import urlencode, quote

# Fallback clipboard commands, tried in order when pyperclip has no backend.
# Covers macOS (pbcopy), Wayland (wl-copy), X11 (xclip, xsel), and Windows
# (clip) so the skill works wherever pyperclip cannot autodetect a mechanism.
_CLIPBOARD_FALLBACKS = (
	["pbcopy"],
	["wl-copy"],
	["xclip", "-selection", "clipboard"],
	["xsel", "--clipboard", "--input"],
	["clip"],
)

def format_mailto_link(recipient_email: str, subject_final: str, body_final: str) -> str:
	params = {
		'subject': subject_final,
		'body': body_final
	}
	encoded = urlencode(params, quote_via=quote)
	return f"mailto:{recipient_email}?{encoded}"

def copy_to_clipboard(text: str) -> bool:
	"""Copy text to the system clipboard.

	Tries pyperclip first, then falls back to wl-copy/xclip/xsel. Returns True
	on success, False if no clipboard mechanism is available.
	"""
	try:
		pyperclip.copy(text)
		return True
	except pyperclip.PyperclipException:
		pass

	for command in _CLIPBOARD_FALLBACKS:
		if shutil.which(command[0]) is None:
			continue
		try:
			subprocess.run(command, input=text, text=True, check=True)
			return True
		except (subprocess.SubprocessError, OSError):
			continue

	return False

def open_in_mail_client(mailto_link: str) -> bool:
	"""Open a mailto: link in the default mail client.

	Uses the platform launcher: `open` (macOS), `start` (Windows), or
	`xdg-open` (Linux). Returns True on success, False if no launcher works.
	This opens a pre-filled compose window; it never sends the email.
	"""
	system = platform.system()
	if system == "Darwin":
		command = ["open", mailto_link]
	elif system == "Windows":
		# `start` is a cmd builtin; the empty title arg avoids quoting issues.
		command = ["cmd", "/c", "start", "", mailto_link]
	else:
		command = ["xdg-open", mailto_link]

	if shutil.which(command[0]) is None:
		return False
	try:
		subprocess.run(command, check=True)
		return True
	except (subprocess.SubprocessError, OSError):
		return False

def output_email(recipient_email: str, subject_final: str, body_final: str, open_client: bool = False) -> None:
	copied = copy_to_clipboard(body_final)
	mailto_link = format_mailto_link(recipient_email, subject_final, body_final)
	if copied:
		print("✓ Email body copied to clipboard")
	else:
		print("⚠ Could not copy to clipboard (install pbcopy/wl-clipboard/xclip); use the mailto link below")
	# Print the link on its own line, unwrapped, so it can be copied verbatim
	# with the mailto: scheme intact. Do not render it as a markdown hyperlink.
	print("Open in email client (copy this line):")
	print(mailto_link)
	if open_client and open_in_mail_client(mailto_link):
		print("✓ Opened in your default mail client")
