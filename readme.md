# 🍞 Bread Van App 
The App is a backendservice for managing the operations of the Bread Van system.  
It provides endpoints for Drivers and Residents to interact with the system, handling everything from scheduling drives to requesting stops.

---

## 🚀 Quick Start / Setup Instructions

```bash
git clone https://github.com/Phantom-Coders-COMP3613/breadvanapp.git
cd breadvanapp
pip install -r requirements.txt
```

### Initialize the database:
```bash
flask init
```
This creates and initializes all accounts and tables.

Default Accounts:
* **Drivers**
  * bob / bobpass
  * mary / marypass
* **Residents**
  * alice / alicepass
  * jane / janepass
  * john / johnpass

---

## 📦 What Is It?

The **Bread Van App** is a command-line interface (CLI) and backend service for scheduling and managing Bread Van drives.  
It supports multiple user roles that interact with the system differently:

- **Driver** — creates and executes drives and handles stop requests  
- **Resident** — requests stops and receives notifications  
- **General Users** — any authenticated user who can browse public information  

It organizes data and workflows into:  
**Area → Street → Drive → Stops → Residents**

---

## 🔐 User Roles & Capabilities

### 🚐 **Driver**
Drivers operate the actual bread van routes.  
They manage the schedule of drives and respond to resident stop requests.

Drivers can:
- **Schedule drives** — pick date/time for upcoming routes  
- **Cancel drives** — remove a future drive  
- **View all their drives** — past and upcoming routes  
- **Start and end drives** — mark route active or complete  
- **View requested stops** — see residents awaiting service  

Drivers serve as the operational backbone of the service.

---

### 🏠 **Resident**
Residents are the customers who request service from the Bread Van.

Residents can:
- **Create an account** — signup does *not* require approval  
- **Request a stop** — select area, street, house number  
- **Cancel a stop** — withdraw request if needed  
- **View inbox messages** — confirmations, updates  
- **View driver statistics** — performance and reliability info  

Residents represent the demand side of the operation.

---

### 👥 **General / User**
General controllers apply to any logged-in user, regardless of their role.

Capabilities include:
- Logging in and out  
- Viewing drives on specific streets  
- Browsing areas and streets  

---

## ✨ Features / Controllers Overview

Run any CLI controller using:

```bash
flask <group> <controller> [args...]
```

---

## 👤 User Controllers | Group: `flask user`

### Login
```bash
flask user login <username> <password>
```

### Logout
```bash
flask user logout
```

### View Drives on a Street
```bash
flask user view_street_drives
```
Prompts to select an area and street, then lists all scheduled drives.

---

## 🚐 Driver Controllers | Group: `flask driver`

### Schedule Drive
```bash
flask driver schedule_drive YYYY-MM-DD HH:MM
```
Prompts to select area & street.  
Cannot schedule drives in the past or more than 1 year ahead.

### Cancel Drive
```bash
flask driver cancel_drive <drive_id>
```

### View My Drives
```bash
flask driver view_my_drives
```

### Start Drive
```bash
flask driver start_drive <drive_id>
```

### End Drive
```bash
flask driver end_drive
```

### View Requested Stops
```bash
flask driver view_requested_stops <drive_id>
```

---

## 🏠 Resident Controllers | Group: `flask resident`

### Create Resident
```bash
flask resident create <username> <password>
```
Prompts for area, street, and house number.  
Logged-in account **not** required.

### Request Stop
```bash
flask resident request_stop
```

### Cancel Stop
```bash
flask resident cancel_stop <drive_id>
```

### View Inbox
```bash
flask resident view_inbox
```

### View Driver Stats
```bash
flask resident view_driver_stats <driver_id>
```

---

## 🔑 Role Requirements
- `flask driver ...` → must be logged in as **Driver**  
- `flask resident ...` → must be logged in as **Resident**
