# parametric-drone-design
A journey in Drone Design.
# Lesson 01 – Parametric Ring (HawaFrame Starter)

This lesson is the **first step** in a hands-on series on parametric drone design using OnShape.

We start with the simplest, yet most powerful building block of the HawaFrame concept:

> A **parametric ring** that adapts to prop size, clearance, and tube geometry using a small set of variables.

This ring will later become the basis for:
- Inflatable or rigid tubes  
- Motor arm layouts  
- Load paths, mounts, and ducts  
- Full drone frame configurations driven by Python

---

## 🎯 Learning Goals

By the end of this lesson, you will be able to:

- Create and manage **variables** in OnShape (`#prop_diameter`, `#tube_inner_radius`, etc.).
- Build a **fully parametric ring** that updates when variables change.
- Understand how **prop geometry → ring geometry** is defined.
- Copy values from a **Python configurator** and drive your CAD model from code.

---

## 🧰 Prerequisites

- An OnShape account (free or paid).
- Basic familiarity with:
  - Sketching circles
  - Adding dimensions
  - Extruding parts
- (Optional but recommended) Python 3 installed to run the configurator.

---

## 📁 Repository Layout (Suggested)

At the repo root:

```text
/parametric-drone-design
    /lesson-01-ring
        README.md          ← this file
        screenshots/
    /configurator
        configurator_v4.py ← Python visual configurator
        sample_outputs/

