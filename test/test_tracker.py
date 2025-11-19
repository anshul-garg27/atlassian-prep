# test_tracker.py

from test import PopularityTracker

def test_basic_increase():
    t = PopularityTracker()
    t.increase("A")
    assert t.mostPopular() == "A"

def test_decrease_zero():
    t = PopularityTracker()
    t.increase("A")
    t.decrease("A")
    assert t.mostPopular() is None

def test_two_items():
    t = PopularityTracker()
    t.increase("A")
    t.increase("B")
    assert t.mostPopular() in {"A", "B"}

