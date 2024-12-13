from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter
def safe_decimal(value):
    """Convert value to a Decimal, or return 0 if invalid."""
    try:
        return Decimal(value)
    except (InvalidOperation, TypeError, ValueError):
        return Decimal(0)