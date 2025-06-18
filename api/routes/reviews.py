from flask_restx import Resource, Namespace, fields
from app.models import Review, db
from flask_login import current_user, login_required

reviews_ns = Namespace('reviews', description='Review operations')

review_model = reviews_ns.model('Review', {
    'content': fields.String(required=True, description='Review content'),
    'car_id': fields.Integer(required=True, description='Car ID')
})

@reviews_ns.route('/car/<int:car_id>')
class ReviewList(Resource):
    @reviews_ns.doc('list_reviews')
    def get(self, car_id):
        """List all reviews for a specific car"""
        reviews = Review.query.filter_by(car_id=car_id).all()
        return [{
            'id': review.id,
            'content': review.content,
            'user_id': review.user_id,
            'car_id': review.car_id
        } for review in reviews]

    @reviews_ns.doc('create_review')
    @reviews_ns.expect(review_model)
    @login_required
    def post(self, car_id):
        """Create a new review for a specific car"""
        data = reviews_ns.payload
        review = Review(
            content=data['content'],
            car_id=car_id,
            user_id=current_user.id
        )
        db.session.add(review)
        db.session.commit()
        return {'message': 'Review created successfully'}, 201 