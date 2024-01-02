# builder is used for the registering and application of rules for specific widgets.
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage
from deck import Deck
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
import pyperclip
from kivy.graphics import Color, Rectangle
import webbrowser
import json
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivymd.uix.screen import MDScreen

from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.screenmanager import MDScreenManager

from kivy.uix.widget import Widget
from PIL import Image as PILImage
from io import BytesIO
from kivy.graphics.texture import Texture
from kivy.uix.image import Image as KivyImage
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.app import MDApp
from kivymd.theming import ThemeManager
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout

# the properties classes are used when you create an eventdispatcher
from kivy.properties import StringProperty, ListProperty

# to change the kivy default setting we use config
# from kivy.config import Config
# Config.set('graphics','width','550')
# Config.set('graphics','height','550')

# this module contains MDApp class that is inherited from app
from kivymd.app import MDApp

# import theming to use them ,color and hover options
from kivymd.theming import ThemableBehavior

# boxlayout arranges children in a vertical or horizontal box
from kivymd.uix.boxlayout import MDBoxLayout

# onelinelistitem will create a list that expands as items are added to it
from kivymd.uix.list import OneLineIconListItem, MDList



# creating the kv file.you can write it also in a separate .kv file
KV = '''
# Menu item in the DrawerList list.
<ItemDrawer>:
    theme_text_color: "Custom"
    theme_text_color: "Custom"
    IconLeftWidget:
        id: icon
        icon: root.icon
        theme_text_color: "Custom"
        text_color: root.text_color


# create a class to use mdboxlayout for the navigation content
<ContentNavigationDrawer>:
    orientation: "vertical"
    padding: "8dp"
    spacing: "8dp"
    canvas.before:
        Rectangle:
            pos: self.pos
            size: self.size

    AnchorLayout:
        size_hint_y: None
        height: avatar.height

        Image:
            id: avatar
            size_hint: None, None
            size: "75dp", "75dp"
            source: "logo.png"

    MDLabel:
        text: "Deck Vault"
        font_style: "Button"
        adaptive_height: True
        halign: 'center'

    MDLabel:
        text: "v1.0.0"
        font_style: "Caption"
        adaptive_height: True
        halign: 'center'
        canvas:
            Color:
                rgba: 0.6, 0.6, 0.6, 1  # Set the color of the line (black in this example)
            Line:
                points: self.x, self.y - 2, self.x + self.width, self.y - 2

    ScrollView:
        DrawerList:
            id: md_list

    ItemDrawer:
        icon: 'star' 
        text: 'Saved Decks'
        pos_hint: {'center_x': 0.5, 'center_y': 1}  # Adjust the position


    
    # MDBoxLayout:
    #     orientation: 'vertical'
    #     size_hint_y: None  # Disable the automatic height calculation
    #     height: dp(300)  # Set the desired height in density-independent pixels (dp)

    MDBoxLayout:
        orientation: 'vertical'
        MDLabel:
            text: 'Developed by glad04'
            font_style: "Caption"
            halign: 'center'  # Align the label text to the left
            theme_text_color: "Custom"
            text_color: (0.7, 0.7, 0.7, 1)  # Set the text color to gray





        


<MDScreenManager>:
    id: scr_mngr

    HomeScreen:
        name: 'home'



<HomeScreen>:
    name: 'home'

    BoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Deck Vault"
            elevation: 10
            left_action_items: [['menu', lambda x: nav_drawer.set_state("open")]]

        MDBoxLayout:
            orientation: 'vertical'

            # Top Layout
            MDBoxLayout:
                orientation: 'vertical'
                size_hint: None, 0.5
                pos_hint: {'center_x': 0.5}

                Image:
                    source: 'logo.png'
                    size_hint: None, None
                    size: 100, 100
                    allow_stretch: False

            MDBoxLayout:
                orientation: 'vertical'
                size_hint: None, 0.5
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}

                MDBoxLayout:
                    orientation: 'vertical'
                    size_hint: None, None
                    size: 400, 80
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}

                    MDTextField:
                        id: deck_link_input
                        hint_text: "Deck Link"
                        multiline: False
                        size_hint: None, None
                        size: 300, 40
                        width: 300
                        height: 40
                        pos_hint: {'center_x': 0.5}
                    MDRaisedButton:
                        text: "Save Deck"
                        on_press: app.save_deck(deck_link_input)
                        size_hint: None, None
                        size: 150, 40
                        width: 150
                        height: 40
                        pos_hint: {'center_x': 0.5}
    MDNavigationDrawer:
        id: nav_drawer
        width: dp(250)  # Set the desired width in density-independent pixels (dp)
        ContentNavigationDrawer:
            id: content_drawer

'''

