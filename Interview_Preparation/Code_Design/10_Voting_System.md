# 🗳️ PROBLEM 10: VOTING/ELECTION SYSTEM

### ⭐⭐⭐⭐ **Design Flexible Voting System with Strategy Pattern**

**Frequency:** MEDIUM at Atlassian
**Difficulty:** Medium
**Focus:** Strategy Pattern, Algorithm Design, Tie-Breaking

---

## 📋 Problem Statement

Design a voting/election system that can handle different voting strategies:
- **Simple Majority**: Candidate with most votes wins
- **Weighted/Ranked Choice**: 1st choice = 3pts, 2nd = 2pts, 3rd = 1pt
- **Instant Runoff (IRV)**: Eliminate lowest, redistribute votes

**Core Requirements:**
- Support multiple voting algorithms (swappable)
- Handle tie-breaking
- Prevent double voting
- Cast votes and determine winners
- Support real-time vote counting

---

## 🎯 Interview Approach

### Step 1: Clarify Requirements (2 min)
```
"Let me clarify:
1. What voting methods should we support?
2. How to handle ties?
3. Should we prevent duplicate voting?
4. Can voters change their vote?
5. Do we need real-time results?"
```

### Step 2: Identify Design Pattern (1 min)
```
"This is a perfect use case for Strategy Pattern:
- VotingStrategy interface defines the algorithm
- Each voting method is a concrete strategy
- ElectionManager uses strategy without knowing details
- Easy to add new voting methods without changing existing code"
```

---

## 🎨 Visual Example

```text
Scenario: 5 voters, 3 candidates (Alice, Bob, Charlie)

==== Simple Majority ====
Alice: ███ (3 votes)
Bob:   ██  (2 votes)
Charlie: █ (1 vote)
Winner: Alice (3 > 2 > 1)

==== Ranked Choice (3-2-1 points) ====
Voter 1: [Alice:1st, Bob:2nd, Charlie:3rd] → A:3, B:2, C:1
Voter 2: [Bob:1st, Alice:2nd, Charlie:3rd] → B:3, A:2, C:1
Voter 3: [Alice:1st, Charlie:2nd, Bob:3rd] → A:3, C:2, B:1

Total Points:
Alice: 3+2+3 = 8
Bob: 2+3+1 = 6
Charlie: 1+1+2 = 4
Winner: Alice (8 points)

==== Instant Runoff ====
Round 1: Alice(2), Bob(2), Charlie(1)
         Charlie eliminated (lowest)
Round 2: Charlie's votes → Bob (2nd choice)
         Alice(2), Bob(3)
Winner: Bob (majority after elimination)
```

---

## 💻 Python Implementation

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Set, Optional
from collections import defaultdict
from enum import Enum
import heapq
from datetime import datetime

# ============ Data Classes ============

@dataclass
class Candidate:
    """Represents a candidate in the election"""
    id: str
    name: str
    
    def __hash__(self):
        return hash(self.id)
    
    def __eq__(self, other):
        if isinstance(other, Candidate):
            return self.id == other.id
        return self.id == str(other)

@dataclass
class Ballot:
    """
    Represents a voter's ballot.
    
    ranked_choices: List of candidate IDs in order of preference
    (first = most preferred)
    """
    voter_id: str
    ranked_choices: List[str]
    timestamp: datetime = field(default_factory=datetime.now)
    
    @property
    def first_choice(self) -> Optional[str]:
        """Get the top choice"""
        return self.ranked_choices[0] if self.ranked_choices else None
    
    def get_choice(self, rank: int) -> Optional[str]:
        """Get choice at specific rank (0-indexed)"""
        if 0 <= rank < len(self.ranked_choices):
            return self.ranked_choices[rank]
        return None

# ============ Strategy Pattern Interface ============

