all:
	./upload.py 1
	od -t a sensor0.txt
	od -t a health0.txt
clean:
	rm -f *.txt
