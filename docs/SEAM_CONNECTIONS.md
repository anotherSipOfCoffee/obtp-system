# Floor and roof seam connections

Original source: WikiHouse Skylark150 6581cc1de0f4daef81a6b5c5a2eaed3c537d1d8f; existing F-S, R-S, TIES.dxf geometry unchanged.

Each adjacent pair at 600 mm pitch now has 12 full ties in the floor top-deck seam and 14 in the roof top-deck seam. No bottom-skin seam row was invented. Roof ties follow the source's one-degree plane, not a level approximation. deckSeamTies in dist/catalogue.js is the shared authority consumed by Studio.

Source floor socket Y centres after placement: 583.453, 988.547, 1183.453, 1588.547, 1783.453, 2188.547, 2383.453, 2788.547, 2983.453, 3388.547, 3583.453, 3988.547 mm; source top deck Z=380. Roof socket centres are extracted from the original top-skin boundary vertices on the flattened one-degree plane at height 225.46 mm. Exact world transforms are recorded in the audit.

52 accepted sampled sections: both 4.5 and 13.5 mm depths at every floor and roof seam socket. Maximum reported overlap 0.649382 mm². This is source-mesh geometric evidence, not full-volume, strength, tool access, installation order or fabrication-clearance approval. The open R-S Brep remains unchanged.

The 2D tessellated tie rings are normalized with buffer(0) for section calculations to remove numerical self-intersections. This is an audit-polygon operation only; source CAD and display meshes are unchanged. Additional end-wall trials in the same audit are rejected and are NOT included in this passing result.

Full open-row count for N modules is now 78N−50, including 74N−50 full ties; W-S 2N, F-S N, R-S N. A four-module row contains 262 instances; eight modules contain 574. The one-module case remains 28. Layer views omit ties as before.

End-wall closure and openings remain incomplete. See OPENINGS_AND_ENDWALLS_CHECKPOINT.md.
