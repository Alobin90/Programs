import arcade
import arcade.gui
import random
from random import randint
import shelve


SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "Fishman's Dream"

BOTTOM = 0.5
GROUND_SCALING = 0.5
WAVES = 1
SEAWEED_SIZE = 0.9425

BOAT_MOVEMENT_SPEED = 5
HOOK_MOVEMENT_SPEED = 5 # x*60

MIN_FISH_SPEED = 100
MAX_FISH_SPEED = 450

MIN_FISH_SIZE = .1
MAX_FISH_SIZE = .175

MIN_LARGE_FISH_SIZE = .125
MAX_LARGE_FISH_SIZE = .225

BOAT_BASE_SCALING = 0.175
HOOK = 0.04
ROPE = 0.05

max_perch = randint(10, 25)

starter_perch = [random.uniform(MIN_FISH_SIZE, MAX_FISH_SIZE) for i in range(max_perch)]
fish_speeds = [randint(MIN_FISH_SPEED, MAX_FISH_SPEED)*((MAX_FISH_SIZE+MIN_FISH_SIZE)/2)/starter_perch[i] for i in range(max_perch)]
fish_animation_index = [1 for i in range(max_perch)]
fish_animation_index_change = [1 for i in range(max_perch)]

waves_splashes = arcade.Sound("sounds/waves_splash.mp3")
arcade.play_sound(waves_splashes, looping=True, volume=0.5)

save = shelve.open('saves/saves_file')
'''save['SavedCoins'] = 0
save['PerchCount'] = 0
save['CarpCount'] = 0
save['LocalScore'] = 0
save['LakeBestScore'] = 0
save['MapChange'] = 0
save['PiranhaCount'] = 0
save['AravanaCount'] = 0
save['FishCount'] = 0'''

