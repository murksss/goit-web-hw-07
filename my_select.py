from connect_db import session
from models import Groups, Students, Teachers, Subjects, Marks
from sqlalchemy import func, desc, and_, select


def display_table(data):
    max_lengths = [max(len(str(item)) for item in column) for column in zip(*data)]

    for row in data:
        print(" | ".join(f"{str(cell):<{max_lengths[i]}}" for i, cell in enumerate(row)))

    print('~' * 50)


def select_1(_session):
    """1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    q = _session.query(
        Students.student_name,
        func.round(func.avg(Marks.mark_value), 2).label('avg_mark')
    ).select_from(Marks).join(Students).group_by(Students.pk_id).order_by(desc('avg_mark')).limit(5).all()

    return q


def select_2(_session):
    """2. Знайти студента із найвищим середнім балом з певного предмета."""
    q = (session.query(
        Students.student_name,
        func.round(func.avg(Marks.mark_value), 2).label('avg_mark'))
         .join(Marks, Students.pk_id == Marks.fk_student_id)
         .filter(Marks.fk_subject_id == 1)
         .group_by(Students.pk_id)
         .order_by(desc(func.avg(Marks.mark_value)))
         .limit(1)
         ).all()

    return q


def select_3(_session):
    """3. Знайти середній бал у групах з певного предмета."""
    q = (session.query(
        Groups.group_name,
        Subjects.subject_name,
        func.round(func.avg(Marks.mark_value), 2).label('avg_mark'))
         .join(Students, Students.fk_group_id == Groups.pk_id)
         .join(Marks, Marks.fk_student_id == Students.pk_id)
         .join(Subjects, Subjects.pk_id == Marks.fk_subject_id)
         .filter(Subjects.pk_id == 3)
         .group_by(Groups.pk_id, Subjects.pk_id)
         .order_by(desc(func.avg(Marks.mark_value)))
         ).all()

    return q


def select_4(_session):
    """4. Знайти середній бал на потоці (по всій таблиці оцінок)."""
    q = (session.query(
        Subjects.subject_name,
        func.round(func.avg(Marks.mark_value), 2).label('avg_mark'))
         .join(Subjects, Subjects.pk_id == Marks.fk_subject_id)
         .group_by(Subjects.pk_id)
         .order_by(desc(func.avg(Marks.mark_value)))
         ).all()

    return q


def select_5(_session):
    """5. Знайти які курси читає певний викладач."""
    q = (session.query(
        Teachers.teacher_name, Subjects.subject_name)
         .join(Subjects, Subjects.fk_teacher_id == Teachers.pk_id)
         .order_by(Teachers.teacher_name)
         ).all()

    return q


def select_6(_session):
    """6. Знайти список студентів у певній групі."""
    q = (session.query(
        Students.student_name,
        Groups.group_name)
         .join(Groups, Groups.pk_id == Students.fk_group_id)
         .filter(Groups.pk_id == 3)
         .order_by(Students.student_name)
         ).all()

    return q


def select_7(_session):
    """7. Знайти оцінки студентів у окремій групі з певного предмета."""
    q = (session.query(
        Subjects.subject_name,
        Groups.group_name,
        Students.student_name,
        Marks.mark_value)
         .join(Students, Students.pk_id == Marks.fk_student_id)
         .join(Groups, Groups.pk_id == Students.fk_group_id)
         .join(Subjects, Subjects.pk_id == Marks.fk_subject_id)
         .filter(and_(Subjects.pk_id == 2, Groups.pk_id == 1))
         .order_by(Students.student_name)
         ).all()

    return q


def select_8(_session):
    """8. Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    q = (
        session.query(
            Teachers.teacher_name,
            Subjects.subject_name,
            func.round(func.avg(Marks.mark_value), 2).label('avg_mark')
        )
        .join(Subjects, Marks.fk_subject_id == Subjects.pk_id)
        .join(Teachers, Subjects.fk_teacher_id == Teachers.pk_id)
        .group_by(Teachers.teacher_name, Subjects.subject_name)
        .order_by(Teachers.teacher_name)
    ).all()

    return q


def select_9(_session):
    """9. Знайти список курсів, які відвідує певний студент."""
    q = (
        session.query(
            Students.student_name,
            Subjects.subject_name
        )
        .join(Marks, Marks.fk_student_id == Students.pk_id)
        .join(Subjects, Subjects.pk_id == Marks.fk_subject_id)
        .filter(Students.pk_id == 2)
        .group_by(Students.student_name, Subjects.pk_id)
        .order_by(Subjects.subject_name)
    ).all()

    return q


def select_10(_session):
    """10. Список курсів, які певному студенту читає певний викладач."""
    q = (
        session.query(
            Students.student_name,
            Teachers.teacher_name,
            Subjects.subject_name
        )
        .join(Marks, Marks.fk_student_id == Students.pk_id)
        .join(Subjects, Subjects.pk_id == Marks.fk_subject_id)
        .join(Teachers, Teachers.pk_id == Subjects.fk_teacher_id)
        .filter(and_(Students.pk_id == 2, Teachers.pk_id == 4))
        .group_by(Students.student_name, Teachers.teacher_name, Subjects.subject_name)
        .order_by(Subjects.subject_name)
    ).all()

    return q


if __name__ == '__main__':
    display_table(select_1(session))
    display_table(select_2(session))
    display_table(select_3(session))
    display_table(select_4(session))
    display_table(select_5(session))
    display_table(select_6(session))
    display_table(select_7(session))
    display_table(select_8(session))
    display_table(select_9(session))
    display_table(select_10(session))
