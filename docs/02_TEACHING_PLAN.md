# CVHS Drift Trike Build - First Principles Teaching Plan
## Instructor Reference: Mr. McAteer
### Pedagogy: First Principles / Engineering Design Process / Error-Proofing

---

## TEACHING PHILOSOPHY FOR THIS PROJECT

This project teaches by asking "why" before "how." Every decision should be derived from physics, materials science, and engineering logic - not from copying someone else's build. Colton and Atticus have the hands-on skill. This plan gives them the framework to make those skills transferable to ANY fabrication challenge.

**Core Approach:**
1. Start with the physics/math of what needs to happen
2. Let the students derive the solution from constraints
3. Build understanding before building parts
4. Eliminate error through process design, not just caution

---

## PHASE 1: FIRST PRINCIPLES FOUNDATION (Week 1-2)

### Lesson 1.1: "What IS a drift trike?" - Force Analysis

**First Principle:** A drift trike works because the rear wheels have less friction than the front wheel. The front wheel grips (steers), the rear wheels slide (drift).

**Student Exercise - Whiteboard Session:**
- Draw a free body diagram of a trike in a turn
- Identify: centripetal force, friction (front vs rear), weight distribution, CG location
- Calculate: If the rider + trike weighs 300 lbs total, and you're turning at 15 MPH in a 20' radius, what centripetal force is needed? (F = mv²/r)
- Ask: "Where does the friction come from? What happens if rear friction is LESS than centripetal force?" (Answer: drift)
- This is WHY PVC sleeves work - they reduce the coefficient of friction on the rear tires

**Connection to Build:** This tells us:
- Rear track width (wider = more stable, harder to flip)
- CG height (lower = more stable)
- Weight distribution (more weight forward = more front grip = easier to initiate drift)

### Lesson 1.2: "Why does removing the governor matter?" - Thermodynamics & Mechanics

**First Principle:** The governor limits RPM to protect the engine at the cost of power. Power = Torque x RPM.

**Student Exercise:**
- Stock: 6.5 HP @ 3,600 RPM. Calculate torque. (T = HP x 5252 / RPM = 9.5 ft-lbs)
- Stage 2: 13 HP @ 7,500 RPM. Calculate torque. (T = 9.1 ft-lbs)
- Discussion: "Wait - the torque went DOWN? Then why does it feel faster?"
- Answer: Power doubled. The engine does work twice as fast. Torque at the WHEEL is multiplied by the gear ratio.
- Wheel torque = Engine torque x Gear ratio x Drivetrain efficiency
- At 6:1 ratio: 9.1 x 6 x 0.85 = 46.4 ft-lbs at the wheel

**Connection to Build:** This determines gear ratio selection, chain/sprocket sizing, and expected performance.

### Lesson 1.3: "Why does the flywheel need to be billet?" - Materials Science

**First Principle:** Centripetal acceleration at the rim of a spinning flywheel = ω²r. As RPM increases, the force trying to tear the flywheel apart increases with the SQUARE of RPM.

**Student Exercise:**
- Calculate centripetal acceleration at the rim of a 7" diameter flywheel at 3,600 RPM vs 7,500 RPM
- ω = RPM x 2π / 60
- a = ω²r
- At 3,600 RPM: a ≈ 5,000 g's
- At 7,500 RPM: a ≈ 21,700 g's (4.3x higher!)
- Cast iron has micro-voids and grain boundaries that act as crack initiation sites
- Billet aluminum is machined from a solid forged block - no voids, consistent grain
- This is WHY the billet flywheel is a safety requirement, not an optional upgrade

**Connection to Build:** Safety-critical decisions must be derived from physics, not opinion.

### Lesson 1.4: "How strong does the frame need to be?" - Structural Analysis

**First Principle:** Every structural member is either in tension, compression, bending, or torsion (or a combination). The frame must handle all expected loads with a safety factor.

