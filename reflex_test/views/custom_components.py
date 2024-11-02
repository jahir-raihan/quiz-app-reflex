import reflex as rx
from typing import Union
from sqlmodel import select


class TestCounter(rx.Model, table=True):

    counter: int


class State(rx.State):

    counter = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.counter = self.counter or self.get_count()

    def increment(self):

        """
        increment the counter
        """

        with rx.session() as session:
            counter_obj = session.exec(
                select(TestCounter).where(TestCounter.id == 1)
            ).first()

            counter_obj.counter += 1
            session.add(counter_obj)
            session.commit()
            self.counter = counter_obj.counter

    def get_count(self):

        """
        Get the initial count
        """

        with rx.session() as session:
            counter_obj = session.exec(
                select(TestCounter).where(TestCounter.id == 1)
            ).first()

            if counter_obj:
                self.counter = counter_obj.counter
            else:
                TestCounter.counter = 1
                session.add(TestCounter(**{'counter': 1}))
                session.commit()
                self.counter = 1

        return self.counter


def my_button():
    return rx.button(f"Pass it out - {State.counter}", on_click=State.increment)