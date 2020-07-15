python3 main.py | tee runtime.txt

newdir=$(ls -td -- */ | head -n 1)

mv runtime.txt $newdir/runtime.txt
