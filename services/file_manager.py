import json
import xml.etree.ElementTree as ET
import os

class FileManager:
    """Gestor de archivos para importación y exportación de respaldos."""
    
    @staticmethod
    def exportar_json(datos: dict, filepath: str) -> str:
        """Exporta un diccionario a un archivo JSON."""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            return filepath
        except Exception as e:
            raise Exception(f"Fallo al exportar JSON: {e}")

    @staticmethod
    def importar_json(filepath: str) -> dict:
        """Importa datos desde un archivo JSON."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"Fallo al importar JSON: {e}")

    @staticmethod
    def exportar_xml(datos: dict, filepath: str) -> str:
        """Exporta datos a formato XML."""
        try:
            root = ET.Element("BibliotecaRespaldos")
            
            # Libros
            libros_elem = ET.SubElement(root, "Libros")
            for libro in datos.get("libros", []):
                le = ET.SubElement(libros_elem, "Libro")
                for k, v in libro.items():
                    ET.SubElement(le, k).text = str(v)
                    
            # Usuarios
            usuarios_elem = ET.SubElement(root, "Usuarios")
            for usr in datos.get("usuarios", []):
                ue = ET.SubElement(usuarios_elem, "Usuario")
                for k, v in usr.items():
                    ET.SubElement(ue, k).text = str(v)

            tree = ET.ElementTree(root)
            tree.write(filepath, encoding='utf-8', xml_declaration=True)
            return filepath
        except Exception as e:
            raise Exception(f"Fallo al exportar XML: {e}")
            
    @staticmethod
    def importar_xml(filepath: str) -> dict:
        """Importa datos desde XML."""
        try:
            tree = ET.parse(filepath)
            root = tree.getroot()
            
            datos = {"libros": [], "usuarios": []}
            
            for libro_elem in root.find("Libros") or []:
                l_dict = {child.tag: child.text for child in libro_elem}
                datos["libros"].append(l_dict)
                
            for usr_elem in root.find("Usuarios") or []:
                u_dict = {child.tag: child.text for child in usr_elem}
                datos["usuarios"].append(u_dict)
                
            return datos
        except Exception as e:
            raise Exception(f"Fallo al importar XML: {e}")
