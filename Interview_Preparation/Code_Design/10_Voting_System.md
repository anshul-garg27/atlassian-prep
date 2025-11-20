# 🗳️ PROBLEM 10: VOTING/ELECTION SYSTEM

### ⭐⭐⭐⭐ **Design Flexible Voting System with Strategy Pattern**

**Frequency:** Appears in **MEDIUM FREQUENCY** of Atlassian LLD rounds!
**Difficulty:** Medium
**Focus:** Strategy Pattern, Algorithm Design, Tie-Breaking

---

## 📋 Problem Statement

Design a voting/election system that can handle different voting strategies:
- **Simple Majority**: Candidate with most votes wins
- **Weighted/Ranked Choice**: 1st choice = 3pts, 2nd = 2pts, 3rd = 1pt
- **Instant Runoff**: Eliminate lowest, redistribute votes

**Core Requirements:**
- Support multiple voting algorithms
- Handle tie-breaking
- Easy to add new voting strategies
- Cast votes and determine winners
- Support real-time vote counting

---

## 🎨 Visual Example

```text
Scenario: 5 voters, 3 candidates (Alice, Bob, Charlie)

==== Simple Majority ====
Alice: ███ (3 votes)
Bob: ██ (2 votes)
Charlie: █ (1 vote)
Winner: Alice

==== Ranked Choice (3-2-1 points) ====
Voter 1: [Alice:1st, Bob:2nd, Charlie:3rd]
Voter 2: [Bob:1st, Alice:2nd, Charlie:3rd]
Voter 3: [Alice:1st, Charlie:2nd, Bob:3rd]

Points:
Alice: 3+2+3 = 8
Bob: 2+3+1 = 6
Charlie: 1+1+2 = 4
Winner: Alice

==== Instant Runoff ====
Round 1: Alice(2), Bob(2), Charlie(1)
Eliminate Charlie, redistribute
Round 2: Alice(2), Bob(3)
Winner: Bob
```

---

## 💻 Implementation

