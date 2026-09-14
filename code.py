from dataclasses import dataclass, asdict
from typing import List, Dict, Any
import json


@dataclass
class Subject:
    name: str
    hours: int
    room: str


@dataclass
class Teacher:
    name: str
    subject: str
    office_hours: str
    email: str


@dataclass
class FreeTimeActivity:
    activity: str
    hours: int
    category: str


class StudentDashboardBackend:
    """Core backend engine for student academic dashboard metrics and state management."""

    def __init__(self, student_name: str = "Youssef Amine"):
        self.student_name = student_name
        self.subjects: List[Subject] = [
            Subject("Python Algorithms", 8, "Lab 3B"),
            Subject("Database Systems", 6, "Room 204"),
            Subject("Web Architecture", 5, "Lab 1A"),
            Subject("Data Structures", 5, "Room 102"),
        ]
        self.teachers: List[Teacher] = [
            Teacher("Dr. Sarah Alami", "Python Algorithms", "Mon/Wed 2-4 PM", "s.alami@univ.ac.ma"),
            Teacher("Prof. Karim Tazi", "Database Systems", "Tue/Thu 10-12 AM", "k.tazi@univ.ac.ma"),
            Teacher("Dr. Nadia Benjelloun", "Web Architecture", "Fri 9-12 AM", "n.benjelloun@univ.ac.ma"),
        ]
        self.freetime_activities: List[FreeTimeActivity] = [
            FreeTimeActivity("Coding Side Projects", 6, "Tech"),
            FreeTimeActivity("Gaming (Strategy & RPG)", 4, "Entertainment"),
            FreeTimeActivity("Reading Tech Blogs & Books", 3, "Self-Improvement"),
            FreeTimeActivity("Football & Gym", 3, "Sports"),
        ]

    def get_weekly_summary(self) -> Dict[str, Any]:
        """Calculates study and free time totals without heavy external dependencies."""
        total_study = sum(s.hours for s in self.subjects)
        total_free = sum(a.hours for a in self.freetime_activities)

        return {
            "student_name": self.student_name,
            "total_study_hours": total_study,
            "total_freetime_hours": total_free,
            "study_to_free_ratio": round(total_study / max(total_free, 1), 2),
            "subjects_count": len(self.subjects),
        }

    def update_student_name(self, new_name: str) -> None:
        """Updates the student name safely."""
        if new_name.strip():
            self.student_name = new_name.strip()

    def update_teacher_name(self, original_name: str, new_name: str) -> bool:
        """Updates a teacher's name by matching their current name."""
        for teacher in self.teachers:
            if teacher.name.lower() == original_name.lower():
                teacher.name = new_name.strip()
                return True
        return False

    def export_all_data(self) -> Dict[str, Any]:
        """Serializes internal state into a clean API-ready JSON dictionary."""
        return {
            "summary": self.get_weekly_summary(),
            "subjects": [asdict(s) for s in self.subjects],
            "teachers": [asdict(t) for t in self.teachers],
            "freetime": [asdict(a) for a in self.freetime_activities],
        }


if __name__ == "__main__":
    engine = StudentDashboardBackend()
    
    # Update example
    engine.update_student_name("Youssef Amrani")
    engine.update_teacher_name("Dr. Sarah Alami", "Dr. Sarah Alami-Prof")

    print(json.dumps(engine.export_all_data(), indent=2))