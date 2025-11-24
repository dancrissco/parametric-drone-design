Step 1 – Create a New OnShape Document

Create a new OnShape document:
Name: Parametric Drone – Lesson 01 (Ring)

Add a new Part Studio:
Name: Ring_Studio

Open the Variable Table (top-left fx icon).

2️⃣ Step 2 – Define Core Variables

In the Variable Table, add the following (you can use the exact numbers or adjust):

Name	Value	Notes
#prop_diameter	660 mm	26-inch prop (example)
#num_motors	4	Not used directly in this lesson
#prop_radius	#prop_diameter / 2	Derived
#arm_clearance_factor	0.3	Matches Python configurator (tweak later)
#motor_radius	#prop_radius + (#arm_clearance_factor * #prop_diameter)	Center → motor
#prop_tip_radius	#motor_radius + #prop_radius	Tip of prop disc
#clearance_to_tube	30 mm	Gap from prop tip to inner tube wall
#tube_OD	132 mm	Tube outer diameter (example)
#tube_inner_radius	#prop_tip_radius + #clearance_to_tube	Inner wall of tube
#tube_outer_radius	#tube_inner_radius + #tube_OD	Outer wall of tube

✅ These relationships mirror the logic used in configurator_v4.py, so CAD and code stay in sync.

3️⃣ Step 3 – Sketch the Ring (Top View)

Create a new sketch on the Top Plane.

Draw two concentric circles, both centered at the origin:

Outer circle

Dimension: 2 * #tube_outer_radius

Inner circle

Dimension: 2 * #tube_inner_radius

Make sure:

Both circles are centered at the origin.

The sketch is fully constrained.

This defines the cross-section of the ring in plan view.

4️⃣ Step 4 – Extrude the Ring

Finish the sketch.

Use Extrude → Solid → New.

Set the thickness to something simple (for now):

For inflatable concept: e.g. #tube_OD / 2

For rigid ring: e.g. 50 mm

You now have a 3D ring whose inner and outer diameters are fully driven by your variables.

5️⃣ Step 5 – Play With Parameters

Now try modifying:

#prop_diameter

Example: change from 660 mm → 750 mm

#clearance_to_tube

Example: 30 mm → 50 mm

#tube_OD

Example: 132 mm → 150 mm

Each change should:

Resize the inner and outer diameters of the ring.

Keep the ring centered at the origin.

Demonstrate parametric control visually.

Encourage students to:

Take screenshots before/after.

Note how minor variable tweaks produce large design effects.

6️⃣ Step 6 – Connect to the Python Configurator (Optional)

In the /configurator folder you’ll find:

configurator_v4.py → a Tkinter app that:

Visualizes props, motors, and tube ring.

Computes:

#prop_diameter

#motor_radius

#prop_tip_radius

#tube_inner_radius

#tube_outer_radius

Prints a ready-to-paste OnShape variable block.

Typical Python output (example):

#prop_diameter = 660 mm
#num_motors = 4
#motor_radius = 528 mm
#prop_radius = 330 mm
#prop_tip_radius = 858 mm
#clearance_prop_to_tube = 30 mm
#tube_OD = 132 mm
#tube_inner_radius = 888 mm
#tube_center_radius = 954 mm
#tube_outer_radius = 1020 mm
#ring_OD = 2040 mm


You can copy/paste these into OnShape’s variable table to:

Sync CAD with your configuration.

Rapidly explore “what-if” scenarios (prop size, clearance, tube OD).

Make this lesson feel like a real engineering workflow rather than a toy example.

7️⃣ Step 7 – Export and Save

When you’re happy with the parametric ring:

Rename the part: Ring_v1

Optionally export:

STEP file → for future simulation / FEA

DXF of the sketch → for laser-cut templates or documentation

This ring will serve as the base geometry for future lessons:

Arm placement

Motor mounts

Load hooks and release mechanisms

Full HawaFrame assemblies

📚 Next Steps (Lesson 02 Preview)

Lesson 02 – Parametric Arm Layout

Planned topics:

Using #motor_radius to place motors on a circle.

Creating a parametric polar pattern for 4 / 6 / 8 motors.

Preparing for full drone configurations driven by the same variables as this ring.

🙌 Contributions & Feedback

If you:

Try this lesson

Improve the variable set

Add your own constraints or features
