from .models import Supervisor
import random

def generate_supervisor_id():
    last = Supervisor.objects.order_by("-id").first()
    if not last:
        return "SUPER-001"

    last_number = int(last.supervisor_id.split("-")[1])
    new_number = last_number + 1
    return f"SUPER-{new_number:03d}"


def generate_passcode():
    return str(random.randint(100000, 999999))
