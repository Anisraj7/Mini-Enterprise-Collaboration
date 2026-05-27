# TODO

- [x] Inspect escalation/delegation services and approval action authorization.
- [x] Identify root cause: approval action authorization ignores escalation/delegation.
- [x] Patch `backend/app/services/approval_service.py` to allow escalated user to act.
- [ ] Add delegation authorization support in approval actions.
- [ ] Add pytest test suite for escalation + delegation authorization and state changes.
- [ ] (Optional) Fix/align frontend if tests show schema mismatch.