class SavedDecksScreen(Screen):
    pass

class CopyDeckButton(ButtonBehavior, Image):
    pass

class OpenDeckButton(ButtonBehavior, Image):
    pass

class SaveDeckButton(Button):
    pass

class ViewSavedDecksButton(Button):
    pass

class HomeScreen(MDScreen):
    pass

class SaveSuccessPopup(Popup):
    def __init__(self, deck_link, **kwargs):
        super(SaveSuccessPopup, self).__init__(**kwargs)
        self.title = 'Deck saved successfully!'
        self.size_hint = (None, None)
        self.size = (400, 200)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.deck = Deck()
        content_layout = BoxLayout(orientation='vertical', spacing=10, padding=10, pos_hint={'center_x': 0.5})
        deck_layout = self.generate_deck_layout(deck_link)
        content_layout.add_widget(deck_layout)
        ok_button = Button(text="OK", background_color=(0, 0, 0, 0)) 
        ok_button.bind(on_press=self.dismiss)
        content_layout.add_widget(ok_button)
        self.content = content_layout


    def generate_deck_layout(self, dl):
        deck_link = dl
        cards_layout = GridLayout(cols=8, spacing=10, size_hint=(None, None), width=300, pos_hint={'center_x': 0.5})
        card_keys = self.deck.decklink_to_cards(deck_link)
        if card_keys is not None:
            for i, card in enumerate(card_keys):
                if i == 0 and card in self.deck.available_evos:
                    card_image_file = f"assets/cards/{card}-ev1.png"
                else:
                    card_image_file = f"assets/cards/{card}.png"
                
                card_image = AsyncImage(source=card_image_file)
                cards_layout.add_widget(card_image)
        return cards_layout

# create a class to use mdboxlayout for the navigation content
class ContentNavigationDrawer(MDBoxLayout):
    pass
# create another class and specifying icon and text colors
class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((1, 1, 1, 1))
    
    def on_release(self):
        print(f"Item '{self.text}' clicked!")
        app = MDApp.get_running_app()
        # app.screen_manager.switch_to('saved_decks')
        app.screen_manager.current = 'saved_decks'


# create a drawerlist class for theming the item list
class DrawerList(ThemableBehavior, MDList):
    # called when tap on menu item
    def set_color_item(self, instance_item):
        # set the color of the icon and text for the menu items
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color

