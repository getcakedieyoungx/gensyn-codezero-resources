# Node Strategy Analysis: The "Marathon Runner"

## Verdict: The "3-Hour Rule" is RISKY / OBSOLETE

The "Run for 3 hours intermittently" strategy was likely effective for the previous RL-Swarm where tasks were more isolated or stateless. CodeZero changes the game mechanics significantly.

### Why the "3-Hour Rule" Fails in CodeZero
1.  **GRPO & Policy Updates:** Solvers update their policy based on collective experience (Rollout Sharing). If you are offline, you miss the "gossip" of peer rollouts. Your local model will fall behind the swarm's intelligence, leading to a lower "Success Rate" when you do come online.
2.  **Difficulty Adjustment:** Proposers adjust difficulty based on sustained solver performance. Short bursts might not provide enough signal for the Proposer to "trust" your node with higher-difficulty (and likely higher-reward) tasks.
3.  **Evaluator Latency:** Evaluators are now LLMs (Qwen 3 4B). The evaluation loop might be slower than simple hash-checking. Disconnecting mid-loop could forfeit rewards for work done.

## Recommended Strategy: "The Marathon Runner"

**Action:** Run 24/7 (or as long as possible) for the first 48 hours of CodeZero.

**Rationale:**
- You want your Solver to ingest as many peer rollouts as possible to optimize its policy (GRPO).
- The "smartest" nodes (most updated policies) will likely win the most rewards.
- Consistency builds "reputation" in the difficulty adjustment algorithms.
