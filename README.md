Building SCADA System
- A modular SCADA (Supervisory Control and Data Acquisition) system for smart building automation,
integrating real-time monitoring, access control, lighting, climate management,
and security features using a Python-based UI and a Modicon M221 PLC.

Features:
- Access Control: RFID-based entry with logging and validation
- Fire Safety: Smoke detection, emergency triggers, sprinkler simulation
- Security System: Intrusion detection and alarm automation
- Parking Lot Management: Vehicle count, gate automation, object detection
- Smart Lighting: Auto/manual controls based on lux and motion
- Climate Control: Heating/Cooling via temperature thresholds
- Admin Dashboard: Real-time status, event logs, and database control
- Multilingual Support: English & Bulgarian
- Simulation Mode: Test inputs/outputs without live hardware

Technology Stack:
- Python 3.10+
- Flet: UI framework (Flutter)
- Modbus TCP: PLC communication protocol
- SQLite: Local database for access control and logs
- Modicon M221 PLC: Industrial automation controller
- EcoStruxure Machine Expert - Basic: PLC programming environment

Instalation:
- The App can be built with "flet pack main_app.py" in the Terminal

Instructions:
- For the App to function properly, both the built app executable and a simulation need to be runnung.
- To run the simulation open Building.smbp in EcoStruxure Machine Expert - Basic and under Comissioning:
  - press Launch simulator;
  - then Start Controller.  

License & Credits:
- Developed by: Georgi Milenov Sokolov as Bachelor's Thesis, Technical University of Varna
- Licensed for academic and personal use
