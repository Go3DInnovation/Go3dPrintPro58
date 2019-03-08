# Copyright (c) 2019 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher.

from typing import cast

from Charon.VirtualFile import VirtualFile

from UM.Mesh.MeshReader import MeshReader
from UM.MimeTypeDatabase import MimeType, MimeTypeDatabase
from UM.PluginRegistry import PluginRegistry
from cura.Scene.CuraSceneNode import CuraSceneNode
from plugins.GCodeReader.GCodeReader import GCodeReader


class UFPReader(MeshReader):

    def __init__(self) -> None:
        super().__init__()

        MimeTypeDatabase.addMimeType(
            MimeType(
                name = "application/x-ufp",
                comment = "Cura UFP File",
                suffixes = ["ufp"]
            )
        )
        self._supported_extensions = [".ufp"]

    def _read(self, file_name: str) -> CuraSceneNode:
        # Open the file
        archive = VirtualFile()
        archive.open(file_name)
        # Get the gcode data from the file
        gcode_data = archive.getData("/3D/model.gcode")
        # Convert the bytes stream to string
        gcode_stream = gcode_data["/3D/model.gcode"].decode("utf-8")

        # Open the GCodeReader to parse the data
        gcode_reader = cast(GCodeReader, PluginRegistry.getInstance().getPluginObject("GCodeReader"))
        gcode_reader.preReadFromStream(gcode_stream)
        return gcode_reader.readFromStream(gcode_stream)