```java
import java.util.*;
import java.util.stream.Collectors;

// ============ Strategy Pattern Interface ============
interface VotingStrategy {
    String determineWinner(List<Ballot> ballots, List<String> candidates);
}

// ============ Ballot Class ============
class Ballot {
    private String voterId;
    private List<String> rankedChoices; // Ordered by preference

    public Ballot(String voterId, List<String> rankedChoices) {
        this.voterId = voterId;
        this.rankedChoices = new ArrayList<>(rankedChoices);
    }

    public String getVoterId() {
        return voterId;
    }

    public List<String> getRankedChoices() {
        return new ArrayList<>(rankedChoices);
    }

    public String getFirstChoice() {
        return rankedChoices.isEmpty() ? null : rankedChoices.get(0);
    }

    public String getChoice(int rank) {
        return (rank >= 0 && rank < rankedChoices.size()) 
               ? rankedChoices.get(rank) 
               : null;
    }
}

// ============ Strategy 1: Simple Majority ============
class SimpleMajorityStrategy implements VotingStrategy {
    @Override
    public String determineWinner(List<Ballot> ballots, List<String> candidates) {
        Map<String, Integer> voteCount = new HashMap<>();

        // Initialize candidates
        for (String candidate : candidates) {
            voteCount.put(candidate, 0);
        }

        // Count votes (only first choice matters)
        for (Ballot ballot : ballots) {
            String choice = ballot.getFirstChoice();
            if (choice != null && voteCount.containsKey(choice)) {
                voteCount.put(choice, voteCount.get(choice) + 1);
            }
        }

        // Find winner
        return voteCount.entrySet().stream()
                .max(Map.Entry.comparingByValue())
                .map(Map.Entry::getKey)
                .orElse(null);
    }
}

// ============ Strategy 2: Weighted Ranked Choice ============
class WeightedRankedChoiceStrategy implements VotingStrategy {
    private int[] weights; // e.g., [3, 2, 1] for 1st, 2nd, 3rd

    public WeightedRankedChoiceStrategy(int[] weights) {
        this.weights = weights;
    }

    @Override
    public String determineWinner(List<Ballot> ballots, List<String> candidates) {
        Map<String, Integer> points = new HashMap<>();

        // Initialize candidates
        for (String candidate : candidates) {
            points.put(candidate, 0);
        }

        // Calculate weighted points
        for (Ballot ballot : ballots) {
            List<String> choices = ballot.getRankedChoices();

            for (int i = 0; i < Math.min(choices.size(), weights.length); i++) {
                String candidate = choices.get(i);
                if (points.containsKey(candidate)) {
                    points.put(candidate, points.get(candidate) + weights[i]);
                }
            }
        }

        // Find winner with most points
        return points.entrySet().stream()
                .max(Map.Entry.comparingByValue())
                .map(Map.Entry::getKey)
                .orElse(null);
    }
}

// ============ Strategy 3: Instant Runoff (IRV) ============
class InstantRunoffStrategy implements VotingStrategy {
    @Override
    public String determineWinner(List<Ballot> ballots, List<String> candidates) {
        Set<String> remainingCandidates = new HashSet<>(candidates);
        List<Ballot> activeBallots = new ArrayList<>(ballots);

        while (remainingCandidates.size() > 1) {
            // Count first-choice votes
            Map<String, Integer> voteCount = new HashMap<>();
            for (String candidate : remainingCandidates) {
                voteCount.put(candidate, 0);
            }

            for (Ballot ballot : activeBallots) {
                String firstChoice = getFirstRemainingChoice(
                        ballot, remainingCandidates);
                if (firstChoice != null) {
                    voteCount.put(firstChoice, voteCount.get(firstChoice) + 1);
                }
            }

            // Check if anyone has majority
            int totalVotes = voteCount.values().stream()
                    .mapToInt(Integer::intValue).sum();

            for (Map.Entry<String, Integer> entry : voteCount.entrySet()) {
                if (entry.getValue() > totalVotes / 2) {
                    return entry.getKey(); // Majority winner
                }
            }

            // Eliminate candidate with fewest votes
            String loser = voteCount.entrySet().stream()
                    .min(Map.Entry.comparingByValue())
                    .map(Map.Entry::getKey)
                    .orElse(null);

            if (loser != null) {
                remainingCandidates.remove(loser);
            }
        }

        return remainingCandidates.iterator().next();
    }

    private String getFirstRemainingChoice(Ballot ballot, 
                                          Set<String> remaining) {
        for (String choice : ballot.getRankedChoices()) {
            if (remaining.contains(choice)) {
                return choice;
            }
        }
        return null;
    }
}

// ============ Tie-Breaking Strategy ============
interface TieBreaker {
    String breakTie(List<String> tiedCandidates);
}

class AlphabeticalTieBreaker implements TieBreaker {
    @Override
    public String breakTie(List<String> tiedCandidates) {
        return tiedCandidates.stream()
                .sorted()
                .findFirst()
                .orElse(null);
    }
}

class RandomTieBreaker implements TieBreaker {
    private Random random = new Random();

    @Override
    public String breakTie(List<String> tiedCandidates) {
        int index = random.nextInt(tiedCandidates.size());
        return tiedCandidates.get(index);
    }
}

// ============ Election Manager ============
class ElectionManager {
    private String electionId;
    private List<String> candidates;
    private List<Ballot> ballots;
    private VotingStrategy strategy;
    private TieBreaker tieBreaker;
    private Set<String> votedUserIds; // Prevent double voting

    public ElectionManager(String electionId, List<String> candidates,
                          VotingStrategy strategy, TieBreaker tieBreaker) {
        this.electionId = electionId;
        this.candidates = new ArrayList<>(candidates);
        this.ballots = new ArrayList<>();
        this.strategy = strategy;
        this.tieBreaker = tieBreaker;
        this.votedUserIds = new HashSet<>();
    }

    public boolean castVote(Ballot ballot) {
        // Prevent double voting
        if (votedUserIds.contains(ballot.getVoterId())) {
            return false;
        }

        // Validate candidates
        for (String choice : ballot.getRankedChoices()) {
            if (!candidates.contains(choice)) {
                throw new IllegalArgumentException(
                        "Invalid candidate: " + choice);
            }
        }

        ballots.add(ballot);
        votedUserIds.add(ballot.getVoterId());
        return true;
    }

    public String getWinner() {
        if (ballots.isEmpty()) {
            return null;
        }

        return strategy.determineWinner(ballots, candidates);
    }

    public Map<String, Integer> getResults() {
        Map<String, Integer> results = new HashMap<>();

        for (String candidate : candidates) {
            results.put(candidate, 0);
        }

        for (Ballot ballot : ballots) {
            String choice = ballot.getFirstChoice();
            if (choice != null && results.containsKey(choice)) {
                results.put(choice, results.get(choice) + 1);
            }
        }

        return results;
    }

    public void changeStrategy(VotingStrategy newStrategy) {
        this.strategy = newStrategy;
    }
}

// ============ Demo ============
public class Main {
    public static void main(String[] args) {
        List<String> candidates = Arrays.asList("Alice", "Bob", "Charlie");

        // Test 1: Simple Majority
        System.out.println("=== Simple Majority ===");
        ElectionManager election1 = new ElectionManager(
                "ELECTION_1",
                candidates,
                new SimpleMajorityStrategy(),
                new AlphabeticalTieBreaker()
        );

        election1.castVote(new Ballot("V1", Arrays.asList("Alice")));
        election1.castVote(new Ballot("V2", Arrays.asList("Bob")));
        election1.castVote(new Ballot("V3", Arrays.asList("Alice")));
        election1.castVote(new Ballot("V4", Arrays.asList("Charlie")));
        election1.castVote(new Ballot("V5", Arrays.asList("Alice")));

        System.out.println("Winner: " + election1.getWinner());
        System.out.println("Results: " + election1.getResults());

        // Test 2: Weighted Ranked Choice
        System.out.println("\n=== Weighted Ranked Choice (3-2-1) ===");
        ElectionManager election2 = new ElectionManager(
                "ELECTION_2",
                candidates,
                new WeightedRankedChoiceStrategy(new int[]{3, 2, 1}),
                new AlphabeticalTieBreaker()
        );

        election2.castVote(new Ballot("V1", 
                Arrays.asList("Alice", "Bob", "Charlie")));
        election2.castVote(new Ballot("V2", 
                Arrays.asList("Bob", "Alice", "Charlie")));
        election2.castVote(new Ballot("V3", 
                Arrays.asList("Alice", "Charlie", "Bob")));

        System.out.println("Winner: " + election2.getWinner());

        // Test 3: Instant Runoff
        System.out.println("\n=== Instant Runoff ===");
        ElectionManager election3 = new ElectionManager(
                "ELECTION_3",
                candidates,
                new InstantRunoffStrategy(),
                new AlphabeticalTieBreaker()
        );

        election3.castVote(new Ballot("V1", 
                Arrays.asList("Alice", "Bob", "Charlie")));
        election3.castVote(new Ballot("V2", 
                Arrays.asList("Bob", "Alice", "Charlie")));
        election3.castVote(new Ballot("V3", 
                Arrays.asList("Charlie", "Bob", "Alice")));
        election3.castVote(new Ballot("V4", 
                Arrays.asList("Alice", "Bob", "Charlie")));
        election3.castVote(new Ballot("V5", 
                Arrays.asList("Bob", "Charlie", "Alice")));

        System.out.println("Winner: " + election3.getWinner());
    }
}
```

