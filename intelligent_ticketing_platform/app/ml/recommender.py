"""
Content-Based Filtering Recommendation System
---------------------------------------------
This module recommends events to users based on:
1. User's preferred categories
2. Categories of events the user has previously booked
"""

from app.models import User, Event, Booking
from datetime import datetime
from collections import Counter


def get_recommendations(user_id, top_n=6):
    """
    Returns a list of recommended events for a given user.
    Uses simple Content-Based Filtering based on categories.
    """
    user = User.query.get(user_id)
    if not user:
        return []

    # 1. Get user's preferred categories
    preferred = []
    if user.preferred_categories:
        preferred = [c.strip().lower() for c in user.preferred_categories.split(',')]

    # 2. Get categories from past bookings
    past_bookings = Booking.query.filter_by(user_id=user_id).all()
    booked_categories = []
    booked_event_ids = []

    for booking in past_bookings:
        if booking.event:
            booked_categories.append(booking.event.category.lower())
            booked_event_ids.append(booking.event_id)

    # Combine preferences
    all_preferred = preferred + booked_categories
    if not all_preferred:
        # If no preference, return popular upcoming events
        return Event.query.filter(
            Event.event_date >= datetime.utcnow()
        ).order_by(Event.event_date).limit(top_n).all()

    # Count most common categories
    category_counts = Counter(all_preferred)
    top_categories = [cat for cat, _ in category_counts.most_common(3)]

    # Find upcoming events in those categories (that user hasn't booked)
    recommended = Event.query.filter(
        Event.event_date >= datetime.utcnow(),
        Event.category.in_([c.title() for c in top_categories]),  # Match capitalization
        ~Event.id.in_(booked_event_ids) if booked_event_ids else True
    ).order_by(Event.event_date).limit(top_n).all()

    return recommended
