from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import Event, Booking
from datetime import datetime

bookings_bp = Blueprint('bookings', __name__)


@bookings_bp.route('/book/<int:event_id>', methods=['GET', 'POST'])
@login_required
def book_ticket(event_id):
    event = Event.query.get_or_404(event_id)

    if request.method == 'POST':
        quantity = int(request.form.get('quantity', 1))

        if quantity <= 0:
            flash('Invalid quantity.', 'danger')
            return redirect(url_for('events.event_detail', event_id=event_id))

        if quantity > event.available_tickets:
            flash(f'Only {event.available_tickets} tickets available.', 'danger')
            return redirect(url_for('events.event_detail', event_id=event_id))

        total_amount = quantity * event.price

        # Create booking
        booking = Booking(
            user_id=current_user.id,
            event_id=event.id,
            quantity=quantity,
            total_amount=total_amount
        )

        # Update available tickets
        event.available_tickets -= quantity

        db.session.add(booking)
        db.session.commit()

        flash(f'Successfully booked {quantity} ticket(s) for {event.title}!', 'success')
        return redirect(url_for('bookings.my_bookings'))

    return render_template('bookings/book.html', event=event)


@bookings_bp.route('/my-bookings')
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.booking_date.desc()).all()
    return render_template('bookings/my_bookings.html', bookings=bookings)