---

## 🧪 Testing Strategy

```java
@Test
public void testSimpleMajority() {
    VotingStrategy strategy = new SimpleMajorityStrategy();
    List<String> candidates = Arrays.asList("A", "B", "C");

    List<Ballot> ballots = Arrays.asList(
            new Ballot("V1", Arrays.asList("A")),
            new Ballot("V2", Arrays.asList("B")),
            new Ballot("V3", Arrays.asList("A")),
            new Ballot("V4", Arrays.asList("C")),
            new Ballot("V5", Arrays.asList("A"))
    );

    String winner = strategy.determineWinner(ballots, candidates);
    assertEquals("A", winner);
}

@Test
public void testTieBreaking() {
    VotingStrategy strategy = new SimpleMajorityStrategy();
    List<String> candidates = Arrays.asList("A", "B");

    List<Ballot> ballots = Arrays.asList(
            new Ballot("V1", Arrays.asList("A")),
            new Ballot("V2", Arrays.asList("B"))
    );

    // Should handle tie scenario
    String winner = strategy.determineWinner(ballots, candidates);
    assertTrue(winner.equals("A") || winner.equals("B"));
}

@Test
public void testPreventDoubleVoting() {
    ElectionManager election = new ElectionManager(
            "TEST", Arrays.asList("A", "B"),
            new SimpleMajorityStrategy(),
            new AlphabeticalTieBreaker()
    );

    assertTrue(election.castVote(new Ballot("V1", Arrays.asList("A"))));
    assertFalse(election.castVote(new Ballot("V1", Arrays.asList("B")))); // Duplicate
}
```

---

## 💡 Interview Discussion Points

**Critical Question to Ask:** "What happens in case of a tie?"
- Alphabetical order?
- Random selection?
- Re-vote?
- Most recent vote wins?

**What Interviewers Look For:**
✅ **Strategy Pattern** for pluggable algorithms
✅ **Tie-breaking logic**
✅ **Prevent double voting**
✅ **Input validation**
✅ **Support for changing strategy**

**Common Mistakes (STRONG NO HIRE):**
❌ Using `LinkedHashMap` thinking it sorts (it maintains insertion order!)
❌ No tie-breaking discussion
❌ Not validating candidate names
❌ Allowing duplicate votes
❌ Inefficient O(N²) sorting when heap would work

---

## 📊 Complexity Analysis

| Strategy | Time | Space |
|----------|------|-------|
| Simple Majority | O(N) | O(C) |
| Weighted Ranked | O(N×R) | O(C) |
| Instant Runoff | O(C×N) | O(C) |

**Where:** N = ballots, C = candidates, R = ranked choices per ballot

---

## 💯 Best Practices

✅ **Strategy Pattern** for flexibility
✅ **Separate tie-breaking** logic
✅ **Prevent double voting** with Set
✅ **Validate inputs** (candidates, ballot format)
✅ **Use PriorityQueue** for top K (not full sort)
✅ **Ask about tie-breaking** before implementing!

**Interview Pro Tip:** This problem tests if you understand **Strategy Pattern** and can discuss trade-offs between voting algorithms!
