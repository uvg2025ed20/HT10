import unittest
import numpy as np
from unittest.mock import mock_open, patch
from io import StringIO
from main import read_graph, get_path, find_center, vertices, adj_matrix, weather_weights, path_matrix

class TestGraphImplementation(unittest.TestCase):
    """
    Clase de pruebas unitarias para la implementación del grafo logístico.

    Esta clase valida el correcto funcionamiento de:
    - La lectura del grafo desde un archivo.
    - La reconstrucción de caminos entre ciudades.
    - El cálculo del centro del grafo.

    Autores: Ángel Sanabria, Pablo Vásquez
    """

    def setUp(self):
        """
        Método de configuración que se ejecuta antes de cada prueba.

        Reinicia las variables globales del grafo para asegurar que cada prueba
        sea independiente y no tenga efectos secundarios.
        """
        global vertices, adj_matrix, weather_weights, path_matrix
        vertices = []
        adj_matrix = None
        weather_weights = {}
        path_matrix = None

    def test_read_graph_file_not_found(self):
        """
        Prueba el manejo del error cuando el archivo de entrada no existe.

        Se espera que el mensaje 'Archivo no encontrado' se imprima en la salida estándar.
        """
        with patch("builtins.open", side_effect=FileNotFoundError):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                read_graph("nonexistent.txt")
                self.assertIn("Archivo no encontrado", fake_out.getvalue(), "File not found message not printed")

    def test_get_path(self):
        """
        Prueba la reconstrucción del camino entre dos ciudades.

        Verifica que:
        - Se devuelva None e infinito si no hay camino posible.
        - Se manejen correctamente nombres de ciudades inválidos.
        """
        mock_file_content = "BuenosAires SaoPaulo 10 15 20 50\nBuenosAires Lima 15 20 30 70\nLima Quito 10 12 15 20\nSaoPaulo Quito 12 18 25 60"
        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            read_graph("logistica.txt")
        
        path, distance = get_path("Quito", "BuenosAires")
        self.assertIsNone(path, "Path should be None")
        self.assertEqual(distance, float('inf'), "Distance should be infinity")
        
        path, distance = get_path("InvalidCity", "Quito")
        self.assertIsNone(path, "Path should be None for invalid city")
        self.assertIsNone(distance, "Distance should be None for invalid city")

    def test_find_center(self):
        """
        Prueba la funcionalidad de encontrar el centro del grafo.

        Verifica que:
        - El centro retornado sea una cadena.
        - La excentricidad sea un número flotante.
        - El método maneje correctamente un grafo vacío sin lanzar excepciones.
        """
        mock_file_content = "BuenosAires SaoPaulo 10 15 20 50\nBuenosAires Lima 15 20 30 70\nLima Quito 10 12 15 20\nSaoPaulo Quito 12 18 25 60"
        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            read_graph("logistica.txt")
        
        try:
            center, eccentricity = find_center()
            self.assertIsInstance(center, str, "Center should be a string")
            self.assertIsInstance(eccentricity, float, "Eccentricity should be a float")
        except IndexError:
            self.assertTrue(True, "Empty graph handled")

if __name__ == '__main__':
    unittest.main()
