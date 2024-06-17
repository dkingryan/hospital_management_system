import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Entry, Button, Listbox
import csv
import datetime

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
        return self.patients if self.patients else []

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
        return self.doctors if self.doctors else []

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

    def list_appointments(self):
        return self.appointments if self.appointments else []

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
        self.appointments.sort(key=lambda x: (x.date, datetime.datetime.strptime(x.time, "%I:%M %p")))
        hospital.save_appointments()
        print("Data organized successfully.")

def close_window(event):
    event.widget.destroy()

def on_select(event):
    selected_index = Lb.curselection()[0]
    selected_value = Lb.get(selected_index)

    if selected_value == "Add Patient":
        add_patient_screen()
    elif selected_value == "List Patients":
        list_patient_screen()
    elif selected_value == "Add Doctor":
        add_doctor_screen()
    elif selected_value == "List Doctors":
        list_doctor_screen()
    elif selected_value == "Schedule Appointment":
        schedule_appointment_screen()
    elif selected_value == "List Appointments":
        list_appointments_screen()
    elif selected_value == "Save Data":
        hospital.save_patients()
        hospital.save_doctors()
        hospital.save_appointments()
        messagebox.showinfo("Save Data", "Data saved successfully.")
    elif selected_value == "Exit":
        master.quit()

def add_patient_screen():
    new_window = Toplevel(master)
    new_window.geometry("230x150")
    new_window.title("Add Patient")
    Label(new_window, text ="Name: ", font=("Arial", 14)).grid(row=0)
    Label(new_window, text="Age: ", font=("Arial", 14)).grid(row=1)
    Label(new_window, text ="Gender: ", font=("Arial", 14)).grid(row=2)

    name_entry = Entry(new_window)
    age_entry = Entry(new_window)
    gender_entry = Entry(new_window)
    name_entry.grid(row=0, column = 1)
    age_entry.grid(row=1,column=1)
    gender_entry.grid(row=2,column=1)

    def add_patient():
        name = name_entry.get()
        age = age_entry.get()
        gender = gender_entry.get()
        patient = Patient(name,age,gender)
        hospital.add_patient(patient)
        hospital.save_patients()
        messagebox.showinfo("Added","Patient added successfully.")
        new_window.destroy()

    Button(new_window, text="Add Patient", command=add_patient, font=("Arial", 14)).grid(row=3, columnspan=2)

def list_patient_screen():
    new_window=Toplevel(master)
    new_window.geometry("800x600")
    new_window.title("List Patients")
    patients = hospital.list_patients()
    for i, patient in enumerate(patients, start=1):
        Label(new_window, text=f"{i}. NAME: {patient.name}, AGE: {patient.age}, GENDER: {patient.gender}", font=("Arial", 14)).pack()

    master.bind('<KeyPress>', lambda event: new_window.destroy())

def add_doctor_screen():
    new_window = Toplevel(master)
    new_window.geometry("230x140")
    new_window.title("Add Doctor")
    Label(new_window, text ="Name: ", font=("Arial", 14)).grid(row=0)
    Label(new_window, text="Specialty: ", font=("Arial", 14)).grid(row=1)

    name_entry = Entry(new_window)
    specialty_entry = Entry(new_window)
    name_entry.grid(row=0, column = 1)
    specialty_entry.grid(row=1,column=1)

    def add_doctor():
        name = name_entry.get()
        specialty = specialty_entry.get()
        doctor = Doctor(name,specialty)
        hospital.add_doctor(doctor)
        hospital.save_doctors()
        messagebox.showinfo("Added","Doctor added successfully.")
        new_window.destroy()

    Button(new_window, text="Add Doctor", command=add_doctor, font=("Arial", 14)).grid(row=3, columnspan=2)

def list_doctor_screen():
    new_window=Toplevel(master)
    new_window.geometry("800x600")
    new_window.title("List Doctors")
    doctors = hospital.list_doctors()
    for i, doctor in enumerate(doctors, start=1):
        Label(new_window, text=f"{i}. NAME: {doctor.name}, SPECIALTY: {doctor.specialty}", font=("Arial", 14)).pack()
    master.bind('<KeyPress>', lambda event: new_window.destroy())

def schedule_appointment_screen():
    new_window=Toplevel(master)
    new_window.geometry("350x200")
    new_window.title("Schedule Appointment")
    Label(new_window, text="Patient Name:", font=("Arial", 14)).grid(row=0)
    Label(new_window, text="Doctor Name:", font=("Arial", 14)).grid(row=1)
    Label(new_window, text="Date (MM-DD-YYYY):", font=("Arial", 14)).grid(row=2)
    Label(new_window, text="Time:", font=("Arial", 14)).grid(row=3)
    Label(new_window, text="Notes:", font=("Arial", 14)).grid(row=4)

    patient_entry = Entry(new_window)
    doctor_entry = Entry(new_window)
    date_entry = Entry(new_window)
    time_entry = Entry(new_window)
    notes_entry = Entry(new_window)

    patient_entry.grid(row=0, column=1)
    doctor_entry.grid(row=1, column=1)
    date_entry.grid(row=2, column=1)
    time_entry.grid(row=3, column=1)
    notes_entry.grid(row=4, column=1)

    def schedule_appointment():
        patient_name = patient_entry.get()
        doctor_name = doctor_entry.get()
        date = date_entry.get()
        time = time_entry.get()
        notes = notes_entry.get()

        patient = next((p for p in hospital.patients if p.name.lower() == patient_name.lower()), None)
        doctor = next((d for d in hospital.doctors if d.name.lower() == doctor_name.lower()), None)

        if not patient or not doctor:
            messagebox.showerror("Error", "Invalid patient or doctor name.")
            return

        hospital.schedule_appointment(patient, doctor, date, time, notes)
        hospital.organize_data()
        messagebox.showinfo("Schedule Appointment", "Appointment scheduled successfully.")
        new_window.destroy()

    Button(new_window, text="Schedule Appointment", command=schedule_appointment, font=("Arial", 14)).grid(row=5, columnspan=2)


def list_appointments_screen():
    new_window = Toplevel(master)
    new_window.title("List Appointments")
    new_window.geometry("1000x800")
    appointments = hospital.list_appointments()
    for i, appointment in enumerate(appointments, start=1):
        Label(new_window,text=f"{i}. PATIENT: {appointment.patient.name}, DOCTOR: {appointment.doctor.name}, DATE: {appointment.date}, TIME: {appointment.time}, NOTES: {appointment.notes}", font=("Arial", 14)).pack()

    master.bind('<KeyPress>', lambda event: new_window.destroy())

master = tk.Tk()
master.geometry("315x300")
master.title("Hospital Management")
hospital = Hospital()
w = Label(master, text='Hospital Management',font=("Arial", 24))
w.grid(row=0, column=5)

Lb=Listbox(master, font=("Arial", 16),)
Lb.insert(1, "Add Patient")
Lb.insert(2, 'List Patients')
Lb.insert(3, "Add Doctor")
Lb.insert(4, "List Doctors")
Lb.insert(5, "Schedule Appointment")
Lb.insert(6, "List Appointments")
Lb.insert(7, "Save Data")
Lb.insert(8,"Exit")
Lb.grid(row=1,column=5)

Lb.bind('<<ListboxSelect>>', on_select)

master.mainloop()