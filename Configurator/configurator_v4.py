import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import math

G = 9.81  # m/s^2

# ---------------------------------------------------------------------
# Simple prop/motor "database"
# max_thrust_N values are rough placeholders – update with real test data later
# ---------------------------------------------------------------------
PROP_DB = {
    "10": {"max_thrust_N": 40},
    "12": {"max_thrust_N": 60},
    "14": {"max_thrust_N": 80},
    "16": {"max_thrust_N": 110},
    "18": {"max_thrust_N": 140},
    "20": {"max_thrust_N": 170},
    "22": {"max_thrust_N": 200},
    "24": {"max_thrust_N": 230},
    "26": {"max_thrust_N": 260},
    "30": {"max_thrust_N": 320},
}

# Will hold the latest OnShape variable block text after Compute()
last_oshape_block = ""

# Canvas reference (set later)
layout_canvas = None


# ---------------------------------------------------------------------
# Coordinate helpers
# ---------------------------------------------------------------------
def mm_to_canvas(x_mm, y_mm, scale, cx, cy):
    """
    Convert mm coordinates (x_mm, y_mm) to canvas pixel coordinates,
    with (0,0) at center, +x to the right, +y up.
    Canvas y increases downward, so we invert y.
    """
    x_px = cx + x_mm * scale
    y_px = cy - y_mm * scale
    return x_px, y_px


def draw_layout(
    tube_outer_radius_mm,
    tube_inner_radius_mm,
    prop_radius_mm,
    motor_radius_mm,
    n_motors,
):
    """
    Draw top-view layout on the canvas:
    - Outer + inner tube circles
    - Arms from center to each motor
    - Motor dots
    - Prop discs
    """
    global layout_canvas
    if layout_canvas is None:
        return

    layout_canvas.delete("all")

    if (
        tube_outer_radius_mm <= 0
        or tube_inner_radius_mm <= 0
        or motor_radius_mm <= 0
        or n_motors <= 0
    ):
        return

    width = int(layout_canvas["width"])
    height = int(layout_canvas["height"])
    cx = width / 2
    cy = height / 2

    # Scale so outer tube fits with margin
    max_radius_mm = tube_outer_radius_mm
    margin_factor = 0.9
    scale = margin_factor * min(width, height) / 2 / max_radius_mm

    if not (scale > 0 and scale < 1e6):
        print("DEBUG: invalid scale:", scale)
        return

    # Draw outer tube
    outer_r_px = tube_outer_radius_mm * scale
    layout_canvas.create_oval(
        cx - outer_r_px,
        cy - outer_r_px,
        cx + outer_r_px,
        cy + outer_r_px,
        width=2,
    )

    # Draw inner tube (to show wall thickness)
    inner_r_px = tube_inner_radius_mm * scale
    layout_canvas.create_oval(
        cx - inner_r_px,
        cy - inner_r_px,
        cx + inner_r_px,
        cy + inner_r_px,
        width=1,
    )

    # Draw each motor & prop
    for i in range(n_motors):
        angle = 2.0 * math.pi * i / float(n_motors)

        # Motor position at motor_radius_mm
        mx_mm = motor_radius_mm * math.cos(angle)
        my_mm = motor_radius_mm * math.sin(angle)
        mx_px, my_px = mm_to_canvas(mx_mm, my_mm, scale, cx, cy)

        # Arm
        layout_canvas.create_line(cx, cy, mx_px, my_px, width=1)

        # Prop disc
        prop_r_px = prop_radius_mm * scale
        layout_canvas.create_oval(
            mx_px - prop_r_px,
            my_px - prop_r_px,
            mx_px + prop_r_px,
            my_px + prop_r_px,
            outline="gray",
        )

        # Motor dot
        motor_dot_r = 4
        layout_canvas.create_oval(
            mx_px - motor_dot_r,
            my_px - motor_dot_r,
            mx_px + motor_dot_r,
            my_px + motor_dot_r,
            width=1,
        )


