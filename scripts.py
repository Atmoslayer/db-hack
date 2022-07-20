import random

from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Chastisement
from datacenter.models import Lesson
from datacenter.models import Subject
from datacenter.models import Commendation


def get_schoolkid_by_name(schoolkid_name):
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        return schoolkid
    except ObjectDoesNotExist:
        print('Имя не найдено')
    except MultipleObjectsReturned:
        schoolkids = []
        schoolkid_objects = Schoolkid.objects.filter(full_name__contains=schoolkid_name)
        for schoolkid_object in schoolkid_objects:
            schoolkids.append(schoolkid_object.full_name)
        print(f'Найдено несколько вариантов: {schoolkids}')


def fix_marks(schoolkid_name):
    schoolkid = get_schoolkid_by_name(schoolkid_name)
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)


def remove_chastisements(schoolkid_name):
    schoolkid = get_schoolkid_by_name(schoolkid_name)
    child_chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    child_chastisements.delete()


def create_commendation(schoolkid_name, subject_title):
    schoolkid = get_schoolkid_by_name(schoolkid_name)
    сommendations = ['Молодец!', 'Отлично, как всегда!',
                    'Уже существенно лучше!', 'Это как раз то, что нужно',
                    'Растёт над собой', 'Очень обрадовал!', 'Талантливо!',
                        'Так держать!', 'Много работал, это видно']
    year_of_study = schoolkid.year_of_study
    group_letter = schoolkid.group_letter
    try:
        subject = Subject.objects.get(title=subject_title, year_of_study=year_of_study)
        subject_lessons = Lesson.objects.filter(year_of_study=year_of_study, group_letter=group_letter,
                                                subject=subject)
        last_lesson = subject_lessons.order_by('date').last()
        сommendation_text = random.choice(сommendations)
        Commendation.objects.create(text=сommendation_text, created=last_lesson.date, schoolkid=schoolkid,
                                    subject=subject, teacher=last_lesson.teacher)
    except ObjectDoesNotExist:
        print('Предмет не найдет')
    except MultipleObjectsReturned:
        print('Несколько предметов найдено, уточните название')