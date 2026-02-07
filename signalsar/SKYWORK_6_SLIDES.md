# Skywork.ai Prompts for 6-Slide SignalSAR Presentation

## Overview
Compressed, high-impact 6-slide presentation optimized for 5-7 minute pitch.

---

## 🎯 6-Slide Structure

1. **Problem + Solution** (Combined)
2. **Product Demo Flow** (Visual journey)
3. **Key Innovation** (< 1ms + Governance + Explainability)
4. **Technical Architecture** (How it works)
5. **Impact & Competitive Edge** (Metrics + Positioning)
6. **Call to Action** (Next steps)

---

## Prompt 1: Problem + Solution (Slide 1)

```
I'm creating a 6-slide hackathon presentation for SignalSAR. I need to combine 
the problem and solution into ONE powerful opening slide.

PROBLEM (Current State):
- Manual SAR writing takes 2-4 hours per report
- 70% of analyst time wasted on false positives
- Inconsistent documentation creates audit risk
- No explainability for regulatory review

SOLUTION (SignalSAR):
- Real-time SAR generation in < 1 millisecond (10,000x faster)
- Evidence-linked explainability with inline transaction references
- Multi-gate governance prevents incomplete submissions
- Adaptive learning reduces false positives over time

Please create ONE slide that:
1. Opens with the pain (2 bullets max, quantified)
2. Transitions to solution with "SignalSAR delivers..."
3. Lists 3 key capabilities with metrics
4. Uses split layout: Problem (left) | Solution (right)
5. Emphasizes the speed metric (< 1ms, 10,000x faster)

Format as markdown for Marp. Use bold for metrics. Keep total to 6-7 bullets.

Target: Financial compliance professionals and technical judges.
```

---

## Prompt 2: Product Demo Flow (Slide 2)

```
I need a visual product flow slide showing the end-to-end journey from 
alert to regulatory submission in ONE slide.

FLOW (6 steps in 3 minutes):
1. Alert Queue → Risk-sorted (score 94 → 52)
2. Investigate → One-click, SAR generated in < 1ms
3. Evidence Pack → 7 artifacts linked (transactions, network, devices)
4. Governance → Confirm typology, record disposition with rationale
5. SAR Review → Editable narrative, 100% compliance score
6. Submit → Cryptographic checksum, immutable audit trail

KEY POINTS:
- Emphasize speed: "< 1 second from alert to draft"
- Show human-in-loop: Steps 4-5 require analyst review
- Highlight governance: 5 validation gates before submission
- Note real-time intervention: Automatic hold_withdrawal for high-risk

Please create a flow slide that:
1. Shows 6 steps as a visual journey (use icons/emojis)
2. Includes timing for each step
3. Highlights automation vs. human review
4. Emphasizes "3-minute journey from detection to submission"
5. Adds a callout box: "Real-time check: Automatic hold_withdrawal"

Format as numbered steps with brief descriptions (1 line each).
Use icons: 🔔 Alert → 🔍 Investigate → 📊 Evidence → ✅ Governance → 📝 Review → 🚀 Submit
```

---

## Prompt 3: Key Innovation (Slide 3)

```
I need ONE slide that showcases the 3 core innovations that make SignalSAR 
unique and hackathon-winning.

THREE PILLARS:

1. SPEED ⚡
   - SAR generation: < 1 millisecond (0.24ms actual)
   - 10,000x faster than manual (2-4 hours → < 1ms)
   - Real-time risk scoring with 7 typology patterns

2. GOVERNANCE 🛡️
   - 5-gate validation before submission
   - Required rationale for all analyst decisions
   - Database-level immutability (triggers block UPDATE/DELETE)
   - Cryptographic checksums (SHA-256)

3. EXPLAINABILITY 🔗
   - Evidence-linked reason codes (7 artifacts per case)
   - Inline transaction references: [Evidence: TXN-123, TXN-456]
   - Multi-artifact analysis (transactions + network + devices)
   - Regulator-friendly, traceable outputs

Please create ONE slide that:
1. Uses 3-column layout: Speed | Governance | Explainability
2. Each column has icon, title, and 3-4 key points
3. Emphasizes metrics (< 1ms, 10,000x, 5 gates, 7 artifacts)
4. Uses bold for numbers
5. Adds tagline at bottom: "Enterprise-grade compliance at startup speed"

Keep each bullet to 5-7 words max. Focus on impact, not implementation.
```

