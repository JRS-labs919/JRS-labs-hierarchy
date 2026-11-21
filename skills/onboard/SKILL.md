---
name: "onboard"
description: Set up or refresh JRS company context so future departments do not repeatedly ask about the business, tools, decision owners and output style. Use for "set up JRS", "teach JRS about my company", "update our company profile" or /jrs:onboard.
---

# JRS-Onboard

Create or refresh `jrs/company-profile.md` in the current working folder. This is the shared context
card departments use to avoid rediscovering stable company facts. It is not a credential store, an
approval policy or a replacement for department house standards.

## Rules

1. Read an existing profile first. Preserve facts that are still supported; never erase a useful
   section merely because the current request does not mention it.
2. Inspect accessible README, company, product and project documentation before asking questions.
   Record the file path behind an observed fact. Do not trawl unrelated personal files.
3. Ask at most one short batch of missing questions. Skip anything already answered by the prompt or
   evidence. A new profile should try to learn: company name and offering, customer/audience, current
   priorities, tools by function, decision owners or approval boundaries, vocabulary, output style,
   and two or three recurring workflows.
4. Never store credentials, tokens, passwords, private keys, payment details, health data or
   unnecessary personal information. Store system names, not access secrets.
5. Mark each entry `Observed`, `Reported`, `Assumption`, or `Unknown`. A user statement is Reported;
   a readable source is Observed. Never convert an assumption into a fact.
6. House standards outrank this profile for a department-specific rule. The current user request and
   repository evidence outrank stale profile text.
7. Use no tier agents or Principal. Onboarding is Lean and should be completed in the session.

## Workflow

### 1. Assess

Read only likely context sources and the existing profile. Summarize what is already known and what
would materially improve future work. Do not connect tools or retrieve business data merely to fill
the profile.

### 2. Clarify once

If critical context is missing, ask one grouped set of no more than seven short questions. The user
may skip any question. If they asked for a quick setup, collect only identity, offering, priorities,
preferred output style and recurring work.

### 3. Write the context card

Use this shape:

```markdown
# JRS company profile
Updated: <yyyy-mm-dd>

## Identity and offering
- <fact> — <Observed: path | Reported: date | Assumption | Unknown>

## Customers and priorities
- ...

## Products and terminology
- ...

## Tools by function
- <function>: <system names only> — <source>

## Decision owners and boundaries
- <decision>: <named role, not invented person> — <source>

## Output preferences
- ...

## Recurring workflows
- <request phrase> -> <JRS department or named chain>

## Unknowns to resolve when relevant
- <unknown> — owner: <role or user>
```

Keep it under 1,200 words. Include only stable, reusable context. Put task-specific facts in the task
record instead.

### 4. Recommend a starting set

Name at most three JRS commands that fit the reported recurring work. Recommend `/jrs:route` when the
owner is unsure where to start. Do not list the whole catalog.

## Report

```
VERDICT: <created | updated | blocked>
USAGE: Lean onboarding - 0 tier-agent dispatches; 0 Principal calls; budget met
PROFILE: <path>
CAPTURED: <sections added or refreshed>
IGNORED: <sensitive or task-specific information deliberately excluded>
START WITH: <at most three commands and why>
OPEN ITEMS: <unknowns that matter later>
```

