import io
import os
import PIL
import secrets

import face_recognition
import numpy as np
from flask import current_app
from flask_login import UserMixin
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Text, Time, func
from sqlalchemy.orm import relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.sql import expression

from app.services import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(Text, nullable=False)
    is_admin = Column(Boolean, server_default=expression.false())
    is_instructor = Column(Boolean, server_default=expression.false())
    is_student = Column(Boolean, server_default=expression.false())

    # Relationships
    instructor = relationship(
        'Instructor',
        backref='user',
        cascade='all, delete',
        uselist=False,
    )
    student = relationship(
        'Student',
        backref='user',
        cascade='all, delete',
        uselist=False,
    )


class Department(db.Model):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)

    # Relationships
    courses = relationship('Course', backref='department', cascade='all, delete')
    instructors = relationship('Instructor', backref='department', cascade='all, delete')


course_subject = db.Table(
    'course_subject',
    Column('course_id', Integer, ForeignKey('courses.id'), nullable=False),
    Column('subject_id', Integer, ForeignKey('subjects.id'), nullable=False),
    UniqueConstraint('course_id', 'subject_id', name='uq_course_subject'),
)


class Course(db.Model):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    name = Column(String(255), unique=True, nullable=False)

    # Relationships
    students = relationship('Student', backref='course', cascade='all, delete')
    subjects = relationship(
        'Subject',
        secondary=course_subject,
        backref='courses',
        cascade='all, delete',
    )

    def subjects_by_term(self, year_level, semester):
        subjects = []

        for subject in self.subjects:
            if subject.year_level == year_level and subject.semester == semester:
                subjects.append(subject)

        return subjects


class Subject(db.Model):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    year_level = Column(String(255), nullable=False)
    semester = Column(String(255), nullable=False)
    descriptive_title = Column(String(255), unique=True, nullable=False)
    course_number = Column(String(255), unique=True, nullable=False)
    lecture_hours = Column(Integer, nullable=False)
    laboratory_hours = Column(Integer, nullable=False)
    units = Column(Integer, nullable=False)

    # Relationships
    faculty_loads = relationship('FacultyLoad', backref='subject', cascade='all, delete')


class Instructor(db.Model):
    __tablename__ = 'instructors'

    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)

    # Relationships
    faculty_loads = relationship('FacultyLoad', backref='instructor', cascade='all, delete')

    def has_subject(self, subject) -> bool:
        for load in self.faculty_loads:
            if load.subject == subject:
                return True

        return False


faculty_load_student = db.Table(
    'faculty_load_student',
    Column('id', Integer, primary_key=True),
    Column('faculty_load_id', Integer, ForeignKey('faculty_loads.id'), nullable=False),
    Column('student_id', Integer, ForeignKey('students.id'), nullable=False),
    UniqueConstraint('faculty_load_id', 'student_id', name='uq_faculty_load_student'),
)


class Student(db.Model):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    student_id = Column(String(255), unique=True, nullable=False)
    last_name = Column(String(64), nullable=False)
    first_name = Column(String(64), nullable=False)
    middle_name = Column(String(64))
    gender = Column(String(64), nullable=False)
    birthdate = Column(Date, nullable=False)
    year_level = Column(String(64), nullable=False)
    contact_number = Column(String(64), nullable=False)
    image = Column(Text)

    # Relationships
    attendance = relationship('Attendance', backref='student', cascade='all, delete')

    def verify_face(self, image) -> bool:
        if not self.image:
            return False

        # Pre-process student image
        profile = face_recognition.load_image_file(
            os.path.join(
                current_app.config['UPLOADS_FOLDER'],
                self.image,
            )
        )
        profile_encoding = face_recognition.face_encodings(profile, num_jitters=5)
        if not profile_encoding:
            return False
        profile_encoding = profile_encoding[0]

        buffer = PIL.Image.open(image)
        buffer = buffer.convert("RGB")

        # Pre-process image upload
        face_locations = face_recognition.face_locations(
            np.array(buffer),
            number_of_times_to_upsample=2,
        )
        if not face_locations:
            return False

        image_encoding = face_recognition.face_encodings(
            np.array(buffer),
            face_locations,
            num_jitters=5,
        )[0]

        result = face_recognition.compare_faces(
            [profile_encoding],
            image_encoding,
            tolerance=0.5,
        )[0]

        # Return the result of the face comparison
        return result


class FacultyLoad(db.Model):
    __tablename__ = 'faculty_loads'

    id = Column(Integer, primary_key=True)
    instructor_id = Column(Integer, ForeignKey('instructors.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    school_year = Column(String(255), nullable=False)
    semester = Column(String(255), nullable=False)
    room = Column(String(255), nullable=False)
    day = Column(String(255), nullable=False)
    time_start = Column(Time, nullable=False)
    time_end = Column(Time, nullable=False)

    __table_args__ = (
        UniqueConstraint('instructor_id', 'subject_id', name='uq_faculty_load'),
    )

    # Relationships
    students = relationship(
        'Student',
        secondary=faculty_load_student,
        backref='schedules',
        cascade='all, delete',
    )
    qrcodes = relationship(
        'QRCode',
        backref='faculty_load',
        cascade='all, delete',
    )


class QRCode(db.Model):
    __tablename__ = 'qrcodes'

    id = Column(Integer, primary_key=True)
    faculty_load_id = Column(Integer, ForeignKey('faculty_loads.id'), nullable=False)
    token = Column(Text, unique=True, default=secrets.token_hex, nullable=False)
    created_at = Column(DateTime, server_default=func.current_timestamp())

    # Relationships
    attendance = relationship('Attendance', backref='qrcode', cascade='all, delete')


class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True)
    qrcode_id = Column(Integer, ForeignKey('qrcodes.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    time_in = Column(DateTime, server_default=func.current_timestamp())
    time_out = Column(DateTime)
    time_in_image = Column(Text)
    time_out_image = Column(Text)


@login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(user_id)
