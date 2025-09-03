from app.limiter_memory import SlidingWindowLimiter


def test_memory_allows_and_denies():
    rl = SlidingWindowLimiter(limit=3, window_seconds=2.0)
    assert rl.allow("alice")
    assert rl.allow("alice")
    assert rl.allow("alice")
    assert rl.allow("bob")  # different user
    assert rl.allow("bob")
    assert rl.allow("bob")
    assert not rl.allow("alice")  # 4th denied
    # After window rolls
    assert rl.allow("alice")
