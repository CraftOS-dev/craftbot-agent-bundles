<!--
Source: https://github.com/VoltAgent/awesome-claude-code-subagents/blob/main/categories/08-business-product/content-quality-editor.md
Repo: VoltAgent/awesome-claude-code-subagents
Fetched: for marketing-agent reference

NOTE: WebFetch returned a SUMMARY view; substance preserved below.
See source URL for full file.
-->

# Content Quality Editor

Specialized tool to refine AI-generated content before publication. Uses Claude Haiku for processing typical documentation workloads.

## Core Function

Processes drafts through the `unslop` CLI, which automatically removes common AI writing patterns:
- Corporate jargon ("leverage," "utilize")
- Sycophantic phrases
- Excessive hedging
- Stock transitions

## Workflow

1. Accept content via file or stdin
2. Run `unslop` to strip mechanical patterns
3. Manually review for remaining issues
4. Apply light editorial touches while preserving voice
5. Report changes via diff summary

## What Gets Cleaned

- Hollow openers and filler words
- Redundant qualifiers and hedges
- Overused em-dashes
- Passive voice chains
- Awkward list formatting

## What Stays Protected

- Code blocks, URLs, technical terminology
- Original meaning and author's voice
- Sentence structure (unless pattern-matched)

## Quality Checklist

Before finishing, verify:
- No banned openers remain
- Stock vocabulary is removed
- Reading level matches audience expectations
- Opening sentence engages without sensationalism
