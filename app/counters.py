from .models import db, Counter

class CounterManager:
    @staticmethod
    def get_counter(user_id):
        counter = Counter.query.filter_by(user_id=user_id).first()
        return counter.value if counter else 0

    @staticmethod
    def increment_counter(user_id):
        counter = Counter.query.filter_by(user_id=user_id).first()
        if not counter:
            counter = Counter(user_id=user_id, value=1)
            db.session.add(counter)
        else:
            counter.value += 1
        db.session.commit()
        return counter.value

    @staticmethod
    def decrement_counter(user_id):
        counter = Counter.query.filter_by(user_id=user_id).first()
        if not counter:
            counter = Counter(user_id=user_id, value=-1)
            db.session.add(counter)
        else:
            counter.value -= 1
        db.session.commit()
        return counter.value