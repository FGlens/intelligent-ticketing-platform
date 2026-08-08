from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.ml.recommender import get_recommendations

recommendations_bp = Blueprint('recommendations', __name__)


@recommendations_bp.route('/recommendations')
@login_required
def recommend():
    """Show personalized event recommendations for the logged-in user"""
    recommended_events = get_recommendations(current_user.id)
    return render_template('events/recommendations.html', events=recommended_events)
