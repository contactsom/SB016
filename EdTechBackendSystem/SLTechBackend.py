from EdTechBackendSystem.Course import Course
from EdTechBackendSystem.Enrollment import Enrollment
from EdTechBackendSystem.Instructor import Instructor
from EdTechBackendSystem.Learner import Learner
from EdTechBackendSystem.User import User


class SLTechBackend:
    def __init__(self):
        self.users = {}  # user_id -> User object
        self.courses = {}  # course_id -> Course object
        self.enrollments = {}  # enrollment_id -> Enrollment object
        self.next_user_id = 1
        self.next_course_id = 1
        self.next_enrollment_id = 1

    def add_user(self, name, email, password, user_type):
        user_id = f"U{self.next_user_id:04d}"
        self.next_user_id += 1

        if user_type.lower() == "learner":
            user = Learner(user_id, name, email, password)
        elif user_type.lower() == "instructor":
            user = Instructor(user_id, name, email, password)
        else:
            user = User(user_id, name, email, password)

        self.users[user_id] = user
        return user

    def get_user(self, user_id):
        return self.users.get(user_id)

    def list_users(self, user_type=None):
        if user_type:
            if user_type.lower() == "learner":
                return [user for user in self.users.values() if isinstance(user, Learner)]
            elif user_type.lower() == "instructor":
                return [user for user in self.users.values() if isinstance(user, Instructor)]
        return list(self.users.values())

    def add_course(self, title, description, duration):
        course_id = f"C{self.next_course_id:04d}"
        self.next_course_id += 1

        course = Course(course_id, title, description, duration)
        self.courses[course_id] = course
        return course

    def get_course(self, course_id):
        return self.courses.get(course_id)

    def list_courses(self):
        return list(self.courses.values())

    def enroll_learner(self, learner_id, course_id, enrollment_date):
        learner = self.get_user(learner_id)
        course = self.get_course(course_id)

        if not learner or not course or not isinstance(learner, Learner):
            return None

        enrollment_id = f"E{self.next_enrollment_id:04d}"
        self.next_enrollment_id += 1

        enrollment = Enrollment(enrollment_id, learner, course, enrollment_date)
        self.enrollments[enrollment_id] = enrollment
        return enrollment

    def get_enrollment(self, enrollment_id):
        return self.enrollments.get(enrollment_id)

    def list_enrollments(self, status=None):
        if status:
            return [enrollment for enrollment in self.enrollments.values() if enrollment.status == status]
        return list(self.enrollments.values())

    def get_learner_enrollments(self, learner_id):
        learner = self.get_user(learner_id)
        if not learner or not isinstance(learner, Learner):
            return []

        return [enrollment for enrollment in self.enrollments.values() if enrollment.learner == learner]

    def get_course_enrollments(self, course_id):
        course = self.get_course(course_id)
        if not course:
            return []

        return [enrollment for enrollment in self.enrollments.values() if enrollment.course == course]

    def assign_instructor(self, instructor_id, course_id):
        instructor = self.get_user(instructor_id)
        course = self.get_course(course_id)

        if not instructor or not course or not isinstance(instructor, Instructor):
            return False

        return instructor.add_course(course)


# Interactive function to handle user input
def run_sltech_system():
    backend = SLTechBackend()

    # Add sample users
    print("Adding sample users...")
    instructor1 = backend.add_user("John Smith", "john@sltech.com", "password123", "instructor")
    instructor2 = backend.add_user("Jane Doe", "jane@sltech.com", "password456", "instructor")
    learner1 = backend.add_user("Bob Johnson", "bob@example.com", "pass1234", "learner")
    learner2 = backend.add_user("Alice Brown", "alice@example.com", "pass5678", "learner")
    print("Users added successfully\n")

    # Add sample courses
    print("Adding sample courses...")
    course1 = backend.add_course("Python Programming", "Learn Python basics and advanced concepts", 8)
    course2 = backend.add_course("Data Science Fundamentals", "Introduction to Data Science with Python", 12)
    course3 = backend.add_course("Web Development", "Full stack web development with HTML, CSS, and JavaScript", 10)
    print("Courses added successfully\n")

    # Assign instructors to courses
    print("Assigning instructors to courses...")
    backend.assign_instructor(instructor1.user_id, course1.course_id)
    backend.assign_instructor(instructor1.user_id, course2.course_id)
    backend.assign_instructor(instructor2.user_id, course3.course_id)
    print("Instructors assigned successfully\n")

    # Enroll learners in courses
    print("Enrolling learners in courses...")
    enrollment1 = backend.enroll_learner(learner1.user_id, course1.course_id, "2025-03-15")
    enrollment2 = backend.enroll_learner(learner1.user_id, course2.course_id, "2025-03-15")
    enrollment3 = backend.enroll_learner(learner2.user_id, course1.course_id, "2025-03-10")
    enrollment4 = backend.enroll_learner(learner2.user_id, course3.course_id, "2025-03-12")
    print("Learners enrolled successfully\n")

    # Display all users
    print("=== All Users ===")
    for user in backend.list_users():
        print(user)
    print()

    # Display all courses with their details
    print("=== All Courses ===")
    for course in backend.list_courses():
        print(course)
    print()

    # Display all enrollments
    print("=== All Enrollments ===")
    for enrollment in backend.list_enrollments():
        print(enrollment)
    print()

    # Drop a course
    print("=== Dropping a Course ===")
    enrollment2.drop_enrollment()
    print(f"Enrollment status after dropping: {enrollment2}")
    print()

    # Display enrolled courses for a learner
    print("=== Enrolled Courses for Bob Johnson ===")
    for course in learner1.get_enrolled_courses():
        print(course)
    print()

    # Display courses taught by an instructor
    print("=== Courses Taught by John Smith ===")
    for course in instructor1.get_courses_taught():
        print(course)
    print()

    print("SL Tech Backend System Demo Completed")


if __name__ == "__main__":
    run_sltech_system()