class Menu(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

        if save['MapChange'] == 0:
            self.background_lake = arcade.load_texture("image/backgrounds/lake.png")
            self.background_sea = arcade.load_texture("image/backgrounds/sea_bottom.png")
            self.background_seaweed = arcade.load_texture("image/backgrounds/lake_seaweed.png")
            self.background_waves = arcade.load_texture("image/backgrounds/waves.png")
        elif save['MapChange'] == 1:
            self.background_lake = arcade.load_texture("image/backgrounds/river.png")
            self.background_sea = arcade.load_texture("image/backgrounds/river_bottom.png")
            self.background_seaweed = arcade.load_texture("image/backgrounds/river_seaweed.png")
            self.background_waves = arcade.load_texture("image/backgrounds/river_waves.png")

        self.coin_gui = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.buttons_active = True

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.gui_box = arcade.gui.UIBoxLayout()

        lake_style = {
            "font_name": ("calibri", "arial"),
            "font_size": 20,
            "font_color": arcade.color.BLACK,
            "border_width": 2,
            "border_color": None,
            "bg_color": (arcade.color_from_hex_string('#B8D6D2')),

            # used if button is pressed
            "bg_color_pressed": arcade.color.WHITE,
            "border_color_pressed": arcade.color.WHITE,  # also used when hovered
            "font_color_pressed": arcade.color.BLACK,
        }

        river_style = {
            "font_name": ("calibri", "arial"),
            "font_size": 20,
            "font_color": arcade.color.BLACK,
            "border_width": 2,
            "border_color": None,
            "bg_color": (arcade.color_from_hex_string('#BDE0CA')),

            # used if button is pressed
            "bg_color_pressed": arcade.color.WHITE,
            "border_color_pressed": arcade.color.WHITE,  # also used when hovered
            "font_color_pressed": arcade.color.BLACK,
        }

        start = None
        change_maps = None
        lore = None
        achives = None
        exit = None

        if save['MapChange'] == 0:
            start = arcade.gui.UIFlatButton(text="Начать ловлю", width=300, style=lake_style)
            change_maps = arcade.gui.UIFlatButton(text="Выбор карты", width=300, style=lake_style)
            lore = arcade.gui.UIFlatButton(text="Предыстория и правила", width=300, height=80, style=lake_style)
            achives = arcade.gui.UIFlatButton(text="Достижения", width=300, style=lake_style)
            exit = arcade.gui.UIFlatButton(text="Выход (Esc)", width=300, style=lake_style)
        elif save['MapChange'] == 1:
            start = arcade.gui.UIFlatButton(text="Начать ловлю", width=300, style=river_style)
            change_maps = arcade.gui.UIFlatButton(text="Выбор карты", width=300, style=river_style)
            lore = arcade.gui.UIFlatButton(text="Предыстория и правила", width=300, height=80, style=river_style)
            achives = arcade.gui.UIFlatButton(text="Достижения", width=300, style=river_style)
            exit = arcade.gui.UIFlatButton(text="Выход (Esc)", width=300, style=river_style)

        self.gui_box.add(start.with_space_around(top=100))
        self.gui_box.add(change_maps.with_space_around(top=3))
        self.gui_box.add(lore.with_space_around(top=3))
        self.gui_box.add(achives.with_space_around(top=3))
        self.gui_box.add(exit.with_space_around(top=3))

        start.on_click = self.on_click_start
        exit.on_click = self.on_click_exit
        change_maps.on_click = self.on_click_change
        achives.on_click = self.on_click_achive
        lore.on_click = self.on_click_lore

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.gui_box)
        )

    def on_click_start(self, event):
        if self.buttons_active:
            game = MyGame()
            self.window.show_view(game)
            self.buttons_active = False
            print(save['MapChange'])
        else: pass

    def on_click_exit(self, event):
        save.close()
        if self.buttons_active:
            arcade.close_window()
        else: pass

    def on_click_change(self, event):
        if self.buttons_active:
            maps = ChangeMap()
            self.window.show_view(maps)
            self.buttons_active = False
            ChangeMap().change_maps_buttons_active = True
        else: pass

    def on_click_achive(self, event):
        if self.buttons_active:
            collected_achive = Achives()
            self.window.show_view(collected_achive)
            self.buttons_active = False
        else: pass

    def on_click_lore(self, event):
        if self.buttons_active:
            upgrades = Lore()
            self.window.show_view(upgrades)
            self.buttons_active = False
        else: pass

    def on_draw(self):
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 640, SCREEN_WIDTH, SCREEN_HEIGHT // 2.75, self.background_lake)
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 1.56, self.background_sea)
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2.55, self.background_seaweed)
        arcade.draw_lrwh_rectangle_textured(0, -348, SCREEN_WIDTH, SCREEN_HEIGHT, self.background_waves)

        self.coin_gui.use()

        if save['MapChange'] == 0:
            arcade.draw_text("Fishman's Dream", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 250,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
            arcade.draw_text(f"Баланс: {save['SavedCoins']:.0f}", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 320,
                             arcade.csscolor.BLACK, 32, anchor_x="center")
        elif save['MapChange'] == 1:
            arcade.draw_text("Fishman's Dream", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 250,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
            arcade.draw_text(f"Баланс: {save['SavedCoins']:.0f}", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 320, arcade.csscolor.WHITE, 32, anchor_x="center")

        self.manager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.close_window()

class GameOver(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        if save['MapChange'] == 0:
            self.background_lake = arcade.load_texture("image/backgrounds/lake.png")
            self.background_sea = arcade.load_texture("image/backgrounds/sea_bottom.png")
            self.background_seaweed = arcade.load_texture("image/backgrounds/lake_seaweed.png")
            self.background_waves = arcade.load_texture("image/backgrounds/waves.png")
        elif save['MapChange'] == 1:
            self.background_lake = arcade.load_texture("image/backgrounds/river.png")
            self.background_sea = arcade.load_texture("image/backgrounds/river_bottom.png")
            self.background_seaweed = arcade.load_texture("image/backgrounds/river_seaweed.png")
            self.background_waves = arcade.load_texture("image/backgrounds/river_waves.png")

    def on_draw(self):
        arcade.start_render()
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 640, SCREEN_WIDTH, SCREEN_HEIGHT // 2.75, self.background_lake)
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 1.56, self.background_sea)
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2.55, self.background_seaweed)
        arcade.draw_lrwh_rectangle_textured(0, -348, SCREEN_WIDTH, SCREEN_HEIGHT, self.background_waves)

        if save['MapChange'] == 0:
            self.location = arcade.color.BLACK
        elif save['MapChange'] == 1:
            self.location = arcade.color.WHITE

        arcade.draw_text("Рыбалка окончена", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 75,
                        self.location, font_size=50, anchor_x="center")
        if save['LocalScore'] == save['LakeBestScore']:
            arcade.draw_text(f"Новый рекорд улова {save['LakeBestScore']:.3f} кг на сумму {save['LocalScore'] * MyGame().kilo_price:.0f}", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30,
                        self.location, font_size=30, anchor_x="center")
        elif save['LocalScore'] < save['LakeBestScore']:
            arcade.draw_text(f"Улова {save['LocalScore']:.3f} кг на сумму {save['LocalScore'] * MyGame().kilo_price:.0f}",
                             SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 30,
                             self.location, font_size=30, anchor_x="center")
        arcade.draw_text("Enter или ПКМ - продолжить",
                         SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2 - 30,
                         self.location,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ENTER:
            menu = Menu()
            self.window.show_view(menu)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        menu = Menu()
        self.window.show_view(menu)

class ChangeMap(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        self.change_maps_buttons_active = True

        if save['MapChange'] == 0:
            self.background_lake = arcade.load_texture("image/backgrounds/lake.png")
            self.background_sea = arcade.load_texture("image/backgrounds/sea_bottom.png")
            self.background_seaweed = arcade.load_texture("image/backgrounds/lake_seaweed.png")
            self.background_waves = arcade.load_texture("image/backgrounds/waves.png")
        elif save['MapChange'] == 1:
            self.background_lake = arcade.load_texture("image/backgrounds/river.png")
            self.background_sea = arcade.load_texture("image/backgrounds/river_bottom.png")
            self.background_seaweed = arcade.load_texture("image/backgrounds/river_seaweed.png")
            self.background_waves = arcade.load_texture("image/backgrounds/river_waves.png")

        self.map_manager = arcade.gui.UIManager()
        self.map_manager.enable()

        self.change_map_box = arcade.gui.UIBoxLayout()

        lake = arcade.gui.UIFlatButton(text="Озеро", width=300)
        river = arcade.gui.UIFlatButton(text="Река", width=300)
        back = arcade.gui.UIFlatButton(text="Назад", width=300)
        self.change_map_box.add(lake.with_space_around(bottom=1))
        self.change_map_box.add(river.with_space_around(bottom=1))
        self.change_map_box.add(back.with_space_around(bottom=1))

        lake.on_click = self.on_click_lake
        river.on_click = self.on_click_river
        back.on_click = self.on_click_back

        self.map_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.change_map_box)
        )

    def on_click_lake(self, event):
        if self.change_maps_buttons_active:
            self.background_lake = arcade.load_texture("image/backgrounds/lake.png")
            self.background_sea = arcade.load_texture("image/backgrounds/sea_bottom.png")
            self.background_seaweed = arcade.load_texture("image/backgrounds/lake_seaweed.png")
            self.background_waves = arcade.load_texture("image/backgrounds/waves.png")
            save['MapChange'] = 0
            print('Changed lake')
        else:
            pass

    def on_click_river(self, event):
        if self.change_maps_buttons_active:
            self.background_lake = arcade.load_texture("image/backgrounds/river.png")
            self.background_sea = arcade.load_texture("image/backgrounds/river_bottom.png")
            self.background_seaweed = arcade.load_texture("image/backgrounds/river_seaweed.png")
            self.background_waves = arcade.load_texture("image/backgrounds/river_waves.png")
            save['MapChange'] = 1
            print('Changed river')
        else:
            pass

    def on_click_back(self, event):
        if self.change_maps_buttons_active:
            menu = Menu()
            self.window.show_view(menu)
            self.change_maps_buttons_active = False
        else: pass

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 640, SCREEN_WIDTH, SCREEN_HEIGHT // 2.75, self.background_lake)
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 1.56, self.background_sea)
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2.55, self.background_seaweed)
        arcade.draw_lrwh_rectangle_textured(0, -348, SCREEN_WIDTH, SCREEN_HEIGHT, self.background_waves)
        self.map_manager.draw()

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            menu = Menu()
            self.window.show_view(menu)

