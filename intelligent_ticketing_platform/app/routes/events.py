from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Event, User
from datetime import datetime

events_bp = Blueprint('events', __name__)


@events_bp.route('/')
def home():
    """Home page - show all upcoming events"""
    events = Event.query.filter(Event.event_date >= datetime.utcnow()).order_by(Event.event_date).all()
    return render_template('events/home.html', events=events)


@events_bp.route('/event/<int:event_id>')
def event_detail(event_id):
    """Show details of a single event"""
    event = Event.query.get_or_404(event_id)
    return render_template('events/detail.html', event=event)


@events_bp.route('/search')
def search():
    """Search events by title or category"""
    query = request.args.get('q', '')
    category = request.args.get('category', '')

    events_query = Event.query.filter(Event.event_date >= datetime.utcnow())

    if query:
        events_query = events_query.filter(Event.title.ilike(f'%{query}%'))
    if category:
        events_query = events_query.filter(Event.category == category)

    events = events_query.order_by(Event.event_date).all()
    return render_template('events/home.html', events=events, search_query=query)
