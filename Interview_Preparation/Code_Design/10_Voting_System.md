# 🗳️ PROBLEM 10: VOTING/ELECTION SYSTEM

### ⭐⭐⭐⭐ **Design Flexible Voting System with Strategy Pattern**

**Frequency:** MEDIUM at Atlassian
**Difficulty:** Medium
**Time to Solve:** 35-45 minutes
**Focus:** Strategy Pattern, Algorithm Design, Tie-Breaking

---

## 📋 Problem Statement

Design a voting/election system that can handle different voting strategies:
- **Simple Majority**: Candidate with most votes wins
- **Weighted/Ranked Choice**: 1st choice = 3pts, 2nd = 2pts, 3rd = 1pt
- **Instant Runoff (IRV)**: Eliminate lowest, redistribute votes

**Core Requirements:**
- Support multiple voting algorithms (swappable at runtime)
- Handle tie-breaking deterministically
- Prevent double voting
- Cast votes and determine winners
- Support real-time vote counting

**Constraints:**
- Each voter can vote once
- Need to support different voting methods
- Tie-breaking must be deterministic
- Algorithm can be changed after votes are cast

---

## 🎯 INTERVIEW FLOW: Step-by-Step Guide

### **PHASE 1: Clarify Requirements (2-3 minutes)**

**SAY THIS:**
> "Before I start designing, let me clarify a few requirements:"

**Questions to Ask:**
1. "What voting methods should we support?"
2. "How should we handle ties?"
3. "Should we prevent duplicate voting?"
4. "Can voters change their vote?"
5. "Do we need real-time results?"
6. "Should ballots support ranked choices?"

**WRITE DOWN the answers. This shows you're thorough.**

---

### **PHASE 2: Identify the Design Pattern (2-3 minutes)**

**SAY THIS:**
> "This is a PERFECT use case for the Strategy Pattern. Let me explain why."

#### **Why Strategy Pattern?**

```text
┌────────────────────────────────────────────────────────────────┐
│                   THE PROBLEM WITHOUT STRATEGY                  │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  def determine_winner(self, method):                           │
│      if method == "majority":                                  │
│          # 50 lines of majority logic                          │
│      elif method == "ranked":                                  │
│          # 50 lines of ranked choice logic                     │
│      elif method == "runoff":                                  │
│          # 50 lines of runoff logic                            │
│      elif method == "approval":                                │
│          # Adding new method? Modify this giant if/else!       │
│                                                                 │
│  PROBLEMS:                                                      │
│  ❌ Violates Open/Closed Principle (OCP)                       │
│  ❌ Single function becomes enormous                            │
│  ❌ Hard to test individual algorithms                          │
│  ❌ Hard to add new voting methods                              │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│                   THE SOLUTION WITH STRATEGY                    │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────┐                       │
│  │      VotingStrategy (Abstract)      │ ← Interface           │
│  │  + determine_winner() → str         │                       │
│  │  + get_results() → Dict             │                       │
│  └─────────────────────────────────────┘                       │
│                  △                                              │
│      ┌───────────┼───────────┐                                  │
│      │           │           │                                  │
│  ┌───────┐  ┌────────┐  ┌─────────┐                            │
│  │Simple │  │Ranked  │  │Instant  │  ← Concrete Strategies     │
│  │Majority│  │Choice  │  │Runoff   │                            │
│  └───────┘  └────────┘  └─────────┘                            │
│                                                                 │
│  BENEFITS:                                                      │
│  ✅ Add new algorithm without touching existing code (OCP)     │
│  ✅ Each algorithm isolated and testable                        │
│  ✅ Runtime swapping: see results under different methods       │
│  ✅ Clean, maintainable code                                    │
└────────────────────────────────────────────────────────────────┘
```

**Real-World Examples:**
> "Strategy Pattern is used everywhere:
> - Java's `Comparator` for sorting strategies
> - Payment processors (Credit Card, PayPal, Crypto)
> - Compression algorithms (ZIP, GZIP, LZ4)
> - Our voting algorithms are exactly the same concept!"

---

### **PHASE 3: High-Level Design (3-4 minutes)**

**SAY THIS:**
> "Let me draw the complete class structure."

