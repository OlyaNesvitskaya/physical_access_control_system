# PhysicalAccessControlSystem

## Description

Person presents access card to a device reader and, if all the conditions stored in the system are met,
person is allowed to enter. All access attempts is recorded to events table whether access is granted or not.

#### Сonditions for access to device: 
* employee card_id must be in employees table; 
* expiration time of card_id must be greater than or equal than date today; 
* device imei must be in devices table; 
* in access_control_table must be a record that contains employee_id and device_id .

The API is protected by authorization, except endpoint - '/drop_in/{card_id}/{imei}'.    
Authorization has done using a token.

#### An API has been implemented with the following functionality:

| HTTP Method        | Endpoints                                    | Action                                                                                         |
|--------------------|----------------------------------------------|------------------------------------------------------------------------------------------------|
| GET                | /drop_in/{card_id}/{imei}                    | Check entry possibility (no authorization)                                                     |
|                    |                                              |                                                                                                |
| POST               | /token                                       | Get access token                                                                               |
| POST               | /users                                       | Create new user                                                                                |
|                    |                                              |                                                                                                |
| GET, POST          | /departments                                 | Show all departments or create department                                                      |
| GET, PATCH, DELETE | /departments/<department_id>                 | Retrieve(or update or delete) department about indicated id                                    |
|                    |                                              |                                                                                                |
| GET, POST          | /employees                                   | Show all employees or create employee                                                          |
| GET, PATCH, DELETE | /employees/<employee_id>                     | Retrieve(or update or delete) employee about indicated id                                      |
| GET                | /employees/<employee_id>/devices             | Obtaining a list of available devices for employee.                                            |
|                    |                                              |                                                                                                |
| GET, POST          | /devices                                     | Show all devices or create employee                                                            |
| GET, PATCH, DELETE | /devices/<device_id>                         | Retrieve(or update or delete) device about indicated id                                        |
| GET                | /devices/<device_id>/employees               | Obtaining a list of employees who are given the opportunity<br/> to enter through this device. |
| POST               | /devices/access                              | Adding an employee to gain access to the device.                                               |
| DELETE             | /devices/<device_id>/employees/<employee_id> | Take away access to the device from the specified employee.                                    |


# Quick Start
### Clone the repo:
* $ git clone https://github.com/OlyaNesvitskaya/physical_access_control_system.git 
* $ cd physical_access_control_system
### Run the project:
* docker-compose build
* docker-compose up
### Run tests in container:
* docker exec -it <*CONTAINER ID*> /bin/bash
* pytest