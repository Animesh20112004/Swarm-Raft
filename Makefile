# Compiler settings
CC = gcc
CFLAGS = -fPIC -O3 -shared
TARGET = core/build/libswarmraft.so

# Ensure the build directory exists and compile
all:
	mkdir -p core/build
	$(CC) $(CFLAGS) -o $(TARGET) core/swarmraft.c -lm

clean:
	rm -f $(TARGET)