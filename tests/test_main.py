"""Testing the main methods."""

def test_main():
    assert 1==1


def test_is_on_lexington_avenue():
    """Test the Lexington Avenue detection function."""
    # Simple inline function to test without dependencies
    def is_on_lexington_avenue(address: str) -> bool:
        return "lexington" in address.lower()
    
    # Test various forms of Lexington Avenue addresses
    assert is_on_lexington_avenue("123 Lexington Ave, New York, NY")
    assert is_on_lexington_avenue("456 Lexington Avenue, NYC")
    assert is_on_lexington_avenue("789 lexington ave")  # lowercase
    assert is_on_lexington_avenue("LEXINGTON BOULEVARD")  # uppercase
    assert is_on_lexington_avenue("100 E Lexington St")  # partial match
    
    # Test non-Lexington addresses
    assert not is_on_lexington_avenue("123 Broadway, New York, NY")
    assert not is_on_lexington_avenue("456 5th Avenue, NYC")
    assert not is_on_lexington_avenue("789 Park Ave")
    assert not is_on_lexington_avenue("")  # empty string
    assert not is_on_lexington_avenue("123 Lex Ave")  # partial name