```text
┌─────────────────────────────────────────────────────────────────┐
│                      ElectionManager                             │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  Context class - uses Strategy without knowing details     │ │
│  │                                                             │ │
│  │  - election_id: str                                        │ │
│  │  - candidates: List[str]                                   │ │
│  │  - ballots: List[Ballot]                                   │ │
│  │  - voter_ids: Set[str]         ← Prevent double voting    │ │
│  │  - strategy: VotingStrategy    ← THE STRATEGY              │ │
│  │  - tie_breaker: TieBreaker     ← Another Strategy!         │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                  │
│  + cast_vote(ballot) → bool       Validates & stores           │
│  + get_winner() → str             Delegates to strategy        │
│  + get_results() → Dict           Delegates to strategy        │
│  + change_strategy(new_strategy)  Runtime swap!                │
└─────────────────────────────────────────────────────────────────┘
            │
            │ uses
            ▼
┌─────────────────────────────────────────────────────────────────┐
│                  VotingStrategy (Abstract)                       │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  @abstractmethod                                            │ │
│  │  def determine_winner(ballots, candidates) → str            │ │
│  │                                                             │ │
│  │  @abstractmethod                                            │ │
│  │  def get_results(ballots, candidates) → Dict                │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
            △
            │ implements
    ┌───────┼───────────────────┐
    │       │                   │
┌───────────┐ ┌──────────────┐ ┌────────────────┐
│  Simple   │ │   Weighted   │ │    Instant     │
│  Majority │ │  RankedChoice│ │    Runoff      │
│           │ │              │ │                │
│ Count 1st │ │ 1st=3, 2nd=2 │ │ Eliminate low  │
│ choice    │ │ 3rd=1 points │ │ redistribute   │
└───────────┘ └──────────────┘ └────────────────┘

┌─────────────────────┐
│       Ballot        │
├─────────────────────┤
│ - voter_id: str     │
│ - ranked_choices:   │
│   List[str]         │ ← Supports all strategies!
│ - timestamp         │
└─────────────────────┘
```

**Key Design Decision - Ballot Format:**
> "I design the Ballot to store RANKED CHOICES even for simple majority.
> This allows us to switch voting methods without re-voting!
> Simple majority just uses the first choice, ranked uses all."

---

### **PHASE 4: Design Patterns & WHY We Use Them (3-4 minutes)**

#### **Pattern 1: Strategy Pattern** ⭐⭐⭐⭐⭐

```python
from abc import ABC, abstractmethod

class VotingStrategy(ABC):
    """
    Strategy interface - defines the algorithm contract.
    
    All concrete strategies MUST implement these methods.
    The ElectionManager doesn't know WHICH strategy it's using.
    """
    
    @abstractmethod
    def determine_winner(self, ballots: List[Ballot], 
                        candidates: List[str]) -> Optional[str]:
        """Determine winner. Strategy-specific logic."""
        pass
    
    @abstractmethod
    def get_results(self, ballots: List[Ballot], 
                   candidates: List[str]) -> Dict[str, int]:
        """Get detailed results. Strategy-specific format."""
        pass
```

**WHY Strategy Pattern?**

| Aspect | Without Strategy | With Strategy |
|--------|------------------|---------------|
| Adding new algorithm | Modify existing code | Add new class |
| Testing | Test entire system | Test algorithm in isolation |
| Code organization | One giant method | Separate focused classes |
| Runtime flexibility | Hardcoded | Swappable at runtime |
| Open/Closed Principle | ❌ Violated | ✅ Respected |

---

#### **Pattern 2: Factory Pattern** ⭐⭐⭐

```python
class ElectionFactory:
    """
    Factory Pattern - create elections with preset configurations.
    
    WHY FACTORY?
    - Encapsulate complex object creation
    - Ensure valid configurations
    - Single place to modify defaults
    """
    
    @staticmethod
    def create_simple_majority(election_id: str, 
                               candidates: List[str]) -> ElectionManager:
        return ElectionManager(
            election_id=election_id,
            candidates=candidates,
            strategy=SimpleMajorityStrategy()
        )
    
    @staticmethod
    def create_instant_runoff(election_id: str, 
                              candidates: List[str]) -> ElectionManager:
        return ElectionManager(
            election_id=election_id,
            candidates=candidates,
            strategy=InstantRunoffStrategy()
        )
```

**WHY Factory?**
> "Instead of client doing:
> `election = ElectionManager(id, candidates, SimpleMajorityStrategy(), AlphabeticalTieBreaker())`
>
> They just call:
> `election = ElectionFactory.create_simple_majority(id, candidates)`
>
> Factory hides complexity and ensures valid configurations."

---

#### **Pattern 3: Strategy for Tie-Breaking** ⭐⭐

```python
class TieBreaker(ABC):
    """
    Another Strategy! Tie-breaking is also pluggable.
    
    Different tie-break methods:
    - Alphabetical (deterministic)
    - Random (non-deterministic)
    - First vote received (temporal)
    """
    
    @abstractmethod
    def break_tie(self, tied_candidates: List[str]) -> str:
        pass
```

**WHY Separate TieBreaker?**
> "Tie-breaking is orthogonal to voting method.
> You might want:
> - Simple majority + alphabetical tie-break
> - Simple majority + random tie-break
>
> By making TieBreaker a separate strategy, we can mix and match!"

---

### **PHASE 5: Data Structures & Why (2 minutes)**

| Data Structure | Used For | Why This Choice |
|----------------|----------|-----------------|
| `List[Ballot]` | Store votes | Ordered by time, supports iteration |
| `Set[str]` | Voted users | O(1) duplicate check |
| `List[str]` | Ranked choices | Ordered preferences |
| `Dict[str, int]` | Vote counts | O(1) lookup and update |
| `Enum` | N/A here | Could use for candidate status |
| `dataclass` | Ballot, Candidate | Clean data containers |

