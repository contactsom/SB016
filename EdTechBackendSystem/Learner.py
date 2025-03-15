from EdTechBackendSystem.User import User


class Learner(User):
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, password)
        self.enrolled_courses = []

    def enroll_course(self, course):
        if course not in self.enrolled_courses:
            self.enrolled_courses.append(course)
            return True
        return False

    def drop_course(self, course):
        if course in self.enrolled_courses:
            self.enrolled_courses.remove(course)
            return True
        return False

    def get_enrolled_courses(self):
        return self.enrolled_courses

    def __str__(self):
        return f"Learner - {super().__str__()}, Enrolled Courses: {len(self.enrolled_courses)}"
