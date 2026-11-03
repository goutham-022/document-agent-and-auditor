
import re

# Industry-standard heuristic patterns targeting prompt injection & jailbreak vectors
INJECTION_PATTERNS = [
    # 1. Instruction overrides
    r"ignore\s+(all\s+)?(previous|prior|above)\s+(instructions|prompts|directives)",
    r"disregard\s+(all\s+)?(previous|prior|above)\s+(instructions|prompts|directives)",
    r"system\s*override",
    r"override\s+system\s+prompt",
    
    # 2. Persona / Role hijacking & jailbreak triggers
    r"you\s+are\s+now\s+(a|an|in)?\s*(unrestricted|dan|developer\s+mode|jailbreak)",
    r"act\s+as\s+(an?\s+)?(unrestricted|jailbroken|evil)",
    r"pretend\s+you\s+(are|have)\s+no\s+(rules|restrictions|limits)",
    
    # 3. Delimiter / Tag faking (faking system prompts)
    r"<\s*/?\s*(system|system_directive|context|instruction)\s*>",
    r"\[\s*system\s*(directive|instruction|override)?\s*\]",
    r"\[\s*inst\s*\]",
]

# Pre-compile for O(1) multi-pattern lookup performance
COMPILED_PATTERNS = [re.compile(pattern, re.IGNORECASE) for pattern in INJECTION_PATTERNS]


def detect_prompt_injection(text: str) -> bool:
    """
    Scans the given input string for known prompt injection / jailbreak patterns.
    Returns True if an adversarial pattern is detected, False otherwise.
    """
    if not text or not text.strip():
        return False

    for pattern in COMPILED_PATTERNS:
        if pattern.search(text):
            return True

    return False


# Pre-compiled regex patterns for standard PII entities
PII_PATTERNS = [
    # 1. Credit Card Numbers (13-19 digits, with optional hyphens or spaces)
    (re.compile(r"\b(?:\d{4}[-\s]?){3}\d{1,4}\b"), "[CREDIT_CARD_REDACTED]"),
    
    # 2. Email Addresses
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"), "[EMAIL_REDACTED]"),
    
    # 3. US Social Security Numbers (SSN: XXX-XX-XXXX)
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[SSN_REDACTED]"),
    
    # 4. Indian Aadhaar Numbers (12 digits: XXXX XXXX XXXX or XXXX-XXXX-XXXX)
    (re.compile(r"\b\d{4}[-\s]\d{4}[-\s]\d{4}\b"), "[AADHAAR_REDACTED]"),
    
    # 5. International & Domestic Phone Numbers
    (re.compile(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"), "[PHONE_REDACTED]"),
]


def mask_pii(text: str) -> str:
    """
    Scans the given input string and replaces sensitive PII
    (emails, phone numbers, credit cards, SSN, Aadhaar) with redaction tokens.
    """
    if not text or not text.strip():
        return text

    sanitized = text
    for pattern, replacement in PII_PATTERNS:
        sanitized = pattern.sub(replacement, sanitized)

    return sanitized