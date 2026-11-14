# Unresolved conflicts

Autonomous mode: these are noted, not resolved. Each needs the problem owner or the team.

1. **Reason vocabulary.** reason_codes lists 14 codes; application_truth uses 5 others (FACE_LOW, POOR_QUALITY, NAME_SPELLING, NAME_MISMATCH_HARD, ADDRESS_STATE_MISMATCH (INFORMATIONAL ONLY)) and never uses 7 of the 14.
   - Suggested handling: Map both vocabularies; score on the truth vocabulary; strip the "(INFORMATIONAL ONLY)" suffix when parsing.
2. **T4 wording vs Specimen 6.** Brief says Aadhaar and marksheet both carry a different name; the NAME_MISMATCH_HARD specimen has it on the marksheet only.
   - Suggested handling: Trigger on any one document carrying a different person.
3. **Auto reject vs human confirm.** Rulebook §6 says any REJECT reason means REJECT; §9 and the brief say NAME_MISMATCH is only recommended.
   - Suggested handling: Output "recommend REJECT, route to human"; count it as correct for REJECT recall.
4. **Reviewer accuracy baseline.** Brief: 97.5% at document level. My application-level roll-up of the same verdicts: 87.0% (522 of 600).
   - Suggested handling: Report both and say which is which; the roll-up rule is my assumption.
5. **"27% never reply".** Data gives 24.8% (never re-uploaded), 27.3% (dropped before KYC) and 42.6% (returned and later dropped).
   - Suggested handling: Pick one definition for the before/after baseline and state it.
6. **Cheque vs penny-drop name.** In all 31 BANK_NAME_MISMATCH cases the two names are different people.
   - Suggested handling: Synthetic artifact; use the penny-drop name as the rule input and flag disagreement.
7. **Exam pass mark.** Data: failures are "Score below 40%". Our demo exam says 50% to pass; the rulebook gives no pass mark.
   - Suggested handling: Align the placeholder to 40% or label it clearly as a demo rule. Needs an owner decision.
8. **Recognised-board list.** Rulebook §4.4 and §9 make unlisted boards Human only but supply no list.
   - Suggested handling: Unresolved: the list must come from the problem owner; today it is inferred from the test set.
9. **O/0 noise vs invalid PAN.** README says O/0 noise is common; Specimen 10 and two other PANs have a letter in a digit position and are REJECT PAN_FORMAT_INVALID.
   - Suggested handling: Unresolved in general; resolved in this data only because typed PAN equals the card (§4.2).
