#! /bin/sh

# remove all previous files
rm -r heideltime-standalone

mkdir heideltime-standalone
mkdir heideltime-standalone/treetagger

cd heideltime-standalone/treetagger

# store directory for later
treetagger_dir="treeTaggerHome = "$(pwd)

# download treetagger files
wget --no-verbose https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tree-tagger-linux-3.2.4.tar.gz 
wget --no-verbose https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tagger-scripts.tar.gz 
wget --no-verbose https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/install-tagger.sh 
wget --no-verbose https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/german.par.gz 
wget --no-verbose https://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/english.par.gz

# install treetagger
sh install-tagger.sh

cd ..

# download HeidelTime-standalone
wget --no-verbose https://github.com/HeidelTime/heideltime/releases/download/VERSION2.2.1/heideltime-standalone-2.2.1.tar.gz
tar xzf heideltime-standalone-2.2.1.tar.gz


cd heideltime-standalone

# store directory for later
heideltime_dir=$(pwd)

# alter config file for HeidelTime-standalone
# sed -i "s/\(considerDate *= *\).*/\1false/" config.props
# sed -i "s/\(considerDuration *= *\).*/\1false/" config.props
# sed -i "s/\(considerSet *= *\).*/\1false/" config.props
# sed -i "s/\(considerTime *= *\).*/\1false/" config.props

original_str="treeTaggerHome = SET ME IN CONFIG.PROPS! (e.g., /home/jannik/treetagger)"
sed -i "s~$original_str~$treetagger_dir~" config.props

# alter config file for python_heideltime
cd ../../python_heideltime
rm config_Heideltime.py
wget --no-verbose https://raw.githubusercontent.com/PhilipEHausner/python_heideltime/master/python_heideltime/config_Heideltime.py

original_str="Heideltime_path = '/path/to/heideltime/'"
replace_str="Heideltime_path = '$heideltime_dir'"
sed -i "s~$original_str~$replace_str~" config_Heideltime.py

echo "HeidelTime-standalone installed successfully. Config files altered."
