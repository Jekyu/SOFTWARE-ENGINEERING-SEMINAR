"""
Logic to do a ticketpayment
"""

from datetime import date
from sqlmodel import Session
from models import Ticket, Payment, Fee
import math


def registrar_salida_y_pago(session: Session, ticketid: int):
    """Registra la salida de un vehículo y calcula el valor a pagar"""

    ticket = session.get(Ticket, ticketid)
    if not ticket:
        raise ValueError("Ticket no encontrado.")
    if ticket.exit is not None:
        raise ValueError("El vehículo ya salió.")

    # 1️⃣ Marcar hora de salida
    ticket.exit = date.today()

    # 2️⃣ Obtener la tarifa
    tarifa = session.get(Fee, ticket.idFee)
    if not tarifa:
        raise ValueError("Tarifa no encontrada.")

    # 3️⃣ Calcular pago (ejemplo: tarifa diaria)
    dias = (ticket.exit - ticket.entry).days or 1
    pago_total = tarifa.priceFee * dias

    # 4️⃣ Crear registro de pago
    pago = Payment(ticketid=ticketid, datepayment=date.today(), payment=pago_total)

    # 5️⃣ Liberar el espacio en el parqueadero
    tipo = tarifa.type
    session.exec(
        f"UPDATE lotspace SET totalSpace = totalSpace + 1 WHERE type = '{tipo}'"
    )

    # 6️⃣ Guardar todo
    session.add(ticket)
    session.add(pago)
    session.commit()
    session.refresh(pago)

    return pago
