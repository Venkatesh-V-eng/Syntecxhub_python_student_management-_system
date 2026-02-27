import json
import os

class Student:
    """Class to represent an individual student."""
    def __init__(self, student_id, name, grade):
        self.student_id = str(student_id)
        self.name = name
        self.grade = grade

    def to_dict(self):
        """Converts the Student object to a dictionary for JSON serialization."""
        return {
            "id": self.student_id, 
            "name": self.name, 
            "grade": self.grade
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a Student object from a dictionary."""
        return cls(data["id"], data["name"], data["grade"])

    def __str__(self):
        """Provides a formatted string representation of the student."""
        return f"{self.student_id: <10} | {self.name: <20} | {self.grade}"


class StudentManager:
    """Manager class to encapsulate all student operations."""
    def __init__(self, filename="students.json"):
        self.filename = filename
        # Using a dictionary with student_id as the key for fast O(1) lookups and unique ID validation
        self.students = {} 
        self.load_data()

    def load_data(self):
        """Loads student records from the JSON file."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                try:
                    data = json.load(file)
                    for item in data:
                        self.students[item["id"]] = Student.from_dict(item)
                except json.JSONDecodeError:
                    self.students = {}
        else:
            self.students = {}

    def save_data(self):
        """Persists the current student records to the JSON file."""
        with open(self.filename, 'w') as file:
            # Convert dictionary values back to a list of dicts for standard JSON format
            json.dump([student.to_dict() for student in self.students.values()], file, indent=4)

    def add_student(self, student_id, name, grade):
        """Adds a new student with unique ID validation."""
        student_id = str(student_id)
        if student_id in self.students:
            print(f"\n❌ Error: A student with ID '{student_id}' already exists.")
            return

        new_student = Student(student_id, name, grade)
        self.students[student_id] = new_student
        self.save_data()
        print(f"\n✅ Success: Student '{name}' added successfully.")

    def update_student(self, student_id, name=None, grade=None):
        """Updates an existing student's name or grade."""
        student_id = str(student_id)
        if student_id not in self.students:
            print(f"\n❌ Error: No student found with ID '{student_id}'.")
            return

        student = self.students[student_id]
        if name:
            student.name = name
        if grade:
            student.grade = grade
            
        self.save_data()
        print(f"\n✅ Success: Student ID '{student_id}' updated successfully.")

    def delete_student(self, student_id):
        """Deletes a student by ID."""
        student_id = str(student_id)
        if student_id in self.students:
            del self.students[student_id]
            self.save_data()
            print(f"\n✅ Success: Student '{student_id}' deleted successfully.")
        else:
            print(f"\n❌ Error: No student found with ID '{student_id}'.")

    def list_students(self):
        """Lists all students in a formatted console output."""
        if not self.students:
            print("\n⚠️ No student records found.")
            return
            
        print("\n" + "=" * 50)
        print(f"{'ID': <10} | {'Name': <20} | {'Grade'}")
        print("-" * 50)
        for student in self.students.values():
            print(student)
        print("=" * 50)


def main():
    """Main CLI application loop."""
    manager = StudentManager()

    while True:
        print("\n=== 🎓 Student Management System ===")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. List All Students")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            student_id = input("Enter Student ID: ").strip()
            name = input("Enter Student Name: ").strip()
            grade = input("Enter Student Grade: ").strip()
            
            if student_id and name and grade:
                manager.add_student(student_id, name, grade)
            else:
                print("\n❌ Error: All fields (ID, Name, Grade) are required.")
                
        elif choice == '2':
            student_id = input("Enter Student ID to update: ").strip()
            print("(Leave fields blank and press Enter if you do not want to change them)")
            name = input("Enter new Name: ").strip()
            grade = input("Enter new Grade: ").strip()
            
            # Convert empty strings to None so the manager knows not to update them
            name = name if name else None
            grade = grade if grade else None
            
            manager.update_student(student_id, name, grade)
            
        elif choice == '3':
            student_id = input("Enter Student ID to delete: ").strip()
            manager.delete_student(student_id)
            
        elif choice == '4':
            manager.list_students()
            
        elif choice == '5':
            print("\nSaving data... Exiting System. Goodbye! 👋\n")
            break
            
        else:
            print("\n⚠️ Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()