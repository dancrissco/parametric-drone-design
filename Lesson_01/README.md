Lesson 01 – Parametric Inflatable Tube Ring (HawaFrame)

This is the first lesson in our Parametric Drone Design Series, where we build the foundational geometry of the HawaFrame:
a fully parametric inflatable ring, controlled entirely by variables and constructed using OnShape's Sweep feature.

This tubular ring establishes the core layout for all future lessons (arms, motor placement, mounts, ducts, and structural connectors).

🎯 Learning Objectives

By the end of this lesson, you will be able to:

Create and manage parametric variables in OnShape

Build an inflatable torus-like tube ring driven by mission geometry

Understand how prop size → motor radius → prop-tip radius → tube radius relate

Use Sweep to extrude a circular profile along a circular path

Prepare the correct geometry for Lesson 02 (arm placement + motor layout)

📐 Overview of the Geometry

All geometry in this lesson matches the Python Configurator (v4.1).
The configurator computes:

#prop_diameter
#prop_radius
#motor_radius               (safe spacing)
#prop_tip_radius
#clearance_prop_to_tube
#tube_inner_radius
#tube_OD
#tube_center_radius
#tube_outer_radius
#ring_OD


The tube has three important radii:

tube_inner_radius → inside of the inflatable tube

tube_center_radius → centerline path of the tube

tube_outer_radius → outer surface of the tube

In this lesson we will model the actual tube, not a flat ring.

📁 Setup Instructions

Create a new OnShape document:

Name: Parametric Drone – Lesson 01 (Inflatable Ring)

In Part Studio 1, enable the Variable Table (fx icon).

1️⃣ Step 1 — Define Variables

Enter the following variables in OnShape exactly as shown:

Variable	Expression	Purpose
#prop_diameter	660 mm	Example for 26-inch props
#prop_radius	#prop_diameter / 2	Auto
#arm_clearance_factor	0.3	Control motor spacing (nominal)
#motor_radius_nominal	#prop_radius + (#arm_clearance_factor * #prop_diameter)	Base motor spacing
#prop_prop_clearance	20 mm	Minimum prop–prop gap
#motor_radius	(paste from configurator)	Actual safe motor radius
#prop_tip_radius	#motor_radius + #prop_radius	Prop tip location
#clearance_prop_to_tube	30 mm	Gap from prop tip to tube
#tube_inner_radius	#prop_tip_radius + #clearance_prop_to_tube	Inside wall of tube
#tube_OD	132 mm	Tube thickness (OD)
#tube_center_radius	#tube_inner_radius + #tube_OD / 2	Sweep path radius
#tube_outer_radius	#tube_inner_radius + #tube_OD	Outside of tube
#ring_OD	2 * #tube_outer_radius	For reference

You can paste the variable block straight from the Configurator’s output.

2️⃣ Step 2 — Sketch the Tube Path (Top Plane)

Create a new sketch on the Top Plane.

Draw a construction circle centered at the origin.

Dimension its radius as:

#tube_center_radius


Fully constrain and finish the sketch.

This is the circular path that the tube will sweep around.

Rename sketch → Tube_Path.

3️⃣ Step 3 — Sketch the Tube Cross-Section (Right Plane)

Create a new sketch on the Right Plane.

Draw a horizontal construction line from the origin to the right.

Dimension the line length to:

#tube_center_radius


(This positions the tube exactly where it belongs.)

At the end of the line, draw a circle.

Dimension the circle’s diameter as:

#tube_OD


Fully constrain and finish sketch.

Rename → Tube_Section.

4️⃣ Step 4 — Sweep the Tubular Ring (THIS is the real “extrusion”)

Now we create the true inflatable ring:

Go to Sweep.

Profile → select the circle from Tube_Section.

Path → select the circle from Tube_Path.

Operation → New.

Click OK.

🎉 You have now created a fully parametric tubular ring.

This is the exact inflatable geometry used in HawaFrame.

5️⃣ Step 5 — Verify the Geometry

Use OnShape’s Measure Tool:

From origin → inside of tube = #tube_inner_radius

From origin → outside of tube = #tube_outer_radius

From origin → mid-thickness = #tube_center_radius

All values should match the configurator’s output.

6️⃣ Step 6 — Save Your Work

Rename the part:

Ring_v1


This ring is now ready for Lesson 2, where we will:

place motors

build parametric arms

create symmetric or asymmetric layouts

generate OnShape assemblies driven by the same variables

🎓 What’s Next

Proceed to:
Lesson 02 – Parametric Arms & Motor Layout

In that lesson you will:

attach arms to the ring

position motors using the motor radius

construct polar patterns (4, 6, 8 motors)

build swivel, tilt, and mount geometry

🙌 Contributions

If you improve the variables, add checks, or generate new functions from the Configurator, please submit a Pull Request or Issue.

This repository is meant to be a living educational engineering tool.