class VotingStrategy(ABC):
    """
    Abstract base class for voting strategies.
    
    Design Pattern: Strategy
    - Encapsulates different voting algorithms
    - Allows runtime swapping of algorithms
    - Open/Closed Principle: Add new strategies without modifying existing code
    """
    
    @abstractmethod
    def determine_winner(self, ballots: List[Ballot], 
                        candidates: List[str]) -> Optional[str]:
        """
        Determine the winner based on the voting algorithm.
        
        Args:
            ballots: List of all cast ballots
            candidates: List of candidate IDs
            
        Returns:
            Winner's candidate ID, or None if no winner
        """
        pass
    
    @abstractmethod
    def get_results(self, ballots: List[Ballot], 
                   candidates: List[str]) -> Dict[str, int]:
        """Get detailed results (scores/votes per candidate)"""
        pass

# ============ Strategy 1: Simple Majority ============

class SimpleMajorityStrategy(VotingStrategy):
    """
    Simple plurality voting - candidate with most first-choice votes wins.
    
    Time: O(N) where N = number of ballots
    Space: O(C) where C = number of candidates
    """
    
    def determine_winner(self, ballots: List[Ballot], 
                        candidates: List[str]) -> Optional[str]:
        results = self.get_results(ballots, candidates)
        
        if not results:
            return None
        
        # Find max votes
        max_votes = max(results.values())
        winners = [c for c, v in results.items() if v == max_votes]
        
        # Handle tie - return first alphabetically (or could use tie-breaker)
        return min(winners) if winners else None
    
    def get_results(self, ballots: List[Ballot], 
                   candidates: List[str]) -> Dict[str, int]:
        vote_count = {c: 0 for c in candidates}
        
        for ballot in ballots:
            choice = ballot.first_choice
            if choice and choice in vote_count:
                vote_count[choice] += 1
        
        return vote_count

# ============ Strategy 2: Weighted Ranked Choice ============

class WeightedRankedChoiceStrategy(VotingStrategy):
    """
    Ranked choice with point values.
    Default: 1st=3pts, 2nd=2pts, 3rd=1pt (Borda count variant)
    
    Time: O(N × R) where N = ballots, R = ranks considered
    Space: O(C)
    """
    
    def __init__(self, weights: List[int] = None):
        # Default weights: [3, 2, 1] for top 3 choices
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
        points = {c: 0 for c in candidates}
        
        for ballot in ballots:
            for rank, candidate_id in enumerate(ballot.ranked_choices):
                if rank >= len(self.weights):
                    break
                
                if candidate_id in points:
                    points[candidate_id] += self.weights[rank]
        
        return points

# ============ Strategy 3: Instant Runoff Voting ============

class InstantRunoffStrategy(VotingStrategy):
    """
    Instant Runoff Voting (IRV) / Ranked Choice Voting.
    
    Algorithm:
    1. Count first-choice votes
    2. If someone has majority (>50%), they win
    3. Otherwise, eliminate candidate with fewest votes
    4. Redistribute eliminated candidate's votes to next choice
    5. Repeat until someone has majority
    
    Time: O(C × N) where C = candidates, N = ballots
    Space: O(C + N)
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
            
            # Check for majority
            for candidate, votes in vote_count.items():
                if votes > total_votes / 2:
                    return candidate
            
            # Find and eliminate candidate with fewest votes
            min_votes = min(vote_count.values())
            losers = [c for c, v in vote_count.items() if v == min_votes]
            
            # Tie-breaker: eliminate alphabetically first
            loser = min(losers)
            remaining.remove(loser)
        
        return remaining.pop() if remaining else None
    
    def _count_votes(self, ballots: List[Ballot], 
                    remaining: Set[str]) -> Dict[str, int]:
        """Count first valid choice for each ballot"""
        vote_count = {c: 0 for c in remaining}
        
        for ballot in ballots:
            choice = self._get_first_remaining_choice(ballot, remaining)
            if choice:
                vote_count[choice] += 1
        
        return vote_count
    
    def _get_first_remaining_choice(self, ballot: Ballot, 
                                   remaining: Set[str]) -> Optional[str]:
        """Get voter's top choice among remaining candidates"""
        for choice in ballot.ranked_choices:
            if choice in remaining:
                return choice
        return None
    
    def get_results(self, ballots: List[Ballot], 
                   candidates: List[str]) -> Dict[str, int]:
        """Return first-round results"""
        return self._count_votes(ballots, set(candidates))

