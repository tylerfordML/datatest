import pytest
from app.service import RomanNumeralTranslateService

# -------------------------
# Fixture
# -------------------------

@pytest.fixture
def service():
    """
    Provides an instance of the Roman numeral service.

    Purpose:
    - Test core conversion logic independently from HTTP layer.
    - Ensures repeatable and isolated tests for service functionality.
    """
    return RomanNumeralTranslateService()


# -------------------------
# Unit Tests
# -------------------------

def test_min_value(service):
    """
    
    Check: Do we allow the smallest value to be a valid input (1) → 'I'
    Purpose: Ensures floor boundary is a valid range is handled correctly.
    
    """
    assert service.convert(1) == "I"


def test_max_value(service):
    """
    Check: Do we allow the max value to be a valid input (255) → 'CCLV'
    Purpose: Ensures the ceiling boundary is a valid range is handled correctly.
    
    """
    assert service.convert(255) == "CCLV"


def test_subtractive_notation(service):
    """
    
    Check: Is subtractive notation handled correctly.
    Purpose: Validates Roman numeral rules are followed.
    https://en.wikipedia.org/wiki/Roman_numerals
    
    """
    assert service.convert(2) == "II"      # Simple addition
    assert service.convert(4) == "IV"      # Subtractive: 1 before 5
    assert service.convert(9) == "IX"      # Subtractive: 1 before 10
    assert service.convert(40) == "XL"     # Subtractive: 10 before 50
    assert service.convert(90) == "XC"     # Subtractive: 10 before 100


def test_multiple_symbols(service):
    """
    
    Check: When a number requires multiple symbols, is it converted correctly.
    Purpose: Ensures the greedy algorithm correctly coalesces the Roman symbols.
    
    """
    assert service.convert(58) == "LVIII"   # L + V + III
    assert service.convert(199) == "CXCIX"  # C + XC + IX


def test_invalid_low(service):
    """
    
    Check: When a value is below the min(1) do we raise a ValueError.
    Purpose: Ensures input validation is working by preventing invalid conversions-- this case under min value.
    
    """
    with pytest.raises(ValueError):
        service.convert(0)


def test_invalid_high(service):
    """
    
    Check: When a value is above the max(255) do we raise a ValueError.
    Purpose: Ensures input validation is working by preventing invalid conversions-- this case over max value.
    
    """
    with pytest.raises(ValueError):
        service.convert(256)
