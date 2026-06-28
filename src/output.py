# [origin ref=wr-65v req=REQ-LETTER-009 c4=writing_agent_src/OutputFormatter]
#   [intent]Copies email body to clipboard and generates mailto: link for terminal output[/intent]
# [/origin]
import shutil
import subprocess
import pyperclip
from urllib.parse import urlencode, quote

# Fallback clipboard commands, tried in order when pyperclip has no backend.
# Covers Wayland (wl-copy) and X11 (xclip, xsel) so the skill works on Linux
# desktops where pyperclip cannot autodetect a copy/paste mechanism.
_CLIPBOARD_FALLBACKS = (
	["wl-copy"],
	["xclip", "-selection", "clipboard"],
	["xsel", "--clipboard", "--input"],
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

def output_email(recipient_email: str, subject_final: str, body_final: str) -> None:
	copied = copy_to_clipboard(body_final)
	mailto_link = format_mailto_link(recipient_email, subject_final, body_final)
	if copied:
		print("✓ Email body copied to clipboard")
	else:
		print("⚠ Could not copy to clipboard (install wl-clipboard or xclip); use the mailto link below")
	print(f"Open in email client: {mailto_link}")