---

## Prompt 4: Technical Architecture (Slide 4)

```
I need a technical architecture slide that shows how SignalSAR works 
while demonstrating production-ready thinking.

ARCHITECTURE:
- Frontend: Vanilla JS + HTML/CSS (lightweight, fast)
- API: RESTful JSON endpoints
- Backend: Flask (Python)
- Core Modules:
  1. Risk Scoring Engine (7 typology patterns)
  2. Evidence Linker (transaction + network + device artifacts)
  3. Governance Gate (5 validation checks)
  4. Compliance Checker (8 required fields)
  5. Audit Logger (immutable, before/after tracking)
- Data Store: SQLite with:
  - Foreign key constraints
  - Unique indexes on submissions
  - Triggers for append-only audit trail
  - SHA-256 checksums

PRODUCTION-READY FEATURES:
- Database triggers enforce immutability
- Migration scripts included
- Automated testing (test_fixes.py)
- Comprehensive documentation

Please create an architecture slide that:
1. Shows visual layers: Frontend → API → Core Logic → Data Store
2. Lists core modules with brief descriptions (1 line each)
3. Highlights production-ready features in a callout box
4. Emphasizes "MVP stack with enterprise-grade compliance"
5. Adds footer: "Modular design enables easy scaling"

Use a simple visual hierarchy. Keep technical but accessible.
Target: Technical judges who appreciate engineering excellence.
```

---

## Prompt 5: Impact & Competitive Edge (Slide 5)

```
I need ONE slide that combines measurable impact with competitive positioning.

MEASURABLE IMPACT:
- Speed: 10,000x faster (2-4 hours → < 1ms)
- Consistency: 100% compliance score, standardized format
- Accountability: Immutable audit trail, required rationale
- Defensibility: Evidence-linked reasoning, cryptographic checksums

COMPETITIVE POSITIONING:
vs. Manual Process:
  - Speed: 10,000x faster
  - Quality: Consistent vs. variable
  - Audit: Immutable trail vs. scattered notes

vs. Other AI Solutions:
  - Transparency: Evidence-linked vs. black box
  - Governance: Human-in-loop vs. autonomous
  - Compliance: Multi-gate validation vs. basic checks

vs. Commercial Solutions:
  - Speed: < 1ms vs. minutes/hours
  - Cost: Open architecture vs. proprietary
  - Adaptability: Modular design vs. locked-in

PROOF POINTS:
- Working prototype with full end-to-end workflow
- Real-time generation verified (0.24ms actual)
- Database-level immutability enforced
- Comprehensive documentation and testing

Please create ONE slide with:
1. Top section: "Measurable Impact" with 4 key metrics
2. Middle section: "Competitive Advantages" comparison table
3. Bottom section: "Proof Points" with 3-4 bullets
4. Use ✅ and ❌ for visual comparison
5. Emphasize "Best of both worlds: Speed + Governance"

Format as 3 distinct sections. Use bold for metrics and key differentiators.
```

---

## Prompt 6: Call to Action (Slide 6)

