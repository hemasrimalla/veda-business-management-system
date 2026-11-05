"""
validators.py
-------------
Input validation helpers and interactive prompt utilities for the CLI.

Provides robust validation functions for:
- Email addresses
- Phone numbers
- Non-empty strings
- Numeric ranges (float, int)
- Categorical options and choices
- Date strings (YYYY-MM-DD)

Also includes loop-driven prompt functions that safely handle user input,
re-prompting on bad input with informative error feedback.
"""

import re
from datetime import datetime
from typing import List, Optional, Callable, Any

# Regular expression pattern for typical email formats
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

# Regular expression for phone numbers: allows optional +, digits, spaces, hyphens, and parens
# Must contain at least 7 digits and at most 15 digits
PHONE_CLEAN_REGEX = re.compile(r"[\s\-\(\)\+]")


def validate_email(email: str) -> bool:
    """Check if the provided email string matches standard email formatting.

    Args:
        email (str): The email string to test.

    Returns:
        bool: True if valid, False otherwise.
    """
    if not email or not isinstance(email, str):
        return False
    return bool(EMAIL_REGEX.match(email.strip()))


def validate_phone(phone: str) -> bool:
    """Validate phone number string.

    Accepts international and local formats containing 7 to 15 digits.
    Permits '+' prefix, hyphens, spaces, and parentheses.

    Args:
        phone (str): The phone string to test.

    Returns:
        bool: True if valid, False otherwise.
    """
    if not phone or not isinstance(phone, str):
        return False
    stripped = phone.strip()
    # Check overall character validity
    if not re.match(r"^[\+]?[0-9\s\-\(\)]{7,20}$", stripped):
        return False
    # Ensure count of numeric digits is between 7 and 15 (E.164 standard)
    digits_only = re.sub(r"\D", "", stripped)
    return 7 <= len(digits_only) <= 15


def validate_non_empty(value: str) -> bool:
    """Check if a string contains non-whitespace characters.

    Args:
        value (str): Text string.

    Returns:
        bool: True if not empty, False otherwise.
    """
    return bool(value and value.strip())


def validate_date_format(date_str: str) -> bool:
    """Check if date string matches YYYY-MM-DD and is a real calendar date.

    Args:
        date_str (str): Date formatted as string.

    Returns:
        bool: True if valid date, False otherwise.
    """
    try:
        datetime.strptime(date_str.strip(), "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False


def prompt_input(
    prompt_text: str,
    validator_fn: Optional[Callable[[str], bool]] = None,
    error_message: str = "Invalid input. Please try again.",
    allow_blank: bool = False,
    default: Optional[str] = None,
) -> str:
    """Repeatedly prompt the user until a valid string is entered.

    Args:
        prompt_text (str): Prompt display string.
        validator_fn (callable, optional): Single-argument validation function.
        error_message (str): Feedback to show on invalid input.
        allow_blank (bool): Whether empty input is accepted.
        default (str, optional): Default value if user presses Enter.

    Returns:
        str: Validated user input string.
    """
    while True:
        try:
            display_prompt = prompt_text
            if default is not None:
                display_prompt = f"{prompt_text} [{default}]: "
            else:
                display_prompt = f"{prompt_text}: "

            user_val = input(display_prompt).strip()

            if not user_val:
                if default is not None:
                    return default
                if allow_blank:
                    return ""
                print("  [!] Error: Input cannot be empty. Please enter a value.")
                continue

            if validator_fn and not validator_fn(user_val):
                print(f"  [!] Error: {error_message}")
                continue

            return user_val
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled by user.")
            raise


def prompt_float(
    prompt_text: str,
    min_val: float = 0.0,
    max_val: Optional[float] = None,
    default: Optional[float] = None,
) -> float:
    """Prompt for a valid floating-point number within an optional range.

    Args:
        prompt_text (str): Prompt text.
        min_val (float): Minimum acceptable value (inclusive).
        max_val (float, optional): Maximum acceptable value (inclusive).
        default (float, optional): Default value if user presses Enter.

    Returns:
        float: Validated float value.
    """
    while True:
        try:
            default_str = f"{default:.2f}" if default is not None else None
            val_str = prompt_input(
                prompt_text,
                allow_blank=(default is not None),
                default=default_str,
            )
            val = float(val_str)
            if val < min_val:
                print(f"  [!] Error: Value cannot be less than {min_val:.2f}.")
                continue
            if max_val is not None and val > max_val:
                print(f"  [!] Error: Value cannot exceed {max_val:.2f}.")
                continue
            return val
        except ValueError:
            print("  [!] Error: Please enter a valid decimal number.")


def prompt_int(
    prompt_text: str,
    min_val: int = 0,
    max_val: Optional[int] = None,
    default: Optional[int] = None,
) -> int:
    """Prompt for a valid integer within an optional range.

    Args:
        prompt_text (str): Prompt text.
        min_val (int): Minimum acceptable integer (inclusive).
        max_val (int, optional): Maximum acceptable integer (inclusive).
        default (int, optional): Default integer if user presses Enter.

    Returns:
        int: Validated integer.
    """
    while True:
        try:
            default_str = str(default) if default is not None else None
            val_str = prompt_input(
                prompt_text,
                allow_blank=(default is not None),
                default=default_str,
            )
            val = int(val_str)
            if val < min_val:
                print(f"  [!] Error: Value must be at least {min_val}.")
                continue
            if max_val is not None and val > max_val:
                print(f"  [!] Error: Value cannot exceed {max_val}.")
                continue
            return val
        except ValueError:
            print("  [!] Error: Please enter a valid whole number (integer).")


def prompt_choice(
    prompt_text: str,
    options: List[str],
    default: Optional[str] = None,
) -> str:
    """Display numbered options and prompt the user to choose one.

    Args:
        prompt_text (str): Instruction or heading for the choice.
        options (list): List of allowed option string choices.
        default (str, optional): Default selected option if Enter is pressed.

    Returns:
        str: Chosen option string.
    """
    print(f"\n{prompt_text}")
    for idx, opt in enumerate(options, 1):
        default_tag = " (default)" if default and opt.lower() == default.lower() else ""
        print(f"  {idx}. {opt}{default_tag}")

    while True:
        choice = input("Select an option (number or text): ").strip()
        if not choice and default:
            return default

        # Check numeric selection
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(options):
                return options[idx - 1]

        # Check text match (case-insensitive)
        for opt in options:
            if opt.lower() == choice.lower():
                return opt

        print(f"  [!] Invalid choice. Please choose between 1 and {len(options)}.")


def prompt_confirm(prompt_text: str, default_yes: bool = True) -> bool:
    """Prompt user for a yes/no confirmation.

    Args:
        prompt_text (str): Question to ask.
        default_yes (bool): If True, default is 'Y', else 'N'.

    Returns:
        bool: True for yes, False for no.
    """
    default_str = "Y/n" if default_yes else "y/N"
    while True:
        ans = input(f"{prompt_text} [{default_str}]: ").strip().lower()
        if not ans:
            return default_yes
        if ans in ["y", "yes"]:
            return True
        if ans in ["n", "no"]:
            return False
        print("  [!] Please enter 'y' for yes or 'n' for no.")
