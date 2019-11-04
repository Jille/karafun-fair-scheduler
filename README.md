# Karafun fair scheduler

Usage is simple:

```shell
$ pip install python-socketio
$ python scheduler.py 123456
```

The scheduler will connect to Karafun and manage your queue. Your guests can queue music as usual and the scheduler will automatically reorder them for fairness.

The algorithm is simple: Alice's second song in the queue will be between Bob's first and third song in the queue. For the rest it's FIFO.

You must turn on "Ask singer's name when adding to queue" in the Karafun remote control settings in order for the scheduler to work. If you don't actually want the names visible, pass `--hide-singers` when invoking the tool.

## Tricks

If you want to queue a song right after the current one, fill in the singers name "_next" and the scheduler will put it on top.

If you want two of yours songs to happen directly after another, append an exclamation mark to your name for the second one.

## Known issues / limitations

If you enable `--hide-singers`, the tool will deduplicate any songs that are queued twice (leaving only the first in the queue). This might be a feature for some, but a problem for others.

`--hide-singers` doesn't work for Community Songs, only for songs from the Karafun catalog.

If you enable `--hide-singers`, restarting the tool without emptying the queue will cause undefined behavior.

Queueing a song with your name and an exclamation mark basically treats the two songs as one. It should probably count as multiple songs instead, and push your further songs back.
