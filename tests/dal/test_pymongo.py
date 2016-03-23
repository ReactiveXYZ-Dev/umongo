import pytest
from datetime import datetime
from functools import namedtuple
from bson import ObjectId
from pymongo import MongoClient, IndexModel, ASCENDING

from ..common import BaseTest, get_pymongo_version
from ..test_indexes import assert_indexes
from ..fixtures import classroom_model

from umongo import Document, fields, exceptions, Reference


# Check if the required dependancies are met to run this driver's tests
major, minor, _ = get_pymongo_version()
if int(major) != 3 or int(minor) < 2:
    dep_error = "pymongo driver requires pymongo>=3.2.0"
else:
    dep_error = None

if not dep_error:  # Make sure the module is valid by importing it
    from umongo.dal import pymongo


@pytest.fixture
def db():
    return MongoClient().umongo_test


@pytest.mark.skipif(dep_error is not None, reason=dep_error)
class TestPymongo(BaseTest):

    def test_create(self, classroom_model):
        Student = classroom_model.Student
        john = Student(name='John Doe', birthday=datetime(1995, 12, 12))
        john.commit()
        assert john.to_mongo() == {
            '_id': john.id,
            'name': 'John Doe',
            'birthday': datetime(1995, 12, 12)
        }


        john2 = Student.find_one(john.id)
        assert john2._data == john._data

    def test_update(self, classroom_model):
        Student = classroom_model.Student
        john = Student(name='John Doe', birthday=datetime(1995, 12, 12))
        john.commit()
        john.name = 'William Doe'
        assert john.to_mongo(update=True) == {'$set': {'name': 'William Doe'}}
        john.commit()
        assert john.to_mongo(update=True) == None
        john2 = Student.find_one(john.id)
        assert john2._data == john._data

    def test_delete(self, classroom_model):
        Student = classroom_model.Student
        Student.collection.drop()
        john = Student(name='John Doe', birthday=datetime(1995, 12, 12))
        john.commit()
        assert Student.collection.find().count() == 1
        john.delete()
        assert Student.collection.find().count() == 0
        with pytest.raises(exceptions.DeleteError):
           john.delete()

    def test_reload(self, classroom_model):
        Student = classroom_model.Student
        john = Student(name='John Doe', birthday=datetime(1995, 12, 12))
        with pytest.raises(exceptions.NotCreatedError):
            john.reload()
        john.commit()
        john2 = Student.find_one(john.id)
        john2.name = 'William Doe'
        john2.commit()
        john.reload()
        assert john.name == 'William Doe'

    def test_cusor(self, classroom_model):
        Student = classroom_model.Student
        Student.collection.drop()
        for i in range(10):
            Student(name='student-%s' % i).commit()
        cursor = Student.find(limit=5, skip=6)
        assert cursor.count() == 10
        assert cursor.count(with_limit_and_skip=True) == 4
        names = []
        for elem in cursor:
            assert isinstance(elem, Student)
            names.append(elem.name)
        assert sorted(names) == ['student-%s' % i for i in range(6, 10)]

        # Make sure this kind of notation doesn't create new cursor
        cursor = Student.find()
        cursor_limit = cursor.limit(5)
        cursor_skip = cursor.skip(6)
        assert cursor is cursor_limit is cursor_skip

    def test_classroom(self, classroom_model):
        student = classroom_model.Student(name='Marty McFly', birthday=datetime(1968, 6, 9))
        student.commit()
        teacher = classroom_model.Teacher(name='M. Strickland')
        teacher.commit()
        course = classroom_model.Course(name='Overboard 101', teacher=teacher)
        course.commit()
        assert student.courses == []
        student.courses.append(course)
        student.commit()
        assert student.to_mongo() == {
            '_id': student.pk,
            'name': 'Marty McFly',
            'birthday': datetime(1968, 6, 9),
            'courses': [course.pk]
        }

    def test_reference(self, classroom_model):
        teacher = classroom_model.Teacher(name='M. Strickland')
        teacher.commit()
        course = classroom_model.Course(name='Overboard 101', teacher=teacher)
        course.commit()
        assert isinstance(course.teacher, Reference)
        teacher_fetched = course.teacher.io_fetch()
        assert teacher_fetched == teacher
        # Test bad ref as well
        course.teacher = Reference(classroom_model.Teacher, ObjectId())
        with pytest.raises(exceptions.ValidationError) as exc:
            course.io_validate()
        assert exc.value.messages == {'teacher': ['Reference not found for document Teacher.']}

    def test_required(self, classroom_model):
        Student = classroom_model.Student
        student = Student(birthday=datetime(1968, 6, 9))

        with pytest.raises(exceptions.ValidationError):
            student.io_validate()

        with pytest.raises(exceptions.ValidationError):
            student.commit()

        student.name = 'Marty'
        student.commit()
        # with pytest.raises(exceptions.ValidationError):
        #     Student.build_from_mongo({})

    def test_io_validate(self, classroom_model):
        Student = classroom_model.Student

        io_field_value = 'io?'
        io_validate_called = False

        def io_validate(field, value):
            assert field == IOStudent.schema.fields['io_field']
            assert value == io_field_value
            nonlocal io_validate_called
            io_validate_called = True

        class IOStudent(Student):
            io_field = fields.StrField(io_validate=io_validate)

        student = IOStudent(name='Marty', io_field=io_field_value)
        assert not io_validate_called

        student.io_validate()
        assert io_validate_called

    def test_io_validate_error(self, classroom_model):
        Student = classroom_model.Student

        def io_validate(field, value):
            raise exceptions.ValidationError('Ho boys !')

        class IOStudent(Student):
            io_field = fields.StrField(io_validate=io_validate)

        student = IOStudent(name='Marty', io_field='io?')
        with pytest.raises(exceptions.ValidationError) as exc:
            student.io_validate()
        assert exc.value.messages == {'io_field': ['Ho boys !']}

    def test_io_validate_multi_validate(self, classroom_model):
        Student = classroom_model.Student
        called = []

        def io_validate1(field, value):
            called.append('io_validate1')

        def io_validate2(field, value):
            called.append('io_validate2')

        class IOStudent(Student):
            io_field = fields.StrField(io_validate=(io_validate1, io_validate2))

        student = IOStudent(name='Marty', io_field='io?')
        student.io_validate()
        assert called == ['io_validate1', 'io_validate2']

    def test_io_validate_list(self, classroom_model):
        Student = classroom_model.Student
        called = []
        values = [1, 2, 3, 4]

        def io_validate(field, value):
            called.append(value)

        class IOStudent(Student):
            io_field = fields.ListField(fields.IntField(io_validate=io_validate))

        student = IOStudent(name='Marty', io_field=values)
        student.io_validate()
        assert called == values

    def test_indexes(self, db):

        class SimpleIndexDoc(Document):
            indexed = fields.StrField()
            no_indexed = fields.IntField()

            class Config:
                collection = db.simple_index_doc
                indexes = ['indexed']

        # Make sure only _id default index is present first
        SimpleIndexDoc.collection.drop_indexes()
        indexes = [e for e in SimpleIndexDoc.collection.list_indexes()]
        assert indexes == [
            {
                'key': {'_id': 1},
                'name': '_id_',
                'ns': 'umongo_test.simple_index_doc',
                'v': 1
            }
        ]

        # Now ask for indexes building
        SimpleIndexDoc.ensure_indexes()
        indexes = [e for e in SimpleIndexDoc.collection.list_indexes()]
        expected_indexes = [
            {
                'key': {'_id': 1},
                'name': '_id_',
                'ns': 'umongo_test.simple_index_doc',
                'v': 1
            },
            {
                'v': 1,
                'key': {'indexed': 1},
                'name': 'indexed_1',
                'ns': 'umongo_test.simple_index_doc'
            }
        ]
        assert indexes == expected_indexes

        # Redoing indexes building should do nothing
        SimpleIndexDoc.ensure_indexes()
        assert indexes == expected_indexes

    def test_indexes_inheritance(self, db):

        class SimpleIndexDoc(Document):
            indexed = fields.StrField()
            no_indexed = fields.IntField()

            class Config:
                collection = db.simple_index_doc
                indexes = ['indexed']

        # Make sure only _id default index is present first
        SimpleIndexDoc.collection.drop_indexes()
        indexes = [e for e in SimpleIndexDoc.collection.list_indexes()]
        assert indexes == [
            {
                'key': {'_id': 1},
                'name': '_id_',
                'ns': 'umongo_test.simple_index_doc',
                'v': 1
            }
        ]

        # Now ask for indexes building
        SimpleIndexDoc.ensure_indexes()
        indexes = [e for e in SimpleIndexDoc.collection.list_indexes()]
        expected_indexes = [
            {
                'key': {'_id': 1},
                'name': '_id_',
                'ns': 'umongo_test.simple_index_doc',
                'v': 1
            },
            {
                'v': 1,
                'key': {'indexed': 1},
                'name': 'indexed_1',
                'ns': 'umongo_test.simple_index_doc'
            }
        ]
        assert indexes == expected_indexes

        # Redoing indexes building should do nothing
        SimpleIndexDoc.ensure_indexes()
        assert indexes == expected_indexes
