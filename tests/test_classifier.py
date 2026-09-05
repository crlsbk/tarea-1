import unittest
from io import StringIO
from unittest.mock import patch

from cli import main
from classifier import CloudServiceClassifier
from models import CloudModel


class CloudServiceClassifierTest(unittest.TestCase):
    def setUp(self) -> None:
        self.classifier = CloudServiceClassifier()

    def test_classifies_each_cloud_model(self) -> None:
        examples = {
            CloudModel.IAAS: "Necesito una virtual machine con storage y una red privada",
            CloudModel.PAAS: "Quiero deployar una web app en una plataforma con runtime administrado",
            CloudModel.SAAS: "Una suscripcion de CRM y correo lista para usar",
            CloudModel.FAAS: "Una funcion serverless activada por un evento",
        }
        for expected_model, text in examples.items():
            with self.subTest(expected_model=expected_model):
                self.assertEqual(self.classifier.classify(text).model, expected_model)

    def test_handles_empty_and_unknown_text(self) -> None:
        self.assertFalse(self.classifier.classify("   ").is_success)
        self.assertFalse(self.classifier.classify("texto desconocido").is_success)

    def test_cli_uses_the_same_classifier_service(self) -> None:
        output = StringIO()
        with patch("sys.stdout", output):
            exit_code = main(
                ["--text", "ejecutar una función cuando se suba una imagen"]
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(output.getvalue().strip(), "Modelo identificado: FaaS")


if __name__ == "__main__":
    unittest.main()