**Student Exercise:**
- Estimate loads: 200 lb rider + 80 lb trike = 280 lbs static
- Dynamic loads (bumps, braking, cornering): multiply by 3x safety factor = 840 lbs design load
- Calculate bending stress in a 1.25" x 1.25" x 0.095" square tube spanning 24" with a 420 lb center point load (half the design load on each rail)
- Section modulus of 1.25" sq tube .095 wall: S ≈ 0.172 in³
- Bending moment: M = PL/4 = 420 x 24 / 4 = 2,520 in-lbs
- Bending stress: σ = M/S = 2,520 / 0.172 = 14,651 PSI
- A-513 (1020/1026 steel) yield strength: ~50,000 PSI
- Factor of safety: 50,000 / 14,651 = 3.4x -- GOOD

**Connection to Build:** The 0.095" wall tube is appropriately sized for main frame rails. The 0.063" wall is fine for secondary structure but NOT for primary load-bearing spans.

---

## PHASE 2: DESIGN (Week 2-3)

### Lesson 2.1: Sketch to CAD

**Exercise:** Students sketch the trike by hand first (3 views: top, side, rear). Then transfer critical dimensions to a simple CAD layout (even graph paper works if no software).

**Key Deliverable:** A dimensioned drawing showing:
- Wheelbase, track width, seat position, engine position
- All tube cuts with lengths and angles
- Gusset locations and sizes
- Axle mount locations

### Lesson 2.2: Cut List and Material Optimization

**First Principle:** Minimize waste by planning all cuts from available stock before cutting anything.

