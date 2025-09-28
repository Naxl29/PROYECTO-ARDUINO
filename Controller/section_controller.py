from typing import List, Dict, Optional
from Model.section import SectionModel


class SectionController:
    def list_sections(self) -> List[Dict]:
        return SectionModel.list_sections()

    def list_sections_with_roles(self) -> List[Dict]:
        return SectionModel.list_sections_with_roles()

    def create_section(self, nombre: str) -> int:
        nombre = (nombre or '').strip()
        if not nombre:
            raise ValueError('El nombre de la sección es obligatorio')
        return SectionModel.create_section(nombre)

    def update_section(self, section_id: int, nombre: Optional[str] = None) -> None:
        SectionModel.update_section(section_id, nombre)

    def assign_device(self, channel: str, section_id: int) -> None:
        SectionModel.assign_device(channel, section_id)

    def sections_map(self) -> Dict[str, Dict]:
        return SectionModel.get_device_sections_map()

    def unassign_device(self, channel: str) -> None:
        SectionModel.remove_assignment(channel)

    def set_section_roles(self, section_id: int, roles: List[str]) -> None:
        SectionModel.set_section_roles(section_id, roles)
