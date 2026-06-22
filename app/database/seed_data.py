import random

from datetime import date
from datetime import timedelta

from app.database.database import SessionLocal

from app.database.models import EmpStatus
from app.database.models import JobHistory
from app.database.models import DeferredBenefit
from app.database.models import Payment

print("Seed file started")

db = SessionLocal()


EMP_STATUS_CODES = ["A", "D", "T", "L"]

EMP_STATUS_SUB_CODES = [
    "Hire",
    "Rehire",
    "Loa",
    "Death",
    "Retired",
    "Military Leave"
]


FIELD_TYPES = [
    "PLN",
    "DIV",
    "LOC",
    "LABGRD",
    "BENGR"
]


PLAN_CODES = [
    "01",
    "02",
    "03",
    "04"
]


DIVISIONS = [
    "1234",
    "6602",
    "8750",
    "9910",
    "4500",
    "3100"
]


LOCATIONS = [
    "NYHQ",
    "CHGO",
    "DALS",
    "AERO",
    "ATL",
    "PHX",
    "SEAT",
    "BOST"
]


LABGRADES = [
    "A1",
    "A2",
    "B1",
    "B2",
    "M1",
    "M2"
]


BENGR_VALUES = [
    "001",
    "002",
    "120",
    "145",
    "174",
    "175",
    "176",
    "201",
    "250"
]


DEFERRED_BENEFIT_STATUS = [
    "DF",
    "VP",
    "VR",
    "VI"
]


PAYMENT_STATUS = [
    "P",
    "V",
    "H"
]


PAYMENT_AMOUNTS = [
    100,
    250,
    500,
    750,
    1000,
    1500,
    2000,
    3000,
    5000
]


DEFERRED_AMOUNTS = [
    5000,
    10000,
    15000,
    25000,
    50000,
    75000,
    100000
]

def seed_emp_status():

    for i in range(1001, 1101):

        employee_id = f"E{i}"

        record = EmpStatus(
            employee_id=employee_id,
            emp_status_code=random.choice(EMP_STATUS_CODES),
            emp_status_sub_code=random.choice(EMP_STATUS_SUB_CODES),
            effective_start_date=date(2020, 1, 1)
            + timedelta(days=random.randint(1, 1500)),
            effective_end_date=date(2030, 12, 31)
        )

        db.add(record)

    db.commit()

    print("Emp Status Loaded:", db.query(EmpStatus).count())


def seed_job_history():

    for i in range(1001, 1101):

        employee_id = f"E{i}"

        values = {
            "PLN": random.choice(PLAN_CODES),
            "DIV": random.choice(DIVISIONS),
            "LOC": random.choice(LOCATIONS),
            "LABGRD": random.choice(LABGRADES),
            "BENGR": random.choice(BENGR_VALUES)
        }

        for field_name, field_value in values.items():

            record = JobHistory(
                employee_id=employee_id,
                effective_date=date(2023, 1, 1),
                field_name=field_name,
                field_value=field_value
            )

            db.add(record)

    db.commit()

    print("Job History Loaded",db.query(JobHistory).count())


def seed_deferred_benefit():

    for i in range(1001, 1081):

        employee_id = f"E{i}"

        record = DeferredBenefit(
            employee_id=employee_id,
            deferred_benefit_status=random.choice(
                DEFERRED_BENEFIT_STATUS
            ),
            deferred_benefit_amount=random.choice(
                DEFERRED_AMOUNTS
            ),
            start_date=date(2022, 1, 1)
            + timedelta(days=random.randint(1, 1000)),
            plan_code=random.choice(PLAN_CODES)
        )

        db.add(record)

    db.commit()

    print("Deferred Benefits Loaded",db.query(DeferredBenefit).count())


def seed_payment():

    for i in range(1001, 1201):

        employee_id = f"E{random.randint(1001,1100)}"
        start_date=date(2024, 1, 1) + timedelta(days=random.randint(1, 365))
        end_date = start_date + timedelta(days=random.randint(30, 1000))
        record = Payment(
            employee_id=employee_id,
            payment_amount=random.choice(PAYMENT_AMOUNTS),
            source_code=f"SRC{random.randint(1,5)}",
            plan_code=random.choice(PLAN_CODES),
            payment_status=random.choice(PAYMENT_STATUS),
            payment_start_date=start_date,
            payment_end_date=end_date
)

        db.add(record)

    db.commit()

    print("Payments Loaded",db.query(Payment).count())

print("Seeding done")

if __name__ == "__main__":

    print("Cleaning existing data...")

    db.query(Payment).delete()
    db.query(DeferredBenefit).delete()
    db.query(JobHistory).delete()
    db.query(EmpStatus).delete()

    db.commit()
    
    print("Starting data load...")

    seed_emp_status()

    seed_job_history()

    seed_deferred_benefit()

    seed_payment()

    db.close()

    print("Data Seeding Completed")