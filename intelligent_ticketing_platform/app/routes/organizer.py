from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Event, Booking
from app.ml.demand_predictor import predict_ticket_demand
from datetime import datetime

organizer_bp = Blueprint('organizer', __name__)


def organizer_required(f):
    """Decorator to allow only organizers"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role not in ['organizer', 'admin']:
            flash('Access denied. Organizers only.', 'danger')
            return redirect(url_for('events.home'))
        return f(*args, **kwargs)
    return decorated_function


@organizer_bp.route('/organizer/dashboard')
@login_required
@organizer_required
def dashboard():
    my_events = Event.query.filter_by(organizer_id=current_user.id).order_by(Event.event_date.desc()).all()
    return render_template('organizer/dashboard.html', events=my_events)


@organizer_bp.route('/organizer/create-event', methods=['GET', 'POST'])
@login_required
@organizer_required
def create_event():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        location = request.form.get('location')
        event_date_str = request.form.get('event_date')
        total_tickets = int(request.form.get('total_tickets'))
        price = float(request.form.get('price'))

        event_date = datetime.strptime(event_date_str, '%Y-%m-%dT%H:%M')

        new_event = Event(
            title=title,
            description=description,
            category=category,
            location=location,
            event_date=event_date,
            total_tickets=total_tickets,
            available_tickets=total_tickets,
            price=price,
            organizer_id=current_user.id
        )

        db.session.add(new_event)
        db.session.commit()

        flash('Event created successfully!', 'success')
        return redirect(url_for('organizer.dashboard'))

    return render_template('organizer/create_event.html')


@organizer_bp.route('/organizer/predict-demand/<int:event_id>')
@login_required
@organizer_required
def predict_demand(event_id):
    event = Event.query.get_or_404(event_id)

    if event.organizer_id != current_user.id and current_user.role != 'admin':
        flash('You can only predict demand for your own events.', 'danger')
        return redirect(url_for('organizer.dashboard'))

    # Get prediction from ML model
    prediction = predict_ticket_demand(event)

    return render_template('organizer/predict_demand.html', event=event, prediction=prediction)
