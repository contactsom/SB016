from EdTechBackendSystem.User import User


class Instructor(User):
    def __init__(self, user_id, name, email, password):
        super().__init__(user_id, name, email, password)
        self.courses_taught = []

    def add_course(self, course):
        if course not in self.courses_taught:
            self.courses_taught.append(course)
            course.set_instructor(self)
            return True
        return False

    def remove_course(self, course):
        if course in self.courses_taught:
            self.courses_taught.remove(course)
            course.set_instructor(None)
            return True
        return False

    def get_courses_taught(self):
        return self.courses_taught

    def __str__(self):
        return f"Instructor - {super().__str__()}, Courses Taught: {len(self.courses_taught)}"
