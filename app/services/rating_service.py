from app.models.movie_rating import MovieRating
from app.repositories.rating_repository import RatingRepository
from app.utils.errors import ConflictError, NotFoundError, ValidationError


class RatingService:
    """Business logic for movie ratings.

    Enforces constraints independently of the HTTP layer so the service
    remains testable without a running Flask app.
    """

    def __init__(self) -> None:
        self._repo = RatingRepository()

    def list_ratings(self) -> list[MovieRating]:
        return self._repo.get_all()

    def create_rating(
        self,
        tmdb_movie_id: int,
        title: str,
        poster_path: str | None,
        rating: int,
    ) -> MovieRating:
        self._assert_valid_rating(rating)

        if self._repo.get_by_tmdb_id(tmdb_movie_id):
            raise ConflictError(
                f"Movie {tmdb_movie_id} already has a rating. Use PUT to update it."
            )

        return self._repo.create(tmdb_movie_id, title, poster_path, rating)

    def update_rating(self, tmdb_movie_id: int, rating: int) -> MovieRating:
        self._assert_valid_rating(rating)

        record = self._repo.get_by_tmdb_id(tmdb_movie_id)
        if not record:
            raise NotFoundError(f"No rating found for movie {tmdb_movie_id}.")

        return self._repo.update(record, rating)

    def delete_rating(self, tmdb_movie_id: int) -> None:
        record = self._repo.get_by_tmdb_id(tmdb_movie_id)
        if not record:
            raise NotFoundError(f"No rating found for movie {tmdb_movie_id}.")

        self._repo.delete(record)

    @staticmethod
    def _assert_valid_rating(rating: int) -> None:
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValidationError("Rating must be an integer between 1 and 5.")
