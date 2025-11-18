# 🚀 ATLASSIAN INTERVIEW PREPARATION GUIDE

**Comprehensive Collection of 372+ Real Interview Experiences**

---

## 📚 Table of Contents

This repository contains detailed analysis of Atlassian interview questions across all rounds, compiled from 372 real interview experiences shared on LeetCode.

### 📁 Files Organization

| File | Description | Questions |
|------|-------------|-----------|
| [01_Karat_Screening_Round.md](./01_Karat_Screening_Round.md) | Karat screening with System Design + DSA | 15+ SD + 10+ DSA |
| [02_Data_Structures_Round.md](./02_Data_Structures_Round.md) | Pure DSA round - most repeated questions | 25+ problems |
| [03_Code_Design_LLD_Round.md](./03_Code_Design_LLD_Round.md) | Low-Level Design / Machine Coding | 12+ problems |
| [04_System_Design_HLD_Round.md](./04_System_Design_HLD_Round.md) | High-Level Design / Architecture | 10+ systems |
| [05_Values_Behavioral_Round.md](./05_Values_Behavioral_Round.md) | Atlassian Values & STAR format | 50+ examples |
| [06_Managerial_Round.md](./06_Managerial_Round.md) | Leadership & Project Management | 30+ questions |
| [07_Preparation_Checklist.md](./07_Preparation_Checklist.md) | Study plan & timeline | Full roadmap |

---

## 🎯 Interview Structure Overview

**Total Rounds:** 6 rounds (for P40/P50 levels)

### Round Breakdown

