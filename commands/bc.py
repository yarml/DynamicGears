from .. import Fusion
from .. import utils

class ButtonCommand:
    def __init__(self, id: str, name: str, description: str):
        self._local_handlers = []
        self._lifecycle_handlers = []
        self.id = id
        self.name = name
        self.description = description
        self.cmd_def = None

    def created(self, args: Fusion.CommandCreatedEventArgs):
        utils.add_handler(args.command.execute, self.execute, local_handlers=self._local_handlers)
        utils.add_handler(args.command.inputChanged, self.input_changed, local_handlers=self._local_handlers)
        utils.add_handler(args.command.executePreview, self.preview, local_handlers=self._local_handlers)
        utils.add_handler(args.command.validateInputs, self.validate, local_handlers=self._local_handlers)
        utils.add_handler(args.command.destroy, self.destroy, local_handlers=self._local_handlers)

    def execute(self, args: Fusion.CommandEventArgs):
        pass
    def input_changed(self, args: Fusion.InputChangedEventArgs):
        pass
    def preview(self, args: Fusion.CommandEventArgs):
        pass
    def validate(self, args: Fusion.ValidateInputsEvent):
        pass
    def destroy(self, args: Fusion.CommandEventArgs):
        self._local_handlers.clear()
    
    def start(self):
        self.cmd_def = utils.UI.commandDefinitions.addButtonDefinition(self.id, self.name, self.description, utils.icon_folder(self.id))
        utils.add_handler(self.cmd_def.commandCreated, self.created, local_handlers=self._lifecycle_handlers)

    def stop(self):
        cmd_def = utils.UI.commandDefinitions.itemById(self.id)
        if cmd_def:
            cmd_def.deleteMe()
        self._lifecycle_handlers.clear()