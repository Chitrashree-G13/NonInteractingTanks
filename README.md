# FOSSEE OpenModelica Screening Task – Non-Interacting Tanks Simulation

## Overview
This repository contains the OpenModelica package and Python automation scripts for simulating a non-interacting two-tank liquid system as part of the FOSSEE OpenModelica task.

The project demonstrates object-oriented modeling in Modelica and programmatic control, data extraction, and dynamic plotting using **OMPython** (`OMCSessionZMQ`) and **Matplotlib**.

---

## Project Structure
* `package.mo`: Main Modelica package containing the system components.
* `Tank.mo`: Model defining the primary inlet tank with conditional flow dynamics.
* `Tank2.mo`: Model defining the second connected tank with safe flow evaluations.
* `TwoConnectedTanks.mo`: Top-level assembly model connecting `Tank` and `Tank2`.
* `FlowConnect.mo`: Custom connector interface for fluid flow between components.
* `run_simulation.py`: Python script automating OMC simulation and result visualization.
* `simulation_results.png`: Plotted liquid height dynamics over time.

---

## Key Technical Highlights
1. **Division by Zero Prevention:** Standardized initial boundary conditions and handled potential zero-flow states ($Q_1 = 0$) at initial time $t = 0$ using smooth dynamic safeguards.
2. **OMPython Automation:** Communicated with the OpenModelica Compiler via ZeroMQ (`OMCSessionZMQ`) to automatically compile, execute, and extract time-series trajectory data.
3. **Data Visualization:** Plotted liquid height trajectories ($h_1$, $h_2$) across simulation time using Matplotlib.

---

## How to Run the Project

### Prerequisites
* OpenModelica
* Python 3.x
* Required Python packages:
  ```bash
  pip install OMPython matplotlib numpy pandas