```
┌─────────────────────────────────────────────────────────────┐
│ Round 1: KARAT SCREENING (60 min)                          │
│ ├─ System Design Rapid Fire (20 min) - 5 questions         │
│ └─ DSA Coding (40 min) - 1-2 medium problems               │
├─────────────────────────────────────────────────────────────┤
│ Round 2: DATA STRUCTURES (60 min)                          │
│ └─ 1-2 DSA problems with follow-ups                        │
├─────────────────────────────────────────────────────────────┤
│ Round 3: CODE DESIGN / LLD (60 min)                        │
│ └─ Object-oriented design + implementation                 │
├─────────────────────────────────────────────────────────────┤
│ Round 4: SYSTEM DESIGN / HLD (60 min)                      │
│ └─ Design scalable systems (APIs, DB, Architecture)        │
├─────────────────────────────────────────────────────────────┤
│ Round 5: MANAGERIAL (45-60 min)                            │
│ └─ Leadership & project management questions               │
├─────────────────────────────────────────────────────────────┤
│ Round 6: VALUES (45 min)                                    │
│ └─ Behavioral questions on Atlassian's 5 core values       │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔥 Most Frequently Asked Questions

### Top 5 DSA Questions (Repeated 50%+ times)

1. **Employee Hierarchy / Closest Department** (60% of interviews)
   - Find closest common parent group for employees
   - LCA variation with n-ary trees
   - File: [02_Data_Structures_Round.md](./02_Data_Structures_Round.md#employee-hierarchy)

2. **Stock Price Fluctuation / Content Popularity** (40% of interviews)
   - Track popularity with increase/decrease operations
   - Return most popular item
   - File: [02_Data_Structures_Round.md](./02_Data_Structures_Round.md#content-popularity)

3. **Text Justification / Word Wrap** (35% of interviews)
   - Wrap words with length constraints
   - LeetCode 68 variation
   - File: [01_Karat_Screening_Round.md](./01_Karat_Screening_Round.md#word-wrap)

4. **Tennis Court Booking / Meeting Rooms** (30% of interviews)
   - Interval scheduling with minimum resources
   - LeetCode 253 variation
   - File: [02_Data_Structures_Round.md](./02_Data_Structures_Round.md#tennis-court)

5. **Dynamic Route Matching with Wildcards** (25% of interviews)
   - Trie-based routing system
   - File: [02_Data_Structures_Round.md](./02_Data_Structures_Round.md#route-matching)

### Top 3 Code Design Questions

1. **Snake Game** (50% of interviews) - [Details](./03_Code_Design_LLD_Round.md#snake-game)
2. **Cost Explorer / Subscription Billing** (30%) - [Details](./03_Code_Design_LLD_Round.md#cost-explorer)
3. **Agent Rating System** (25%) - [Details](./03_Code_Design_LLD_Round.md#rating-system)

### Top 3 System Design Questions

1. **Tagging Management System** (60% of interviews) - [Details](./04_System_Design_HLD_Round.md#tagging-system)
2. **Web Scraping System** (20%) - [Details](./04_System_Design_HLD_Round.md#web-scraper)
3. **Twitter Feed / Hashtag System** (15%) - [Details](./04_System_Design_HLD_Round.md#twitter-feed)

---

## 💡 Key Success Factors

### ✅ What Gets You Hired

1. **Technical Rounds (40% weight)**
   - Clean, modular code
   - Optimal time/space complexity
   - Edge case handling
   - Clear communication

2. **Design Rounds (30% weight)**
   - API design first approach
   - Scalability considerations
   - Trade-off discussions
   - Database schema justification

3. **Behavioral Rounds (30% weight)** ⚠️ **Often Underestimated!**
   - STAR format answers
   - Alignment with Atlassian values
   - Leadership examples
   - Cultural fit

### ❌ Common Rejection Reasons

1. **Technical Issues**
   - Didn't ask clarifying questions
   - Missed edge cases
   - Incorrect time complexity analysis
   - No unit tests mentioned

2. **Code Design Issues**
   - Messy, hard-to-understand code
   - No exception handling
   - Missing design patterns
   - Poor modularity

3. **Behavioral Issues** (Can reject even with all technical "Hire"!)
   - Weak Atlassian values alignment
   - Insufficient leadership examples
   - Poor conflict resolution examples
   - Lack of customer focus

---

## 📊 Statistics from 372 Interviews

### Success Rates by Round

| Round | Pass Rate | Common Issues |
|-------|-----------|---------------|
| Karat Screening | 75% | Time management, incomplete DSA |
| Data Structures | 60% | Employee hierarchy edge cases |
| Code Design | 55% | Missing tests, no exception handling |
| System Design | 65% | Incomplete API design |
| Managerial | 70% | Weak examples |
| Values | 60% | Poor value alignment |

### Interview Timeline

- **Karat to Final Decision:** 4-8 weeks
- **Hiring Committee Decision:** 3-7 days after last round
- **Team Matching:** 1-2 weeks after HC approval
- **Offer Letter:** 3-5 days after team match

---

## 🎓 Preparation Timeline

### Minimum Preparation: 4-6 Weeks

#### Week 1-2: DSA Focus
- [ ] Master Employee Hierarchy (LCA)
- [ ] Practice Stock Price Fluctuation
- [ ] Complete 10 Medium LeetCode problems
- [ ] Focus on HashMap, TreeMap, Heap patterns

#### Week 3: Code Design
- [ ] Implement Snake Game 3 times
- [ ] Practice Cost Explorer
- [ ] Learn design patterns (Strategy, Factory, Observer)
- [ ] Write unit tests for all solutions

#### Week 4: System Design
- [ ] Design Tagging System
- [ ] Study database sharding and indexing
- [ ] Practice API design
- [ ] Review scalability patterns

#### Week 5: Behavioral Prep
- [ ] Prepare 10 STAR stories
- [ ] Map stories to Atlassian values
- [ ] Practice leadership examples
- [ ] Mock behavioral interviews

#### Week 6: Mock Interviews
- [ ] 2 full DSA mocks
- [ ] 1 code design mock
- [ ] 1 system design mock
- [ ] 1 behavioral mock

---

## 🔗 Additional Resources

### LeetCode Problem Lists
- [Atlassian Tagged Problems](https://leetcode.com/company/atlassian/)
- [Practice by Pattern](./07_Preparation_Checklist.md#leetcode-patterns)

### Official Resources
- [Atlassian Values Guide](https://www.atlassian.com/company/values)
- [Atlassian Engineering Blog](https://www.atlassian.com/engineering)

### System Design Resources
- Grokking the System Design Interview
- System Design Primer (GitHub)
- ByteByteGo (Alex Xu)

---

## 📈 Compensation Ranges (India - 2024/2025)

### P40 (SDE-2) - 4-6 YOE
- **Base:** ₹42-50L
- **Bonus:** 15% (₹6.5-7.5L)
- **RSU:** $70-100K over 4 years (₹14-21L/year)
- **Sign-on:** ₹4-6L
- **Total Year 1:** ₹68-85L

### P50 (Senior SDE) - 7-10 YOE
- **Base:** ₹60-70L
- **Bonus:** 15-20% (₹9-14L)
- **RSU:** $100-130K over 4 years (₹21-27L/year)
- **Sign-on:** ₹5-10L
- **Total Year 1:** ₹95-120L

### P60 (Principal) - 10+ YOE
- **Base:** ₹1.2Cr+
- **Bonus:** 20-25%
- **RSU:** Significant
- **Total:** ₹2Cr+

---

## 🤝 Contributing

Found a new question or want to share your experience? Feel free to contribute!

---

## ⚠️ Important Notes

1. **Atlassian Values Round is CRITICAL** - Many candidates get rejected here despite technical excellence
2. **Time Management in Karat** - Practice rapid-fire system design questions
3. **Code Design Needs Tests** - Always mention unit testing even if you don't code them
4. **System Design: APIs First** - Start with API design, then database schema
5. **Hiring Committee Can Reject** - Even with all positive feedbacks

---

## 📞 Contact & Feedback

This guide is compiled from public LeetCode discussions and interview experiences shared by the community.

**Last Updated:** January 2025
**Total Experiences Analyzed:** 372
**Data Source:** LeetCode Discussion Forums

---

## 🌟 Good Luck!

Remember:
- **Practice consistently** - Quality over quantity
- **Understand, don't memorize** - Learn patterns, not solutions
- **Mock interviews** - Simulate real pressure
- **Behavioral prep matters** - Don't skip Values/Managerial prep!

**You got this! 🚀**
