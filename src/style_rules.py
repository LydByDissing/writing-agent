# [origin ref=wr-65v req=REQ-LETTER-004 c4=writing_agent_src/StyleRules]
#   [intent]Defines canonical LLM marker rules and provides detection function[/intent]
# [/origin]
import re

HEDGING_OPENERS = {
	'it seems', 'it appears', 'perhaps', 'possibly', 'maybe', 'i think',
	'i believe', 'in my opinion', 'it might', 'it could', 'one could argue',
	'some might say', 'arguably', 'i would argue', 'it seems to me',
	'in my view', 'if you ask me', 'i guess', 'i suppose'
}

FILLER_CLOSINGS = {
	'looking forward to hearing from you', 'thanks again', 'thank you again',
	'best regards', 'kind regards', 'warm regards', 'sincerely', 'yours truly',
	'hope to hear from you', 'talk to you soon', 'catch you later',
	'let me know if you have any questions', 'feel free to reach out'
}

EM_DASH_PATTERN = re.compile(r'—|–|--')
BULLET_LIST_PATTERN = re.compile(r'^\s*[-*•]\s+', re.MULTILINE)
EXCLAMATION_PATTERN = re.compile(r'!')
QUESTION_MARK_PATTERN = re.compile(r'\?')

def check(body: str = '', subject: str = '') -> list[str]:
	markers = []
	if body:
		if EM_DASH_PATTERN.search(body):
			markers.append('em-dash')
		if BULLET_LIST_PATTERN.search(body):
			markers.append('bullet-list')
		hedging = _check_hedging_openers(body)
		if hedging:
			markers.append('hedging-opener')
		filler = _check_filler_closings(body)
		if filler:
			markers.append('filler-closing')
		exclamations = len(EXCLAMATION_PATTERN.findall(body))
		if exclamations > 1:
			markers.append('multiple-exclamation-marks')
		if _check_consecutive_sentence_starts(body):
			markers.append('consecutive-same-word-starts')
	if subject:
		words = subject.split()
		if len(words) > 8:
			markers.append('subject-too-long')
		if QUESTION_MARK_PATTERN.search(subject):
			markers.append('question-mark-in-subject')
	return markers

def _check_hedging_openers(body) -> bool:
	sentences = re.split(r'[.!?]\s+', body)
	for sent in sentences:
		s = sent.lower().strip()
		for opener in HEDGING_OPENERS:
			if s.startswith(opener):
				return True
	return False

def _check_filler_closings(body) -> bool:
	b = body.lower()
	for closing in FILLER_CLOSINGS:
		if closing in b:
			return True
	return False

def _check_consecutive_sentence_starts(body) -> bool:
	sentences = re.split(r'[.!?]\s+', body)
	prev_first_word = None
	for sent in sentences:
		s = sent.strip()
		if not s:
			continue
		words = s.split()
		if words:
			first_word = words[0].lower()
			if first_word == prev_first_word:
				return True
			prev_first_word = first_word
	return False
