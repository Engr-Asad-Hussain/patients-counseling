## Getting started with Patients-Counseling System

Hey folks! Hope you are doing well. Lets explore this Postman Collection with hands-on demostration.

### Setup
You will need to install Postman application and import this `PostmanCollection.json` file. You will see following folders and categories. Each categories contains of multiple requests.
```
Patients-System
|-- Patients 
|-- Counsellors
|-- Appointments
```

### Getting started with Category-Patients
First try out `GET /api/patients/` endpoint. Initially you will get an empty list in response, since there are no patients in the database - only active patients will be visible.
So why are you waiting ...? Lets add new patients into the system using `POST /api/patients/` endpoint. Place the following json-body to insert your first patient:
```json
{
    "name": "Badman",
    "email": "badman@demo.com",
    "password": "password123@"
}
```
These are required arguments - if you don't provide valid arguments you will be responded with the error(s). You will get the following response if you enter all the fields correctly:
```json
{
    "id": 1,
    "name": "Badman",
    "email": "badman@demo.com",
    "password": "password123@",
    "is_active": true
}
```

Lets add two more patients in the system:
```json
{
    "name": "Pokimon",
    "email": "pokimon@demo.com",
    "password": "password123@"
}
```
```json
{
    "name": "Benten",
    "email": "benten@demo.com",
    "password": "password123@"
}
```
Now, we have 3 patients with `[1, 2, 3]`. You can find the detail for each specific patient in `GET /api/patients/:id/` endpoint. And also you can update any specific field for each patient via `PUT /api/patients/:id/` endpoint - keep in mind that email is unique and cannot be change or update.

You can also delete the patients `DELETE /api/patients/:id/` endpoint. The message will indicate that *"Patient has been inactivated.* - it means that patient is not deleted from the database instead it flaged as inactive. Lets try to delete `id=3` patient.
```json
{
    "message": "Patient has been inactivated."
}
```

### Getting started with Category-Counsellors
(This is similar to Patients - Create 3 counsellors inwhich 2 must be active and shall be in inactivated state. Assuming `[1, 2, 3]` with `id=3` as deleted.)


### Getting started with Category-Appointments
Now, lets make sure each patient and counsellor setup the appointments. Start with `POST /api/appointments/` endpoint. Try the following json-body to create your first appointment:
```json
{
    "patient": 1,
    "counsellor": 1,
    "appointment_date": "2024-04-10T10:00:00"
}
```
You will get an error message if you hit the endpoint again with the same body indicating *"Active appointment with the same patient and counsellor already exists."*. Try few more appointments yourself then we can more forward ...

Its time to check the list of all the appoitments and you can achieve this with `GET /api/appointments/` endpoint. This endpoints can be used with query arguments:
- `/api/appointments/` returns all the appointments.
- `/api/appointments/?patient_id=1` will return all appointments for specific patient.
- `/api/appointments/?counsellor_id=1` will return all appointments for specific counsellor.
- `/api/appointments/?counsellor_id=1` will return all appointments for specific counsellor.
- `/api/appointments/?sort=-appointment_date` will return sorted appointments in descending order. You can pass `sort=appointment_date` to get the list of appointments in the ascending order.
- `/api/appointments/?start_date=2024-04-10T10:00:00` will return all the appointments greater/equal to the start date.
- `/api/appointments/?end_date=2024-04-10T10:00:00` will return all the appointments lesser/equal to the end date.

Concluding the appointments with the `DELETE /api/appointments/:id/` endpoint which is used to hard-delete the appointments from the database.