# ---------------------------------------------------------------------
# Core computation
# ---------------------------------------------------------------------
def compute():
    """Compute geometry + thrust, update text output + OnShape block + drawing."""
    global last_oshape_block

    # ---- Parse inputs safely ----
    try:
        prop_in = float(str(prop_size_var.get()).strip())
        n_motors = int(str(num_motors_var.get()).strip())
        payload_kg = float(str(payload_var.get()).strip() or 0.0)
        frame_kg = float(str(frame_var.get()).strip() or 0.0)
        twr = float(str(twr_var.get()).strip() or 2.0)
        clearance_mm = float(str(clearance_var.get()).strip() or 0.0)
    except ValueError:
        output_text.config(state="normal")
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Please check your inputs (numbers only).")
        output_text.config(state="disabled")
        last_oshape_block = ""
        return

    if n_motors <= 0:
        output_text.config(state="normal")
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "Number of motors must be greater than zero.")
        output_text.config(state="disabled")
        last_oshape_block = ""
        return

    if clearance_mm < 0:
        clearance_mm = 0.0  # no negative clearances

    # ---- Geometry ----
    # Prop size
    prop_mm = prop_in * 25.4
    prop_radius = prop_mm / 2.0

    # Motor radius (center → motor)
    motor_radius = prop_radius + 0.3 * prop_mm  # tweak 0.3 as needed

    # Prop tip radius from center
    prop_tip_radius = motor_radius + prop_radius

    # Clearance from prop tip to INNER tube wall
    tube_inner_radius = prop_tip_radius + clearance_mm

    # Simple rule-of-thumb tube OD: at least 100 mm, or 20% of prop diameter
    tube_OD_mm = max(100.0, 0.20 * prop_mm)
    tube_wall_mm = tube_OD_mm / 2.0  # just a placeholder; adjust later

    # Tube centerline & outer radius
    tube_center_radius = tube_inner_radius + tube_OD_mm / 2.0
    tube_outer_radius = tube_inner_radius + tube_OD_mm

    ring_OD = 2.0 * tube_outer_radius

    # ---- Thrust calculations ----
    total_mass = payload_kg + frame_kg         # kg
    total_weight = total_mass * G              # N
    total_thrust_required = twr * total_weight # N
    thrust_per_motor = total_thrust_required / n_motors

    # ---- Motor suitability ----
    prop_key = str(prop_size_var.get()).strip()
    max_thrust_N = PROP_DB.get(prop_key, {}).get("max_thrust_N")

    status_lines = []
    if max_thrust_N is None:
        status_lines.append(
            "Motor status: No motor data for this prop size (update PROP_DB)."
        )
    else:
        if thrust_per_motor <= 0:
            status_lines.append(
                "Motor status: Thrust per motor is zero or negative (check inputs)."
            )
        else:
            margin_ratio = max_thrust_N / thrust_per_motor
            margin_pct = (margin_ratio - 1.0) * 100.0
            if margin_ratio >= 1.3:
                status_lines.append(
                    f"Motor status: OK – est. margin ≈ {margin_pct:.0f}% above required thrust."
                )
            elif margin_ratio >= 1.0:
                status_lines.append(
                    f"Motor status: BORDERLINE – only ≈ {margin_pct:.0f}% margin above required thrust."
                )
            else:
                shortfall_pct = (1.0 - margin_ratio) * 100.0
                status_lines.append(
                    f"Motor status: UNDERPOWERED – short by ≈ {shortfall_pct:.0f}% of required thrust."
                )
            status_lines.append(
                f"(DB max thrust per motor: {max_thrust_N:.0f} N, required: {thrust_per_motor:.0f} N)"
            )

    # ---- OnShape variable block ----
    oshape_lines = [
        "=== OnShape variable block (copy-paste) ===",
        f"#prop_diameter = {prop_mm:.0f} mm",
        f"#num_motors = {n_motors}",
        f"#motor_radius = {motor_radius:.0f} mm  // center to motor",
        f"#prop_radius = {prop_radius:.0f} mm",
        f"#prop_tip_radius = {prop_tip_radius:.0f} mm",
        f"#clearance_prop_to_tube = {clearance_mm:.0f} mm",
        f"#tube_OD = {tube_OD_mm:.0f} mm",
        f"#tube_wall = {tube_wall_mm:.0f} mm   // placeholder",
        f"#tube_inner_radius = {tube_inner_radius:.0f} mm",
        f"#tube_center_radius = {tube_center_radius:.0f} mm",
        f"#tube_outer_radius = {tube_outer_radius:.0f} mm",
        f"#ring_OD = {ring_OD:.0f} mm",
    ]
    # Persist only the actual variables (without the heading) for save-to-file
    last_oshape_block = "\n".join(oshape_lines[1:])

    # ---- Build full text output for the GUI ----
    lines = []
    lines.append("=== CONFIG RESULTS ===")
    lines.append(f"Prop diameter: {prop_in:.1f} in  ({prop_mm:.0f} mm)")
    lines.append(f"Number of motors: {n_motors}")
    lines.append("")
    lines.append(f"Motor radius (center → motor): {motor_radius:.0f} mm")
    lines.append(f"Prop radius: {prop_radius:.0f} mm")
    lines.append(f"Prop tip radius: {prop_tip_radius:.0f} mm")
    lines.append(f"Prop-tip clearance to tube inner wall: {clearance_mm:.0f} mm")
    lines.append(f"Tube OD (auto): {tube_OD_mm:.0f} mm")
    lines.append(f"Tube inner radius: {tube_inner_radius:.0f} mm")
    lines.append(f"Tube center radius: {tube_center_radius:.0f} mm")
    lines.append(f"Tube outer radius: {tube_outer_radius:.0f} mm")
    lines.append(f"Ring OD (overall frame): {ring_OD:.0f} mm")
    lines.append("")
    lines.append(f"Total mass (payload + frame): {total_mass:.2f} kg")
    lines.append(f"Desired T/W: {twr:.2f}")
    lines.append(f"Total thrust required: {total_thrust_required:.0f} N")
    lines.append(f"Thrust per motor: {thrust_per_motor:.0f} N")
    lines.append("")
    lines.extend(status_lines)
    lines.append("")
    lines.extend(oshape_lines)

    output = "\n".join(lines)

    # ---- Show in text box ----
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, output)
    output_text.config(state="disabled")

    # ---- Update drawing ----
    draw_layout(
        tube_outer_radius_mm=tube_outer_radius,
        tube_inner_radius_mm=tube_inner_radius,
        prop_radius_mm=prop_radius,
        motor_radius_mm=motor_radius,
        n_motors=n_motors,
    )


