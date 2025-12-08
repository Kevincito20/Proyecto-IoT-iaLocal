from app.service import servicio_conversacion as sc
def test_no_se_supera_el_maximo_de_conversaciones():
    """
    Verifica que, al reiniciar varias veces, solo se conserven
    como máximo tres conversaciones.
    """

    sc.reiniciar_conversacion()
    sc.agregar_mensaje("usuario", "mensaje 1")

    sc.reiniciar_conversacion()
    sc.agregar_mensaje("usuario", "mensaje 2")

    sc.reiniciar_conversacion()
    sc.agregar_mensaje("usuario", "mensaje 3")

    sc.reiniciar_conversacion()
    sc.agregar_mensaje("usuario", "mensaje 4")

    resumen = sc.obtener_resumen_conversaciones()
    assert len(resumen) <= 3

    ids = [item["id_conversacion"] for item in resumen]
    assert max(ids) in ids