# ============ Tie-Breaker Strategies ============

class TieBreaker(ABC):
    """Abstract tie-breaking strategy"""
    
    @abstractmethod
    def break_tie(self, tied_candidates: List[str]) -> str:
        pass

class AlphabeticalTieBreaker(TieBreaker):
    """Break ties alphabetically (deterministic)"""
    
    def break_tie(self, tied_candidates: List[str]) -> str:
        return min(tied_candidates)

class RandomTieBreaker(TieBreaker):
    """Break ties randomly"""
    
    def break_tie(self, tied_candidates: List[str]) -> str:
        import random
        return random.choice(tied_candidates)

class FirstVoteTieBreaker(TieBreaker):
    """Candidate who received first vote wins tie"""
    
    def __init__(self, ballots: List[Ballot]):
        self.vote_order = {}
        for i, ballot in enumerate(ballots):
            if ballot.first_choice not in self.vote_order:
                self.vote_order[ballot.first_choice] = i
    
    def break_tie(self, tied_candidates: List[str]) -> str:
        return min(tied_candidates, 
                  key=lambda c: self.vote_order.get(c, float('inf')))

# ============ Election Manager ============

class ElectionManager:
    """
    Manages an election with configurable voting strategy.
    
    Responsibilities:
    - Validate and store ballots
    - Prevent duplicate voting
    - Delegate winner determination to strategy
    - Support strategy switching
    """
    
    def __init__(self, election_id: str, candidates: List[str],
                 strategy: VotingStrategy,
                 tie_breaker: TieBreaker = None):
        self.election_id = election_id
        self.candidates = list(candidates)
        self.strategy = strategy
        self.tie_breaker = tie_breaker or AlphabeticalTieBreaker()
        
        self._ballots: List[Ballot] = []
        self._voter_ids: Set[str] = set()  # Prevent duplicate voting
        self._is_closed = False
    
    def cast_vote(self, ballot: Ballot) -> bool:
        """
        Cast a vote.
        
        Returns: True if vote accepted, False if rejected
        
        Validation:
        - Election not closed
        - Voter hasn't already voted
        - All choices are valid candidates
        """
        if self._is_closed:
            return False
        
        if ballot.voter_id in self._voter_ids:
            return False  # Duplicate vote
        
        # Validate candidates
        for choice in ballot.ranked_choices:
            if choice not in self.candidates:
                raise ValueError(f"Invalid candidate: {choice}")
        
        self._ballots.append(ballot)
        self._voter_ids.add(ballot.voter_id)
        return True
    
    def get_winner(self) -> Optional[str]:
        """Determine the winner using current strategy"""
        if not self._ballots:
            return None
        
        return self.strategy.determine_winner(self._ballots, self.candidates)
    
    def get_results(self) -> Dict[str, int]:
        """Get current results"""
        return self.strategy.get_results(self._ballots, self.candidates)
    
    def change_strategy(self, new_strategy: VotingStrategy) -> None:
        """
        Change voting strategy.
        
        Useful for comparing results under different methods.
        """
        self.strategy = new_strategy
    
    def close_election(self) -> None:
        """Close election to new votes"""
        self._is_closed = True
    
    def get_statistics(self) -> Dict:
        """Get election statistics"""
        return {
            "election_id": self.election_id,
            "total_votes": len(self._ballots),
            "candidates": len(self.candidates),
            "is_closed": self._is_closed,
            "strategy": type(self.strategy).__name__,
        }

