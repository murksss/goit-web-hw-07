from connect_db import session
from models import Groups, Students, Teachers, Subjects, Marks
import calendar
from datetime import datetime
import faker
from random import randint, choice

NUMBER_GROUPS = 3
NUMBER_STUDENTS = 40
NUMBER_TEACHERS = 4


def generate_random_date(year):
    month = randint(1, 12)
    days_in_month = calendar.monthrange(year, month)[1]
    day = randint(1, days_in_month)
    return datetime(year, month, day).date().isoformat()


def generate_fake_data(number_of_gropus,
                       number_of_students,
                       number_of_teachers,
                       ) -> tuple:
    """ generate fake data list """

    fake_groups = list()
    fake_students = list()
    fake_teachers = list()

    fake = faker.Faker()

    # create groups list
    for _ in range(number_of_gropus):
        fake_groups.append(fake.unique.lexify(text="?????"))

    # create students list
    for _ in range(number_of_students):
        fake_students.append(fake.unique.name())

    # create subjects list
    fake_subjects = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'Computer Science', 'Art', 'Music']

    # create teachers list
    for _ in range(number_of_teachers):
        fake_teachers.append(fake.unique.name())

    fake_marks = range(1, 101)

    return fake_groups, fake_students, fake_subjects, fake_teachers, fake_marks


def insert_data(groups, students, subjects, teachers, marks) -> None:

    for_groups = [Groups(group_name=group) for group in groups]
    session.add_all(for_groups)
    groups_ids = [group.pk_id for group in session.query(Groups).all()]

    for_students = [Students(student_name=student, fk_group_id=choice(groups_ids)) for student in students]
    session.add_all(for_students)
    students_ids = [student.pk_id for student in session.query(Students).all()]

    for_teachers = [Teachers(teacher_name=teacher) for teacher in teachers]
    session.add_all(for_teachers)
    teachers_ids = [teacher.pk_id for teacher in session.query(Teachers).all()]

    for_subjects = [
        Subjects(subject_name=subject, fk_teacher_id=choice(teachers_ids)) for subject in subjects
    ]
    session.add_all(for_subjects)
    subjects_ids = [subject.pk_id for subject in session.query(Subjects).all()]

    for_marks = [
        Marks(
            mark_value=choice(marks),
            mark_date=generate_random_date(2024),
            fk_subject_id=choice(subjects_ids),
            fk_student_id=choice(students_ids)
        ) for _ in range(len(students) * randint(13, 21))
    ]
    session.add_all(for_marks)

    session.commit()


if __name__ == "__main__":
    insert_data(*generate_fake_data(NUMBER_GROUPS, NUMBER_STUDENTS, NUMBER_TEACHERS))
