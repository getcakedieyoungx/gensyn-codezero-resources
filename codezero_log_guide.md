# How to Read Your CodeZero Logs: Are You Actually Learning?

**A Technical Guide for Solver Node Runners**

---

## Introduction

So you've spun up your CodeZero node, and your terminal is flooding with cryptic log messages. You see words like "Policy Update," "Rollout," "Reward," and "Difficulty Adjustment"—but what does it all *mean*? More importantly: **Is your node actually learning, or is it just burning electricity?**

This guide breaks down the anatomy of CodeZero logs so you can understand what's happening under the hood and verify that you're contributing to the cooperative AI swarm.

---

## The Three Core Log Types

CodeZero nodes generate three primary categories of logs:

1. **Training Logs** – Your node is actively learning from problems
2. **Network Logs** – Communication with Proposers and other Solvers
3. **Reward Logs** – Confirmation that your solutions were valuable

Let's decode each one.

---

## 1. Training Logs: "Is My Node Learning?"

### What to Look For: `Policy Update`

**Example Log:**
```
[2025-11-22 14:23:45] INFO: Policy update received (epoch=127, loss=0.0342)
[2025-11-22 14:23:46] INFO: Gradient applied: avg_norm=0.0089
```

**What This Means:**
- **Policy Update** = Your node just updated its internal "strategy" for solving problems
- **Epoch** = Training iteration number (higher = more experience)
- **Loss** = How "wrong" your current policy is (lower is better)
  - `loss > 0.1` → Still learning the basics
  - `loss < 0.05` → Getting competent
  - `loss < 0.01` → Highly optimized
- **Gradient Applied** = The mathematical "nudge" that improves your policy
  - `avg_norm` measures how big the update was
  - Very small values (`< 0.001`) might mean you've plateaued

> [!TIP]
> **Healthy Learning Pattern:** You should see loss *decreasing* over time. If loss stays flat for 50+ epochs, your node might be stuck on problems that are too hard or too easy.

---

### What to Look For: `Rollout Generated`

**Example Log:**
```
[2025-11-22 14:24:12] DEBUG: Rollout generated (problem_id=0x3a7f, steps=42, diversity_score=0.73)
```

**What This Means:**
- **Rollout** = A complete solution attempt for a coding problem
- **problem_id** = Unique identifier for the problem you're solving
- **steps** = How many "thinking steps" your model took
  - More steps ≠ better (could mean inefficiency)
  - Fewer steps = more elegant solution