# ============ Election Factory ============

class ElectionFactory:
    """Factory for creating elections with common configurations"""
    
    @staticmethod
    def create_simple_majority(election_id: str, 
                               candidates: List[str]) -> ElectionManager:
        return ElectionManager(
            election_id=election_id,
            candidates=candidates,
            strategy=SimpleMajorityStrategy()
        )
    
    @staticmethod
    def create_ranked_choice(election_id: str, candidates: List[str],
                            weights: List[int] = None) -> ElectionManager:
        return ElectionManager(
            election_id=election_id,
            candidates=candidates,
            strategy=WeightedRankedChoiceStrategy(weights)
        )
    
    @staticmethod
    def create_instant_runoff(election_id: str, 
                              candidates: List[str]) -> ElectionManager:
        return ElectionManager(
            election_id=election_id,
            candidates=candidates,
            strategy=InstantRunoffStrategy()
        )

# ============ Demo ============

def main():
    candidates = ["Alice", "Bob", "Charlie"]
    
    # ===== Test 1: Simple Majority =====
    print("=" * 50)
    print("TEST 1: Simple Majority")
    print("=" * 50)
    
    election1 = ElectionFactory.create_simple_majority("E1", candidates)
    
    # Cast votes
    election1.cast_vote(Ballot("V1", ["Alice"]))
    election1.cast_vote(Ballot("V2", ["Bob"]))
    election1.cast_vote(Ballot("V3", ["Alice"]))
    election1.cast_vote(Ballot("V4", ["Charlie"]))
    election1.cast_vote(Ballot("V5", ["Alice"]))
    
    print(f"Results: {election1.get_results()}")
    print(f"Winner: {election1.get_winner()}")
    
    # Try duplicate vote
    result = election1.cast_vote(Ballot("V1", ["Bob"]))
    print(f"Duplicate vote accepted: {result}")  # Should be False
    
    # ===== Test 2: Weighted Ranked Choice =====
    print("\n" + "=" * 50)
    print("TEST 2: Weighted Ranked Choice (3-2-1)")
    print("=" * 50)
    
    election2 = ElectionFactory.create_ranked_choice("E2", candidates)
    
    election2.cast_vote(Ballot("V1", ["Alice", "Bob", "Charlie"]))
    election2.cast_vote(Ballot("V2", ["Bob", "Alice", "Charlie"]))
    election2.cast_vote(Ballot("V3", ["Alice", "Charlie", "Bob"]))
    
    print(f"Points: {election2.get_results()}")
    print(f"Winner: {election2.get_winner()}")
    
    # ===== Test 3: Instant Runoff =====
    print("\n" + "=" * 50)
    print("TEST 3: Instant Runoff Voting")
    print("=" * 50)
    
    election3 = ElectionFactory.create_instant_runoff("E3", candidates)
    
    # Scenario where Alice leads initially but loses after redistribution
    election3.cast_vote(Ballot("V1", ["Alice", "Bob", "Charlie"]))
    election3.cast_vote(Ballot("V2", ["Alice", "Bob", "Charlie"]))
    election3.cast_vote(Ballot("V3", ["Bob", "Charlie", "Alice"]))
    election3.cast_vote(Ballot("V4", ["Bob", "Charlie", "Alice"]))
    election3.cast_vote(Ballot("V5", ["Charlie", "Bob", "Alice"]))  # Charlie eliminated, vote goes to Bob
    
    print(f"First-round: {election3.get_results()}")
    print(f"Winner after runoff: {election3.get_winner()}")
    
    # ===== Test 4: Strategy Switching =====
    print("\n" + "=" * 50)
    print("TEST 4: Same Votes, Different Strategies")
    print("=" * 50)
    
    election4 = ElectionManager("E4", candidates, SimpleMajorityStrategy())
    
    # Add votes
    for ballot in [
        Ballot("V1", ["Alice", "Bob", "Charlie"]),
        Ballot("V2", ["Bob", "Alice", "Charlie"]),
        Ballot("V3", ["Charlie", "Bob", "Alice"]),
    ]:
        election4.cast_vote(ballot)
    
    print(f"Simple Majority: {election4.get_winner()}")
    
    election4.change_strategy(WeightedRankedChoiceStrategy([3, 2, 1]))
    print(f"Ranked Choice: {election4.get_winner()}")
    
    election4.change_strategy(InstantRunoffStrategy())
    print(f"Instant Runoff: {election4.get_winner()}")
    
    print("\n" + "=" * 50)
    print("Statistics:", election4.get_statistics())

