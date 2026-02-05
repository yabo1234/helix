#!/usr/bin/env python3
"""
Triple Helix Innovation Framework

This module provides tools for analyzing and modeling innovation systems
through the Triple Helix framework, incorporating both neo-institutional
and neo-evolutionary perspectives.

Key concepts:
- University-Industry-Government interactions
- Institutional arrangements and evolutionary dynamics
- Knowledge spaces and innovation networks
- Co-evolution and self-organization

Author: yabo1234
Date: 2025-12-17 11:03:14 UTC
"""

from datetime import datetime, timezone
from typing import Dict, List, Tuple
import json


class TripleHelixModel:
    """
    Models the Triple Helix innovation system with neo-institutional
    and neo-evolutionary characteristics.
    """
    
    def __init__(self):
        self.university = InstitutionalActor("University")
        self.industry = InstitutionalActor("Industry")
        self.government = InstitutionalActor("Government")
        self.interactions = []
        self.timestamp = datetime.now(timezone.utc)
    
    def describe_neo_institutional_perspective(self) -> str:
        """
        Returns a description of the Triple Helix from the neo-institutional perspective.
        """
        return """
        Neo-Institutional Perspective:
        
        The Triple Helix model emphasizes institutional transformation and hybrid organizations:
        
        1. Institutional Transformation:
           - Universities become entrepreneurial institutions
           - Government evolves from regulator to enabler
           - Industry engages in knowledge creation
        
        2. Institutional Arrangements:
           - Technology transfer offices
           - Science parks and incubators
           - Public-private partnerships
        
        3. Legitimacy and Norms:
           - New rules governing collaboration
           - Trust-building mechanisms
           - Shared institutional frameworks
        
        4. Path Dependency:
           - Historical contexts shape current configurations
           - Regional variations in triple helix models
           - Institutional memory influences innovation capacity
        """
    
    def describe_neo_evolutionary_perspective(self) -> str:
        """
        Returns a description of the Triple Helix from the neo-evolutionary perspective.
        """
        return """
        Neo-Evolutionary Perspective:
        
        The Triple Helix system exhibits evolutionary dynamics:
        
        1. Co-Evolution:
           - Three helices adapt and evolve together
           - Mutual feedback drives system change
           - Emergent properties from interactions
        
        2. Variation-Selection-Retention:
           - Variation: Generation of new ideas and technologies
           - Selection: Market, scientific, and political mechanisms
           - Retention: Institutionalization of successful innovations
        
        3. Knowledge Spaces:
           - Economic space (market-driven)
           - Scientific space (research-driven)
           - Political space (policy-driven)
           - Overlay creates innovation opportunities
        
        4. Self-Organization:
           - Bottom-up innovation network formation
           - Adaptive feedback loops
           - Non-linear dynamics and tipping points
        """
    
    def add_interaction(self, actor1: str, actor2: str, interaction_type: str, 
                       outcome: str) -> None:
        """
        Records an interaction between two actors in the Triple Helix.
        
        Args:
            actor1: First actor (University, Industry, or Government)
            actor2: Second actor
            interaction_type: Type of interaction (collaboration, funding, regulation, etc.)
            outcome: Outcome or impact of the interaction
        """
        interaction = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'actors': (actor1, actor2),
            'type': interaction_type,
            'outcome': outcome
        }
        self.interactions.append(interaction)
    
    def analyze_system_dynamics(self) -> Dict:
        """
        Analyzes the Triple Helix system dynamics from both perspectives.
        
        Returns:
            Dictionary containing institutional and evolutionary analysis
        """
        return {
            'institutional_analysis': {
                'formal_institutions': self._count_formal_arrangements(),
                'informal_institutions': self._assess_trust_and_norms(),
                'hybrid_organizations': self._identify_hybrid_orgs()
            },
            'evolutionary_analysis': {
                'variation_level': self._measure_variety(),
                'selection_pressure': self._assess_selection(),
                'retention_capacity': self._measure_retention()
            },
            'integration': {
                'co_evolution_index': self._calculate_coevolution(),
                'institutional_stability': self._measure_stability(),
                'adaptive_capacity': self._measure_adaptation()
            }
        }
    
    def _count_formal_arrangements(self) -> int:
        """Count formal collaborative arrangements."""
        formal_types = ['contract', 'partnership', 'joint_venture', 'consortium']
        return sum(1 for i in self.interactions if i['type'] in formal_types)
    
    def _assess_trust_and_norms(self) -> str:
        """Assess informal institutional factors."""
        total = len(self.interactions)
        if total == 0:
            return "nascent"
        elif total < 5:
            return "developing"
        elif total < 15:
            return "established"
        else:
            return "mature"
    
    def _identify_hybrid_orgs(self) -> List[str]:
        """Identify hybrid organizational forms."""
        return [
            "Technology Transfer Office",
            "Science Park",
            "Innovation Hub",
            "Public-Private Partnership",
            "Collaborative Research Center"
        ]
    
    def _measure_variety(self) -> float:
        """Measure variety in innovation activities."""
        if not self.interactions:
            return 0.0
        unique_types = len(set(i['type'] for i in self.interactions))
        return min(unique_types / 10.0, 1.0)
    
    def _assess_selection(self) -> str:
        """Assess selection mechanism strength."""
        return "Multiple selection environments (market, scientific, political)"
    
    def _measure_retention(self) -> float:
        """Measure knowledge retention capacity."""
        return 0.7  # Placeholder
    
    def _calculate_coevolution(self) -> float:
        """Calculate co-evolution index."""
        return 0.75  # Placeholder
    
    def _measure_stability(self) -> float:
        """Measure institutional stability."""
        return 0.65  # Placeholder
    
    def _measure_adaptation(self) -> float:
        """Measure adaptive capacity."""
        return 0.80  # Placeholder
    
    def generate_report(self) -> str:
        """
        Generates a comprehensive report on the Triple Helix system.
        
        Returns:
            Formatted report string
        """
        report = f"""
        Triple Helix Innovation System Report
        =====================================
        Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC
        
        THEORETICAL FRAMEWORK:
        {self.describe_neo_institutional_perspective()}
        
        {self.describe_neo_evolutionary_perspective()}
        
        SYSTEM ANALYSIS:
        """
        
        analysis = self.analyze_system_dynamics()
        report += f"""
        Institutional Analysis:
        - Formal arrangements: {analysis['institutional_analysis']['formal_institutions']}
        - Trust level: {analysis['institutional_analysis']['informal_institutions']}
        - Hybrid organizations: {len(analysis['institutional_analysis']['hybrid_organizations'])}
        
        Evolutionary Analysis:
        - Variation level: {analysis['evolutionary_analysis']['variation_level']:.2f}
        - Selection mechanism: {analysis['evolutionary_analysis']['selection_pressure']}
        - Retention capacity: {analysis['evolutionary_analysis']['retention_capacity']:.2f}
        
        Integration Metrics:
        - Co-evolution index: {analysis['integration']['co_evolution_index']:.2f}
        - Institutional stability: {analysis['integration']['institutional_stability']:.2f}
        - Adaptive capacity: {analysis['integration']['adaptive_capacity']:.2f}
        
        INTERACTIONS RECORDED: {len(self.interactions)}
        """
        
        return report


