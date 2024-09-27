from pygame_sprite_manager.ui.sprite_maker import sprite_to_int_array


def save_to_cache():
    ints_to_byte_file("cache", sprite_to_int_array())


def ints_to_byte_file(filename, ints):
    file = open("files/" + filename, "wb")
    file.write(bytes(ints))
    file.close()