class Lore(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        if save['MapChange'] == 0:
            self.background_lake = arcade.load_texture("image/backgrounds/lake.png")
            self.background_sea = arcade.load_texture("image/backgrounds/sea_bottom.png")
            self.background_seaweed = arcade.load_texture("image/backgrounds/lake_seaweed.png")
            self.background_waves = arcade.load_texture("image/backgrounds/waves.png")
        elif save['MapChange'] == 1:
            self.background_lake = arcade.load_texture("image/backgrounds/river.png")
            self.background_sea = arcade.load_texture("image/backgrounds/river_bottom.png")
            self.background_seaweed = arcade.load_texture("image/backgrounds/river_seaweed.png")
            self.background_waves = arcade.load_texture("image/backgrounds/river_waves.png")

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 640, SCREEN_WIDTH, SCREEN_HEIGHT // 2.75, self.background_lake)
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 1.56, self.background_sea)
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2.55, self.background_seaweed)
        arcade.draw_lrwh_rectangle_textured(0, -348, SCREEN_WIDTH, SCREEN_HEIGHT, self.background_waves)

        arcade.draw_lrwh_rectangle_textured(-10, 0, SCREEN_WIDTH, SCREEN_HEIGHT, arcade.load_texture("image/static_meshes/rules_bg.png"))

        font_size = 20

        arcade.draw_text("Вот уже 5 лет молодой рыбак путешествует по миру в поисках новых видов рыб.", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 210, arcade.csscolor.BLACK, font_size, anchor_x="center")
        arcade.draw_text("Он посетил множество стран, побывал на многих известных прудах и реках.", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 180, arcade.csscolor.BLACK, font_size, anchor_x="center")
        arcade.draw_text("В своих записках, рыбак указал пару мест, которые ему больше всего понравились.", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 150, arcade.csscolor.BLACK, font_size, anchor_x="center")
        arcade.draw_text("Однажды, читая новости в газете, герой узнает, что в этом году проходит соревнование среди рыбаков.", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 120, arcade.csscolor.BLACK, font_size, anchor_x="center")
        arcade.draw_text("Главный приз - платиновая статуэтка опаснейшей рыбы в мире.", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 90, arcade.csscolor.BLACK, font_size, anchor_x="center")
        arcade.draw_text("Рыбак решает опробовать свои силы и попытаться выйграть статуэтку.", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60, arcade.csscolor.BLACK, font_size, anchor_x="center")
        arcade.draw_text("Правила участия:", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 30, arcade.csscolor.BLACK, font_size, anchor_x="center")
        arcade.draw_text("1. Участник может использовать только деревянную лодку, выданную огранизацией.", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 60, arcade.csscolor.BLACK, font_size, anchor_x="center")
        arcade.draw_text("2. Рыбачить разрешено только в локациях, которые указаны в меню Выбора уровня.", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 90, arcade.csscolor.BLACK, font_size, anchor_x="center")
        arcade.draw_text("3. Время рыбалки ограничено с 13:00 до 17:00 для усложнения ловли", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 120, arcade.csscolor.BLACK, font_size, anchor_x="center")
        arcade.draw_text("4. В разделе Достижений отображаются все достижения игрока, а также некоторые награды.", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 150, arcade.csscolor.BLACK, font_size, anchor_x="center")
        arcade.draw_text("Помогите рыбаку выйграть соревнование.", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 240, arcade.csscolor.BLACK, font_size, anchor_x="center")
        arcade.draw_text("Удачи!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 270, arcade.csscolor.BLACK, font_size, anchor_x="center")

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        menu = Menu()
        self.window.show_view(menu)

class Achives(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show(self):
        self.background_achive = arcade.load_texture("image/backgrounds/achive_background.png")
        self.unknown_achive = arcade.load_texture("image/static_meshes/unknown_achive.png")

        self.screen = arcade.Scene()

        self.screen.add_sprite_list("Achives")

        self.achives_buttons = True

        if save['PerchCount'] > 0:
            self.achive1_check = True
        else:
            self.achive1_check = False

        if save['CarpCount'] > 0:
            self.achive2_check = True
        else:
            self.achive2_check = False

        if save['PiranhaCount'] > 0:
            self.achive3_check = True
        else:
            self.achive3_check = False

        if save['AravanaCount'] > 0:
            self.achive4_check = True
        else:
            self.achive4_check = False

        if save['PerchCount'] >= 100 and save['CarpCount'] >= 100 and save['PiranhaCount'] >= 100 and save['AravanaCount'] >= 100:
            self.achive5_check = True
        else:
            self.achive5_check = False

        if save['FishCount'] >= 5000 and save['SavedCoins'] >= 50000:
            self.achive6_check = True
        else:
            self.achive6_check = False

        self.achive_manager = arcade.gui.UIManager()
        self.achive_manager.enable()
        self.back_menu_from_achive = arcade.gui.UIBoxLayout()

        back_menu = arcade.gui.UIFlatButton(text="Меню", width=300)
        self.back_menu_from_achive.add(back_menu.with_space_around(right=50, top=120))

        back_menu.on_click = self.on_click_back_menu

        self.achive_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="right",
                anchor_y="top",
                child=self.back_menu_from_achive)
        )

        if self.achive1_check:
            self.achive1 = arcade.Sprite("image/fish/perch_right.png", 0.5)
        else:
            self.achive1 = arcade.Sprite("image/fish/perch_right.png", 0)
        self.achive1.center_y = SCREEN_HEIGHT // 2 + 230
        self.achive1.center_x = SCREEN_WIDTH // 2 - 470
        self.screen.add_sprite("Achives", self.achive1)

        if self.achive2_check:
            self.achive2 = arcade.Sprite("image/fish/carp_right.png", 0.5)
        else:
            self.achive2 = arcade.Sprite("image/fish/carp_right.png", 0)
        self.achive2.center_y = SCREEN_HEIGHT // 2 - 200
        self.achive2.center_x = SCREEN_WIDTH // 2 - 470
        self.screen.add_sprite("Achives", self.achive2)

        if self.achive3_check:
            self.achive3 = arcade.Sprite("image/fish/piranha_right.png", 0.5)
        else:
            self.achive3 = arcade.Sprite("image/fish/piranha_right.png", 0)
        self.achive3.center_y = SCREEN_HEIGHT // 2 + 230
        self.achive3.center_x = SCREEN_WIDTH // 2 + 70
        self.screen.add_sprite("Achives", self.achive3)

        if self.achive4_check:
            self.achive4 = arcade.Sprite("image/fish/aravana_right.png", 0.5)
        else:
            self.achive4 = arcade.Sprite("image/fish/aravana_right.png", 0)
        self.achive4.center_y = SCREEN_HEIGHT // 2 - 200
        self.achive4.center_x = SCREEN_WIDTH // 2 + 70
        self.screen.add_sprite("Achives", self.achive4)

        if self.achive5_check:
            self.achive5 = arcade.Sprite("image/static_meshes/achive_150.png", 0.5)
        else:
            self.achive5 = arcade.Sprite("image/static_meshes/achive_150.png", 0)
        self.achive5.center_y = SCREEN_HEIGHT // 2 + 160
        self.achive5.center_x = SCREEN_WIDTH // 2 + 590
        self.screen.add_sprite("Achives", self.achive5)

        if self.achive6_check:
            self.achive6 = arcade.Sprite("image/static_meshes/achive_5000.png", 0.5)
        else:
            self.achive6 = arcade.Sprite("image/static_meshes/achive_5000.png", 0)
        self.achive6.center_y = SCREEN_HEIGHT // 2 - 280
        self.achive6.center_x = SCREEN_WIDTH // 2 + 590
        self.screen.add_sprite("Achives", self.achive6)


    def on_click_back_menu(self, event):
        if self.achives_buttons:
            menu = Menu()
            self.window.show_view(menu)
            self.achives_buttons = False
        else:
            pass

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background_achive)
        if not self.achive2_check:
            arcade.draw_lrwh_rectangle_textured(180, 220, 189, 122, self.unknown_achive)
        if not self.achive1_check:
            arcade.draw_lrwh_rectangle_textured(180, SCREEN_HEIGHT-340, 189, 122, self.unknown_achive)
        if not self.achive4_check:
            arcade.draw_lrwh_rectangle_textured(SCREEN_WIDTH//2-20, 220, 189, 122, self.unknown_achive)
        if not self.achive3_check:
            arcade.draw_lrwh_rectangle_textured(SCREEN_WIDTH//2-20, SCREEN_HEIGHT-340, 189, 122, self.unknown_achive)
        self.achive_manager.draw()
        self.screen.draw()

        if self.achive1_check:
            arcade.draw_text("Окунь",
                             SCREEN_WIDTH / 2 - 470,
                             SCREEN_HEIGHT / 2 + 330,
                                 arcade.color.WHITE,
                             font_size=40, anchor_x='center')
            if save['PerchCount'] > 999:
                arcade.draw_text(f"Всего поймано: +999",
                             SCREEN_WIDTH / 2 - 480,
                             SCREEN_HEIGHT / 2 + 90,
                             arcade.color.WHITE,
                             font_size=30, anchor_x='center')
            else:
                arcade.draw_text(f"Всего поймано: {save['PerchCount']}",
                             SCREEN_WIDTH / 2 - 470,
                             SCREEN_HEIGHT / 2 + 90,
                             arcade.color.WHITE,
                             font_size=30, anchor_x='center')

        if self.achive2_check:
            arcade.draw_text("Карп",
                             SCREEN_WIDTH / 2 - 470,
                             SCREEN_HEIGHT / 2 - 110,
                             arcade.color.WHITE,
                             font_size=40, anchor_x='center')
            if save['CarpCount'] > 999:
                arcade.draw_text(f"Всего поймано: +999",
                             SCREEN_WIDTH / 2 - 480,
                             SCREEN_HEIGHT / 2 - 350,
                             arcade.color.WHITE,
                             font_size=30, anchor_x='center')
            else:
                arcade.draw_text(f"Всего поймано: {save['CarpCount']}",
                             SCREEN_WIDTH / 2 - 470,
                             SCREEN_HEIGHT / 2 - 350,
                             arcade.color.WHITE,
                             font_size=30, anchor_x='center')

        if self.achive3_check:
            arcade.draw_text("Пиранья",
                             SCREEN_WIDTH / 2 + 70,
                             SCREEN_HEIGHT / 2 + 330,
                             arcade.color.WHITE,
                             font_size=40, anchor_x='center')
            if save['PiranhaCount'] > 999:
                arcade.draw_text(f"Всего поймано: +999",
                             SCREEN_WIDTH / 2 + 70,
                             SCREEN_HEIGHT / 2 + 90,
                             arcade.color.WHITE,
                             font_size=30, anchor_x='center')
            else:
                arcade.draw_text(f"Всего поймано: {save['PiranhaCount']}",
                             SCREEN_WIDTH / 2 + 70,
                             SCREEN_HEIGHT / 2 + 90,
                             arcade.color.WHITE,
                             font_size=30, anchor_x='center')

        if self.achive4_check:
            arcade.draw_text("Аравана",
                             SCREEN_WIDTH / 2 + 70,
                             SCREEN_HEIGHT / 2 - 110,
                             arcade.color.WHITE,
                             font_size=40, anchor_x='center')
            if save['PiranhaCount'] > 999:
                arcade.draw_text(f"Всего поймано: +999",
                                 SCREEN_WIDTH / 2 + 70,
                                 SCREEN_HEIGHT / 2 - 350,
                                 arcade.color.WHITE,
                                 font_size=30, anchor_x='center')
            else:
                arcade.draw_text(f"Всего поймано: {save['AravanaCount']}",
                                 SCREEN_WIDTH / 2 + 70,
                                 SCREEN_HEIGHT / 2 - 350,
                                 arcade.color.WHITE,
                                 font_size=30, anchor_x='center')


    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ENTER:
            menu = Menu()
            self.window.show_view(menu)

class PauseMenu(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_show(self):
        if save['MapChange'] == 0:
            self.background_lake = arcade.load_texture("image/backgrounds/lake.png")
            self.background_sea = arcade.load_texture("image/backgrounds/sea_bottom.png")
            self.background_seaweed = arcade.load_texture("image/backgrounds/lake_seaweed.png")
            self.background_waves = arcade.load_texture("image/backgrounds/waves.png")
        elif save['MapChange'] == 1:
            self.background_lake = arcade.load_texture("image/backgrounds/river.png")
            self.background_sea = arcade.load_texture("image/backgrounds/river_bottom.png")
            self.background_seaweed = arcade.load_texture("image/backgrounds/river_seaweed.png")
            self.background_waves = arcade.load_texture("image/backgrounds/river_waves.png")

    def on_draw(self):
        arcade.start_render()
        self.clear()

        arcade.draw_lrwh_rectangle_textured(0, 640, SCREEN_WIDTH, SCREEN_HEIGHT // 2.75, self.background_lake)
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 1.56, self.background_sea)
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT // 2.55, self.background_seaweed)
        arcade.draw_lrwh_rectangle_textured(0, -348, SCREEN_WIDTH, SCREEN_HEIGHT, self.background_waves)

        if save['MapChange'] == 0:
            self.location = arcade.color.BLACK
        elif save['MapChange'] == 1:
            self.location = arcade.color.WHITE

        arcade.draw_text("На паузе", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                         self.location, font_size=50, anchor_x="center")

        arcade.draw_text("Esc - вернуться в меню",
                         SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2,
                         self.location,
                         font_size=20,
                         anchor_x="center")
        arcade.draw_text("Enter - продолжить игру",
                         SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2 - 30,
                         self.location,
                         font_size=20,
                         anchor_x="center")

        arcade.draw_text("При выходе в меню, прогресс не сохраниться",
                         SCREEN_WIDTH / 2,
                         SCREEN_HEIGHT / 2 - 90,
                         self.location,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            menu = Menu()
            self.window.show_view(menu)
            Menu().buttons_active = True
        elif key == arcade.key.ENTER:
            self.window.show_view(self.game_view)

class MyGame(arcade.View):

        def __init__(self):
            super().__init__()


            self.background_lake = None
            self.background_sea = None
            self.lake_seaweed = None

            self.perch_animated_sprite = None
            self.kilo_price = 50

            self.bottom_list = None
            self.waves = None

            self.boat = None

            self.passengers = []
            self.passenger_limit = 1

            self.score_gui = None
            self.score = 0
            self.score_limit = 0

            self.exit_gui = None
            self.moving_gui = None
            self.dollar_gui = None

            self.screne = None
            self.physics_engine_boat = None
            self.physics_engine_hook = None
            self.physics_engine_rope = None

            self.total_time = 720.0
            self.output = "00:00"

            self.framing = 0
            self.time_color = arcade.csscolor.BLACK
            self.time_scalling = 25

            self.fishing_splash = None

            self.game_over = False

            #boat settings
            self.hook_sprite = None
            self.rope = None
            self.hook_catch_fish = False

            self.boat_sprite = arcade.Sprite("image/boat/boat_right.png", BOAT_BASE_SCALING)
            self.boat_sprite.center_x = 250
            self.boat_sprite.center_y = 655

            self.boat_min_y = self.boat_sprite.center_y - 15
            self.boat_max_y = self.boat_sprite.center_y - 5
            self.boat_vector = -1 / 2

            self.rope = arcade.Sprite("image/boat/rope.png", ROPE)
            self.rope.center_x = self.boat_sprite.center_x
            self.rope.center_y = self.boat_sprite.center_y + 10

            self.hook_sprite = arcade.Sprite("image/boat/hook_right.png", HOOK)
            self.hook_sprite.center_x = self.rope.center_x
            self.hook_sprite.center_y = self.rope.center_y - 85

            self.setup()

        def setup(self):
            if save['MapChange'] == 0:
                self.background_lake = arcade.load_texture("image/backgrounds/lake.png")
                self.background_sea = arcade.load_texture("image/backgrounds/sea_bottom.png")
            elif save['MapChange'] == 1:
                self.background_lake = arcade.load_texture("image/backgrounds/river.png")
                self.background_sea = arcade.load_texture("image/backgrounds/river_bottom.png")


            self.screne = arcade.Scene()

            self.screne.add_sprite_list("Rope")
            self.screne.add_sprite_list("Hook")
            self.screne.add_sprite_list("Boat")

            for x in range(max_perch):
                fish = None
                if save['MapChange'] == 0:
                    vector = "left"
                    fish = arcade.Sprite("image/fish/perch_" + vector + ".png", starter_perch[x])
                    if x%2 == 0:
                        vector = "right"
                    if x%3 == 0:
                        fish = arcade.Sprite("image/fish/carp_" + vector + ".png", starter_perch[x])
                elif save['MapChange'] == 1:
                    vector = "left"
                    fish = arcade.Sprite("image/fish/aravana_" + vector + ".png", starter_perch[x])
                    if x%2 == 0:
                        vector = "right"
                    if x%3 == 0:
                        fish = arcade.Sprite("image/fish/piranha_" + vector + ".png", starter_perch[x])
                add_perch = "Fish" + str(x)
                fish.center_x = randint(0, SCREEN_WIDTH)
                fish.center_y = randint(100, 500)
                self.screne.add_sprite(add_perch, fish)

            self.screne.add_sprite_list("LakeSeaweed")
            self.screne.add_sprite_list("Waves")

            if save['MapChange'] == 0:
                self.lake_seaweed = arcade.Sprite("image/backgrounds/lake_seaweed.png", SEAWEED_SIZE)
            elif save['MapChange'] == 1:
                self.lake_seaweed = arcade.Sprite("image/backgrounds/river_seaweed.png", SEAWEED_SIZE)
            self.lake_seaweed.center_x = SCREEN_WIDTH//2
            self.lake_seaweed.center_y =200
            self.screne.add_sprite("LakeSeaweed", self.lake_seaweed)

            self.screne.add_sprite_list("Bottom")

            self.score_gui = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
            self.exit_gui = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
            self.moving_gui = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
            self.dollar_gui = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
            self.score = 0
            self.score_limit = 2.5

            self.screne.add_sprite("Boat", self.boat_sprite)
            self.screne.add_sprite("Hook", self.hook_sprite)
            self.screne.add_sprite("Rope", self.rope)

            self.waves_offset = 0
            self.waves_offset_max = 124

            if save['MapChange'] == 0:
                self.waves = arcade.Sprite("image/backgrounds/waves.png", WAVES)
            elif save['MapChange'] == 1:
                self.waves = arcade.Sprite("image/backgrounds/river_waves.png", WAVES)
            self.waves.center_x = self.boat_sprite.center_x + 550
            self.waves.center_y = self.boat_sprite.center_y - 720
            self.screne.add_sprite("Waves", self.waves)

            self.setup_physics()

        def setup_physics(self):
            self.physics_engine_boat = arcade.PhysicsEngineSimple(
                self.boat_sprite, self.screne.get_sprite_list("Bottom")
            )
            self.physics_engine_hook = arcade.PhysicsEngineSimple(
                self.hook_sprite, self.screne.get_sprite_list("Bottom")
            )
            self.physics_engine_rope = arcade.PhysicsEngineSimple(
                self.rope, self.screne.get_sprite_list("Bottom")
            )

        def stop_boat(self):
            self.boat_sprite.change_x = 0
            self.hook_sprite.change_x = 0
            self.rope.change_x = 0
            self.hook_sprite.change_y = 0

        def periodical_movement(self):
            self.boat_sprite.center_y += self.boat_vector
            self.rope.center_y += self.boat_vector
            self.hook_sprite.center_y += self.boat_vector
            if self.boat_sprite.center_y < self.boat_min_y:
                self.boat_vector = 1 / 8
            elif self.boat_sprite.center_y > self.boat_max_y:
                self.boat_vector = -1 / 8

            rope_distance = arcade.get_distance_between_sprites(self.boat_sprite, self.hook_sprite)
            if (self.rope.center_y < self.boat_sprite.center_y + 50):
                self.rope.height = rope_distance
                self.rope.center_y = self.hook_sprite.center_y - 10 + rope_distance // 2
                if self.rope.height > 700:
                    self.rope.height = 700

            if self.hook_sprite.center_y >= self.boat_sprite.center_y - 20:
                self.hook_sprite.center_y = self.boat_sprite.center_y - 20
            if self.hook_sprite.center_y <= 20:
                self.hook_sprite.center_y = 20

            if self.boat_sprite.center_x <= 200:
                self.boat_sprite.change_x = BOAT_MOVEMENT_SPEED
                self.hook_sprite.change_x = BOAT_MOVEMENT_SPEED
                self.rope.change_x = BOAT_MOVEMENT_SPEED

                self.hook_sprite.center_x = self.rope.center_x
                self.hook_sprite.texture = arcade.load_texture("image/boat/hook_left.png", flipped_horizontally=True)
                self.boat_sprite.texture = arcade.load_texture("image/boat/boat_right.png")

                self.rope.center_x = self.boat_sprite.center_x
                self.hook_sprite.center_x = self.boat_sprite.center_x

            elif self.boat_sprite.center_x >= SCREEN_WIDTH - 200:
                self.boat_sprite.change_x = -BOAT_MOVEMENT_SPEED
                self.hook_sprite.change_x = -BOAT_MOVEMENT_SPEED
                self.rope.change_x = -BOAT_MOVEMENT_SPEED

                self.hook_sprite.center_x = self.rope.center_x
                self.hook_sprite.texture = arcade.load_texture("image/boat/hook_left.png")
                self.boat_sprite.texture = arcade.load_texture("image/boat/boat_left.png")

                self.rope.center_x = self.boat_sprite.center_x
                self.hook_sprite.center_x = self.boat_sprite.center_x

        def set_texture(self, variant):
            self.boat_sprite.texture = arcade.load_texture("image/boat/boat_" + variant + ".png")
            if variant == "right":
                self.hook_sprite.center_x = self.rope.center_x
                self.hook_sprite.texture = arcade.load_texture("image/boat/hook_left.png", flipped_horizontally=True)
            elif variant == "left":
                self.hook_sprite.center_x = self.rope.center_x
                self.hook_sprite.texture = arcade.load_texture("image/boat/hook_left.png")

        def on_draw(self):

            arcade.start_render()
            self.clear()
            arcade.draw_lrwh_rectangle_textured(0, 640, SCREEN_WIDTH, SCREEN_HEIGHT//2.75, self.background_lake)
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT//1.56, self.background_sea)
            self.screne.draw()

            self.score_gui.use()
            score_text = f"Поймано рыб на общий вес: {self.score:.3f}/{save['LakeBestScore']:.3f} кг ({self.score*(self.kilo_price):.0f})"
            arcade.draw_text(score_text, 20, 10, arcade.csscolor.BLUE, 20)

            self.exit_gui.use()
            exit_text = f"Выход: ESC"
            arcade.draw_text(exit_text, 20, 950, arcade.csscolor.BLACK, 16)

            self.moving_gui.use()
            moving_text = f"Движение: WASD или ←↑↓→"
            arcade.draw_text(moving_text, 20, 975, arcade.csscolor.BLACK, 16)

            self.dollar_gui.use()
            dollar_text = f"Цена за килограмм: "+str(self.kilo_price)
            arcade.draw_text(dollar_text, SCREEN_WIDTH - 275, 10, arcade.color.BLACK, 16)

            arcade.draw_text(self.output, SCREEN_WIDTH//2, SCREEN_HEIGHT - 50, self.time_color, self.time_scalling, anchor_x="center")

        def on_key_press(self, key, modifiers):
            if self.hook_catch_fish == False and len(self.passengers) == 0:
                if key == arcade.key.RIGHT or key == arcade.key.D:
                    self.set_texture("right")
                    self.boat_sprite.change_x = BOAT_MOVEMENT_SPEED
                    self.hook_sprite.change_x = BOAT_MOVEMENT_SPEED
                    self.rope.change_x = BOAT_MOVEMENT_SPEED
                elif key == arcade.key.LEFT or key == arcade.key.A:
                    self.set_texture("left")
                    self.boat_sprite.change_x = -BOAT_MOVEMENT_SPEED
                    self.hook_sprite.change_x = -BOAT_MOVEMENT_SPEED
                    self.rope.change_x = -BOAT_MOVEMENT_SPEED
                elif (key == arcade.key.UP or key == arcade.key.W) and len(self.passengers) < self.passenger_limit:
                    self.hook_sprite.change_y = HOOK_MOVEMENT_SPEED
                elif (key == arcade.key.DOWN or key == arcade.key.S) and len(self.passengers) < self.passenger_limit:
                    self.hook_sprite.change_y = -HOOK_MOVEMENT_SPEED

            if key == arcade.key.ESCAPE:
                pause_menu = PauseMenu(self)
                self.window.show_view(pause_menu)
        def on_key_release(self, key, modifiers):
            if key == arcade.key.RIGHT or key == arcade.key.D:
                self.boat_sprite.change_x = 0
                self.hook_sprite.change_x = 0
                self.rope.change_x = 0
            elif key == arcade.key.LEFT or key == arcade.key.A:
                self.boat_sprite.change_x = 0
                self.hook_sprite.change_x = 0
                self.rope.change_x = 0
            elif key == arcade.key.UP or key == arcade.key.W:
                self.hook_sprite.change_y = 0
                self.rope.change_y = 0
            elif key == arcade.key.DOWN or key == arcade.key.S:
                self.hook_sprite.change_y = 0
                self.rope.change_y = 0

        def on_update(self, delta_time):
            self.periodical_movement()
            self.physics_engine_boat.update()
            self.physics_engine_hook.update()
            self.physics_engine_rope.update()

            index = randint(0, len(self.screne.get_sprite_list("Fish1")) - 1)
            hook_speed = 300
            on_hook_perch_count = 0
            self.framing += 1

            self.total_time += delta_time
            minutes = int(self.total_time) // 60
            seconds = int(self.total_time) % 60
            self.output = f"{minutes:02d}:{seconds:02d}"
            if self.output >= "14:30":
                self.time_color = arcade.csscolor.RED
                self.time_scalling = 35
            if self.output == "12:10" and not self.game_over:
                self.game_over = True
                save['LocalScore'] = self.score
                if self.score > save['LakeBestScore']:
                    save['LakeBestScore'] = self.score
                save['SavedCoins'] += self.score * self.kilo_price
                print(save['LocalScore'])
                print(save['LakeBestScore'])
                game_over_view = GameOver()
                self.window.show_view(game_over_view)


            self.waves_offset += 1
            self.waves.center_x -= 1
            if self.waves_offset >= self.waves_offset_max:
                self.waves.center_x += self.waves_offset_max
                self.waves_offset = 0

            for x in range(max_perch):
                current_fish = self.screne.get_sprite_list("Fish" + str(x))[index]
                even = x%2
                motion = 1
                motion_name = "right"
                if even:
                    motion = -1
                    motion_name = "left"
                center_save_x = current_fish.center_x*1
                center_save_y = current_fish.center_y*1
                current_fish.remove_from_sprite_lists()
                calculated_speed = 6-(fish_speeds[x]//100+1)
                if calculated_speed <= 0:
                    calculated_speed = 1
                if self.framing%calculated_speed == 0:
                    fish_animation_index[x] += fish_animation_index_change[x]
                    if fish_animation_index[x] == 5:
                        fish_animation_index_change[x] = -1
                    if fish_animation_index[x] == 1:
                        fish_animation_index_change[x] = 1
                if save['MapChange'] == 0:
                    current_fish = arcade.Sprite("image/fish/perch_tail_"+motion_name+"_"+str(fish_animation_index[x])+".png", starter_perch[x])
                    if x%3 == 0:
                        current_fish = arcade.Sprite("image/fish/carp_tail_"+motion_name+"_"+str(fish_animation_index[x])+".png", starter_perch[x])
                elif save['MapChange'] == 1:
                    current_fish = arcade.Sprite("image/fish/aravana_tail_"+motion_name+"_"+str(fish_animation_index[x])+".png", starter_perch[x])
                    if x%3 == 0:
                        current_fish = arcade.Sprite("image/fish/piranha_tail_"+motion_name+"_"+str(fish_animation_index[x])+".png", starter_perch[x])
                self.screne.add_sprite("Fish" + str(x), current_fish)
                current_fish.center_x = center_save_x
                current_fish.center_y = center_save_y
                current_fish.center_x += motion * fish_speeds[x] * delta_time

                if not (-150 < current_fish.center_x < SCREEN_WIDTH + 150):
                    current_fish.center_x = [-150, SCREEN_WIDTH + 150][randint(0, 1)]
                    current_fish.center_y = randint(100, 500)
                    fish_speeds[x] = randint(MIN_FISH_SPEED, MAX_FISH_SPEED)

                if arcade.check_for_collision(self.hook_sprite, current_fish) and (len(self.passengers) < self.passenger_limit or x in self.passengers):
                    if not x in self.passengers:
                        self.passengers.append(x)
                    current_fish.center_x = self.hook_sprite.center_x
                    current_fish.center_y = self.hook_sprite.center_y - 25
                    angle = 90
                    if even: angle = 270
                    current_fish.angle = angle
                    self.hook_catch_fish = True
                    on_hook_perch_count += 1
                    if on_hook_perch_count == 1:
                        self.hook_sprite.center_y += hook_speed * delta_time
                    elif on_hook_perch_count > 1 and on_hook_perch_count < 4:
                        self.hook_sprite.center_y -= (hook_speed // on_hook_perch_count + 1) * delta_time
                    self.stop_boat()
                else:
                    current_fish.angle = 0
                    self.hook_catch_fish = False
                    if x in self.passengers:
                        self.passengers.remove(x)
                        fish_speeds[x] = MAX_FISH_SPEED*1.5

                if arcade.check_for_collision_with_list(self.boat_sprite, self.screne.get_sprite_list("Fish" + str(x))) and x in self.passengers:
                    catch = randint(1,4)
                    if catch == 1:
                        self.fishing_splash = arcade.load_sound("sounds/fishing_splash_1.mp3",)
                        arcade.play_sound(self.fishing_splash, volume=0.5)
                    elif catch == 2:
                        self.fishing_splash = arcade.load_sound("sounds/fishing_splash_2.mp3",)
                        arcade.play_sound(self.fishing_splash, volume=0.5)
                    elif catch == 3:
                        self.fishing_splash = arcade.load_sound("sounds/fishing_splash_3.mp3")
                        arcade.play_sound(self.fishing_splash)
                    elif catch == 4:
                        self.fishing_splash = arcade.load_sound("sounds/fishing_splash_4.mp3")
                        arcade.play_sound(self.fishing_splash)
                    if save['MapChange'] == 0:
                        if x%3 != 0:
                            save['PerchCount'] += 1
                        if x%3 == 0:
                            save['CarpCount'] += 1
                    elif save['MapChange'] == 1:
                        if x % 3 != 0:
                            save['AravanaCount'] += 1
                        if x % 3 == 0:
                            save['PiranhaCount'] += 1
                    save['FishCount'] += 1
                    current_fish.remove_from_sprite_lists()
                    fish_weight = random.uniform(MIN_FISH_SIZE, MAX_FISH_SIZE)
                    vector = "right"
                    fish = arcade.Sprite("image/fish/perch_" + vector + ".png", fish_weight)
                    if even:
                        vector = "left"
                        fish = arcade.Sprite("image/fish/carp_"+vector+".png", fish_weight)
                    fish.center_x = SCREEN_WIDTH + 140
                    fish.center_y = randint(100, 500)
                    self.screne.add_sprite("Fish" + str(x), fish)
                    if fish == arcade.load_texture("image/fish/perch_" + vector + ".png"):
                        print(1)
                    self.score += fish_weight * 1.5
                    self.hook_catch_fish = False
                    if x in self.passengers:
                        self.passengers.remove(x)
                    fish_speeds[x] = randint(MIN_FISH_SPEED,MAX_FISH_SPEED)*((MAX_FISH_SIZE+MIN_FISH_SIZE)/2)/fish_weight


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Fishman's Dream")
    menu = Menu()
    window.show_view(menu)
    arcade.run()

if __name__ == "__main__":
    main()