**Student Exercise:**
- Create a cut list from the design
- Map cuts onto the available stock lengths (20', 10', 24')
- Optimize to minimize scrap
- Label each piece

**Error-Proofing:** Cut list goes on the whiteboard. Every cut is checked off as completed. Measure twice, cut once - literally enforce this as process.

### Lesson 2.3: Jig Design

**First Principle:** Jigs eliminate human error in positioning. If two parts must be at a specific angle or distance, build a jig rather than relying on measurement each time.

**Student Exercise:**
- Design a welding jig for the rear frame (can be as simple as angle iron clamped to the welding table)
- Design a jig for cutting tube to consistent lengths
- Design a fixture for aligning the axle mount bearing blocks

---

## PHASE 3: FABRICATION (Week 3-6)

### Lesson 3.1: Engine Build (Small Engines Class)

**Sequence:**
1. Document the stock engine - photos, measurements, compression test
2. Disassemble following shop manual procedure
3. Remove governor components
4. Install billet flywheel (proper torque specs - look up and USE a torque wrench)
5. Install billet connecting rod
6. Install cam, valve springs
7. Reassemble with new gaskets
8. Set valve lash
9. Install performance air filter, exhaust, carb (if upgrading)

**Error-Proofing Techniques:**
- Photo-document each step before and after
- Use parts trays labeled for each sub-assembly
- Torque specs written on whiteboard for each fastener
- Two-person verification: one person torques, other verifies and checks off

### Lesson 3.2: Frame Fabrication (Metals/Fab Class)

**Sequence:**
1. Prepare donor bicycle (cut, clean, inspect)
2. Cut all frame tubes per cut list (mark each piece)
3. Deburr and prep all cuts
4. Tack-weld rear frame on flat table using jig
5. Check for square (diagonal measurements must be equal)
6. Full weld rear frame
7. Fit bicycle front end to rear frame
8. Tack junction, check alignment (is the front wheel centered?)
9. Weld junction with gussets
10. Fabricate and weld engine mount
11. Fabricate and weld axle bearing mounts
12. Fabricate seat mount, foot pegs, chain guard
13. Grind/clean all welds
14. Test fit engine, axle, wheels before paint

**Error-Proofing Techniques:**
- Always tack first, check, then full weld
- Use string lines to check frame alignment
- Measure diagonals for square at every major step
- "Dry fit" (clamp without welding) all components before welding
- Keep a running photo log

### Lesson 3.3: Machining Components (Mill/Lathe Work)

**Potential Projects for the Students:**
1. **Hub adapters** - If using Colton's Amazon wheels, machine adapter plates to mate wheel bolt pattern to axle hub bolt pattern
2. **Axle bearing mount plates** - CNC plasma cut, then face on mill for flatness
3. **Brake caliper mounting bracket** - Design and machine from flat stock
4. **Engine mounting plate** - If using plate mount, CNC plasma and drill
5. **Gusset plates** - CNC plasma from 1/4" or 3/16" plate

**Lathe Projects:**
- Turn any spacers/bushings needed for axle assembly
- Face bearing mount plates for flush fit
- Turn hub adapters if going round-to-round

---

## PHASE 4: ASSEMBLY AND TEST (Week 6-8)

### Lesson 4.1: Systems Integration

**First Principle:** Assemble in order of "hardest to change later" first.

**Sequence:**
1. Install axle and bearings (critical alignment)
2. Install engine on mount
3. Install torque converter or clutch
4. Install chain, set tension
5. Install wheels
6. Install brakes (front and rear)
7. Install controls (throttle, brake levers, kill switches)
8. Route all cables cleanly
9. Install tether kill switch
10. Final safety inspection (checklist - see student docs)

### Lesson 4.2: Testing Protocol

See Engineering Plan Section 10 for the three-phase test protocol.

**Key Teaching Moment:** The test protocol IS the engineering. Building the trike is only half the project. Validating that it works safely is the other half. Professional engineers spend as much time on testing as on design.

---

## PHASE 5: REFLECTION AND DOCUMENTATION (Week 8-9)

### Lesson 5.1: Performance Analysis

**Student Exercise:**
- Measure actual top speed (GPS app on phone)
- Compare to calculated top speed from gear ratio math
- Discuss sources of error (friction losses, tire slip, wind resistance)
- Calculate actual power at the wheel using acceleration data (if ambitious)

### Lesson 5.2: Design Review

**Student Exercise:**
- What would you change?
- What broke or needed modification?
- What was over-engineered? Under-engineered?
- How would you make it lighter? Faster? Safer?
- Write a one-page "lessons learned" document

### Lesson 5.3: Presentation

**Student Deliverable:** Present the project to the class, administration, or at a school event:
- Problem statement
- Design choices and WHY (first principles reasoning)
- Fabrication process
- Test results
- What they learned

---

## ELIMINATING HUMAN ERROR - SYSTEMATIC APPROACHES

These are process-level techniques that Mr. McAteer should embed into the workflow:

| Technique | Application |
|-----------|------------|
| **Checklists** | Pre-ride safety check, engine build torque sequence, weld prep checklist |
| **Two-Person Verification** | All critical measurements, all torque values, all safety checks |
| **Jigs and Fixtures** | Frame welding alignment, consistent tube cuts, axle alignment |
| **Photo Documentation** | Every step photographed before and after - creates accountability and reference |
| **Cut Once, Check Twice** | No tube gets cut without two independent measurements agreeing |
| **Dry Assembly** | Everything gets clamped and test-fit before permanent joining |
| **Written Procedures** | Students write the procedure BEFORE doing the work (forces thinking ahead) |
| **Color Coding** | Mark 0.095 wall tubes with one color, 0.063 with another - prevents mix-ups |

---

## ASSESSMENT RUBRIC (Suggested)

| Category | Weight | Criteria |
|----------|--------|----------|
| Engineering Documentation | 20% | Drawings, calculations, cut lists, procedures |
| Fabrication Quality | 25% | Weld quality, fit-up, dimensional accuracy |
| Engine Build | 20% | Proper assembly, torque specs, break-in procedure |
| Safety Implementation | 20% | All safety systems functional, testing completed |
| Reflection/Presentation | 15% | Lessons learned, first-principles reasoning demonstrated |

---

## STANDARDS ALIGNMENT

This project naturally aligns with:
- **NGSS Engineering Practices:** Defining problems, developing models, planning investigations, analyzing data, designing solutions
- **CTE Welding/Fabrication Standards:** Joint design, welding processes, blueprint reading, measurement
- **CTE Small Engine Standards:** Engine theory, disassembly/reassembly, troubleshooting, performance modification
- **Math Application:** Geometry, algebra, unit conversion, ratio/proportion
- **Physics Application:** Forces, energy, rotational dynamics, friction, materials properties

---

*Teaching plan prepared for Mr. McAteer, CVHS*
*First Principles Approach: Understand WHY before HOW*