class NavigationDrawer(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Purple"
        self.theme_cls.theme_style = "Dark"  # Set the default theme style to Dark
        self.theme_cls.primary_text_color = "Custom"  # Set the text color to Custom

        Builder.load_string(KV)

        self.screen_manager = MDScreenManager()
        # home_screen = HomeScreen(name='home')

        # self.screen_manager.add_widget(home_screen)
        

        return self.screen_manager


    def on_start(self):
        self.deck = Deck()
        saved_decks_screen = self.create_saved_decks_screen()
        self.screen_manager.add_widget(saved_decks_screen)


    def switch_to_home_screen(self, instance):
        # Switch to the home screen
        self.screen_manager.current = 'home'
    
    def view_saved_decks(self, instance=None):
        # Switch to the saved decks screen
        print("View Saved Decks clicked!")
        self.screen_manager.switch_to(self.create_saved_decks_screen())

    def update_deck_display(self, deck_link):
        self.generate_deck(deck_link)
        pass

    def generate_deck_layout(self, dl, k):
        # Get the deck link from the TextInput
        deck_link = dl

        # Create a BoxLayout to hold the grid view of cards and the copy button
        # deck_layout = BoxLayout(orientation='vertical', spacing=5, padding=(0, 5, 0, 0), size_hint_y=None, height=150)  # Set height based on your design
        deck_layout = BoxLayout(orientation='vertical', spacing=5, padding=(0, 10, 0, 0), size_hint_y=None, height=150)

        # Create a new GridLayout for the cards
        cards_layout = GridLayout(cols=8, spacing=10, size_hint=(None, None), width=Window.width)
        
        # Call the Deck class method to get the card keys from the deck link
        card_keys = self.deck.decklink_to_cards(deck_link)

        # Check if card_keys is not None before proceeding
        if card_keys is not None:
            # Iterate through card keys and add cards to the GridLayout
            for i, card in enumerate(card_keys):
                if i == 0 and card in self.deck.available_evos:
                    card_image_file = f"assets/cards/{card}-ev1.png"
                else:
                    card_image_file = f"assets/cards/{card}.png"
                
                # Create an AsyncImage widget for each card
                card_image = AsyncImage(source=card_image_file)
                cards_layout.add_widget(card_image)
        
        label_button_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), height=40, spacing=10)

        # Create the deck label
        deck_name_label = Label(text=f"Deck {k}:", size_hint=(None, 1), width='100dp')  # Adjust width as needed

        # Add an empty widget to push the copy button to the right
        empty_widget = Widget(size_hint_x=None, width=1)

        # Create the copy button
        copy_button = OpenDeckButton(source="copy-files.png", on_press=lambda x: self.open_deck_link(card_keys), size_hint_x=None, width='50dp')  # Adjust width as needed

        # Add the deck label, empty widget, and copy button to the horizontal layout
        label_button_layout.add_widget(deck_name_label)
        label_button_layout.add_widget(empty_widget)
        label_button_layout.add_widget(copy_button)

        # Add the horizontal layout to the main BoxLayout
        deck_layout.add_widget(label_button_layout)


        # Add the GridLayout for cards to the BoxLayout
        deck_layout.add_widget(cards_layout)

        # Add a separator line (you can customize this)
        separator = Image(source="separator_image.png", size_hint_y=None, height=2)
        deck_layout.add_widget(separator)

        return deck_layout
        
    def save_deck(self, deck_link):
        # Save the deck to a JSON file
        # Modify this logic based on your deck structure and requirements
        dl_input = deck_link
        deck_link = dl_input.text
        dl_input.text = ""
        
        try:
            saved_deck = {
            "deck_link": deck_link,
            "cards": [card_key for card_key in self.deck.decklink_to_cards(deck_link)]
            }
        except:
            return 
        # Read existing saved decks from file
        saved_decks = []
        try:
            with open("saved_decks.json", "r") as json_file:
                saved_decks = json.load(json_file)
        except FileNotFoundError:
            pass  # File doesn't exist yet

        # Check if the deck already exists in the list
        if saved_deck not in saved_decks:
            # Add the new deck to the list
            saved_decks.append(saved_deck)

            # Write the entire list back to the file
            with open("saved_decks.json", "w") as json_file:
                json.dump(saved_decks, json_file, indent=2)

            # Display a message
            print("Deck saved!")

            # Update the deck display (optional)
            SaveSuccessPopup(deck_link=deck_link).open()
        else:
            # Display a popup indicating that the deck is already saved
            self.show_duplicate_save_popup()    

    def create_saved_decks_screen(self):
        # Create a screen for displaying saved decks
        saved_decks_screen = SavedDecksScreen(name='saved_decks')
        
        # Create a BoxLayout with vertical orientation
        top_box_layout = MDBoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=60)  # Adjust the height as needed
        
        # Add the back button to the top layout
        back_button = MDRaisedButton(text="<", size_hint_y=None, height=40)
        back_button.bind(on_press=self.switch_to_home_screen)
        button_bg_color = back_button.theme_cls.primary_color
        # Create an MDBoxLayout
        # box = MDTopAppBar()

        top_box_layout.add_widget(back_button)
        # top_box_layout.add_widget(box)
        
        # Read saved decks from file
        try:
            with open("saved_decks.json", "r") as json_file:
                saved_decks = json.load(json_file)

                # Create a GridLayout for displaying saved decks
                saved_decks_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
                saved_decks_layout.bind(minimum_height=saved_decks_layout.setter('height'))

                i = 1
                for saved_deck in saved_decks:
                    # Generate the deck layout and add it to the saved decks layout
                    generated_deck_layout = self.generate_deck_layout(saved_deck['deck_link'], i)
                    saved_decks_layout.add_widget(generated_deck_layout)
                    i += 1
            
            container_layout = BoxLayout(orientation='vertical')
            # Wrap the saved_decks_layout in a ScrollView
            scroll_view = ScrollView(size_hint=(1, None), height=self.root.height-50)  # Set height based on your design
            scroll_view.add_widget(saved_decks_layout)

            # Add the ScrollView to the saved decks screen
            container_layout.add_widget(top_box_layout)
            container_layout.add_widget(scroll_view)
            saved_decks_screen.add_widget(container_layout)

            # Add the top layout to the saved decks screen


        except FileNotFoundError:
            print("No saved decks yet.")

        return saved_decks_screen



# run the app
NavigationDrawer().run()
