import csv

class Patient:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

class Doctor:
    def __init__(self, name, specialty):
        self.name = name
        self.specialty = specialty

class Appointments:
    def __init__(self,patient, doctor, date, time, notes):
        self.patient = patient
        self.doctor = doctor
        self.date = date
        self.time = time
        self.notes = notes

class Hospital:
    def __init__(self):
        self.patients = []
        self.doctors = []
        self.appointments = []
        self.load_patients()
        self.load_doctors()
        self.load_appointments()

    def add_patient(self, patient):
        self.patients.append(patient)

    def list_patients(self):
        print("\nPatients: ")
        for i, patient in enumerate(self.patients, start = 1):
            print (f"{i}. NAME: {patient.name}, AGE: {patient.age}, GENDER: {patient.gender}")

    def save_patients(self):
        with open('patients.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for patient in self.patients:
                writer.writerow([patient.name, patient.age, patient.gender])
        print("Patients information saved")

    def load_patients(self):
        try:
            with open('patients.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        name, age, gender = row
                        self.patients.append(Patient(name, age, gender))
        except FileNotFoundError:
            pass

    def add_doctor(self, doctor):
        self.doctors.append(doctor)

    def list_doctors(self):
        print("\nDoctors: ")
        for i, doctor in enumerate(self.doctors, start = 1):
            print (f"{i}. NAME: {doctor.name}, SPECIALTY: {doctor.specialty}")

    def save_doctors(self):
        with open('doctors.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for doctor in self.doctors:
                writer.writerow([doctor.name, doctor.specialty])
            print("Doctor information saved")

    def load_doctors(self):
        try:
            with open('doctors.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        name, specialty = row
                        self.doctors.append(Doctor(name, specialty))
        except FileNotFoundError:
            pass

    def schedule_appointment(self, patient, doctor, date, time, notes):
        appointment = Appointments(patient, doctor, date, time, notes)
        self.appointments.append(appointment)
        print("Appointment added")

    def list_appointment(self):
        print("\nAppointments: ")

        for i, appointment in enumerate (self.appointments, start =1):
            print (f"{i}. PATIENT: {appointment.patient.name}, DOCTOR: {appointment.doctor.name}, DATE: {appointment.date}, TIME: {appointment.time}, NOTES: {appointment.notes}")

    def save_appointments(self):
        with open('appointments.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for appointment in self.appointments:
                writer.writerow([appointment.patient.name, appointment.doctor.name, appointment.date, appointment.time, appointment.notes])
        print("Appointment information saved")

    def load_appointments(self):
        try:
            with open('appointments.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:
                        try:
                            patient_name, doctor_name, date, time, notes = row
                        except ValueError:
                            patient_name, doctor_name, date, time = row
                            notes = ""
                        patient = next((p for p in self.patients if p.name == patient_name), None)
                        doctor = next((d for d in self.doctors if d.name == doctor_name), None)
                        if patient and doctor:
                            self.appointments.append(Appointments(patient, doctor, date, time, notes))
        except FileNotFoundError:
            pass

    def organize_data(self):
        self.appointments.sort(key=lambda x: x.time)
        self.appointments.sort(key=lambda x: x.date)
        print("Data organized successfully.")


def main():
    hospital = Hospital()

    while True:
        print("\nHospital Care Management System")
        print("1. Add Patient")
        print("2. List Patient")
        print("3. Add Doctor")
        print("4. List Doctors")
        print("5. Schedule Appointment")
        print("6. List Appointments")
        print ("7. Organize Data")
        print("8. Save Data")
        print ("9. Exit")

        choice = input("Choose an option: ")
        if choice.isdigit():
            if choice == "1":
                name = input ("Enter patient's name: ")
                age = input("Enter patient's age: ")
                gender = input("Enter patient's gender: ")
                patient = Patient(name, age, gender)
                hospital.add_patient(patient)
                hospital.save_patients()
                print("Patient added")
            elif choice == "2":
                hospital.list_patients()

            elif choice == "3":
                name = input("Enter doctor's name: ")
                specialty = input("Enter doctor's specialty: ")
                doctor = Doctor(name, specialty)
                hospital.add_doctor(doctor)
                hospital.save_doctors()
                print("Doctor added")

            elif choice == "4":
                hospital.list_doctors()

            elif choice == "5":
                if not hospital.patients or not hospital.doctors:
                    print("Please add patients and doctors first")
                    continue

                patient_name = input("Enter patient name: ")
                doctor_name = input("Enter doctor's name: ")

                patient = next((p for p in hospital.patients if p.name.lower() == patient_name.lower()), None)
                doctor = next((d for d in hospital.doctors if d.name.lower() == doctor_name.lower()), None)

                if not patient:
                    print("Invalid patient name. Enter patient's information first")
                if not doctor:
                    print("Invalid doctor name. Enter doctor's information first")

                if patient and doctor:
                    date = input("Enter appointment date (MM-DD-YYYY): ")
                    time = input("Enter the time: ")
                    notes = input("Notes: ")
                    hospital.schedule_appointment(patient, doctor, date, time, notes)
                    hospital.save_appointments()

            elif choice == "6":
                hospital.list_appointment()

            elif choice == "7":
                hospital.organize_data()

            elif choice == "8":
                hospital.save_patients()
                hospital.save_doctors()
                hospital.save_appointments()

            elif choice == "9":
                print("Exiting...")
                break

            else:
                print("Invalid choice. Please enter a valid option.")
        else:
            print("Invalid choice. Please enter a number.")

if __name__ == '__main__':
    main()