if __name__ == "__main__":
    main()
```

---

## 🎯 Interview Explanation Flow

### 1. Identify the Pattern (30 sec)
```
"This is a classic Strategy Pattern use case:
- Multiple algorithms for the same problem (counting votes)
- Need to swap algorithms at runtime
- Each strategy encapsulates its own logic
- Open/Closed Principle: add new strategies without changing manager"
```

### 2. Key Design Decisions (1 min)
```
"Critical decisions:
1. Ballot stores ranked choices (supports all strategies)
2. Strategy interface with determine_winner and get_results
3. ElectionManager handles validation, strategy delegates counting
4. Separate TieBreaker strategy for flexibility
5. Factory methods for common configurations"
```

### 3. Important Question (30 sec)
```
"ALWAYS ASK: How should we handle ties?
- Alphabetical order (deterministic)
- Random selection
- Re-vote
- First to receive vote
- Custom tie-breaker strategy"
```

---

## 📊 Complexity Analysis

| Strategy | Time | Space |
|----------|------|-------|
| Simple Majority | O(N) | O(C) |
| Weighted Ranked | O(N × R) | O(C) |
| Instant Runoff | O(C × N) | O(C + N) |

**Where:** N = ballots, C = candidates, R = ranks per ballot

---

## 💡 Interview Tips

### What Interviewers Look For:
✅ **Strategy Pattern** implementation
✅ **Tie-breaking** discussion
✅ **Duplicate vote prevention**
✅ **Input validation**
✅ **Clean separation** of concerns

### Common Mistakes (STRONG NO HIRE):
❌ Using `LinkedHashMap` thinking it sorts (it maintains insertion order!)
❌ No tie-breaking discussion or handling
❌ Not validating candidate names
❌ Allowing duplicate votes
❌ Hardcoding specific algorithm instead of using strategy

### Questions to Ask:
- "How should ties be handled?"
- "Can voters change their vote?"
- "Do we need real-time results?"
- "Should we support ranked ballots?"
- "What's the expected scale (voters/candidates)?"

---

## 🚀 Extensions

### 1. Real-time Results with Observer Pattern
```python
class ObservableElection(ElectionManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._observers = []
    
    def add_observer(self, callback):
        self._observers.append(callback)
    
    def cast_vote(self, ballot: Ballot) -> bool:
        result = super().cast_vote(ballot)
        if result:
            for observer in self._observers:
                observer(self.get_results())
        return result
```

### 2. Vote History and Audit
```python
@dataclass
class VoteAuditEntry:
    timestamp: datetime
    voter_id_hash: str  # Hashed for privacy
    ballot_hash: str
    action: str  # "cast", "modified", "invalidated"
```

### 3. Distributed Voting
```python
class DistributedElection:
    """Voting across multiple regions with eventual consistency"""
    
    def merge_results(self, region_results: List[Dict]) -> Dict:
        # Merge votes from different regions
        pass
```

---

## 🔗 Related Concepts

- **Strategy Pattern**: Core pattern for swappable algorithms
- **Factory Pattern**: Creating elections with preset configurations
- **Observer Pattern**: Real-time result updates
- **Consensus Algorithms**: Distributed voting systems