**Key Insight - Ballot Design:**
> "Ballots store `ranked_choices: List[str]` not just one choice.
> For simple majority: use `ranked_choices[0]`
> For ranked choice: use all with weights
> For instant runoff: redistribute based on preferences
>
> One ballot format supports ALL strategies!"

---

### **PHASE 6: Write the Code (15-20 minutes)**

```python
"""
Voting/Election System with Strategy Pattern
=============================================
Flexible voting system supporting multiple counting algorithms.

Design Patterns:
- Strategy Pattern: Swappable voting algorithms
- Factory Pattern: Election creation with presets
- Strategy Pattern (again): Pluggable tie-breakers

Real-World Algorithms:
- Simple Majority: Most common, used in most elections
- Borda Count (Weighted): Used in sports polls, Eurovision
- Instant Runoff: Used in Australian elections, Oscar voting

Time Complexity: Varies by strategy (see each class)
Space Complexity: O(V × C) where V = voters, C = candidates
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional
from collections import defaultdict
from datetime import datetime


# ============ Data Classes ============

@dataclass
class Ballot:
    """
    A voter's ballot with ranked preferences.
    
    Design Decision: Store ranked choices even for simple majority.
    This allows switching voting methods without re-voting!
    
    Example:
        Ballot("voter1", ["Alice", "Bob", "Charlie"])
        - For majority: only Alice (first choice) counts
        - For ranked: Alice=3pts, Bob=2pts, Charlie=1pt
        - For runoff: if Alice eliminated, vote goes to Bob
    """
    voter_id: str
    ranked_choices: List[str]
    timestamp: datetime = field(default_factory=datetime.now)
    
    @property
    def first_choice(self) -> Optional[str]:
        """Get top choice (for simple majority)."""
        return self.ranked_choices[0] if self.ranked_choices else None
    
    def get_choice(self, rank: int) -> Optional[str]:
        """Get choice at specific rank (0-indexed)."""
        if 0 <= rank < len(self.ranked_choices):
            return self.ranked_choices[rank]
        return None


# ============ Strategy Pattern: Voting Algorithms ============

class VotingStrategy(ABC):
    """
    Abstract Strategy for vote counting algorithms.
    
    This is the KEY abstraction:
    - ElectionManager uses this interface
    - It doesn't know which concrete strategy is used
    - New strategies can be added without changing ElectionManager
    
    SOLID Principle: Open/Closed
    - Open for extension (add new strategies)
    - Closed for modification (don't change existing code)
    """
    
    @abstractmethod
    def determine_winner(self, ballots: List[Ballot], 
                        candidates: List[str]) -> Optional[str]:
        """
        Determine the winner using this strategy's algorithm.
        
        Args:
            ballots: All cast ballots
            candidates: List of candidate IDs
            
        Returns:
            Winner's ID, or None if no winner
        """
        pass
    
    @abstractmethod
    def get_results(self, ballots: List[Ballot], 
                   candidates: List[str]) -> Dict[str, int]:
        """
        Get detailed results (scores/votes per candidate).
        
        Returns format depends on strategy:
        - Majority: {"Alice": 5, "Bob": 3} (vote counts)
        - Ranked: {"Alice": 15, "Bob": 10} (point totals)
        """
        pass


class SimpleMajorityStrategy(VotingStrategy):
    """
    Simple plurality voting - most first-choice votes wins.
    
    Algorithm: Count first choices, highest count wins.
    
    Time: O(V) where V = number of ballots
    Space: O(C) where C = number of candidates
    
    Real-World Use: Most elections worldwide
    
    Example:
        3 voters: [Alice], [Alice], [Bob]
        Result: Alice wins with 2 votes (67%)
    """
    
    def determine_winner(self, ballots: List[Ballot], 
                        candidates: List[str]) -> Optional[str]:
        results = self.get_results(ballots, candidates)
        
        if not results:
            return None
        
        # Find max votes
        max_votes = max(results.values())
        winners = [c for c, v in results.items() if v == max_votes]
        
        # Tie-breaker: alphabetical (deterministic)
        return min(winners) if winners else None
    
    def get_results(self, ballots: List[Ballot], 
                   candidates: List[str]) -> Dict[str, int]:
        """Count first-choice votes."""
        vote_count = {c: 0 for c in candidates}
        
        for ballot in ballots:
            choice = ballot.first_choice
            if choice and choice in vote_count:
                vote_count[choice] += 1
        
        return vote_count


class WeightedRankedChoiceStrategy(VotingStrategy):
    """
    Ranked choice with point values (Borda Count variant).
    Default: 1st = 3pts, 2nd = 2pts, 3rd = 1pt
    
    Algorithm: Assign points based on rank position.
    
    Time: O(V × R) where V = ballots, R = ranks considered
    Space: O(C)
    
    Real-World Use: 
    - AP College Football Poll
    - Eurovision Song Contest
    - MVP voting in sports
    
    Example:
        Voter 1: [Alice, Bob, Charlie] → Alice:3, Bob:2, Charlie:1
        Voter 2: [Bob, Alice, Charlie] → Bob:3, Alice:2, Charlie:1
        Total: Alice:5, Bob:5, Charlie:2
    """
    
    def __init__(self, weights: List[int] = None):
        """
        Args:
            weights: Points for each rank position.
                     Default [3, 2, 1] for top 3.
        """
        self.weights = weights or [3, 2, 1]
    
    def determine_winner(self, ballots: List[Ballot], 
                        candidates: List[str]) -> Optional[str]:
        results = self.get_results(ballots, candidates)
        
        if not results:
            return None
        
        max_points = max(results.values())
        winners = [c for c, p in results.items() if p == max_points]
        
        return min(winners) if winners else None
    
    def get_results(self, ballots: List[Ballot], 
                   candidates: List[str]) -> Dict[str, int]:
        """Calculate points for each candidate."""
        points = {c: 0 for c in candidates}
        
        for ballot in ballots:
            for rank, candidate_id in enumerate(ballot.ranked_choices):
                if rank >= len(self.weights):
                    break  # Only count up to weight list length
                
                if candidate_id in points:
                    points[candidate_id] += self.weights[rank]
        
        return points


class InstantRunoffStrategy(VotingStrategy):
    """
    Instant Runoff Voting (IRV) / Ranked Choice Voting.
    
    Algorithm:
    1. Count first-choice votes
    2. If someone has majority (>50%), they win
    3. Otherwise, eliminate candidate with fewest votes
    4. Redistribute their votes to next choices
    5. Repeat until someone has majority
    
    Time: O(C × V) where C = candidates, V = ballots
    Space: O(C + V)
    
    Real-World Use:
    - Australian House of Representatives
    - Academy Awards (Best Picture)
    - San Francisco mayoral elections
    
    Example:
        Round 1: Alice(2), Bob(2), Charlie(1)
                 No majority, Charlie eliminated
        Round 2: Charlie's voter's 2nd choice was Bob
                 Alice(2), Bob(3)
                 Bob wins with majority!
    """
    
    def determine_winner(self, ballots: List[Ballot], 
                        candidates: List[str]) -> Optional[str]:
        remaining = set(candidates)
        active_ballots = list(ballots)
        
        while len(remaining) > 1:
            # Count first-choice votes among remaining candidates
            vote_count = self._count_votes(active_ballots, remaining)
            total_votes = sum(vote_count.values())
            
            if total_votes == 0:
                return None
            
            # Check for majority (> 50%)
            for candidate, votes in vote_count.items():
                if votes > total_votes / 2:
                    return candidate
            
            # Find and eliminate candidate with fewest votes
            min_votes = min(vote_count.values())
            losers = [c for c, v in vote_count.items() if v == min_votes]
            
            # Tie-breaker for elimination: alphabetical
            loser = min(losers)
            remaining.remove(loser)
            # Ballots automatically redistribute (next valid choice)
        
        return remaining.pop() if remaining else None
    
    def _count_votes(self, ballots: List[Ballot], 
                    remaining: Set[str]) -> Dict[str, int]:
        """Count first valid choice for each ballot."""
        vote_count = {c: 0 for c in remaining}
        
        for ballot in ballots:
            choice = self._get_first_remaining_choice(ballot, remaining)
            if choice:
                vote_count[choice] += 1
        
        return vote_count
    
    def _get_first_remaining_choice(self, ballot: Ballot, 
                                   remaining: Set[str]) -> Optional[str]:
        """Get voter's top choice among remaining candidates."""
        for choice in ballot.ranked_choices:
            if choice in remaining:
                return choice
        return None
    
    def get_results(self, ballots: List[Ballot], 
                   candidates: List[str]) -> Dict[str, int]:
        """Return first-round results."""
        return self._count_votes(ballots, set(candidates))


# ============ Strategy Pattern: Tie-Breakers ============

class TieBreaker(ABC):
    """
    Strategy for breaking ties.
    
    Tie-breaking is separate from voting method because:
    - Different elections may want different tie-break rules
    - Same voting method can use different tie-breakers
    """
    
    @abstractmethod
    def break_tie(self, tied_candidates: List[str]) -> str:
        pass


class AlphabeticalTieBreaker(TieBreaker):
    """Break ties alphabetically (deterministic, reproducible)."""
    
    def break_tie(self, tied_candidates: List[str]) -> str:
        return min(tied_candidates)


class RandomTieBreaker(TieBreaker):
    """Break ties randomly (non-deterministic)."""
    
    def break_tie(self, tied_candidates: List[str]) -> str:
        import random
        return random.choice(tied_candidates)


class FirstVoteTieBreaker(TieBreaker):
    """Winner is whoever received a vote first."""
    
    def __init__(self, ballots: List[Ballot]):
        self.vote_order = {}
        for i, ballot in enumerate(ballots):
            if ballot.first_choice not in self.vote_order:
                self.vote_order[ballot.first_choice] = i
    
    def break_tie(self, tied_candidates: List[str]) -> str:
        return min(tied_candidates, 
                  key=lambda c: self.vote_order.get(c, float('inf')))


# ============ Election Manager (Context) ============

class ElectionManager:
    """
    Manages an election with configurable voting strategy.
    
    This is the CONTEXT in Strategy Pattern:
    - Holds reference to Strategy interface
    - Delegates algorithm execution to strategy
    - Doesn't know which concrete strategy is used
    
    Responsibilities:
    - Validate and store ballots
    - Prevent duplicate voting
    - Delegate winner determination to strategy
    - Support runtime strategy switching
    
    Thread Safety Note:
    - Not thread-safe as-is
    - For production: use locks around ballot operations
    """
    
    def __init__(self, election_id: str, candidates: List[str],
                 strategy: VotingStrategy,
                 tie_breaker: TieBreaker = None):
        """
        Initialize election.
        
        Args:
            election_id: Unique election identifier
            candidates: List of candidate IDs
            strategy: Voting algorithm to use
            tie_breaker: Optional tie-break strategy
        """
        self.election_id = election_id
        self.candidates = list(candidates)
        self.strategy = strategy
        self.tie_breaker = tie_breaker or AlphabeticalTieBreaker()
        
        self._ballots: List[Ballot] = []
        self._voter_ids: Set[str] = set()  # Prevent double voting
        self._is_closed = False
    
    def cast_vote(self, ballot: Ballot) -> bool:
        """
        Cast a vote.
        
        Validations:
        1. Election not closed
        2. Voter hasn't already voted
        3. All choices are valid candidates
        
        Returns: True if vote accepted, False if rejected
        """
        if self._is_closed:
            return False
        
        # Check for duplicate voting
        if ballot.voter_id in self._voter_ids:
            return False
        
        # Validate all candidates exist
        for choice in ballot.ranked_choices:
            if choice not in self.candidates:
                raise ValueError(f"Invalid candidate: {choice}")
        
        self._ballots.append(ballot)
        self._voter_ids.add(ballot.voter_id)
        return True
    
    def get_winner(self) -> Optional[str]:
        """
        Determine winner using current strategy.
        
        The strategy does the actual work!
        """
        if not self._ballots:
            return None
        
        return self.strategy.determine_winner(self._ballots, self.candidates)
    
    def get_results(self) -> Dict[str, int]:
        """Get current results from strategy."""
        return self.strategy.get_results(self._ballots, self.candidates)
    
    def change_strategy(self, new_strategy: VotingStrategy) -> None:
        """
        Change voting strategy at runtime!
        
        This is powerful:
        - See how results differ under various methods
        - No re-voting needed
        - Ballots already contain ranked preferences
        """
        self.strategy = new_strategy
    
    def close_election(self) -> None:
        """Close election to new votes."""
        self._is_closed = True
    
    @property
    def total_votes(self) -> int:
        """Get total number of votes cast."""
        return len(self._ballots)
    
    def get_statistics(self) -> Dict:
        """Get election statistics."""
        return {
            "election_id": self.election_id,
            "total_votes": len(self._ballots),
            "candidates": len(self.candidates),
            "is_closed": self._is_closed,
            "strategy": type(self.strategy).__name__,
        }


# ============ Factory Pattern ============

class ElectionFactory:
    """
    Factory for creating elections with common configurations.
    
    Why Factory?
    - Hide complexity of object creation
    - Ensure valid combinations
    - Single place to change defaults
    """
    
    @staticmethod
    def create_simple_majority(election_id: str, 
                               candidates: List[str]) -> ElectionManager:
        """Create election with simple majority voting."""
        return ElectionManager(
            election_id=election_id,
            candidates=candidates,
            strategy=SimpleMajorityStrategy()
        )
    
    @staticmethod
    def create_ranked_choice(election_id: str, candidates: List[str],
                            weights: List[int] = None) -> ElectionManager:
        """Create election with weighted ranked choice."""
        return ElectionManager(
            election_id=election_id,
            candidates=candidates,
            strategy=WeightedRankedChoiceStrategy(weights)
        )
    
    @staticmethod
    def create_instant_runoff(election_id: str, 
                              candidates: List[str]) -> ElectionManager:
        """Create election with instant runoff voting."""
        return ElectionManager(
            election_id=election_id,
            candidates=candidates,
            strategy=InstantRunoffStrategy()
        )


# ============ Demo ============

def main():
    """Demonstrate voting system with different strategies."""
    print("=" * 60)
    print("VOTING SYSTEM DEMO - Strategy Pattern")
    print("=" * 60)
    
    candidates = ["Alice", "Bob", "Charlie"]
    
    # ===== Test 1: Simple Majority =====
    print("\n" + "=" * 50)
    print("TEST 1: Simple Majority")
    print("=" * 50)
    
    election1 = ElectionFactory.create_simple_majority("E1", candidates)
    
    election1.cast_vote(Ballot("V1", ["Alice"]))
    election1.cast_vote(Ballot("V2", ["Bob"]))
    election1.cast_vote(Ballot("V3", ["Alice"]))
    election1.cast_vote(Ballot("V4", ["Charlie"]))
    election1.cast_vote(Ballot("V5", ["Alice"]))
    
    print(f"Results: {election1.get_results()}")
    print(f"Winner: {election1.get_winner()}")
    
    # Test duplicate vote prevention
    result = election1.cast_vote(Ballot("V1", ["Bob"]))
    print(f"Duplicate vote accepted? {result}")  # Should be False
    
    # ===== Test 2: Weighted Ranked Choice =====
    print("\n" + "=" * 50)
    print("TEST 2: Weighted Ranked Choice (3-2-1 points)")
    print("=" * 50)
    
    election2 = ElectionFactory.create_ranked_choice("E2", candidates)
    
    election2.cast_vote(Ballot("V1", ["Alice", "Bob", "Charlie"]))
    election2.cast_vote(Ballot("V2", ["Bob", "Alice", "Charlie"]))
    election2.cast_vote(Ballot("V3", ["Alice", "Charlie", "Bob"]))
    
    print("Ballots:")
    print("  V1: Alice(3) > Bob(2) > Charlie(1)")
    print("  V2: Bob(3) > Alice(2) > Charlie(1)")
    print("  V3: Alice(3) > Charlie(2) > Bob(1)")
    print(f"Points: {election2.get_results()}")
    print(f"Winner: {election2.get_winner()}")
    
    # ===== Test 3: Instant Runoff =====
    print("\n" + "=" * 50)
    print("TEST 3: Instant Runoff Voting")
    print("=" * 50)
    
    election3 = ElectionFactory.create_instant_runoff("E3", candidates)
    
    # Scenario: Alice leads but loses after redistribution
    election3.cast_vote(Ballot("V1", ["Alice", "Bob", "Charlie"]))
    election3.cast_vote(Ballot("V2", ["Alice", "Bob", "Charlie"]))
    election3.cast_vote(Ballot("V3", ["Bob", "Charlie", "Alice"]))
    election3.cast_vote(Ballot("V4", ["Bob", "Charlie", "Alice"]))
    election3.cast_vote(Ballot("V5", ["Charlie", "Bob", "Alice"]))
    
    print(f"First round: {election3.get_results()}")
    print(f"Winner after runoff: {election3.get_winner()}")
    print("(Charlie eliminated, vote transferred to Bob)")
    
    # ===== Test 4: Strategy Switching =====
    print("\n" + "=" * 50)
    print("TEST 4: Same Votes, Different Strategies")
    print("=" * 50)
    
    election4 = ElectionManager("E4", candidates, SimpleMajorityStrategy())
    
    for ballot in [
        Ballot("V1", ["Alice", "Bob", "Charlie"]),
        Ballot("V2", ["Bob", "Alice", "Charlie"]),
        Ballot("V3", ["Charlie", "Bob", "Alice"]),
    ]:
        election4.cast_vote(ballot)
    
    print(f"Simple Majority Winner: {election4.get_winner()}")
    
    election4.change_strategy(WeightedRankedChoiceStrategy([3, 2, 1]))
    print(f"Ranked Choice Winner: {election4.get_winner()}")
    
    election4.change_strategy(InstantRunoffStrategy())
    print(f"Instant Runoff Winner: {election4.get_winner()}")
    
    print("\n" + "=" * 50)
    print("Statistics:", election4.get_statistics())


if __name__ == "__main__":
    main()
```

