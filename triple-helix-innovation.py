#!/usr/bin/env python3
"""
Triple Helix Innovation Script

This script demonstrates the Triple Helix innovation model which represents
the interaction between academia, industry, and government in knowledge-based economies.

The script displays:
- Current date and time (UTC)
- Current user login information
- Triple Helix innovation model visualization
- Objectives of the Triple Helix innovation model
"""

import datetime
import getpass
import os
import sys


def get_current_datetime_utc():
    """Get current date and time in UTC with YYYY-MM-DD HH:MM:SS format."""
    return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S")


def get_current_user():
    """Get the current user's login name."""
    try:
        return getpass.getuser()
    except Exception:
        return os.environ.get('USER', 'unknown')


def display_triple_helix_objectives():
    """Display the objectives of the Triple Helix innovation model."""
    print("\n" + "="*70)
    print("TRIPLE HELIX INNOVATION OBJECTIVES".center(70))
    print("="*70)
    print("""
    The Triple Helix model is an OBJECTIVE-BASED framework with key goals:
    
    PRIMARY OBJECTIVES:
    
    1. KNOWLEDGE GENERATION & TRANSFER
       → Facilitate continuous flow of knowledge between spheres
       → Transform academic research into practical applications
       
    2. ECONOMIC DEVELOPMENT & COMPETITIVENESS
       → Drive regional and national economic growth
       → Enhance innovation capacity and global competitiveness
       
    3. COLLABORATIVE INNOVATION ECOSYSTEM
       → Create synergies through multi-stakeholder partnerships
       → Build innovation spaces (tech parks, incubators, clusters)
       
    4. SOCIAL PROBLEM SOLVING
       → Address societal challenges through innovation
       → Ensure innovation benefits broader society
       
    5. SUSTAINABLE GROWTH
       → Balance economic, social, and environmental objectives
       → Foster long-term sustainable development
    
    The model aims to create a self-reinforcing cycle where each sphere
    contributes its unique capabilities toward shared innovation objectives.
    """)
    print("="*70)


def display_triple_helix_model():
    """Display a visual representation of the Triple Helix innovation model."""
    print("\n" + "="*70)
    print("TRIPLE HELIX INNOVATION MODEL".center(70))
    print("="*70)
    print("""
    The Triple Helix model represents the interaction between:
    
    1. ACADEMIA (Universities & Research Institutions)
       └─ Knowledge creation, research, education
       
    2. INDUSTRY (Private Sector & Business)
       └─ Innovation application, commercialization, products
       
    3. GOVERNMENT (Public Sector & Policy)
       └─ Regulation, funding, infrastructure support
    
    These three spheres work together in a dynamic relationship:
    
         ╔═══════════╗
         ║ ACADEMIA  ║
         ╚═══════════╝
              / \\
             /   \\
            /     \\
           /       \\
    ╔═══════════╗   ╔═══════════╗
    ║ INDUSTRY  ║───║ GOVERNMENT║
    ╚═══════════╝   ╚═══════════╝
    
    Innovation occurs at the intersection of all three!
    """)
    print("="*70)


def main():
    """Main function to demonstrate the script's functionality."""
    print("\n" + "="*70)
    print("TRIPLE HELIX INNOVATION - SCRIPT EXECUTION".center(70))
    print("="*70)
    
    # Display current date and time
    current_time = get_current_datetime_utc()
    print(f"\n1. Current Date and Time (UTC - YYYY-MM-DD HH:MM:SS formatted): {current_time}")
    
    # Display current user
    current_user = get_current_user()
    print(f"2. Current User's Login: {current_user}")
    print(f"3. Script Location: {os.path.abspath(__file__)}")
    
    # Display the Triple Helix model
    display_triple_helix_model()
    
    # Display the objectives of the Triple Helix model
    display_triple_helix_objectives()
    
    # Additional information
    print("\nScript execution completed successfully!")
    print(f"Python Version: {sys.version.split()[0]}")
    print("="*70 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
