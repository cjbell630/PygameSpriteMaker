import numpy


def ints_from_byte_file(filename):
    file = open("files/" + filename, "rb")
    ints = []
    for b in file.read():
        ints.append(int(b))
    file.close()
    return ints


def read_numpy_from_file(filename: str) -> numpy.ndarray:
    ints = ints_from_byte_file(filename)
    print(ints)
    count = 0
    palette = []
    count += 1
    for i in range(0, ints[0]):
        palette.append((ints[count], ints[count + 1], ints[count + 2]))
        count += 3
    print("palette " + str(palette))
    horiz_tiles = ints[count]
    count += 1
    vert_tiles = ints[count]
    count += 1
    array = []
    print("horiz: " + str(horiz_tiles))
    print("vert: " + str(vert_tiles))
    for x in range(0, horiz_tiles):
        array.append([])
        for y in range(0, vert_tiles):
            array[x].append(palette[ints[count]])
            count += 1
    return numpy.array(array)
