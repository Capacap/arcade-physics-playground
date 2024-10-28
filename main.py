import arcade.physics_engines
import arcade.sprite
import arcade.sprite_list
import arcade
import random
import pymunk
from arcade.pymunk_physics_engine import PymunkPhysicsEngine

WINDOW_WIDTH = 1024 # Initial width of window
WINDOW_HEIGHT = 1024 # Initial height of window
WINDOW_TITLE = "Physics Playground" # Title of window
BOX_COUNT = 64 # Number of boxes to spawn

class PhysicsPlaygroundView(arcade.View):
    def __init__(self):
        super().__init__()

        # Window background color
        arcade.set_background_color(arcade.color.AMAZON)

        # Data attributes for dragging of objects and camera
        self.drag_shape_target = None
        self.dragging_camera = False

        # Data attributes for cursor motion tracking
        self.current_cursor_point = (0.0, 0.0)
        self.previous_cursor_point = (0.0, 0.0)

        # Create main camera
        camera_position = (0, 0)
        camera_projection = arcade.LRBT(left=0, right=WINDOW_WIDTH, bottom=0, top=WINDOW_HEIGHT)
        camera_viewport = self.window.rect
        self.main_camera = arcade.camera.Camera2D(position=camera_position, projection=camera_projection, viewport=camera_viewport)

        # Create sprites and sprite list
        self.sprite_list = arcade.sprite_list.SpriteList()
        for i in range(BOX_COUNT):
            x = random.randrange(0, WINDOW_WIDTH, 1)
            y = random.randrange(0, WINDOW_HEIGHT, 1)
            sprite = arcade.sprite.Sprite(":resources:images/tiles/boxCrate_double.png", 0.25, x, y)
            self.sprite_list.append(sprite)

        # Add physics to sprites in sprite list
        self.physics_engine = PymunkPhysicsEngine(damping=0.75, gravity=(0.0, 0.0))
        self.physics_engine.add_sprite_list(self.sprite_list, mass=2, friction=0.75, damping=0.1, collision_type="box")

    def on_resize(self, width, height):
        # Make camera projection and viewport fit the new window size
        self.main_camera.width = width
        self.main_camera.height = height
        self.main_camera.viewport = arcade.XYWH(0, 0, width, height, arcade.rect.AnchorPoint.BOTTOM_LEFT)

    def on_draw(self):
        # Clear existing canvas
        self.clear()

        # Draw sprites using the main camera
        with self.main_camera.activate():
            self.sprite_list.draw()

    def on_update(self, delta_time):
        # Get cursor movement delta
        dx = self.current_cursor_point[0] - self.previous_cursor_point[0]
        dy = self.current_cursor_point[1] - self.previous_cursor_point[1]

        # Update dragged body velocity
        if self.drag_shape_target is not None and not self.dragging_camera:
            self.drag_shape_target.shape.body.velocity = (dx / delta_time, dy / delta_time)
        # Update camera position if dragging the camera
        elif self.dragging_camera:
            self.main_camera.position = (self.main_camera.position.x - dx, self.main_camera.position.y - dy)

        # Update physics simulation
        self.physics_engine.step()

        # Update cursor motion tracking
        self.previous_cursor_point = self.current_cursor_point

    def on_mouse_motion(self, x, y, dx, dy):
        # Update cursor motion tracking
        self.current_cursor_point = (x, y)

    def on_mouse_press(self, x, y, button, key_modifiers):
        # Left mouse button functionality
        if button == arcade.MOUSE_BUTTON_LEFT:
            shapes_under_cursor = self.get_shapes_under_cursor()
            if len(shapes_under_cursor) > 0:
                self.drag_shape_target = shapes_under_cursor[0]
            else:
                self.dragging_camera = True

    def on_mouse_release(self, x, y, button, key_modifiers):
        # Left mouse button functionality
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.drag_shape_target = None
            self.dragging_camera = False

    def get_shapes_under_cursor(self):
            # Project cursor screen position into a world position
            world_point = self.current_cursor_point

            # Get all shapes under the cursor
            shapes_under_cursor = self.physics_engine.space.point_query((world_point[0], world_point[1]), 1.0, pymunk.ShapeFilter())

            return shapes_under_cursor


def main():
    # Instantiate the window and start the game
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, resizable=True)
    game = PhysicsPlaygroundView()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()