# 🍞 Bread Van App CLI
This project provides a command-line interface (CLI) for managing and interacting with the Bread Van App.
 It is built with Flask CLI and click, and supports multiple roles: Admin, Driver, and Resident.

## 🚀 Quick Start / Setup Instructions

```bash
git clone https://github.com/Phantom-Coders-COMP3613/breadvanapp.git
cd breadvanapp
pip install -r requirements.txt

### Initialize the database:
flask init
```

### Initialize the database:
```bash
flask init
```
This creates and initializes all accounts and tables.
* Admin
  * admin / adminpass
* Drivers
  * bob / bobpass
  * mary / marypass
* Residents
  * alice / alicepass
  * jane / janepass
  * john / johnpass

## 📦 What is it

The **Bread Van App** is a command-line interface (CLI) and backend service for scheduling and managing Bread Van drives. It supports three separate user roles:

- **Admin** — manages system configuration (drivers, areas, streets)  
- **Driver** — operates drives and handles resident stop requests  
- **Resident** — requests stops and interacts as a customer  

It facilitates structured workflows: area → street → drive → stops → residents.

---



## 🔐 User Roles & Capabilities

### **Admin**
Admins maintain and configure the entire Bread Van service.  
Their responsibilities include setting up service areas, creating driver accounts, and ensuring the system remains organized and accurate.

Admins can:
- **Manage drivers** — create and delete drivers; view all registered users.
- **Configure service regions** — add areas (e.g., “San Juan”), add streets within areas.
- **Maintain structure** — delete areas or streets when needed.
- **View system-wide data** — list all areas, all streets, all users.

Admins do *not* schedule or drive routes; they ensure the platform is ready for drivers and residents.

---

### 🚐 **Driver**
Drivers operate the actual bread van routes.  
They manage the schedule of drives and respond to resident stop requests.

Drivers can:
- **Schedule drives** — pick date/time for upcoming bread van routes.
- **Cancel drives** — remove a future drive before it starts.
- **View all their drives** — review past and upcoming routes.
- **Start and end drives** — begin a route when on the road and close it after completing all stops.
- **View requested stops** — see which residents requested service on a specific drive.

Drivers act as the service operators.

---

###  🏠  **Resident**
Residents are the customers using the Bread Van service.  
They request stops so that drivers know where to visit during a route.

Residents can:
- **Create an account** — registration does not require admin approval.
- **Request a stop** — choose their area, street, and house number for a specific drive.
- **Cancel a stop** — withdraw a stop request if they no longer need service.
- **View inbox messages** — receive confirmations or notifications.
- **View driver statistics** — learn about a driver’s performance.

Residents represent the demand side of the service.

---

### **General / User**
These commands apply to any logged-in user, regardless of their role.

General capabilities include:
- **Logging in and out**
- **Viewing available drives** for a specific street
- **Browsing data** depending on permissions (e.g., areas and streets)

These are the baseline commands that support all roles.

---

## ✨ Features / Commands Overview

### Run any CLI command using:
```bash
flask <group> <command> [args...]
```


## 👤 User Commands | Group: flask user
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
Prompts to select an area and street, then lists scheduled drives.



## 🛠️ Admin Commands | Group: flask admin
Admins manage drivers, areas, and streets.
### List Users
```bash
flask admin list
```

### Create Driver
```bash
flask admin create_driver <username> <password>
```

### Delete Driver
```bash
flask admin delete_driver <driver_id>
```

### Add Area
```bash
flask admin add_area <name>
```

### Add Street
```bash
flask admin add_street <area_id> <name>
```

### Delete Area
```bash
flask admin delete_area <area_id>
```

### Delete Street
```bash
flask admin delete_street <street_id>
```

### View All Areas
```bash
flask admin view_all_areas
```

### View All Streets
```bash
flask admin view_all_streets
```


## 🚐 Driver Commands | Group: flask driver
Drivers manage drives and stops.
### Schedule Drive
```bash
flask driver schedule_drive YYYY-MM-DD HH:MM
```
Prompts to select area & street.
Drives cannot be scheduled in the past nor more than 1 year ahead of the current date.


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


## 🏠 Resident Commands | Group: flask resident
Residents can request stops and view their inbox.
### Create Resident
```bash
flask resident create <username> <password>
```
Prompts for area, street, and house number. 
A logged-in account is not required to create a resident.

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


## 🔑 Role Requirements
* flask admin ... → must be logged in as Admin
* flask driver ... → must be logged in as Driver
* flask resident ... → must be logged in as Resident