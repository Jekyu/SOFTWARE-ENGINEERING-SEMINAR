from database import run_query
from datetime import datetime
from services.vehicle_services import register_vehicle, get_vehicle


def registrar_entrada(placa, tipo):
    existe = run_query(
        "SELECT * FROM ticket WHERE licenseplate = %s AND exit IS NULL",
        (placa,),
        fetch=True,
    )
    if existe:
        return {"error": "Vehículo ya dentro."}
    run_query(
        "INSERT INTO ticket (ownerdoc, entry, licenseplate, idFee, idUser) VALUES (%s, %s, %s, %s, %s)",
        ("000", datetime.now(), placa, "F001", "U001"),
    )
    return {"ok": f"Vehículo {placa} ingresó correctamente."}


def registrar_salida(placa):
    ticket = run_query(
        "SELECT * FROM ticket WHERE licenseplate = %s AND exit IS NULL",
        (placa,),
        fetch=True,
    )
    if not ticket:
        return {"error": "No hay ticket activo."}
    ticket = ticket[0]
    entry_time = ticket["entry"]
    horas = round((datetime.now() - entry_time).seconds / 3600, 2) or 1
    pago = horas * 2000
    run_query(
        "UPDATE ticket SET exit = %s WHERE ticketid = %s",
        (datetime.now(), ticket["ticketid"]),
    )
    run_query(
        "INSERT INTO payment (ticketid, datepayment, payment) VALUES (%s, %s, %s)",
        (ticket["ticketid"], datetime.now(), pago),
    )
    return {"ok": f"Salida registrada. Total a pagar: {pago}"}