```
I need a powerful closing slide that reinforces the value proposition 
and invites engagement.

KEY MESSAGES:
- SignalSAR transforms compliance operations with AI, governance, and traceability
- Real-time SAR generation (< 1ms) with evidence-linked explainability
- Human-in-the-loop governance ensures regulatory compliance
- Working prototype demonstrates production-ready thinking

VALUE PROPOSITION (3 Pillars):
⚡ Analyst Speed
   - Faster alert-to-draft cycles
   - Reduced false positive fatigue
   - 10,000x time savings

🛡️ Governance
   - Human-in-the-loop controls
   - Structured audit logging
   - Regulatory defensibility

🔗 Explainability
   - Evidence-linked reasoning
   - Regulator-friendly outputs
   - Traceable decision trail

NEXT STEPS:
- Live demo available
- Full documentation provided
- Production roadmap ready

CONTACT:
- Website: signalsar.ai
- Email: contact@signalsar.ai
- Lab: Compliance Solutions Lab

Please create a closing slide that:
1. Reinforces 3 pillars with icons and brief descriptions
2. Includes memorable tagline (5-7 words)
3. Shows contact information clearly
4. Invites questions with engaging prompt
5. Uses visual elements (icons for each pillar)

Tagline options to consider:
- "Compliance Intelligence at Machine Speed"
- "AI-Powered Compliance, Human-Approved"
- "Transform Compliance with Explainable AI"

Choose or create a tagline that emphasizes speed + governance + transparency.

Format with 3 columns for pillars, contact info at bottom, tagline prominent.
```

---

## 🚀 Quick Usage Guide

### Step-by-Step Process:

1. **Copy Prompt 1** → Paste into Skywork.ai
2. Review output → Iterate if needed ("Make it 20% more concise")
3. Copy revised content → Paste into your Marp presentation
4. **Repeat for Prompts 2-6**

### Iteration Examples:

**If too long:**
```
Please make this 30% more concise while keeping 
the key metrics (< 1ms, 10,000x, 5 gates).
```

**If too technical:**
```
Simplify the language for a business audience 
while maintaining technical credibility.
```

**If needs more impact:**
```
Make this more compelling by emphasizing the 
10,000x speed improvement and regulatory benefits.
```

---

## 📊 Key Metrics Reference

Copy-paste these into any prompt:

```
VERIFIED METRICS:
- Speed: < 1 millisecond (0.24ms actual)
- Improvement: 10,000x faster than manual
- Compliance: 100% field completeness
- Evidence: 7 artifacts linked per case
- Governance: 5 validation gates
- Typologies: 7 ML-detected patterns
- Citations: 4 evidence references per narrative
- Immutability: Database triggers enforce append-only
- Checksums: SHA-256 cryptographic verification
```

---

## 🎯 6-Slide Presentation Structure

```
┌─────────────────────────────────────────────────┐
│ Slide 1: Problem + Solution                     │
│ • Pain points (2 bullets)                       │
│ • Solution capabilities (3 bullets with metrics)│
│ Time: 60 seconds                                │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ Slide 2: Product Demo Flow                      │
│ • 6-step visual journey                         │
│ • Timing for each step                          │
│ • Human-in-loop highlights                      │
│ Time: 90 seconds                                │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ Slide 3: Key Innovation (3 Pillars)             │
│ • Speed: < 1ms, 10,000x faster                  │
│ • Governance: 5 gates, immutability             │
│ • Explainability: Evidence-linked               │
│ Time: 90 seconds                                │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ Slide 4: Technical Architecture                 │
│ • Stack overview                                │
│ • Core modules                                  │
│ • Production-ready features                     │
│ Time: 60 seconds                                │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ Slide 5: Impact & Competitive Edge              │
│ • Measurable impact (4 metrics)                 │
│ • Competitive comparison                        │
│ • Proof points                                  │
│ Time: 90 seconds                                │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ Slide 6: Call to Action                         │
│ • 3 pillars reinforcement                       │
│ • Tagline                                       │
│ • Contact info                                  │
│ Time: 30 seconds                                │
└─────────────────────────────────────────────────┘

TOTAL TIME: 7 minutes (perfect for 5-10 min slot)
```

---

## 💡 Pro Tips for 6-Slide Format

### 1. Density Management
- Each slide should have ONE clear message
- Use visual hierarchy (headers, bold, icons)
- Keep bullets to 5-7 words max
- Use numbers and metrics liberally

### 2. Visual Appeal
- Use icons/emojis for quick recognition
- Split layouts for comparison (Problem | Solution)
- 3-column layouts for pillars
- Callout boxes for key points

### 3. Timing Strategy
- Slide 1: Hook with problem + solution (60s)
- Slides 2-3: Core value (90s each)
- Slide 4: Technical credibility (60s)
- Slide 5: Business case (90s)
- Slide 6: Close strong (30s)

