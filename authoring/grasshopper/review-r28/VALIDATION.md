# R28 validation — 28 September 2026

- Full portable regression: **134 tests passed** in 223.465 seconds.
- Final focused room-configurator suite: **13 tests passed**, including later refinements to central passage location, skeleton roof-type response, exposed terrace edges and maximum 1800 mm terrace boards.
- Actual A/B/C GH component scripts exercised with wrapped native-style inputs. Invalid upstream data clears outputs. The native factory compatibility test now covers all three creators.
- Shared preset building generator and arrangement function are deliberately blocked in the plan-to-skeleton test: generation succeeds from the new plan and shared member recipes alone.
- Cases cover duplicates, six rooms, impossible neighbour cycles, open/closed boundaries, exterior access, typed bounds, door fit before geometry, both roof/foundation choices, all terrace modes, all panel options, façade omission, source immutability and assembly completeness.
- A portable 3DM was reopened, object count reconciled, and all objects checked solid. Local plan/skeleton/detail visuals for three programmes were generated and inspected; final plan wall/opening diagrams were rendered.
- The previous main and research creators and canonical construction modules remain unchanged.
- Native Rhino/GH creation, canvas appearance, viewport behaviour, save/reopen and interactive exports remain unverified. No capacity, supplier, habitation or SLD acceptance is asserted.
