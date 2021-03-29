import json
import logging
from time import sleep
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction

logger = logging.getLogger(__name__)


class DemoExtension(Extension):

    def __init__(self):
        super(DemoExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        items = []
        logger.info('preferences %s' % json.dumps(extension.preferences))

#       for i in range(5):
#       item_name = extension.preferences['item_name']

#       Create Connect entry for the menu
        data = {'action_name': 'Connnect was clicked','action_icon':'images/Connect.png'}
        items.append(ExtensionResultItem(icon='images/Connect.png',
                                            name='%s' % ('Connect'),
                                            description='Item description',
                                            on_enter=ExtensionCustomAction(data, keep_app_open=True)))

#       Create disconnect entry for the menu        
        data = {'action_name': 'Disconnect was clicked','action_icon':'images/Disconnect.png'}
        items.append(ExtensionResultItem(icon='images/Disconnect.png',
                                            name='%s' % ('Disconnect'),
                                            description='Item description',
                                            on_enter=ExtensionCustomAction(data, keep_app_open=True)))

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        data = event.get_data()
        return RenderResultListAction([ExtensionResultItem(icon=data['action_icon'],
                                                           name=data['action_name'],
                                                           on_enter=HideWindowAction())])


if __name__ == '__main__':
    DemoExtension().run()
