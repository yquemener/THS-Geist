all: sp

clean:
	-$(DEL_FILE) *.o sp

sp: splay.cpp
	g++ splay.cpp -o sp -lopencv_core -lopencv_highgui -lopencv_imgproc -lopencv_objdetect

