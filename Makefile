CC = gcc
CFLAGS = -fPIC -shared -O3
TARGET = core/build/libswarmraft.dll
SRC = core/swarmraft.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET) -lm

clean:
	del /f core\build\libswarmraft.dll