INPUT_00=./src/*.cpp

CC=g++

TARGET=./bin/schedule

${TARGET}: ${INPUT_00}
	${CC} ${INPUT_00} -o ${TARGET} 