# ---------------------------------------------------------------------
# Save OnShape variables
# ---------------------------------------------------------------------
def save_oshape_block():
    """Save the latest OnShape variable block to a .txt file."""
    global last_oshape_block

    if not last_oshape_block:
        messagebox.showwarning(
            "No data",
            "Please click 'Compute' first to generate the OnShape variable block."
        )
        return

    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        title="Save OnShape variables"
    )

    if not filepath:
        return  # User canceled

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(last_oshape_block)
        messagebox.showinfo("Saved", f"OnShape variables saved to:\n{filepath}")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save file:\n{e}")


# ---------------------------------------------------------------------
# GUI setup
# ---------------------------------------------------------------------
root = tk.Tk()
root.title("Drone Prop / Frame Configurator v4 (with clearance & tube)")

main_frame = ttk.Frame(root, padding=10)
main_frame.grid(row=0, column=0, sticky="nsew")

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Input variables
prop_size_var = tk.StringVar(value="26")
num_motors_var = tk.StringVar(value="4")
payload_var = tk.StringVar(value="10.0")    # example default
frame_var = tk.StringVar(value="5.5")       # example default
twr_var = tk.StringVar(value="2.0")
clearance_var = tk.StringVar(value="30")    # mm from prop tip to tube inner wall

# Row 0: Prop size
ttk.Label(main_frame, text="Prop diameter (inches):").grid(row=0, column=0, sticky="w")
prop_combo = ttk.Combobox(
    main_frame,
    textvariable=prop_size_var,
    values=["10", "12", "14", "16", "18", "20", "22", "24", "26", "30"],
    width=10,
    state="readonly",
)
prop_combo.grid(row=0, column=1, sticky="w")

# Row 1: Number of motors
ttk.Label(main_frame, text="Number of motors:").grid(row=1, column=0, sticky="w")
motors_combo = ttk.Combobox(
    main_frame,
    textvariable=num_motors_var,
    values=["4", "6", "8"],
    width=10,
    state="readonly",
)
motors_combo.grid(row=1, column=1, sticky="w")

# Row 2: Payload mass
ttk.Label(main_frame, text="Payload mass (kg):").grid(row=2, column=0, sticky="w")
ttk.Entry(main_frame, textvariable=payload_var, width=12).grid(row=2, column=1, sticky="w")

# Row 3: Frame mass
ttk.Label(main_frame, text="Frame + battery + motors mass (kg):").grid(row=3, column=0, sticky="w")
ttk.Entry(main_frame, textvariable=frame_var, width=12).grid(row=3, column=1, sticky="w")

# Row 4: Thrust-to-weight ratio
ttk.Label(main_frame, text="Desired T/W ratio:").grid(row=4, column=0, sticky="w")
ttk.Entry(main_frame, textvariable=twr_var, width=12).grid(row=4, column=1, sticky="w")

# Row 5: Clearance
ttk.Label(main_frame, text="Prop-tip clearance to tube (mm):").grid(row=5, column=0, sticky="w")
ttk.Entry(main_frame, textvariable=clearance_var, width=12).grid(row=5, column=1, sticky="w")

# Row 6: Buttons
compute_button = ttk.Button(main_frame, text="Compute", command=compute)
compute_button.grid(row=6, column=0, pady=10, sticky="ew")

save_button = ttk.Button(main_frame, text="Save OnShape variables…", command=save_oshape_block)
save_button.grid(row=6, column=1, pady=10, sticky="ew")

# Row 7: Canvas label
ttk.Label(main_frame, text="Top view layout (tube + props):").grid(
    row=7, column=0, columnspan=2, sticky="w"
)

# Row 8: Layout canvas
layout_canvas = tk.Canvas(main_frame, width=400, height=400, bg="white")
layout_canvas.grid(row=8, column=0, columnspan=2, pady=(0, 10), sticky="nsew")

# Row 9: Output text box
output_text = tk.Text(main_frame, width=80, height=18, wrap="word")
output_text.grid(row=9, column=0, columnspan=2, sticky="nsew")
output_text.config(state="disabled")

# Configure resizing
main_frame.rowconfigure(8, weight=1)  # canvas
main_frame.rowconfigure(9, weight=1)  # text
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)

if __name__ == "__main__":
    root.mainloop()
