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