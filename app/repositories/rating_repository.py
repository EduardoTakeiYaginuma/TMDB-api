from app import db
from app.models.movie_rating import MovieRating


class RatingRepository:
    """All database access for MovieRating. No business logic here."""

    def get_all(self) -> list[MovieRating]:
        return (
            db.session.query(MovieRating)
            .order_by(MovieRating.updated_at.desc())
            .all()
        )

    def get_by_tmdb_id(self, tmdb_movie_id: int) -> MovieRating | None:
        return db.session.query(MovieRating).filter_by(tmdb_movie_id=tmdb_movie_id).first()

    def create(
        self,
        tmdb_movie_id: int,
        title: str,
        poster_path: str | None,
        rating: int,
    ) -> MovieRating:
        record = MovieRating(
            tmdb_movie_id=tmdb_movie_id,
            title=title,
            poster_path=poster_path,
            rating=rating,
        )
        db.session.add(record)
        db.session.commit()
        db.session.refresh(record)
        return record

    def update(self, record: MovieRating, rating: int) -> MovieRating:
        record.rating = rating
        db.session.commit()
        db.session.refresh(record)
        return record

    def delete(self, record: MovieRating) -> None:
        db.session.delete(record)
        db.session.commit()
