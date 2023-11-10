import pytest

from list.utils.database_utils import diff_db_and_cache
from list.models import Projects


@pytest.fixture()
def create_repos_in_db():
    Projects.objects.create(repo_id=1, date='2023-12-01')
    Projects.objects.create(repo_id=2, date='2023-12-01')
    Projects.objects.create(repo_id=3, date='2023-12-01')
    Projects.objects.create(repo_id=4, date='2023-12-01')


@pytest.mark.django_db
def test_diff_db_and_cache(create_repos_in_db):
    cache_data = [
        {'repo_id': 1},
        {'repo_id': 2},
    ]

    result = diff_db_and_cache(cache_data)

    assert isinstance(result, list)
    assert result == [3, 4]
    assert result != [1, 2], 'Вероятно возвращены записи, совпадающие с кэшем и с БД; либо возвращены данные из кэша'
    assert result != [1, 2, 3, 4], 'Функция просто вернула данные из БД'
