python src/clean_corpus.py $PWD corpus/bataclan corpus/CorpusBataclan_en.1M.raw.txt
python context2vec/context2vec/train/corpus_by_sent_length.py corpus/bataclan
nohup python context2vec/context2vec/train/train_context2vec.py  -i "corpus/bataclan.DIR"  -w "bataclan.words"  -m "bataclan.model"  -c lstm  --deep yes  -t 3  --dropout 0.1  -u 300  -e 6  -p 0.75  -b 100  -g 0 > train.log 2>&1 &
