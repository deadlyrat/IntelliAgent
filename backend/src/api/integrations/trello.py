import os
import requests
from typing import Optional


class TrelloClient:
    """Cliente para interactuar con la API de Trello"""

    def __init__(self):
        self.api_key = os.environ.get("TRELLO_API_KEY")
        self.api_token = os.environ.get("TRELLO_API_TOKEN")
        self.base_url = "https://api.trello.com/1"

        if not self.api_key or not self.api_token:
            raise ValueError("TRELLO_API_KEY and TRELLO_API_TOKEN must be set")

    def create_card(
        self,
        list_id: str,
        name: str,
        desc: str = "",
        pos: str = "bottom"
    ) -> dict:
        """
        Crea una nueva tarjeta en Trello

        Args:
            list_id: ID de la lista donde se creará la tarjeta
            name: Nombre de la tarjeta
            desc: Descripción de la tarjeta
            pos: Posición de la tarjeta (top, bottom, o número)

        Returns:
            Diccionario con los datos de la tarjeta creada
        """
        url = f"{self.base_url}/cards"

        query = {
            'key': self.api_key,
            'token': self.api_token,
            'idList': list_id,
            'name': name,
            'desc': desc,
            'pos': pos
        }

        response = requests.post(url, params=query)
        response.raise_for_status()

        return response.json()

    def get_lists(self, board_id: str) -> list:
        """
        Obtiene todas las listas de un tablero

        Args:
            board_id: ID del tablero

        Returns:
            Lista de listas del tablero
        """
        url = f"{self.base_url}/boards/{board_id}/lists"

        query = {
            'key': self.api_key,
            'token': self.api_token
        }

        response = requests.get(url, params=query)
        response.raise_for_status()

        return response.json()

    def get_boards(self) -> list:
        """
        Obtiene todos los tableros del usuario

        Returns:
            Lista de tableros
        """
        url = f"{self.base_url}/members/me/boards"

        query = {
            'key': self.api_key,
            'token': self.api_token
        }

        response = requests.get(url, params=query)
        response.raise_for_status()

        return response.json()


def create_trello_card(list_id: str, title: str, description: str) -> dict:
    """
    Función helper para crear una tarjeta de Trello

    Args:
        list_id: ID de la lista de Trello
        title: Título de la tarjeta
        description: Descripción de la tarjeta

    Returns:
        Diccionario con información de la tarjeta creada
    """
    try:
        client = TrelloClient()
        card = client.create_card(list_id, title, description)
        return {
            "success": True,
            "card_id": card.get("id"),
            "card_url": card.get("url"),
            "message": "Tarjeta creada exitosamente"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Error al crear la tarjeta"
        }