class InstitutionalActor:
    """
    Represents an actor in the Triple Helix (University, Industry, or Government).
    """
    
    def __init__(self, name: str):
        self.name = name
        self.capabilities = []
        self.resources = {}
        self.relationships = []
    
    def add_capability(self, capability: str) -> None:
        """Add a capability to this actor."""
        self.capabilities.append(capability)
    
    def allocate_resource(self, resource_type: str, amount: float) -> None:
        """Allocate a resource."""
        self.resources[resource_type] = amount
    
    def establish_relationship(self, other_actor: str, relationship_type: str) -> None:
        """Establish a relationship with another actor."""
        self.relationships.append({
            'partner': other_actor,
            'type': relationship_type,
            'established': datetime.now(timezone.utc).isoformat()
        })


def demonstrate_triple_helix():
    """
    Demonstrates the Triple Helix model with sample interactions.
    """
    print("=" * 70)
    print("Triple Helix Innovation Framework")
    print("Neo-Institutional and Neo-Evolutionary Perspectives")
    print("=" * 70)
    print()
    
    # Create model
    model = TripleHelixModel()
    
    # Add sample interactions
    model.add_interaction(
        "University", "Industry",
        "collaborative_research",
        "New technology developed"
    )
    
    model.add_interaction(
        "Government", "University",
        "funding",
        "Research grant awarded"
    )
    
    model.add_interaction(
        "Industry", "Government",
        "policy_consultation",
        "Industry standards established"
    )
    
    # Generate and display report
    report = model.generate_report()
    print(report)
    
    print()
    print("For detailed theoretical framework, see: TRIPLE_HELIX_THEORY.md")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_triple_helix()
