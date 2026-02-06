#!/usr/bin/env python3
"""
Test script to verify the Triple Helix evolution feature.

This script tests that the chatbot correctly identifies and responds to
queries about the evolution of the Triple Helix model from metaphor to 
theory to movement.
"""

from triple_helix_engine import generate_reply


def test_evolution_intent():
    """Test that evolution-related queries trigger the correct intent."""
    test_cases = [
        "Tell me about the evolution of Triple Helix",
        "What is the history of this model?",
        "Explain the development from metaphor to theory",
        "How did Triple Helix become a movement?",
        "Origins of the Triple Helix concept",
    ]
    
    print("Testing evolution intent detection...\n")
    for query in test_cases:
        result = generate_reply(query)
        intent = result.meta['intent']
        status = "✓" if intent == "evolution" else "✗"
        print(f"{status} Query: '{query}'")
        print(f"   Intent detected: {intent}\n")
    

def test_evolution_response():
    """Test that evolution responses contain key information."""
    result = generate_reply("Tell me about the evolution from metaphor to theory to movement")
    
    print("\nTesting evolution response content...\n")
    
    required_phrases = [
        "Metaphor (1990s)",
        "Theory (Late 1990s-2000s)",
        "Movement (2010s-Present)",
        "Henry Etzkowitz and Loet Leydesdorff",
        "TRIPLE_HELIX_EVOLUTION.md",
    ]
    
    for phrase in required_phrases:
        if phrase in result.answer:
            print(f"✓ Contains: {phrase}")
        else:
            print(f"✗ Missing: {phrase}")
    
    print(f"\n--- Full Response ---\n{result.answer}\n")


def test_other_intents_unchanged():
    """Test that other intents still work correctly."""
    test_cases = [
        ("I need funding for a project", "funding"),
        ("Help me with commercialization", "commercialization"),
        ("What about policy implications?", "policy"),
        ("I want to do research", "research"),
        ("Looking for partnerships", "partnership"),
    ]
    
    print("\nTesting other intents still work...\n")
    for query, expected in test_cases:
        result = generate_reply(query)
        intent = result.meta['intent']
        status = "✓" if intent == expected else "✗"
        print(f"{status} Query: '{query}' -> {intent} (expected: {expected})")


if __name__ == "__main__":
    print("=" * 60)
    print("Triple Helix Evolution Feature Test")
    print("=" * 60)
    print()
    
    test_evolution_intent()
    test_evolution_response()
    test_other_intents_unchanged()
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)