---

### **PHASE 7: Walk Through Edge Cases (3-4 minutes)**

| Edge Case | How Handled | Code Location |
|-----------|-------------|---------------|
| **Double voting** | Track voter_ids in Set | `cast_vote()` check |
| **Invalid candidate** | Raise ValueError | `cast_vote()` validation |
| **Tie** | Alphabetical tie-breaker | `determine_winner()` |
| **No votes** | Return None | `get_winner()` check |
| **Election closed** | Return False on cast_vote | `cast_vote()` check |
| **Empty ballot** | first_choice returns None | `Ballot.first_choice` |
| **Partial rankings** | Only count available ranks | Strategy implementations |

**Tie-Breaking is CRITICAL:**
> "ALWAYS ask the interviewer how to handle ties!
> Common options:
> - Alphabetical (deterministic, reproducible)
> - Random (fair but non-reproducible)
> - First vote received (rewards early supporters)
> 
> I default to alphabetical because it's deterministic."

---

### **PHASE 8: Testing Strategy (2-3 minutes)**

```python
import pytest

class TestVotingSystem:
    
    def test_simple_majority_basic(self):
        """Candidate with most votes wins."""
        election = ElectionFactory.create_simple_majority("E1", ["A", "B"])
        
        election.cast_vote(Ballot("V1", ["A"]))
        election.cast_vote(Ballot("V2", ["A"]))
        election.cast_vote(Ballot("V3", ["B"]))
        
        assert election.get_winner() == "A"
        assert election.get_results() == {"A": 2, "B": 1}
    
    def test_ranked_choice_points(self):
        """Ranked choice calculates points correctly."""
        election = ElectionFactory.create_ranked_choice("E1", ["A", "B", "C"])
        
        election.cast_vote(Ballot("V1", ["A", "B", "C"]))
        # A gets 3, B gets 2, C gets 1
        
        results = election.get_results()
        assert results["A"] == 3
        assert results["B"] == 2
        assert results["C"] == 1
    
    def test_instant_runoff_redistribution(self):
        """Votes redistribute when candidate eliminated."""
        election = ElectionFactory.create_instant_runoff("E1", ["A", "B", "C"])
        
        # Round 1: A=2, B=2, C=1 → C eliminated
        # Round 2: C's voter's 2nd choice is B → A=2, B=3 → B wins
        election.cast_vote(Ballot("V1", ["A", "B", "C"]))
        election.cast_vote(Ballot("V2", ["A", "B", "C"]))
        election.cast_vote(Ballot("V3", ["B", "A", "C"]))
        election.cast_vote(Ballot("V4", ["B", "A", "C"]))
        election.cast_vote(Ballot("V5", ["C", "B", "A"]))  # Redistributes to B
        
        assert election.get_winner() == "B"
    
    def test_duplicate_vote_rejected(self):
        """Same voter cannot vote twice."""
        election = ElectionFactory.create_simple_majority("E1", ["A", "B"])
        
        assert election.cast_vote(Ballot("V1", ["A"])) == True
        assert election.cast_vote(Ballot("V1", ["B"])) == False  # Rejected
        
        assert election.total_votes == 1
    
    def test_invalid_candidate_raises(self):
        """Voting for non-existent candidate raises error."""
        election = ElectionFactory.create_simple_majority("E1", ["A", "B"])
        
        with pytest.raises(ValueError):
            election.cast_vote(Ballot("V1", ["Z"]))  # Z not a candidate
    
    def test_strategy_switch(self):
        """Can switch strategies and get different results."""
        election = ElectionManager("E1", ["A", "B"], SimpleMajorityStrategy())
        
        election.cast_vote(Ballot("V1", ["A", "B"]))
        election.cast_vote(Ballot("V2", ["B", "A"]))
        
        # Tie in simple majority
        winner1 = election.get_winner()  # "A" (alphabetical tie-break)
        
        election.change_strategy(WeightedRankedChoiceStrategy([3, 2, 1]))
        # A: 3+2=5, B: 2+3=5 → Still tie
        winner2 = election.get_winner()  # "A" (alphabetical tie-break)
        
        assert winner1 == winner2  # Both "A" due to tie-break
    
    def test_tie_alphabetical(self):
        """Ties broken alphabetically."""
        election = ElectionFactory.create_simple_majority("E1", ["Bob", "Alice"])
        
        election.cast_vote(Ballot("V1", ["Bob"]))
        election.cast_vote(Ballot("V2", ["Alice"]))
        
        # Tie: Alice wins alphabetically
        assert election.get_winner() == "Alice"
```

