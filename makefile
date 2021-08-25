clean:
	rm -rf **/*.xcworkspace
	rm -rf **/*.xcodeproj
	rm -rf ./buck-out/
	rm -rf ./.buckd/
	./buck clean

install_lldb_remap:
	echo "command source ${HOME}/.lldb-remap" >> ${HOME}/.lldbinit

xcode:
	make clean
	./buck project VeryCoolApp --experimental && open VeryCoolApp/VeryCoolApp.xcworkspace

buck:
	curl -L https://github.com/Lcsmarcal/lldb-intermittent-behavior-sample/releases/download/release/buck.pex --output ./buck
	chmod u+x ./buck

first_run:
	make install_lldb_remap
	make buck
	make xcode