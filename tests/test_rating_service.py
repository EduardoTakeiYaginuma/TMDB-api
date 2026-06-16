import pytest
from app.services.rating_service import RatingService
from app.utils.errors import ConflictError, NotFoundError, ValidationError


def _create(tmdb_id=1, title='Test Movie', poster=None, rating=4):
    return RatingService().create_rating(
        tmdb_movie_id=tmdb_id,
        title=title,
        poster_path=poster,
        rating=rating,
    )


def test_list_ratings_empty(app):
    assert RatingService().list_ratings() == []


def test_create_rating_success(app):
    r = _create()
    assert r.tmdb_movie_id == 1
    assert r.title == 'Test Movie'
    assert r.rating == 4
    assert r.poster_path is None


def test_create_rating_persists(app):
    _create(tmdb_id=10, rating=3)
    all_ratings = RatingService().list_ratings()
    assert len(all_ratings) == 1
    assert all_ratings[0].rating == 3


def test_create_rating_duplicate_raises_conflict(app):
    _create(tmdb_id=5)
    with pytest.raises(ConflictError):
        _create(tmdb_id=5)


def test_create_rating_below_min_raises_validation(app):
    with pytest.raises(ValidationError):
        _create(rating=0)


def test_create_rating_above_max_raises_validation(app):
    with pytest.raises(ValidationError):
        _create(rating=6)


def test_create_rating_not_int_raises_validation(app):
    with pytest.raises(ValidationError):
        _create(rating=3.5)  # type: ignore[arg-type]


def test_update_rating_success(app):
    _create(tmdb_id=2, rating=2)
    updated = RatingService().update_rating(2, 5)
    assert updated.rating == 5


def test_update_rating_not_found_raises_not_found(app):
    with pytest.raises(NotFoundError):
        RatingService().update_rating(999, 3)


def test_update_rating_invalid_value_raises_validation(app):
    _create(tmdb_id=3, rating=3)
    with pytest.raises(ValidationError):
        RatingService().update_rating(3, 7)


def test_delete_rating_success(app):
    _create(tmdb_id=4, rating=1)
    RatingService().delete_rating(4)
    assert RatingService().list_ratings() == []


def test_delete_rating_not_found_raises_not_found(app):
    with pytest.raises(NotFoundError):
        RatingService().delete_rating(999)


def test_list_ratings_ordered_by_updated_at_desc(app):
    _create(tmdb_id=10, rating=5)
    _create(tmdb_id=20, rating=2)
    RatingService().update_rating(10, 1)  # bumps updated_at of id=10
    ratings = RatingService().list_ratings()
    assert ratings[0].tmdb_movie_id == 10
