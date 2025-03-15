class Course:
    def __init__(self, course_id, title, description, duration):
        self.course_id = course_id
        self.title = title
        self.description = description
        self.duration = duration  # in weeks
        self.instructor = None
        self.enrolled_learners = []

    def set_instructor(self, instructor):
        self.instructor = instructor

    def add_learner(self, learner):
        if learner not in self.enrolled_learners:
            self.enrolled_learners.append(learner)
            return True
        return False

    def remove_learner(self, learner):
        if learner in self.enrolled_learners:
            self.enrolled_learners.remove(learner)
            return True
        return False

    def list_learners(self):
        return self.enrolled_learners

    def __str__(self):
        instructor_name = self.instructor.name if self.instructor else "No instructor assigned"
        return f"Course ID: {self.course_id}, Title: {self.title}, Duration: {self.duration} weeks, Instructor: {instructor_name}, Enrolled Learners: {len(self.enrolled_learners)}"
