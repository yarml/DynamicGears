from collections.abc import Callable
from abc import ABC, abstractmethod
from .InputFlow import InputFlow
from ..Fusion import FusionCore, Fusion
from .. import Utils

class DesignCommand(ABC):
    def __init__(self, id: str, name: str, description: str, resid: str | None = None):
        self._local_handlers = []
        self._lifecycle_handlers = []
        self.id = id
        self.resid = id if resid is None else resid
        self.name = name
        self.description = description
        self.cmd_def = None
        self.flow = self.make_flow()
        self.preselect_handlers: dict[str, Callable[[FusionCore.Selection, FusionCore.ObjectCollection], bool]] = dict()

    def preselect_set(self, input: FusionCore.SelectionCommandInput, handler: Callable[[FusionCore.ObjectCollection], bool]):
        self.preselect_handlers[input.id] = handler
    def preselect_unset(self, input: FusionCore.SelectionCommandInput):
        self.preselect_handlers.pop(input.id)

    @abstractmethod
    def make_flow(self) -> InputFlow:
        pass

    @abstractmethod
    def make_ui(self, inputs: FusionCore.CommandInputs):
        pass

    # Lifecycle    
    def start(self):
        self.cmd_def = Utils.UI.commandDefinitions.addButtonDefinition(self.id, self.name, self.description, Utils.resdir(self.resid))
        Utils.add_handler(self.cmd_def.commandCreated, self.on_create, local_handlers=self._lifecycle_handlers)
    def stop(self):
        if self.cmd_def:
            self.cmd_def.deleteMe()

    # Event handling
    def on_execute(self, args: FusionCore.CommandEventArgs):
        pass
    def on_preview(self, args: FusionCore.CommandEventArgs):
        pass

    def on_validate(self, args: FusionCore.ValidateInputsEventArgs):
        args.areInputsValid = self.flow.validate()
    def on_input_changed(self, args: FusionCore.InputChangedEventArgs):
        self.flow.process()

    # Selection events
    def on_pre_select(self, args: FusionCore.SelectionEventArgs):
        handler = self.preselect_handlers.get(args.activeInput.id)
        if handler is not None:
            args.isSelectable = handler(args.selection,  args.additionalEntities)

    def on_pre_select_end(self, args: FusionCore.SelectionEventArgs):
        pass
    def on_pre_select_mouse_move(self, args: FusionCore.SelectionEventArgs):
        pass
    def on_pre_select_start(self, args: FusionCore.SelectionEventArgs):
        pass
    def on_select(self, args: FusionCore.SelectionEventArgs):
        pass
    def on_unselect(self, args: FusionCore.SelectionEventArgs):
        pass

    # Keyboard/Mouse Events
    def on_key_down(self, args: FusionCore.KeyboardEventArgs):
        pass
    def on_key_up(self, args: FusionCore.KeyboardEventArgs):
        pass
    def on_mouse_click(self, args: FusionCore.MouseEventArgs):
        pass
    def on_mouse_double_click(self, args: FusionCore.MouseEventArgs):
        pass
    def on_mouse_down(self, args: FusionCore.MouseEventArgs):
        pass
    def on_mouse_drag(self, args: FusionCore.MouseEventArgs):
        pass
    def on_mouse_drag_begin(self, args: FusionCore.MouseEventArgs):
        pass
    def on_mouse_drag_end(self, args: FusionCore.MouseEventArgs):
        pass
    def on_mouse_move(self, args: FusionCore.MouseEventArgs):
        pass
    def on_mouse_up(self, args: FusionCore.MouseEventArgs):
        pass
    def on_mouse_wheel(self, args: FusionCore.MouseEventArgs):
        pass

    # Misc events
    def on_navigating_url(self, args: FusionCore.NavigationEventArgs):
        pass
    def on_incoming_from_html(self, args: FusionCore.HTMLEventArgs):
        pass

    # Lifecycle events
    def on_activate(self, args: FusionCore.CommandEventArgs):
        pass
    def on_deactivate(self, args: FusionCore.CommandEventArgs):
        pass
    def on_destroy(self, args: FusionCore.CommandEventArgs):
        self._local_handlers.clear()

    def on_create(self, args: FusionCore.CommandCreatedEventArgs):
        design = Fusion.Design.cast(Utils.APP.activeProduct)
        comp = design.activeComponent

        self.design = design
        self.comp = comp

        Utils.add_handler(args.command.activate, self.on_activate, local_handlers=self._local_handlers)
        Utils.add_handler(args.command.deactivate, self.on_deactivate, local_handlers=self._local_handlers)
        Utils.add_handler(args.command.destroy, self.on_destroy, local_handlers=self._local_handlers)
        Utils.add_handler(args.command.execute, self.on_execute, local_handlers=self._local_handlers)
        Utils.add_handler(args.command.executePreview, self.on_preview, local_handlers=self._local_handlers)
        Utils.add_handler(args.command.incomingFromHTML, self.on_incoming_from_html, local_handlers=self._local_handlers)
        Utils.add_handler(args.command.inputChanged, self.on_input_changed, local_handlers=self._local_handlers)
        Utils.add_handler(args.command.keyDown, self.on_key_down, local_handlers=self._local_handlers)
        Utils.add_handler(args.command.keyUp, self.on_key_up, local_handlers=self._local_handlers)
        Utils.add_handler(args.command.mouseClick, self.on_mouse_click, local_handlers=self._local_handlers)
        Utils.add_handler(args.command.mouseDoubleClick, self.on_mouse_double_click, local_handlers=self._local_handlers)
        Utils.add_handler(args.command.mouseDown, self.on_mouse_down, local_handlers=self._local_handlers)
        Utils.add_handler(args.command.mouseDrag, self.on_mouse_drag, local_handlers=self._local_handlers)
        Utils.add_handler(args.command.mouseDragBegin, self.on_mouse_drag_begin, local_handlers=self._local_handlers)
        Utils.add_handler(args.command.mouseDragEnd, self.on_mouse_drag_end, local_handlers=self._local_handlers)
        Utils.add_handler(args.command.mouseMove, self.on_mouse_move, local_handlers=self._local_handlers)
        Utils.add_handler(args.command.mouseUp, self.on_mouse_up, local_handlers=self._local_handlers)
        Utils.add_handler(args.command.mouseWheel, self.on_mouse_wheel, local_handlers=self._local_handlers)
        Utils.add_handler(args.command.navigatingURL, self.on_navigating_url, local_handlers=self._local_handlers)
        Utils.add_handler(args.command.preSelect, self.on_pre_select, local_handlers=self._local_handlers)
        Utils.add_handler(args.command.preSelectEnd, self.on_pre_select_end, local_handlers=self._local_handlers)
        Utils.add_handler(args.command.preSelectMouseMove, self.on_pre_select_mouse_move, local_handlers=self._local_handlers)
        Utils.add_handler(args.command.preSelectStart, self.on_pre_select_start, local_handlers=self._local_handlers)
        Utils.add_handler(args.command.select, self.on_select, local_handlers=self._local_handlers)
        Utils.add_handler(args.command.unselect, self.on_unselect, local_handlers=self._local_handlers)
        Utils.add_handler(args.command.validateInputs, self.on_validate, local_handlers=self._local_handlers)

        self.make_ui(args.command.commandInputs)

        self.flow.process()



    