---

### **PHASE 9: Complexity Analysis (1 minute)**

| Strategy | Time | Space |
|----------|------|-------|
| Simple Majority | **O(V)** | O(C) |
| Weighted Ranked | O(V × R) | O(C) |
| Instant Runoff | O(C × V) | O(C + V) |

**Where:** V = votes, C = candidates, R = ranks per ballot

**Why Instant Runoff is slower:**
> "Instant Runoff may need C rounds, each scanning all V ballots.
> Simple Majority is just one pass through all ballots.
> For large elections, consider Simple Majority first!"

---

### **PHASE 10: Extensions & Follow-ups (5+ minutes)**

#### **Q1: "How would you add real-time results?"**

```python
class ObservableElection(ElectionManager):
    """
    Observer Pattern for real-time result updates.
    
    When a vote is cast, all observers are notified.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._observers = []
    
    def add_observer(self, callback):
        """Register a callback for vote events."""
        self._observers.append(callback)
    
    def cast_vote(self, ballot: Ballot) -> bool:
        result = super().cast_vote(ballot)
        if result:
            # Notify all observers
            for observer in self._observers:
                observer(self.get_results())
        return result

# Usage
election = ObservableElection("E1", candidates, SimpleMajorityStrategy())
election.add_observer(lambda r: print(f"Live results: {r}"))
```

