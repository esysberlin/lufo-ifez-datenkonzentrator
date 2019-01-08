default: main

CPP_FILES = $(wildcard *.cpp)
OBJ_FILES = $(CPP_FILES:%.cpp=%.o)
HPP_FILES = $(wildcard *.h)

main: $(OBJ_FILES)
	g++ -o $@ $^ -lwiringPi

main.o: $(CPP_FILES) $(HPP_FILES)
	g++ -c $(CPP_FILES)
