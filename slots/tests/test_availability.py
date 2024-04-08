from datetime import date, datetime, time, timedelta
from django.test import TestCase

from django.contrib.auth.models import User

from slots.availability import get_availability, Slot, get_slots_for_service
from slots.models import MasterSchedule, Service


class AvailabilityTestCase(TestCase):
    def setUp(self):
        self.master = User.objects.create_user(username='master')
        self.client = User.objects.create_user(username='client')
        self.service = Service.objects.create(name='Service', duration=timedelta(hours=1))
        MasterSchedule.objects.create(
            master=self.master,
            working_days=[0, 1, 2, 3, 4],
            start_time=time(9, 0),
            end_time=time(18, 0),
        )

    def test_availability_non_working_day(self):
        sunday = date(2024, 4, 7)

        availability = get_availability(self.master, sunday)
        self.assertEqual(availability, [])

    def test_availability_working_day(self):
        monday = date(2024, 4, 8)

        availability = get_availability(self.master, monday)
        self.assertEqual(availability, [
            Slot(start_time=time(9), end_time=time(18)),
        ])

    def test_availability_with_booking_at_the_start(self):
        monday = date(2024, 4, 8)

        self.master.master_bookings.create(
            start_time=datetime.combine(monday, time(9, 0)),
            end_time=datetime.combine(monday, time(10, 0)),
            client=self.client,
            service=self.service,
        )

        availability = get_availability(self.master, monday)
        self.assertEqual(availability, [
            Slot(start_time=time(10), end_time=time(18)),
        ])

    def test_availability_with_booking_at_the_middle(self):
        monday = date(2024, 4, 8)

        self.master.master_bookings.create(
            start_time=datetime.combine(monday, time(13, 0)),
            end_time=datetime.combine(monday, time(14, 0)),
            client=self.client,
            service=self.service,
        )

        availability = get_availability(self.master, monday)
        self.assertEqual(availability, [
            Slot(start_time=time(9), end_time=time(13)),
            Slot(start_time=time(14), end_time=time(18)),
        ])

    def test_get_slots_for_service(self):
        monday = date(2024, 4, 8)

        self.master.master_bookings.create(
            start_time=datetime.combine(monday, time(13, 0)),
            end_time=datetime.combine(monday, time(14, 0)),
            client=self.client,
            service=self.service,
        )

        slots = get_slots_for_service(self.master, monday, self.service)

        self.assertEqual(slots, [
            Slot(start_time=time(9), end_time=time(10)),
            Slot(start_time=time(10), end_time=time(11)),
            Slot(start_time=time(11), end_time=time(12)),
            Slot(start_time=time(12), end_time=time(13)),
            Slot(start_time=time(14), end_time=time(15)),
            Slot(start_time=time(15), end_time=time(16)),
            Slot(start_time=time(16), end_time=time(17)),
            Slot(start_time=time(17), end_time=time(18)),
        ])
