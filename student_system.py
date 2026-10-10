import csv
import os
import pandas as pd
import matplotlib.pyplot as plt

FILE = "student_records.csv"
FIELDS = ["ID", "Name", "Age", "Course", "Python", "SQL", "Excel"]
SUBJECTS = ["Python", "SQL", "Excel"]
PASS_MARK = 40          # must score at least this in every subject to pass
RISK_THRESHOLD = 50     # flag anyone below this in any subject

students = []


# ---------------------------------------------------------------
# File handling
# ---------------------------------------------------------------
def save_students():
    with open(FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(students)


def load_students():
    if not os.path.exists(FILE):
        load_sample_data()
        return
    with open(FILE, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if all(field in row for field in FIELDS):
                students.append(row)


def load_sample_data():
    """Illustrative practice data, not real student results."""
    sample = [
        (101, "Rahul", 85, 78, 90), (102, "Priya", 92, 88, 95),
        (103, "Amit", 35, 42, 38), (104, "Sneha", 65, 72, 80),
        (105, "Kiran", 28, 30, 25), (106, "Anjali", 75, 82, 70),
        (107, "Rohan", 55, 48, 60), (108, "Pooja", 88, 91, 85),
    ]
    for sid, name, py, sql, xl in sample:
        students.append({"ID": str(sid), "Name": name, "Age": "20",
                         "Course": "Data Analytics",
                         "Python": str(py), "SQL": str(sql), "Excel": str(xl)})
    save_students()


# ---------------------------------------------------------------
# Input helpers (validation)
# ---------------------------------------------------------------
def ask_mark(subject):
    while True:
        value = input(f"Enter {subject} marks (0-100): ").strip()
        try:
            mark = float(value)
            if 0 <= mark <= 100:
                return str(int(mark)) if mark == int(mark) else str(mark)
        except ValueError:
            pass
        print("Invalid marks. Enter a number between 0 and 100.")


def ask_age():
    while True:
        value = input("Enter Student Age: ").strip()
        if value.isdigit() and 0 < int(value) < 120:
            return value
        print("Invalid age. Enter a whole number.")


def find_student(student_id):
    for student in students:
        if student["ID"] == student_id:
            return student
    return None


# ---------------------------------------------------------------
# CRUD features
# ---------------------------------------------------------------
def add_student():
    student_id = input("Enter Student ID: ").strip()
    if not student_id:
        print("ID cannot be empty.")
        return
    if find_student(student_id):
        print("A student with this ID already exists.")
        return

    name = input("Enter Student Name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    age = ask_age()
    course = input("Enter Course: ").strip()

    student = {"ID": student_id, "Name": name, "Age": age, "Course": course}
    for subject in SUBJECTS:
        student[subject] = ask_mark(subject)

    students.append(student)
    save_students()
    print("Student added successfully!")


def print_student(student):
    print("ID:", student["ID"])
    print("Name:", student["Name"])
    print("Age:", student["Age"])
    print("Course:", student["Course"])
    for subject in SUBJECTS:
        print(f"{subject}:", student[subject])


def view_students():
    if len(students) == 0:
        print("No students found.")
        return
    print("\n----- Student Records -----")
    for student in students:
        print_student(student)
        print("--------------------------")


def search_student():
    search_id = input("Enter Student ID to search: ").strip()
    student = find_student(search_id)
    if student:
        print("\nStudent Found")
        print_student(student)
    else:
        print("Student not found.")


def update_student():
    update_id = input("Enter Student ID to update: ").strip()
    student = find_student(update_id)
    if not student:
        print("Student not found.")
        return

    print("Student Found!")
    student["Name"] = input("Enter New Name: ").strip() or student["Name"]
    student["Age"] = ask_age()
    student["Course"] = input("Enter New Course: ").strip() or student["Course"]
    for subject in SUBJECTS:
        student[subject] = ask_mark(subject)

    save_students()          # now runs after a successful update
    print("Student details updated successfully!")


def delete_student():
    delete_id = input("Enter Student ID to delete: ").strip()
    student = find_student(delete_id)
    if not student:
        print("Student not found.")
        return

    students.remove(student)
    save_students()          # now runs after a successful delete
    print("Student deleted successfully!")


# ---------------------------------------------------------------
# Analysis features
# ---------------------------------------------------------------
def get_dataframe():
    """Build a DataFrame from the latest records, with numeric marks."""
    if len(students) == 0:
        print("No student data to analyse.")
        return None
    df = pd.DataFrame(students)
    for subject in SUBJECTS:
        df[subject] = pd.to_numeric(df[subject])
    return df


def assign_grade(mark):
    if mark >= 90:
        return "A"
    elif mark >= 75:
        return "B"
    elif mark >= 60:
        return "C"
    elif mark >= 40:
        return "D"
    return "F"


def average_by_subject():
    df = get_dataframe()
    if df is None:
        return
    print("\nAverage marks by subject:")
    print(df[SUBJECTS].mean().round(2).to_string())


def highest_lowest():
    df = get_dataframe()
    if df is None:
        return
    print("\nHighest and lowest scores:")
    for s in SUBJECTS:
        top = df.loc[df[s].idxmax()]
        low = df.loc[df[s].idxmin()]
        print(f"{s}: highest {top['Name']} ({top[s]}), "
              f"lowest {low['Name']} ({low[s]})")


def pass_percentage():
    df = get_dataframe()
    if df is None:
        return
    passed = (df[SUBJECTS] >= PASS_MARK).all(axis=1).sum()
    pct = passed / len(df) * 100
    print(f"\nPass rule: at least {PASS_MARK} in every subject")
    print(f"Passed: {passed}/{len(df)}")
    print(f"Pass percentage: {pct:.2f}%")
    print(f"Fail percentage: {100 - pct:.2f}%")

    # Improvement 1: pass percentage for each subject separately
    subject_pass = (df[SUBJECTS] >= PASS_MARK).mean() * 100
    print(f"\nSubject-wise pass percentage (at least {PASS_MARK} in that subject):")
    print(subject_pass.round(2).to_string())
    lowest = subject_pass[subject_pass == subject_pass.min()]
    print(f"Lowest pass rate: {', '.join(lowest.index)} ({lowest.iloc[0]:.2f}%)")


def grade_distribution():
    df = get_dataframe()
    if df is None:
        return
    df["grade"] = df[SUBJECTS].mean(axis=1).apply(assign_grade)
    counts = df["grade"].value_counts().reindex(
        ["A", "B", "C", "D", "F"], fill_value=0)
    print("\nGrade distribution (based on average marks):")
    print(counts.to_string())


def students_at_risk():
    df = get_dataframe()
    if df is None:
        return
    risk = df[(df[SUBJECTS] < RISK_THRESHOLD).any(axis=1)]
    print(f"\nStudents below {RISK_THRESHOLD} in at least one subject:")
    if risk.empty:
        print("None.")
    else:
        print(risk[["ID", "Name"] + SUBJECTS].to_string(index=False))


def student_ranking():
    """Improvement 2: rank students by average marks, highest first."""
    df = get_dataframe()
    if df is None:
        return
    df["Average"] = df[SUBJECTS].mean(axis=1).round(2)
    ranked = df.sort_values("Average", ascending=False).reset_index(drop=True)
    ranked.insert(0, "Rank", ranked.index + 1)
    print("\nStudent ranking (by average marks):")
    print(ranked[["Rank", "Name", "Average"]].to_string(index=False))
    print(f"\nTop performer: {ranked.loc[0, 'Name']}")
    print(f"Needs the most support: {ranked.loc[len(ranked) - 1, 'Name']}")


def correlation_analysis():
    """Improvement 3: how strongly do subject marks move together?"""
    df = get_dataframe()
    if df is None:
        return
    if len(df) < 3:
        print("Correlation needs at least 3 students to be meaningful.")
        return
    print("\nCorrelation between subject marks:")
    print(df[SUBJECTS].corr().round(2).to_string())
    print("\nNote: correlation shows that marks move together; "
          "it does not show that one subject causes the other.")


def show_charts():
    df = get_dataframe()
    if df is None:
        return

    # Chart 1: average marks by subject
    df[SUBJECTS].mean().plot(kind="bar", color=["#4C72B0", "#55A868", "#C44E52"])
    plt.title("Average Marks by Subject")
    plt.xlabel("Subject")
    plt.ylabel("Average Marks")
    plt.xticks(rotation=0)
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.show()

    # Chart 2: grade distribution
    grades = df[SUBJECTS].mean(axis=1).apply(assign_grade)
    counts = grades.value_counts().reindex(["A", "B", "C", "D", "F"], fill_value=0)
    counts.plot(kind="bar", color="#4C72B0")
    plt.title("Student Grade Distribution")
    plt.xlabel("Grade")
    plt.ylabel("Number of Students")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

    # Chart 3: subject-wise pass percentage
    subject_pass = (df[SUBJECTS] >= PASS_MARK).mean() * 100
    subject_pass.plot(kind="bar", color=["#4C72B0", "#55A868", "#C44E52"])
    plt.title("Pass Percentage by Subject")
    plt.xlabel("Subject")
    plt.ylabel("Pass Percentage (%)")
    plt.xticks(rotation=0)
    plt.ylim(0, 100)
    plt.tight_layout()
    plt.show()

    # Chart 4: each student's marks with the pass-mark line
    df.set_index("Name")[SUBJECTS].plot(kind="bar", figsize=(9, 5))
    plt.axhline(PASS_MARK, color="red", linestyle="--",
                label=f"Pass mark ({PASS_MARK})")
    plt.title("Student Marks by Subject")
    plt.ylabel("Marks")
    plt.xticks(rotation=0)
    plt.legend()
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------
# Menu
# ---------------------------------------------------------------
def main():
    load_students()

    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("\n===== STUDENT PERFORMANCE ANALYSIS =====")
        print("6. Average Marks by Subject")
        print("7. Highest and Lowest Scores")
        print("8. Pass Percentage")
        print("9. Grade Distribution")
        print("10. Students at Risk")
        print("11. Student Ranking")
        print("12. Correlation Between Subjects")
        print("13. Display Performance Charts")
        print("14. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            update_student()
        elif choice == "5":
            delete_student()
        elif choice == "6":
            average_by_subject()
        elif choice == "7":
            highest_lowest()
        elif choice == "8":
            pass_percentage()
        elif choice == "9":
            grade_distribution()
        elif choice == "10":
            students_at_risk()
        elif choice == "11":
            student_ranking()
        elif choice == "12":
            correlation_analysis()
        elif choice == "13":
            show_charts()
        elif choice == "14":
            print("Thank you!")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