### 4. Narrative Flow
```
Problem → Solution → How It Works → Why It Matters → What's Next
```

---

## ✅ Quality Checklist

After creating all 6 slides:

- [ ] Each slide has ONE clear message
- [ ] All metrics verified (< 1ms, 10,000x, etc.)
- [ ] Visual hierarchy guides attention
- [ ] Total presentation fits 5-7 minutes
- [ ] Technical terms explained
- [ ] Competitive advantages clear
- [ ] Call to action compelling
- [ ] Contact info correct

---

## 🎬 Presentation Script Outline

### Slide 1 (60s):
"Financial institutions face a critical challenge: Manual SAR writing takes 
2-4 hours per report, and 70% of analyst time is wasted on false positives. 
SignalSAR solves this with real-time SAR generation in less than 1 millisecond—
that's 10,000 times faster than manual processes—while maintaining evidence-
linked explainability and multi-gate governance."

### Slide 2 (90s):
"Let me show you how it works. From alert to regulatory submission takes just 
3 minutes. The analyst sees a risk-sorted queue, clicks investigate, and a 
complete SAR is generated instantly. The system links 7 evidence artifacts, 
the analyst confirms the typology and records their disposition, reviews the 
narrative, and submits with a cryptographic checksum. Every step is audited."

### Slide 3 (90s):
"SignalSAR is built on three pillars. First, speed: sub-millisecond generation 
with 7 typology patterns. Second, governance: 5 validation gates and database-
level immutability ensure regulatory compliance. Third, explainability: every 
claim has evidence, with inline transaction references that regulators can 
trace. This is enterprise-grade compliance at startup speed."

### Slide 4 (60s):
"The architecture is lightweight but production-ready. We use a simple stack—
Flask, SQLite, vanilla JavaScript—but with enterprise features: database 
triggers enforce immutability, foreign key constraints ensure integrity, and 
SHA-256 checksums verify submissions. The modular design makes scaling 
straightforward."

### Slide 5 (90s):
"The impact is measurable: 10,000 times faster than manual processes, 100% 
compliance scores, and immutable audit trails. Compared to manual processes, 
we're faster and more consistent. Compared to other AI solutions, we're 
transparent and human-in-loop. Compared to commercial solutions, we're faster 
and more adaptable. And this isn't vaporware—we have a working prototype with 
verified performance."

### Slide 6 (30s):
"SignalSAR transforms compliance operations with AI-powered speed, human-in-
loop governance, and evidence-linked explainability. We're ready for your 
questions and would love to show you a live demo. Thank you."

---

## 🚨 Common Mistakes to Avoid

1. **Don't overcrowd slides** - 6 slides means each must be focused
2. **Don't skip metrics** - Numbers make claims credible
3. **Don't forget governance** - It's your key differentiator
4. **Don't use jargon** - Explain technical terms
5. **Don't rush the close** - Strong ending matters

---

## 📚 Reference Documents

Keep these open while using Skywork.ai:

1. **SLIDES_ALIGNMENT_ANALYSIS.md** - Verify all claims
2. **REALTIME_SAR_SUMMARY.md** - Performance metrics
3. **This document** - Prompts and structure

---

## 🎯 Success Criteria

Your 6-slide presentation should:

- [ ] Open with compelling problem + solution
- [ ] Show clear product flow
- [ ] Emphasize 3 core innovations
- [ ] Demonstrate technical credibility
- [ ] Prove competitive advantage
- [ ] Close with strong call to action
- [ ] Fit 5-7 minute time slot
- [ ] Use verified metrics throughout

---

## 🚀 Next Steps

1. **Copy Prompt 1** from above
2. **Paste into Skywork.ai**
3. **Review and iterate** if needed
4. **Copy output** to your presentation
5. **Repeat for Prompts 2-6**
6. **Practice timing** (should be 5-7 minutes)
7. **Test demo** to ensure it works

---

Good luck! Your compressed 6-slide presentation will be powerful and memorable. 🎉
