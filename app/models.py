
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .extensions import db
# ======================
# Base
# ======================
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# ======================
# Bridge Table (Many-to-Many)
# ======================
class ServiceMechanics(Base):
    __tablename__ = "service_mechanics"

    ticket_id: Mapped[int] = mapped_column(
        ForeignKey("service_tickets.id"),
        primary_key=True
    )

    mechanic_id: Mapped[int] = mapped_column(
        ForeignKey("mechanics.id"),
        primary_key=True
    )

# ======================
# Customers
# ======================
class Customers(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(50), nullable=False)

    service_tickets = relationship(
        "ServiceTickets",
        back_populates="customer"
    )

# ======================
# Mechanics
# ======================
class Mechanics(Base):
    __tablename__ = "mechanics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(50), nullable=False)
    salary: Mapped[float] = mapped_column(nullable=False)

    tickets = relationship(
        "ServiceTickets",
        secondary="service_mechanics",
        back_populates="mechanics"
    )

# ======================
# Service Tickets
# ======================
class ServiceTickets(Base):
    __tablename__ = "service_tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    vin: Mapped[str] = mapped_column(db.String(255), nullable=False)
    service_date: Mapped[str] = mapped_column(db.String(255), nullable=False)
    description: Mapped[str] = mapped_column(db.String(255), nullable=False)

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False
    )

    customer = relationship(
        "Customers",
        back_populates="service_tickets"
    )

    mechanics = relationship(
        "Mechanics",
        secondary="service_mechanics",
        back_populates="tickets"
    )

