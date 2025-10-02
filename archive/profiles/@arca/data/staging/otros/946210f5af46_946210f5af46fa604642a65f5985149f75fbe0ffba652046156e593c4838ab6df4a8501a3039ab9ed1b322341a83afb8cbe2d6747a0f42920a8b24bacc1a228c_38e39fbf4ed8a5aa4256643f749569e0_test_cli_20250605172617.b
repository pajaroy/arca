import unittest
from unittest.mock import patch
from io import StringIO
from core.cli import AlmaCLI

class TestCLI(unittest.TestCase):
    def test_ayuda_lista_comandos(self):
        cli = AlmaCLI()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli.onecmd("!ayuda")
            output = fake_out.getvalue().strip()
            self.assertIn("Comandos disponibles:", output)
            self.assertIn("!ayuda", output)
            self.assertIn("!salir", output)

    def test_salir_finaliza_sesion(self):
        cli = AlmaCLI()
        self.assertTrue(cli.onecmd("!salir"))

    def test_comando_invalido_muestra_error(self):
        cli = AlmaCLI()
        with patch('sys.stdout', new=StringIO()) as fake_out:
            cli.onecmd("!invalido")
            output = fake_out.getvalue().strip()
            self.assertIn("Error: Comando no reconocido", output)

if __name__ == '__main__':
    unittest.main()