- **diversity_score** = How unique your solution is compared to other Solvers
  - `0.0` = Identical to everyone else (bad for GRPO)
  - `1.0` = Completely unique (good, but verify it's correct!)

> [!IMPORTANT]
> **CodeZero's Secret Sauce:** The system *rewards diversity*. If you see `diversity_score > 0.6`, you're contributing novel solutions that help the entire swarm learn faster.

---

## 2. Network Logs: "Am I Connected to the Swarm?"

### What to Look For: `Proposer Connected`

**Example Log:**
```
[2025-11-22 14:20:01] INFO: Connected to Proposer (node_id=0x9c2e, difficulty=3)
[2025-11-22 14:20:02] INFO: Received problem batch (count=5, timeout=120s)
```

**What This Means:**
- **Proposer** = The node that's sending you coding problems
- **difficulty** = Problem complexity level (1-5 scale)
  - `difficulty=1` → Simple syntax tasks
  - `difficulty=3` → Medium algorithms
  - `difficulty=5` → Complex multi-step problems
- **timeout** = How long you have to submit solutions

> [!WARNING]
> **Red Flag:** If you see `Proposer disconnected` frequently, check your network stability. Cooperative learning requires consistent uptime.

---

### What to Look For: `Difficulty Adjustment`

**Example Log:**
```
[2025-11-22 14:30:45] INFO: Difficulty adjusted: 3 → 4 (swarm_success_rate=0.82)
```

**What This Means:**
- The network is **dynamically adjusting** problem difficulty based on collective performance
- **swarm_success_rate** = What % of Solvers are succeeding
  - `> 0.8` → Problems are too easy, difficulty increases
  - `< 0.5` → Problems are too hard, difficulty decreases

**Why This Matters:**
This is **proof of cooperative learning**. Unlike Bitcoin (where difficulty only goes up), CodeZero adjusts *in both directions* to keep the swarm in the "Goldilocks zone" of learning—not too easy, not too hard.

---

## 3. Reward Logs: "Did I Earn Anything?"

### What to Look For: `Reward Received`

**Example Log:**
```
[2025-11-22 14:35:12] INFO: Reward received (amount=0.0042 GENSYN, problem_id=0x3a7f, rank=3/12)
```

**What This Means:**
- **amount** = How much you earned for this solution
- **rank** = Your solution's quality compared to other Solvers
  - `rank=1/12` → Best solution (highest reward)
  - `rank=6/12` → Middle of the pack
  - `rank=12/12` → Worst solution (minimal/no reward)

> [!NOTE]
> **Reward Distribution:** CodeZero uses **Group Relative Policy Optimization (GRPO)**, which means rewards are *relative* to other Solvers. Even if your solution is "correct," you earn less if everyone else found a better approach.

---

### What to Look For: `Evaluation Score`

**Example Log:**
```
[2025-11-22 14:35:10] DEBUG: Evaluation complete (correctness=0.95, efficiency=0.78, novelty=0.82)
```

**What This Means:**
- **correctness** = Does your code actually work? (0.0-1.0)
- **efficiency** = How fast/memory-efficient is it?
- **novelty** = How different is it from other solutions?

**The Formula:**
```
Final Reward = (correctness × 0.5) + (efficiency × 0.25) + (novelty × 0.25)
```

**Example Calculation:**
```
(0.95 × 0.5) + (0.78 × 0.25) + (0.82 × 0.25) = 0.875 → High reward
```

> [!TIP]
> **Optimization Strategy:** If you're consistently scoring low on `novelty`, your model might be overfitting to common patterns. Try adjusting your sampling temperature or exploration parameters.

---

## Advanced: Reading Between the Lines

### Pattern 1: "The Plateau"
```
[14:00] loss=0.045
[14:05] loss=0.044
[14:10] loss=0.044
[14:15] loss=0.045
```
**Diagnosis:** Your node has learned everything it can from the current difficulty level.  
**Action:** Wait for a difficulty adjustment, or manually request harder problems (if supported).

---

### Pattern 2: "The Reward Drought"
```
[14:00] Rollout generated
[14:05] Rollout generated
[14:10] Rollout generated
[14:15] No rewards received in last 15 minutes
```
**Diagnosis:** Your solutions are being submitted but not rewarded.  
**Possible Causes:**
- Your solutions are incorrect (check `correctness` scores)
- Other Solvers are consistently outperforming you
- Network latency is causing late submissions

---

### Pattern 3: "The Diversity Collapse"
```
[14:00] diversity_score=0.72
[14:05] diversity_score=0.68
[14:10] diversity_score=0.31
[14:15] diversity_score=0.12
```
**Diagnosis:** Your solutions are becoming too similar to the swarm.  
**Why This Happens:** As the network converges on optimal strategies, diversity naturally decreases.  
**Is This Bad?** Not necessarily—it means the swarm is reaching consensus. But if it happens too early, it could indicate premature convergence.

---

## Quick Reference: Log Severity Levels

| Level | Meaning | Example |
|-------|---------|---------|
| `DEBUG` | Detailed technical info | `Rollout generated (steps=42)` |
| `INFO` | Normal operations | `Policy update received` |
| `WARN` | Potential issues | `High memory usage detected` |
| `ERROR` | Something broke | `Failed to connect to Proposer` |
| `FATAL` | Node is shutting down | `Unrecoverable error in RL engine` |

> [!CAUTION]
> **If you see `ERROR` or `FATAL` logs:** Check your configuration, network connection, and system resources. A node that's constantly erroring isn't contributing to the swarm.

---

## Putting It All Together: A Healthy Node Session

Here's what a productive 30-minute session should look like:

```
[14:00:00] INFO: Connected to Proposer (difficulty=3)
[14:00:05] INFO: Received problem batch (count=5)
[14:02:30] DEBUG: Rollout generated (diversity_score=0.68)
[14:02:35] INFO: Reward received (amount=0.0038, rank=4/10)
[14:05:00] INFO: Policy update received (loss=0.041)
[14:07:15] DEBUG: Rollout generated (diversity_score=0.71)
[14:07:20] INFO: Reward received (amount=0.0045, rank=2/10)
[14:10:00] INFO: Policy update received (loss=0.038)
[14:15:30] INFO: Difficulty adjusted: 3 → 4
[14:16:00] DEBUG: Rollout generated (diversity_score=0.64)
[14:16:05] INFO: Reward received (amount=0.0052, rank=3/12)
[14:20:00] INFO: Policy update received (loss=0.044)
[14:25:10] DEBUG: Rollout generated (diversity_score=0.69)
[14:25:15] INFO: Reward received (amount=0.0048, rank=2/11)
[14:30:00] INFO: Policy update received (loss=0.040)
```

**What We See:**
✅ Regular problem solving (every ~5 minutes)  
✅ Consistent rewards (rank 2-4 out of 10-12)  
✅ Decreasing loss (0.041 → 0.038 → 0.040, with slight variance)  
✅ Healthy diversity scores (0.64-0.71)  
✅ Difficulty adjustment triggered by swarm performance  

---

## FAQ: Common Log Mysteries

### Q: "I see `Policy update` but no `Reward received`. Am I broken?"
**A:** No. Policy updates happen based on *shared rollouts* from the entire swarm, not just your own rewards. You're learning from other Solvers' experiences too—that's the cooperative part!

### Q: "My `diversity_score` is always > 0.9. Is that good?"
**A:** Maybe. High diversity means you're exploring unique solutions, but if your `correctness` is low, you might just be generating random garbage. Check your evaluation scores.

### Q: "I haven't seen a `Difficulty Adjustment` in hours. Is the network stuck?"
**A:** Difficulty adjusts when the swarm's success rate crosses certain thresholds. If everyone is performing consistently, difficulty stays stable. This is normal.

### Q: "What's the difference between `epoch` and `problem_id`?"
**A:** 
- **epoch** = Training iteration (internal to your node)
- **problem_id** = Specific coding problem from the network

You can solve multiple problems per epoch, or spend multiple epochs on one hard problem.

---

## Conclusion: Trust, But Verify

CodeZero's cooperative learning is powerful, but it's not magic. By understanding your logs, you can:

1. **Verify your node is actually learning** (decreasing loss, regular policy updates)
2. **Confirm you're contributing value** (consistent rewards, healthy diversity)
3. **Diagnose issues early** (reward droughts, diversity collapse, connection problems)

**The Bottom Line:** If you see regular `Policy updates`, `Reward received` logs with decent ranks, and `diversity_score > 0.5`, you're doing it right. Your node is learning, the swarm is benefiting, and you're earning your place in the cooperative AI revolution.

---

**Next Steps:**
- Monitor your logs for 24 hours and track your average `loss` and `reward` trends
- Compare your `diversity_score` with other node runners in the Discord
- Share interesting log patterns with the community—you might discover new optimization strategies together

**Remember:** In CodeZero, we learn faster when we share notes. 🤝🤖

---

*Written for the Gensyn community | Last updated: November 2025*
