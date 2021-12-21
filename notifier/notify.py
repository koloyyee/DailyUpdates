from pynotifier import Notification

Notification(
    title='Hello!',
    description='Here is the first notification!',
    # On Windows .ico is required, on Linux - .png
    icon_path=None,
    duration=10,
    urgency='low'
).send()
