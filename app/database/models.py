from app.database.database import Base
from sqlalchemy import Column, Integer, String, Date, Float, Text, DateTime,Boolean
from datetime import datetime


class EmpStatus(Base):
    __tablename__ = "emp_status"

    id = Column(Integer, primary_key=True, index = True)

    employee_id = Column(String)

    emp_status_code = Column(String)
    emp_status_sub_code = Column(String)

    effective_start_date = Column(Date)
    effective_end_date = Column(Date)


class JobHistory(Base):
    __tablename__ = "job_history"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(String, index=True)

    effective_date = Column(Date)

    field_name = Column(String)

    field_value = Column(String)



class DeferredBenefit(Base):
    __tablename__ = "deferred_benefit"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(String, index=True)

    deferred_benefit_status = Column(String)

    deferred_benefit_amount = Column(Float)

    start_date = Column(Date)

    plan_code = Column(String)


class Payment(Base):
    __tablename__ = "payment"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(String, index=True)

    payment_amount = Column(Float)

    source_code = Column(String)

    plan_code = Column(String)

    payment_status = Column(String)

    payment_start_date = Column(Date)

    payment_end_date = Column(Date, nullable=True)

class QueryHistory(Base):

    __tablename__ = "query_history"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    question = Column(
        Text,
        nullable=False
    )

    generated_sql = Column(
        Text,
        nullable=False
    )

    row_count = Column(
        Integer
    )

    execution_time_ms = Column(
        Integer
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    is_valid_sql = Column(
        Boolean,
        default=False
    )

    execution_success = Column(
        Boolean,
        default=False
    )

    response_time_ms = Column(
        Integer
    )

    hallucination_detected = Column(
        Boolean,
        default=False
    )
    hallucination_score = Column(Integer, default=0)