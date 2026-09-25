# Foundation bearing and wall aperture · geometry study

## Foundation

The optional `includeFoundation` System generator switch adds two continuous, 300 mm wide, 200 mm deep **illustrative** bearing strips below the 4,572 mm floor span. Their centrelines lie near the long perimeter edges; transverse separation is 4,572 mm. One floor–support interface is recorded for each 600 mm floor bay, with `capacity:null` and `fasteners:null`. A support strip in a viewer is a coordination geometry, not a verified footing, foundation depth, ground beam, drainage design or buildable detail. There is no soil bearing value or structural reaction in the project. The bottom is 200 mm below the assumed terrain datum, and the top is at datum; the generated roof remains below the 5 m dimensional screen.

A site-specific foundation choice needs geotechnical ground and groundwater information, actions, settlement/frost assessment, drainage and a designed route for uplift and lateral force from roof through wall and floor to the ground. Do not size footing width, depth, reinforcement, anchorage or excavation from the illustrative strip. JRC's [Eurocode 7 geotechnical design overview](https://eurocodes.jrc.ec.europa.eu/EN-Eurocodes/eurocode-7-geotechnical-design) identifies ground investigation and foundation verification; Lithuania's [STR 2.05.21:2016 geotechnical requirements](https://e-tar.lt/rs/actualedition/f701a690440311e6bd3bfefc575ccac4/LtSmGVkCBa/) and the Lithuanian building inspectorate's [IGG explanation](https://vtpsi.lrv.lt/lt/naujienos/inzineriniai-geologiniai-ir-geotechniniai-tyrimai-igg-ka-apie-juos-reikia-zinoti-projektuojant-pastatus/) govern the site-specific path.

## Cassette window object

`openingStudy()` exposes one standalone 1,200 mm wide, 195 mm deep, 2,100 mm high wall object study: two 90 mm jamb regions, a 900 mm sill, an upper 90 mm header and two sheet zones. The nominal aperture is 1,020 mm wide from z=945 to 1,800 mm; it is **not placed** into an assembly, and the on-screen openings controls remain disabled. No header load, stud/header connection, sheet edge fastening, weather sealing, glazing or thermal detail has been verified. A door cannot be inferred from this window object. The study is kept separate to avoid silently removing structural wall pieces from a valid generated shell.

## Material quantity

`woodVolume(scene)` sums the axis-aligned solid bounding-box volume of each `timber` and `plywood` part in each instantiated System cassette, in m³. Plywood is included; concrete foundation and generic furniture are excluded. No waste factor, procurement cut list, density, grade or fastening is included. Visible layer or hidden skins must not be used for a whole-building purchase quantity: generate with `layer:'all', skin:true` for that purpose. The result currently describes the earlier 4,572 mm shell, not the owner's narrow solved Sauna layout.
