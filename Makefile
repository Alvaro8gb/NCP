.PHONY: run

run:
	python ncp/modules.py 

clean:
	rm out/multiple/*.json
	rm out/one_diag/*.json
	rm out/no_diags/*.json
	find . -name '__pycache___' -type d -exec rm -r {} +

profile:
	kernprof -l -v ncp/modules.py > perfilado.out

time:
	time python ncp/modules.py 

count:
	./couting_file.sh ./out/multiple
	./couting_file.sh ./out/one_diag
	./couting_file.sh ./out/no_diags
setup:
	python setup.py sdist
build-docker:
	sudo docker build -t ncp .
run-docker:
	sudo docker run --name ncp_api -p 8008:8000 ncp
rm-cache:
	find . -name "*.pyc" -delete
