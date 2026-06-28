# [origin ref=wr-65v req=REQ-LETTER-009 c4=writing_agent_src/OutputFormatter]
#   [intent]Copies email body to clipboard and generates mailto: link for terminal output[/intent]
# [/origin]
import pyperclip
from urllib.parse import urlencode, quote

def format_mailto_link(recipient_email: str, subject_final: str, body_final: str) -> str:
	params = {
		'subject': subject_final,
		'body': body_final
	}
	encoded = urlencode(params, quote_via=quote)
	return f"mailto:{recipient_email}?{encoded}"

def output_email(recipient_email: str, subject_final: str, body_final: str) -> None:
	pyperclip.copy(body_final)
	mailto_link = format_mailto_link(recipient_email, subject_final, body_final)
	print("✓ Email body copied to clipboard")
	print(f"Open in email client: {mailto_link}")
