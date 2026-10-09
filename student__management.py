"""
STUDENT MANAGEMENT SYSTEM - FILE-BASED VERSION
No database needed! Uses JSON files to store data.

Features:
1. Add Student
2. View All Students
3. Search Student
4. Update Student
5. Delete Student
6. View Statistics
"""

import json
import os
from datetime import datetime

# File where we store student data
DATA_FILE = 'students.json'


# ============================================================
# 1. LOAD DATA FROM FILE
# ============================================================
def load_students():
    """Load students from JSON file. If file doesn't exist, return empty list."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as file:
                return json.load(file)
        except:
            return []
    return []


# ============================================================
# 2. SAVE DATA TO FILE
# ============================================================
def save_students(students):
    """Save students to JSON file."""
    with open(DATA_FILE, 'w') as file:
        json.dump(students, file, indent=4)
    print("✅ Data saved successfully!")


# ============================================================
# 3. ADD A STUDENT
# ============================================================
def add_student():
    print("\n--- ADD NEW STUDENT ---")
    students = load_students()
    
    roll_number = input("Enter Roll Number: ").strip()
    name = input("Enter Full Name: ").strip()
    email = input("Enter Email: ").strip()
    phone = input("Enter Phone Number: ").strip()
    course = input("Enter Course (e.g. BCA, BSc): ").strip()
    
    # Validation
    if not roll_number or not name:
        print("⚠️  Roll number and name cannot be empty.")
        return
    
    # Check if roll number already exists
    for student in students:
        if student['roll_number'] == roll_number:
            print("⚠️  Student with this roll number already exists!")
            return
    
    # Get age
    age_input = input("Enter Age: ").strip()
    try:
        age = int(age_input)
    except ValueError:
        print("⚠️  Age must be a number.")
        return
    
    # Create new student record
    new_student = {
        'id': len(students) + 1,
        'roll_number': roll_number,
        'name': name,
        'email': email,
        'phone': phone,
        'course': course,
        'age': age,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Add to list and save
    students.append(new_student)
    save_students(students)
    print(f"✅ Student '{name}' added successfully!")


# ============================================================
# 4. VIEW ALL STUDENTS
# ============================================================
def view_all_students():
    print("\n--- ALL STUDENTS ---")
    students = load_students()
    
    if not students:
        print("No students found. Add some students first!")
        return
    
    # Print table header
    print(f"\n{'ID':<5}{'Roll No':<12}{'Name':<20}{'Email':<28}{'Phone':<14}{'Course':<10}{'Age':<5}")
    print("-" * 94)
    
    
    # Print each student
    for s in students:
        print(f"{s['id']:<5}{s['roll_number']:<12}{s['name']:<20}{(s.get('email', '') or ''):<28}{(s.get('phone', '') or ''):<14}{(s.get('course', '') or ''):<10}{s.get('age', ''):<5}")
    
    print(f"\nTotal Students: {len(students)}")


# ============================================================
# 5. SEARCH A STUDENT
# ============================================================
def search_student():
    print("\n--- SEARCH STUDENT ---")
    students = load_students()
    roll_number = input("Enter Roll Number to search: ").strip()
    
    for student in students:
        if student['roll_number'] == roll_number:
            print("\n✅ Student Found:")
            print(f"  ID           : {student['id']}")
            print(f"  Roll Number  : {student['roll_number']}")
            print(f"  Name         : {student['name']}")
            print(f"  Email        : {student.get('email', 'N/A')}")
            print(f"  Phone        : {student.get('phone', 'N/A')}")
            print(f"  Course       : {student.get('course', 'N/A')}")
            print(f"  Age          : {student.get('age', 'N/A')}")
            return
    
    print("⚠️  No student found with that roll number.")


# ============================================================
# 6. UPDATE A STUDENT
# ============================================================
def update_student():
    print("\n--- UPDATE STUDENT ---")
    students = load_students()
    roll_number = input("Enter Roll Number of student to update: ").strip()
    
    # Find the student
    student = None
    for s in students:
        if s['roll_number'] == roll_number:
            student = s
            break
    
    if not student:
        print("⚠️  No student found with that roll number.")
        return
    
    print("Leave a field blank to keep its current value.\n")
    
    # Update fields
    name = input(f"New Name [{student['name']}]: ").strip() or student['name']
    email = input(f"New Email [{student.get('email', '')}]: ").strip() or student.get('email', '')
    phone = input(f"New Phone [{student.get('phone', '')}]: ").strip() or student.get('phone', '')
    course = input(f"New Course [{student.get('course', '')}]: ").strip() or student.get('course', '')
    
    age_input = input(f"New Age [{student.get('age', '')}]: ").strip()
    if age_input:
        try:
            age = int(age_input)
        except ValueError:
            print("⚠️  Age must be a number. Keeping old value.")
            age = student.get('age', '')
    else:
        age = student.get('age', '')
    
    # Update the student
    student['name'] = name
    student['email'] = email
    student['phone'] = phone
    student['course'] = course
    student['age'] = age
    
    # Save all students
    save_students(students)
    print("✅ Student record updated successfully!")


# ============================================================
# 7. DELETE A STUDENT
# ============================================================
def delete_student():
    print("\n--- DELETE STUDENT ---")
    students = load_students()
    roll_number = input("Enter Roll Number of student to delete: ").strip()
    
    # Find the student
    student = None
    for s in students:
        if s['roll_number'] == roll_number:
            student = s
            break
    
    if not student:
        print("⚠️  No student found with that roll number.")
        return
    
    # Confirm deletion
    confirm = input(f"Are you sure you want to delete '{student['name']}'? (yes/no): ").strip().lower()
    if confirm == 'yes':
        students.remove(student)
        save_students(students)
        print("✅ Student deleted successfully.")
    else:
        print("Deletion cancelled.")


# ============================================================
# 8. STATISTICS
# ============================================================
def student_statistics():
    print("\n--- STUDENT STATISTICS ---")
    students = load_students()
    
    if not students:
        print("No students found yet.")
        return
    
    total = len(students)
    print(f"Total Students: {total}")
    
    # Calculate average age
    ages = [s.get('age', 0) for s in students if s.get('age')]
    if ages:
        avg_age = sum(ages) / len(ages)
        print(f"Average Age   : {avg_age:.1f} years")
    
    # Count by course
    courses = {}
    for student in students:
        course = student.get('course', 'N/A')
        courses[course] = courses.get(course, 0) + 1
    
    print("\nStudents per Course:")
    for course, count in courses.items():
        print(f"  {course:<15}: {count}")


# ============================================================
# 9. MAIN MENU
# ============================================================
def main_menu():
    while True:
        print("\n" + "=" * 42)
        print("       STUDENT MANAGEMENT SYSTEM")
        print("=" * 42)
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. View Statistics")
        print("7. Exit")
        print("=" * 42)
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            add_student()
        elif choice == "2":
            view_all_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            student_statistics()
        elif choice == "7":
            print("\nThank you for using Student Management System. Goodbye! 👋")
            break
        else:
            print("⚠️  Invalid choice. Please enter a number between 1 and 7.")


# ============================================================
# RUN THE PROGRAM
# ============================================================
if __name__ == "__main__":
    main_menu()