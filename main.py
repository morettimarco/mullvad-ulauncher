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

import subprocess, logging, os, time


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
        data = {'action_name': 'Connect','action_icon':'images/Connect.png','action_command':'connect'}
        items.append(ExtensionResultItem(icon=data['action_icon'],
                                            name=data['action_name'],
                                            description='Item description',
                                            on_enter=ExtensionCustomAction(data, keep_app_open=True)))

#       Create disconnect entry for the menu        
        data = {'action_name': 'Disconnect','action_icon':'images/Disconnect.png','action_command':'disconnect'}
        items.append(ExtensionResultItem(icon=data['action_icon'],
                                            name=data['action_name'],
                                            description='Item description',
                                            on_enter=ExtensionCustomAction(data, keep_app_open=True)))

#       Create reconnect entry for the menu        
        data = {'action_name': 'Reconnect','action_icon':'images/Reconnect.png','action_command':'reconnect'}
        items.append(ExtensionResultItem(icon=data['action_icon'],
                                            name=data['action_name'],
                                            description='Item description',
                                            on_enter=ExtensionCustomAction(data, keep_app_open=True)))

        return RenderResultListAction(items)


class ItemEnterEventListener(EventListener):
    def on_event(self, event, extension):
        root = os.path.dirname(os.path.realpath(__file__))
        iconprop = "--icon="+root+"/images/480px-Mullvad_logo.svg.png"
        data = event.get_data()


        subprocess.run(['notify-send', iconprop, 'Mullvad '+data['action_name']]+'...', stdout=subprocess.PIPE)

        #Execute mullvad CLI command
        subprocess.run(['mullvad', data['action_command']], stdout=subprocess.PIPE)
        
        
        return RenderResultListAction([ExtensionResultItem(icon=data['action_icon'],
                                                           name=data['action_name'],
                                                           on_enter=HideWindowAction())])


if __name__ == '__main__':
    DemoExtension().run()
