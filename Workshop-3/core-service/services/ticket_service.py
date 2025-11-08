"""
Logic to create a ticket
"""

from datetime import date
from sqlmodel import Session, select
from models import Ticket, Vehicle, LotSpace
import crud


def registrar_entrada(
    session: Session, ownerdoc: str, licenseplate: str, idFee: str, idUser: str
):
    """Registra la entrada de un vehículo al parqueadero"""

    # Verificar si el vehículo ya tiene un ticket sin salida
    ticket_existente = session.exec(
        select(Ticket).where(Ticket.licenseplate == licenseplate, Ticket.exit == None)
    ).first()

    if ticket_existente:
        raise ValueError("El vehículo ya está registrado dentro del parqueadero.")

    # Verificar que haya espacio disponible
    vehiculo = session.get(Vehicle, licenseplate)
    if not vehiculo:
        raise ValueError("Vehículo no registrado.")

    espacio = session.exec(
        select(LotSpace).where(LotSpace.type == vehiculo.type)
    ).first()

    if not espacio or espacio.totalSpace <= 0:
        raise ValueError(f"No hay espacios disponibles para {vehiculo.type}")

    # Reducir espacio disponible
    espacio.totalSpace -= 1
    session.add(espacio)

    # Crear el ticket
    nuevo_ticket = Ticket(
        ownerdoc=ownerdoc,
        entry=date.today(),
        licenseplate=licenseplate,
        idFee=idFee,
        idUser=idUser,
    )

    session.add(nuevo_ticket)
    session.commit()
    session.refresh(nuevo_ticket)

    return nuevo_ticket
