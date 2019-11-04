# Karafun fair scheduler

Usage is simple:

```shell
$ pip install python-socketio
$ python scheduler.py 123456
```

The scheduler will connect to Karafun and manage your queue. Your guests can queue music as usual and the scheduler will automatically reorder them for fairness.

The algorithm is simple: Alice's second song in the queue will be between Bob's first and third song in the queue. For the rest it's FIFO.

You must turn on "Ask singer's name when adding to queue" in the Karafun remote control settings in order for the scheduler to work. If you don't actually want the names visible, pass `--hide-singers` when invoking the tool. If you enable `--hide-singers`, restarting the tool without emptying the queue will cause undefined behavior.