---

#### **Q2: "How would you add approval voting?"**

```python
class ApprovalVotingStrategy(VotingStrategy):
    """
    Approval Voting: Vote for as many candidates as you like.
    Candidate with most approvals wins.
    
    Ballot format: ranked_choices = all approved candidates
    """
    
    def determine_winner(self, ballots, candidates):
        results = self.get_results(ballots, candidates)
        max_approvals = max(results.values())
        winners = [c for c, v in results.items() if v == max_approvals]
        return min(winners)
    
    def get_results(self, ballots, candidates):
        approvals = {c: 0 for c in candidates}
        for ballot in ballots:
            for choice in ballot.ranked_choices:
                if choice in approvals:
                    approvals[choice] += 1
        return approvals
```

---

#### **Q3: "How would you make this distributed?"**

```python
class DistributedElection:
    """
    Voting across multiple regions with eventual consistency.
    
    Each region has local election, results merged.
    """
    
    def __init__(self, election_id: str, candidates: List[str]):
        self.election_id = election_id
        self.candidates = candidates
        self.regional_results: Dict[str, Dict[str, int]] = {}
    
    def add_regional_result(self, region: str, results: Dict[str, int]):
        """Add results from a region."""
        self.regional_results[region] = results
    
    def get_merged_results(self) -> Dict[str, int]:
        """Merge results from all regions."""
        merged = {c: 0 for c in self.candidates}
        for region_results in self.regional_results.values():
            for candidate, votes in region_results.items():
                merged[candidate] += votes
        return merged
```

