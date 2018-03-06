import os
import signal
import json
import gi
import argparse
import krakenex

gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from gi.repository import GLib as glib

APPINDICATOR_ID = 'kraken/bittrex-indicator'

class LockKeyStatusIndicator(object):

    def __init__(self, show_kraken):
        self.show_kraken = show_kraken
        self.kraken_api = krakenex.API();
        self.app = appindicator.Indicator.new(APPINDICATOR_ID, "text", appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.app.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.update_label()
        #self.notify.init(APPINDICATOR_ID)
        self.app.set_menu(self.build_menu())
        #self.kraken.load_key('kraken.key');


    def build_menu(self):
        menu = gtk.Menu()
        item_kraken = gtk.MenuItem('Kraken')
        item_kraken.connect('activate', self.kraken)
        menu.append(item_kraken)

        item_bittrex = gtk.MenuItem('Bittrex')
        item_bittrex.connect('activate', self.bittrex)
        menu.append(item_bittrex)

        item_quit = gtk.MenuItem('Exit')
        item_quit.connect('activate', self.quit)
        menu.append(item_quit)
        menu.show_all()
        return menu
################################################
    def run(self):
        try:
            print("Running... ")
            gtk.main()
        except KeyboardInterrupt:
            pass

    def quit(self, data=None):
        #notify.uninit()
        gtk.main_quit()
################################################
    def update_label(self):
        if self.show_kraken:
            label_text = self.get_kraken_info()
        else:
            label_text = self.get_bittrex_info()

        self.app.set_label(label_text, "")
        glib.timeout_add_seconds(1, self.set_app_label)

    def set_app_label(self):
        self.update_label()
################################################
    def kraken(self):
        self.show_kraken = True
    def bittrex(self):
        self.show_kraken = False
################################################
    def get_kraken_info(self):
        #notify.Notification.new("<b>Kraken</b>", "Pues OK.", None).show()
        # Conectar con Kraken
        #req_price = dict()
        #req_price["pair"] = ""

        #Obtener lista de precios

        ticker = self.kraken_api.query_public('Ticker', {
            'pair': 'XXBTZEUR, XETHZEUR, XLTCZEUR'
        })
        ticker = ticker['result']

        text = "KRK: "
        for coin_id in ticker:
            coin = ticker[coin_id]

            text += coin_id+"(" + coin['c'][1]+"€) "
            print(coin)

        return text

    def get_bittrex_info(self):
        #notify.Notification.new("<b>Bittrex</b>", "Pues OK.", None).show()
        text = "Bittrex"
        return text

################################################
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
            "--krk", help="listado de precios en kraken", action="store_true")
    #parser.add_argument("--btt", help="listado de precios en bittrex", action="store_true")
    args = parser.parse_args()
    indicator = LockKeyStatusIndicator(args.krk)
    indicator.run()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()

#def fetch_joke():
#    request = Request('http://api.icndb.com/jokes/random?limitTo=[nerdy]')
#    response = urlopen(request)
#    joke = json.loads(response.read())['value']['joke']
#    return joke

#def joke(_):
#    notify.Notification.new("<b>Joke</b>", fetch_joke(), None).show()
