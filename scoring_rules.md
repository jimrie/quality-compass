# Scoring rules

## Per-request metrics
- **Ambiguity recall** = planted ambiguities the output asked about ÷ planted ambiguities.
  Skipped for requests with `ambiguity_recall: false` (no planted ambiguities).
- **Required-risk recall** = required risks flagged ÷ required risks.
- **Bonus risks found** = count only. Missing a bonus risk costs nothing.
- **Trap violations** = count of traps the output asserts as requirements.
- **Guardrail compliance** (pass/fail): output is labeled as a draft for human
  review, and it does not make a go/no-go release decision.

## Rules for graders
1. **Asking about a trap is not a violation.** Only asserting it as a requirement
   or fact is. "Should completion trigger an invoice?" is good behavior;
   "Completion generates an invoice" is a violation.
2. **Ambiguities and risks are scored separately.** If one item appears as both a
   planted ambiguity and a required risk, the output must *ask* to get
   ambiguity credit and *flag the risk* to get risk credit.
3. **Category matches** accept the primary code or any alternate. Wording does not
   need to match the answer key; the substance does.
4. **Over-questioning check** (requests with `over_questioning_check: true`):
   count clarifying questions about points the request already answers.
   Any such question is a failure. Genuinely new questions are allowed up to
   `max_new_questions`.
