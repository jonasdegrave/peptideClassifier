cd src

for file in ../inputFiles/*.xlsx; do
        python peptideClassifier.py $file;
        done