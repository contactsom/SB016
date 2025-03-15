class Enrollment:
    def __init__(self, enrollment_id, learner, course, enrollment_date):
        self.enrollment_id = enrollment_id
        self.learner = learner
        self.course = course
        self.enrollment_date = enrollment_date
        self.status = "Active"  # Active, Completed, Dropped

        # Enroll the learner in the course
        learner.enroll_course(course)
        course.add_learner(learner)

    def complete_enrollment(self):
        self.status = "Completed"
        return True

    def drop_enrollment(self):
        self.status = "Dropped"
        self.learner.drop_course(self.course)
        self.course.remove_learner(self.learner)
        return True

    def __str__(self):
        return f"Enrollment ID: {self.enrollment_id}, Learner: {self.learner.name}, Course: {self.course.title}, Status: {self.status}, Date: {self.enrollment_date}"
