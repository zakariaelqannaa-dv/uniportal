import json
import os
from dataclasses import dataclass, asdict
from typing import List, Optional

# ==========================================
# 1. DATA MODELS (Using Dataclasses)
# ==========================================

@dataclass
class Teacher:
    teacher_id: str
    name: str
    subject: str
    office_hours: str

@dataclass
class Student:
    student_id: str
    name: str
    major: str
    study_hours_per_week: int
    free_time_activities: List[str]

# ==========================================
# 2. SYSTEM MANAGER (Business Logic & Storage)
# ==========================================

class UniversitySystem:
    """Manages the university data, including loading and saving to a JSON file."""
    
    FILE_PATH = "uni_dashboard_data.json"

    def __init__(self):
        self.student: Optional[Student] = None
        self.teachers: List[Teacher] = []
        self.load_data()

    def _generate_mock_data(self):
        """Generates default data if no JSON file exists."""
        self.student = Student(
            student_id="CS-2024-890",
            name="Youssef Amrani",
            major="Computer Science (Data Engineering)",
            study_hours_per_week=32,
            free_time_activities=["Algorithmic Trading", "Tennis", "Reading Research Papers"]
        )
        self.teachers = [
            Teacher(teacher_id="T01", name="Dr. Amina Benali", subject="Advanced Algorithms", office_hours="Mon/Wed 14:00 - 16:00"),
            Teacher(teacher_id="T02", name="Prof. Karim Tazi", subject="Distributed Databases", office_hours="Tue/Thu 10:00 - 12:00")
        ]
        self.save_data()

    def load_data(self):
        """Loads data from the JSON file."""
        if not os.path.exists(self.FILE_PATH):
            self._generate_mock_data()
            return

        try:
            with open(self.FILE_PATH, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.student = Student(**data.get("student", {}))
                self.teachers = [Teacher(**t) for t in data.get("teachers", [])]
        except Exception as e:
            print(f"\n[!] Error loading data: {e}. Generating default data...")
            self._generate_mock_data()

    def save_data(self):
        """Serializes current objects and saves them to the JSON file."""
        data = {
            "student": asdict(self.student),
            "teachers": [asdict(t) for t in self.teachers]
        }
        with open(self.FILE_PATH, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)

    def update_student_name(self, new_name: str) -> None:
        if self.student:
            self.student.name = new_name
            self.save_data()

    def update_teacher_name(self, t_id: str, new_name: str) -> bool:
        for teacher in self.teachers:
            if teacher.teacher_id.upper() == t_id.upper():
                teacher.name = new_name
                self.save_data()
                return True
        return False


# ==========================================
# 3. USER INTERFACE (Terminal Render & Menus)
# ==========================================

class DashboardCLI:
    """Handles terminal rendering and user input loops."""
    
    # ANSI Color Codes for aesthetic terminal output
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

    def __init__(self):
        self.system = UniversitySystem()

    def clear_screen(self):
        """Clears the terminal screen for a clean UI update."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_dashboard(self):
        """Renders the dashboard with data formatted cleanly."""
        self.clear_screen()
        print(f"{self.CYAN}{self.BOLD}" + "=" * 60)
        print("               UNIVERSITY ACADEMIC DASHBOARD")
        print("=" * 60 + f"{self.ENDC}")

        # Student Section
        s = self.system.student
        print(f"\n{self.HEADER}🎓 [ STUDENT PROFILE ]{self.ENDC}")
        print(f"   {self.BOLD}Name{self.ENDC}         : {s.name}")
        print(f"   {self.BOLD}ID Number{self.ENDC}    : {s.student_id}")
        print(f"   {self.BOLD}Major{self.ENDC}        : {s.major}")
        print(f"   {self.BOLD}Study/Week{self.ENDC}   : {s.study_hours_per_week} hours")
        print(f"   {self.BOLD}Free Time{self.ENDC}    : {', '.join(s.free_time_activities)}")

        # Teachers Section
        print(f"\n{self.HEADER}👨‍🏫 [ FACULTY OVERVIEW ]{self.ENDC}")
        for t in self.system.teachers:
            print(f"   {self.BLUE}[{t.teacher_id}]{self.ENDC} {self.BOLD}{t.name}{self.ENDC}")
            print(f"         Subject      : {t.subject}")
            print(f"         Office Hours : {t.office_hours}")
            print("   " + "-" * 40)
        print(f"{self.CYAN}" + "=" * 60 + f"{self.ENDC}\n")

    def run(self):
        """Main application loop."""
        while True:
            self.display_dashboard()

            print(f"{self.BOLD}System Actions:{self.ENDC}")
            print("  [1] Edit Student Name")
            print("  [2] Edit Faculty Member Name")
            print("  [3] Exit System\n")

            choice = input(f"{self.WARNING}Select an action (1-3) > {self.ENDC}").strip()

            if choice == "1":
                new_name = input(f"{self.GREEN}Enter new student name: {self.ENDC}").strip()
                if new_name:
                    self.system.update_student_name(new_name)
                    print(f"{self.GREEN}✔ Student profile updated successfully!{self.ENDC}")
                else:
                    print(f"{self.FAIL}✖ Name cannot be empty.{self.ENDC}")
                self._pause()

            elif choice == "2":
                t_id = input(f"{self.GREEN}Enter the Faculty ID (e.g., T01): {self.ENDC}").strip()
                new_t_name = input(f"{self.GREEN}Enter the new name for this faculty member: {self.ENDC}").strip()
                
                if new_t_name:
                    success = self.system.update_teacher_name(t_id, new_t_name)
                    if success:
                        print(f"{self.GREEN}✔ Faculty profile updated successfully!{self.ENDC}")
                    else:
                        print(f"{self.FAIL}✖ Faculty ID '{t_id}' not found in the system.{self.ENDC}")
                else:
                    print(f"{self.FAIL}✖ Name cannot be empty.{self.ENDC}")
                self._pause()

            elif choice == "3":
                self.clear_screen()
                print(f"{self.GREEN}Saving state... Terminating session. Goodbye!{self.ENDC}")
                break
            
            else:
                print(f"{self.FAIL}✖ Invalid input. Please try again.{self.ENDC}")
                self._pause()

    def _pause(self):
        """Helper to pause the terminal before refreshing the UI."""
        input(f"\n{self.BOLD}Press Enter to return to the dashboard...{self.ENDC}")


# ==========================================
# 4. EXECUTION
# ==========================================
if __name__ == "__main__":
    app = DashboardCLI()
    app.run()