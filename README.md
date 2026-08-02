# Automated Simulation and Analysis of a Non-Interacting Two-Tank Liquid System using OpenModelica

## Overview

This repository contains my solution for the **FOSSEE OpenModelica Screening Task**. The project models and simulates a **Non-Interacting Two-Tank Liquid System** using OpenModelica. It also includes a Python-based desktop application developed with **PyQt6** for launching simulations and an automation script using **OMPython** for executing simulations programmatically.

The project demonstrates object-oriented modeling, desktop application development, simulation automation, input validation, and scientific visualization.

---

## Repository

**Project Name:** NonInteractingTanks

---

## Features

- Object-oriented Modelica implementation
- Interactive PyQt6 desktop application
- OpenModelica executable launcher
- Automated simulation using OMPython
- Simulation parameter validation
- Real-time execution log console
- Scientific visualization using Matplotlib
- Modular and maintainable project structure

---

## Repository Structure

```text
NonInteractingTanks/
│
├── .gitignore
├── package.mo
├── package.order
├── FlowConnect.mo
├── Tank.mo
├── Tank2.mo
├── TwoConnectedTanks.mo
├── TwoConnectedTanks.exe
├── TwoConnectedTanks.bat
├── TwoConnectedTanks_init.xml
├── app.py                          # PyQt6 desktop application
├── run_simulation.py               # OMPython automation script
├── simulation_results.png          # Generated simulation plot
└── README.md
```

---

## Technologies Used

- OpenModelica v1.27.0 (64-bit)
- Modelica
- Python 3.14.4
- PyQt6
- OMPython
- Matplotlib
- NumPy
- Pandas

---

## Prerequisites

Install the required Python packages:

```bash
pip install PyQt6 OMPython matplotlib numpy pandas
```

---

# Running the Project

## 1. Launch the Desktop Application

Start the application using:

```bash
python app.py
```

The PyQt6 desktop interface will open, providing an interactive environment to configure and execute OpenModelica simulations.

### Using the Desktop Application

1. Launch the application using the above command.
2. Click **Browse** and select the compiled OpenModelica executable (`TwoConnectedTanks.exe`).
3. Enter the required simulation parameters:
   - **Start Time**
   - **Stop Time**
4. Click **Launch Simulation**.
5. The application validates the input parameters before execution.
6. The selected executable is launched using Python's `subprocess` module.
7. Execution logs and simulation status are displayed in the integrated output console.
8. Upon successful completion, the simulation generates the corresponding result files.


> **Note:** Before launching the simulation, ensure that `TwoConnectedTanks.exe` has been successfully generated from the OpenModelica model and is available within the project directory.

---

## 2. Run the Automated Simulation Script

The project also provides an automation script for executing the model directly through OpenModelica.

Run:

```bash
python run_simulation.py
```

This script performs the following tasks:

- Connects to the OpenModelica Compiler (OMC) using **OMPython**.
- Loads the Modelica package.
- Compiles and simulates the model programmatically.
- Extracts simulation data.
- Generates visualization plots using Matplotlib.

---

## Desktop Application Features

- Browse OpenModelica executable
- Automatic executable detection
- Simulation parameter validation
- Execution log console
- Error handling using dialog boxes
- Professional PyQt6 user interface

---

## Input Validation

The application validates simulation parameters before execution.

Condition:

```text
0 ≤ Start Time < Stop Time < 5
```

If invalid values are entered, the application displays an appropriate validation message.

---

## Project Workflow

```text
User
   │
   ▼
Desktop GUI (PyQt6)
   │
   ▼
Input Validation
   │
   ▼
Launch OpenModelica Executable
   │
   ▼
Simulation Execution
   │
   ▼
Console Output
   │
   ▼
Simulation Results
```

---

## Learning Outcomes

This project helped me gain practical experience in:

- OpenModelica modeling
- Modelica package development
- Python automation using OMPython
- Desktop GUI development with PyQt6
- Object-Oriented Programming
- Simulation execution using subprocess
- Scientific plotting using Matplotlib
- Input validation and exception handling

---

## Future Improvements

- Multiple model support
- Solver selection
- Automatic result plotting
- Export simulation reports
- Dark/Light theme switching
- Parameter configuration panel
- Recent executable history

---

## Author

**Chitrashree G**

B.E. Computer Science & Design

Project developed as part of the **FOSSEE OpenModelica Screening Task**.

---

## License

This project is shared for educational and demonstration purposes as part of the FOSSEE OpenModelica Screening Task.