---

## ❌ Common Mistakes (What NOT to Do)

### **MISTAKE 1: Giant If-Else Instead of Strategy** ❌

```python
# WRONG - Violates Open/Closed Principle!
def determine_winner(self, method):
    if method == "majority":
        # 50 lines...
    elif method == "ranked":
        # 50 lines...
    elif method == "runoff":
        # 50 lines...
    # Adding new method = modifying this code!

# CORRECT - Strategy Pattern
def determine_winner(self):
    return self.strategy.determine_winner(self.ballots, self.candidates)
    # Adding new method = just create new Strategy class!
```

---

### **MISTAKE 2: No Tie-Breaking Discussion** ❌

```python
# WRONG - What if Alice and Bob both have 5 votes?
def get_winner(self):
    max_votes = max(results.values())
    winners = [c for c, v in results.items() if v == max_votes]
    return winners[0]  # Non-deterministic! Dict order varies!

# CORRECT - Deterministic tie-break
def get_winner(self):
    max_votes = max(results.values())
    winners = [c for c, v in results.items() if v == max_votes]
    return min(winners)  # Alphabetical, deterministic
```

---

### **MISTAKE 3: Allowing Duplicate Votes** ❌

```python
# WRONG - No duplicate check!
def cast_vote(self, ballot):
    self.ballots.append(ballot)  # Same voter can vote 100 times!

# CORRECT - Track voters
def cast_vote(self, ballot):
    if ballot.voter_id in self._voter_ids:
        return False  # Already voted
    self._voter_ids.add(ballot.voter_id)
    self._ballots.append(ballot)
    return True
```

---

## 💯 Interview Checklist

- [ ] ✅ **Identified Strategy Pattern** as core design
- [ ] ✅ **Explained WHY Strategy** (OCP, testability, flexibility)
- [ ] ✅ **Drew class diagram** with Context and Strategies
- [ ] ✅ **Designed universal Ballot** (ranked choices support all methods)
- [ ] ✅ **Implemented 3+ strategies** (Majority, Ranked, Runoff)
- [ ] ✅ **Prevented duplicate voting** (Set of voter IDs)
- [ ] ✅ **Discussed tie-breaking** (deterministic vs random)
- [ ] ✅ **Used Factory Pattern** for election creation
- [ ] ✅ **Showed runtime strategy switching**

---

## 📚 Quick Reference Card

```
┌────────────────────────────────────────────────────────────┐
│                VOTING SYSTEM CHEAT SHEET                   │
├────────────────────────────────────────────────────────────┤
│ CORE PATTERN: Strategy                                    │
│   - VotingStrategy: Abstract base with determine_winner() │
│   - Concrete: SimpleMajority, RankedChoice, InstantRunoff │
│   - ElectionManager: Context that uses strategy           │
│                                                            │
│ WHY STRATEGY PATTERN?                                     │
│   ✅ Add new algorithms without changing existing code    │
│   ✅ Runtime switching to compare results                 │
│   ✅ Each algorithm testable in isolation                 │
│   ✅ Open/Closed Principle                                │
│                                                            │
│ BALLOT DESIGN:                                            │
│   ranked_choices: List[str]                               │
│   - Majority uses [0] (first choice)                      │
│   - Ranked uses all with weights                          │
│   - Runoff redistributes based on preferences             │
│   ONE FORMAT SUPPORTS ALL STRATEGIES!                     │
│                                                            │
│ ALGORITHMS:                                               │
│   - Simple Majority: Count first choices, O(V)            │
│   - Weighted/Borda: Assign points by rank, O(V×R)         │
│   - Instant Runoff: Eliminate lowest, redistribute, O(C×V)│
│                                                            │
│ GOTCHAS:                                                  │
│   ⚠️ ALWAYS discuss tie-breaking!                        │
│   ⚠️ Prevent duplicate voting (Set of voter IDs)         │
│   ⚠️ Validate candidates exist                           │
└────────────────────────────────────────────────────────────┘
```

---

**Related Problems:**
- Design Payment Processing System (Strategy for payment methods)
- Design Sorting System (Strategy for sort algorithms)
- Design Compression System (Strategy for compression algorithms)

**Real-World Voting Systems:**
- Simple Majority: Most US elections
- Ranked Choice: Australia, San Francisco
- Borda Count: Eurovision, sports MVP voting

